import sys
import utime
import machine
import json
from .WiFiManager import WiFiManager
from .MQTTManager import MQTTManager
from .UpdateManager import UpdateManager
from .sensors.StatusLED import StatusLED
from .sensors import HomeMotionSensor, HomeWeatherSensor, HomeLEDDimmer
from .Timer import Timer
from .Configs import DeviceConfig, DeviceSettings
# import config
import ubinascii
import urequests


def save_data(data):
    with open('/home/saved-data.json', 'w') as f:
        json.dump(data, f)


def load_data():
    with open('/home/saved-data.json', 'r') as f:
        return json.load(f)


class HomeError(Exception):
    pass


class Home:
    settings = None
    status_pin = False
    wifi_manager = None
    mqtt_manager = None
    update_manager = None
    display_name = None
    device_info = None
    device_configs = None
    sensor_configs = None
    sensors = None

    """
    Home class is a wrapper around the MQTT, WiFi and Update managers.
    It provides a simple interface to handle connections and updates.
    """

    def __init__(self, use_ping=True):
        """
        Initializes Home with the provided configuration dictionary.

        Parameters:
        config (dict): A dictionary containing the configurations for
        unit id, WiFiManager, MQTTManager and UpdateManager.
         Each of these configurations is another dictionary that
         includes all the necessary parameters for the respective manager.
        """
        self._platform = sys.platform
        if self._platform not in ['rp2', 'esp32']:
            raise HomeError(f"Unsupported platform: {self._platform}")

        if self._platform == "rp2":
            self.status_pin = "LED"
        elif self._platform == 'esp32':
            self.status_pin = 2
        self.device_settings = DeviceSettings()
        self.unit_id = ubinascii.hexlify(machine.unique_id()).decode()
        self.command_topic = f"command/#"
        self.log_topic = f"z-home/log/{self.unit_id}"

        self.timer = None
        self.use_ping = use_ping
        self.sensors = []
        print("\nPlatform: ", self._platform, "\nName: ", self.device_settings.name, "\nUnit: ", self.unit_id)

    def connect_wifi(self):
        ssid = self.device_settings.ssid
        password = self.device_settings.password
        self.wifi_manager = WiFiManager(ssid, password)
        print("\nconnecting WiFi")
        self.wifi_manager.connect_wifi()

    def request_configs(self):
        print(f'requesting settings from: {self.device_settings.host}')
        response = urequests.get(f'{self.device_settings.host}/api/home/devices/{self.unit_id}')
        if response.status_code == 200:
            print(f'received settings')
            data = response.json()
            if data is None:
                return data
            save_data(data)
            if data['display_name'] != self.device_settings.name:
                self.device_settings.name = data['display_name']
                self.device_settings.save()
                print(f'device name updated to: {self.device_settings.name}')
            return data

    def announce_ones_self(self):
        data = {
            "id": self.unit_id,
            "platform": self._platform,
            "display_name": self.device_settings.name,
            "device_info": {
                "name": self.device_settings.name,
                "manufacturer": "ZRW",
                "model": f"{self._platform.upper()}-Circuit",
                "identifiers": self.unit_id
            }
        }
        response = urequests.post(f'{self.device_settings.host}/api/home/devices/add', json=data)
        print("announcing device...")
        if response.status_code == 200:
            data = response.json()
            print("device added")
            return data['device']
        return data

    def connect_mqtt(self):
        if self.settings.mqtt is None:
            raise HomeError("no mqtt connection details found")
        self.mqtt_manager = MQTTManager(unit_id=self.unit_id,
                                        server=self.settings.mqtt.host,
                                        port=self.settings.mqtt.port,
                                        username=self.settings.mqtt.username,
                                        password=self.settings.mqtt.password)
        print("\nconnecting MQTT")
        self.mqtt_manager.connect_mqtt()

    def connect_ftp(self):
        if self.settings.ftp is not None:
            self.update_manager = UpdateManager(unit_id=self.unit_id,
                                                observer_func=self.log,
                                                host=self.settings.ftp.host,
                                                user=self.settings.ftp.username,
                                                password=self.settings.ftp.password)

    def fetch_device_configs(self):
        if not self.wifi_manager.is_connected():
            raise HomeError("not connected to wifi")

        info = self.request_configs()
        if not info:
            info = self.announce_ones_self()
        if not info:
            try:
                info = load_data()
                print('loaded data from saved file')
            except json.JSONDecodeError:
                info = False
            except OSError:
                info = False
        if not info:
            raise HomeError("unable to locate configs")

        self.settings = DeviceConfig.parse_config(info)
        self.display_name = self.settings.name
        self.sensor_configs = self.settings.sensors
        self.device_info = self.settings.device_info

    def setup_sensors(self):

        if self.sensor_configs is not None:
            for i in self.sensor_configs:
                sensor_type = i.get('sensor_type')
                name = i.get('name')
                sensor_config = i.get('sensor_config')
                topics = sensor_config.get('topics') if sensor_config is not None else None
                sensor_index = self.sensor_configs.index(i) + 1
                if sensor_type == 'motion':
                    motion = HomeMotionSensor(self, name, sensor_config, topics, sensor_index)
                    motion.publish_discovery(self.device_info)
                    motion.enable_interrupt()
                    self.sensors.append(motion)

                elif sensor_type == 'led':
                    led = HomeLEDDimmer(self, name, sensor_config, topics, sensor_index)
                    led.publish_discovery(self.device_info)
                    led.publish_brightness()
                    led.publish_state()
                    self.sensors.append(led)

                elif sensor_type == 'weather':
                    measurement_interval_ms = sensor_config.get('measurement_interval_ms')
                    weather = HomeWeatherSensor(self, name, sensor_config, topics, sensor_index)
                    weather.enable_interrupt(measurement_interval_ms)
                    weather.publish_discovery(self.device_info)
                    self.sensors.append(weather)

    def setup_subscriptions(self):
        self.set_callback(self.on_message)
        self.subscribe(self.command_topic)
        self.subscribe_sensors()

    def start_sequence(self):
        self.connect_wifi()
        self.fetch_device_configs()
        self.connect_mqtt()
        self.log("Connected to Wifi and MQTT")
        self.connect_ftp()
        self.set_connection_check_timer()
        self.setup_sensors()
        print(self.sensors)
        self.setup_subscriptions()
        if self.wifi_manager.is_connected() and self.mqtt_manager.is_connected:
            if self.status_pin:
                led = StatusLED(self.status_pin)
                led.blink_light()
                led.blink_light()
                if self.settings.led_on_after_connect:
                    led.on()

    def status_led_off(self):
        light = StatusLED(self.status_pin)
        light.off()

    def restart_on_error(self, error_message):
        print(error_message)
        self.log(f'{error_message} - Restarting', log_type='error')
        self.status_led_off()
        utime.sleep(5)
        machine.reset()

    def log(self, log_message, log_type='info'):
        if self.mqtt_manager.is_connected:
            self.publish(self.log_topic, json.dumps({
                "unit_id": self.unit_id,
                "display_name": self.display_name,
                "message": log_message,
                "type": log_type
            }))

    def set_connection_check_timer(self):
        self.timer = Timer(timer_number=0, period=5000, mode=machine.Timer.PERIODIC, callback=self.check_connections)

    def subscribe_sensors(self):
        if self.sensors is not None:
            for s in self.sensors:
                if hasattr(s, 'subscribe_to'):
                    for t in s.subscribe_to:
                        self.subscribe(t)

    def check_connections(self):
        """
        Checks the WiFi connection and reconnects if the connection is lost.
        """
        if not self.wifi_manager.is_connected():
            print('Lost Wi-Fi connection. Reconnecting...')
            self.wifi_manager.connect_wifi()
            self.log("Reconnected Wifi")
        if not self.mqtt_manager.is_connected:
            self.mqtt_manager.connect_mqtt()
            self.setup_subscriptions()
            self.log("Reconnected MQTT")
        else:
            if self.use_ping:
                self.mqtt_ping()

    def on_message(self, topic, msg):
        """
        Handles the MQTT messages.

        :param topic: The topic of the message.
        :param msg: The received message.
        """
        if self.sensors is not None:
            for s in self.sensors:
                if hasattr(s, 'on_message'):
                    s.on_message(topic, msg)

        t = topic.decode('utf-8')
        if t == f'command/{self.unit_id}' or t == 'command/all-units' or t == f'command/{self.display_name}':

            try:
                msg = msg.decode('utf-8')
                instructions = json.loads(msg)

                command = instructions.get("command")
                file_list = instructions.get("file_list")

                print(f'\nreceived command: {command}\n')
                if command != 'check-in':
                    self.log(f'received command: {command}', log_type='info')

                if command == 'update':
                    print('downloading update...')
                    self.log("downloading update", log_type='update')
                    self.update_manager.download_and_update('/' + msg)
                elif command == 'update_home_package':
                    pass
                elif command == 'update_config':
                    new_config = instructions.get("new_config")
                    h = new_config.get('host')
                    n = new_config.get('name')
                    ws = new_config.get('wifi_ssid')
                    wp = new_config.get('wifi_password')
                    if h is not None and n is not None and ws is not None and wp is not None:
                        self.device_settings.save_new_config(new_config)

                elif command == 'update_host':

                    new_host = instructions.get("host")
                    if new_host is not None:
                        self.device_settings.host = new_host
                        self.device_settings.save()

                elif command == 'update_all':
                    print('\ndownloading all...\n')
                    self.log("downloading update", log_type='update')
                    to_update = self.update_manager.download_all(file_list)

                    print("\nto_update:", *to_update, sep="\n")
                    self.log("updating files", log_type='update')
                    self.update_manager.update_all(to_update)

                    print("\ndeleting update files...\n")
                    self.update_manager.remove_update_directory()

                    print('\nrestarting...')
                    self.log("Finished updating. Restarting", log_type='update')
                    utime.sleep(2)
                    machine.reset()

                elif command == 'check-in':
                    self.log('here', log_type='check-in')

                elif command == 'restart':
                    print('restarting...')
                    self.log("Received Restart Command. Restarting", log_type='restart')

                    utime.sleep(2)
                    machine.reset()

                else:
                    self.log(f"Unknown command: {command}", log_type='error')

                    print(f"\nUnknown command: {command}\n")

            except KeyError:
                print("Error: Expected keys are not in the message.")
                self.log("Error: Expected keys are not in the message.", log_type='error')
            except Exception as e:
                print(f"Error in Home.on_message: {e}")
                self.log(f"Error in Home.on_message: {e}", log_type='error')

    def publish(self, topic, message, **kwargs):
        """
        Publishes a message to a specific topic on the MQTT broker.

        :param topic: The topic to publish the message to.
        :param message: The message to be published.
        """
        self.mqtt_manager.publish(topic, message, **kwargs)

    def subscribe(self, topic):
        """
        Subscribes to a specific topic on the MQTT broker.

        :param topic: The topic to subscribe to.
        """
        self.mqtt_manager.subscribe(topic)

    def set_callback(self, callback_function):
        """
        Sets the callback function for MQTT messages.

        :param callback_function: The callback function.
        """
        self.mqtt_manager.set_callback(callback_function)

    def check_msg(self):
        """
        Checks for MQTT messages.
        """
        self.mqtt_manager.check_msg()

    def mqtt_ping(self):
        self.mqtt_manager.ping()

    def main(self):
        self.start_sequence()
        print("------listening for messages------")
        self.log("listening for messages")
        while True:
            self.check_msg()
            utime.sleep_ms(100)

    def run(self):
        try:
            self.main()
        except KeyboardInterrupt:
            self.status_led_off()
        except Exception as e:
            self.restart_on_error(f'Main Loop Error: \n\t{e}')
