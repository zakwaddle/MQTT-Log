from .lib.umqtt.simple import MQTTClient


class MQTTManager:
    """
    MQTTManager class helps to manage the MQTT client of the device.
    """

    def __init__(self, unit_id, server, port, username, password):
        """
        Initializes MQTTManager with provided parameters.

        Parameters:
        unit_id (str): The unit id of the device.
        server (str): The MQTT broker server address.
        port (int): The port number of the MQTT broker server.
        username (str): The username for the MQTT broker server.
        password (str): The password for the MQTT broker server.
        """
        self.unit_id = unit_id
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.mqtt_client = None

        self.connect_mqtt()

    def connect_mqtt(self):
        """
        Connects to the MQTT broker with provided server, port, username, and password.

        Returns:
        None
        """
        self.mqtt_client = MQTTClient(self.unit_id, self.server, self.port, self.username, self.password)
        self.mqtt_client.connect()
        print('Connected to MQTT broker:', self.server)

    def publish(self, topic, message):
        """
        Publishes a message to a specific topic on the MQTT broker.

        Parameters:
        topic (str): The topic to publish the message to.
        message (str): The message to be published.

        Returns:
        None
        """
        self.mqtt_client.publish(topic, message)

    def subscribe(self, topic):
        """
        Subscribes to a specific topic on the MQTT broker.

        Parameters:
        topic (str): The topic to subscribe to.

        Returns:
        None
        """
        self.mqtt_client.subscribe(topic)

    def set_callback(self, callback_function):
        """
        Sets the callback function that will be called when a message arrives for a subscribed topic.

        Parameters:
        callback_function (function): The callback function.

        Returns:
        None
        """
        self.mqtt_client.set_callback(callback_function)

    def check_msg(self):
        """
        Checks for any incoming messages on the subscribed topics.

        Returns:
        None
        """
        self.mqtt_client.check_msg()
