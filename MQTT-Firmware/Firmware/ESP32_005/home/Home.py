import sys
import utime
import machine
from .WiFiManager import WiFiManager
from .MQTTManager import MQTTManager
from .UpdateManager import UpdateManager


class Home:
    """
    Home class is a wrapper around the MQTT, WiFi and Update managers.
    It provides a simple interface to handle connections and updates.
    """

    def __init__(self, config):
        """
        Initializes Home with the provided configuration dictionary.

        Parameters:
        config (dict): A dictionary containing the configurations for unit id, WiFiManager, MQTTManager and UpdateManager. Each of these configurations is another dictionary that includes all the necessary parameters for the respective manager.

        For example:
        config = {
            "unit_id": "ESP32_004",
            "wifi": {
                "ssid": "YourWiFiSSID",
                "password": "YourWiFiPassword"
            },
            "mqtt": {
                "server": "mqtt.example.com",
                "port": 1883,
                "username": "mqtt_user",
                "password": "mqtt_password"
            },
            "ftp": {
                "host": "ftp.example.com",
                "user": "ftp_user",
                "password": "ftp_password"
            }
        }
        """
        self.unit_id = config["unit_id"]
        self.command_topic = f"{self.unit_id}/command"

        print("Platform: ", sys.platform, "\nUnit: ", self.unit_id, "\n")

        self.wifi_manager = WiFiManager(**config["wifi"])
        self.mqtt_manager = MQTTManager(unit_id=self.unit_id, **config["mqtt"])
        self.update_manager = UpdateManager(unit_id=self.unit_id, **config["ftp"])

    def on_message(self, topic, msg):
        """
        Handles the MQTT messages.

        :param topic: The topic of the message.
        :param msg: The received message.

        Returns:
        None
        """
        t = topic.decode('utf-8')
        if t == self.command_topic:
            instructions = msg.decode('utf-8')

            try:
                command, message = instructions.split('/', 1)
            except ValueError:
                command = instructions
                message = ""

            print(f'\n-received command-\n\tcommand: {command}\n\tmessage: {message}\n')

            if command == 'update':
                print('downloading update...')
                self.update_manager.download_and_update('/' + message)

            elif command == 'restart':
                print('restarting...')
                utime.sleep(2)
                machine.reset()

    def publish(self, topic, message):
        """
        Publishes an MQTT message.

        Parameters:
        topic (str): The topic of the message.
        message (str): The message to be published.

        Returns:
        None
        """
        self.mqtt_manager.publish(topic, message)

    def subscribe(self, topic):
        """
        Subscribes to an MQTT topic.

        Parameters:
        topic (str): The topic to subscribe to.

        Returns:
        None
        """
        self.mqtt_manager.subscribe(topic)

    def set_callback(self, callback_function):
        """
        Sets the callback function for MQTT messages.

        Parameters:
        callback_function (function): The callback function.

        Returns:
        None
        """
        self.mqtt_manager.set_callback(callback_function)

    def check_msg(self):
        """
        Checks for MQTT messages.

        Returns:
        None
        """
        self.mqtt_manager.check_msg()
