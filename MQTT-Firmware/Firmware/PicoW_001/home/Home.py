import sys
import utime
import machine
import json
from .WiFiManager import WiFiManager
from .MQTTManager import MQTTManager
from .UpdateManager import UpdateManager
from .sensors.StatusLED import StatusLED


class HomeError(Exception):
    pass


class Home:
    status_pin = False
    """
    Home class is a wrapper around the MQTT, WiFi and Update managers.
    It provides a simple interface to handle connections and updates.
    """

    def __init__(self, config, use_ping=True):
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

        self.unit_id = config["unit_id"]
        self.command_topic = f"command/{self.unit_id}"
        self.timer = None
        self.use_ping = use_ping

        print("\nPlatform: ", self._platform, "\nUnit: ", self.unit_id)

        self.wifi_manager = WiFiManager(**config["wifi"])
        self.mqtt_manager = MQTTManager(unit_id=self.unit_id, **config["mqtt"])
        self.update_manager = UpdateManager(unit_id=self.unit_id, **config["ftp"])

    def platform_timer(self, timer_number=-1, **kwargs):
        if self._platform == "rp2":
            return machine.Timer(**kwargs)
        elif self._platform == 'esp32':
            if timer_number > 0:
                timer_number = timer_number * -1
            timer = machine.Timer(timer_number)
            timer.init(**kwargs)
            return timer

    def set_connection_check_timer(self):
        self.timer = self.platform_timer(timer_number=0,
                                         period=5000,
                                         mode=machine.Timer.PERIODIC,
                                         callback=self.check_connections)

    def connect(self, use_status_led=True, led_on_after_connect=True):
        print("\nconnecting WiFi")
        self.wifi_manager.connect_wifi()
        print("\nconnecting MQTT")
        self.mqtt_manager.connect_mqtt()
        self.set_connection_check_timer()
        if self.wifi_manager.is_connected() and self.mqtt_manager.is_connected and use_status_led:
            if self.status_pin:
                led = StatusLED(self.status_pin)
                led.blink_light()
                led.blink_light()
                if led_on_after_connect:
                    led.on()

    def check_connections(self, _):
        """
        Checks the WiFi connection and reconnects if the connection is lost.
        """
        if not self.wifi_manager.is_connected():
            print('Lost Wi-Fi connection. Reconnecting...')
            self.wifi_manager.connect_wifi()
            self.mqtt_manager.connect_mqtt()
        if not self.mqtt_manager.is_connected:
            self.mqtt_manager.connect_mqtt(clean_session=False)
        else:
            if self.use_ping:
                self.mqtt_ping(_)

    def on_message(self, topic, msg):
        """
        Handles the MQTT messages.


        :param topic: The topic of the message.
        :param msg: The received message.
        """
        t = topic.decode('utf-8')
        if t == self.command_topic:
            try:
                msg = msg.decode('utf-8')
                instructions = json.loads(msg)

                command = instructions.get("command")
                file_list = instructions.get("file_list")

                print(f'\nreceived command: {command}\n')

                if command == 'update':
                    print('downloading update...')
                    self.update_manager.download_and_update('/' + msg)

                elif command == 'update_all':
                    print('\ndownloading all...\n')
                    to_update = self.update_manager.download_all(file_list)

                    print("\nto_update:", *to_update, sep="\n")
                    self.update_manager.update_all(to_update)

                    print("\ndeleting update files...\n")
                    self.update_manager.remove_update_directory()

                    print('\nrestarting...')
                    machine.reset()

                elif command == 'restart':
                    print('restarting...')
                    utime.sleep(2)
                    machine.reset()

                else:
                    print(f"\nUnknown command: {command}\n")

            except KeyError:
                print("Error: Expected keys are not in the message.")
            except Exception as e:
                print(f"Error in Home.on_message: {e}")

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

    def mqtt_ping(self, _):
        # print("ping!")
        self.mqtt_manager.ping()
