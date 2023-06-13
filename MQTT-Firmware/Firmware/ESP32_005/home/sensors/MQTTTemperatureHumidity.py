import machine
import dht
import sys


class MQTTTemperatureHumidity:
    """
    MQTTTemperatureHumidity class for interfacing DHT22 sensor with MQTT.

    This class can handle the temperature and humidity data from a DHT22 sensor,
    and publish the readings to specific MQTT topics.

    :param pin: GPIO pin where the DHT22 data pin is connected.
    :param client: An MQTT client instance to publish the data.
    :param temp_topic: MQTT topic where the temperature data will be published.
    :param humidity_topic: MQTT topic where the humidity data will be published.
    :param timer_index: Index for the hardware timer. Default is 1.
    """
    def __init__(self, pin: int, client, temp_topic: str, humidity_topic: str, timer_index: int = 1):
        self.pin = machine.Pin(pin, machine.Pin.IN)
        self.sensor = dht.DHT22(self.pin)
        self.client = client
        self.temperature_topic = temp_topic
        self.humidity_topic = humidity_topic
        self.timer_index = timer_index

    def read_sensor(self) -> tuple:
        """Read the temperature and humidity from the sensor."""
        self.sensor.measure()
        temp = self.sensor.temperature()
        humidity = self.sensor.humidity()
        return temp, humidity

    def update(self):
        """Update the temperature and humidity readings and publish to MQTT topics."""
        temperature, humidity = self.read_sensor()
        print('Temperature:', temperature, '°C')
        print('Humidity:', humidity, '%')
        self.client.publish(self.temperature_topic, str(temperature))
        self.client.publish(self.humidity_topic, str(humidity))

    def timer(self, update_period_ms: int):
        """Start or reset the timer that triggers the sensor update."""
        self.update()
        if sys.platform == "esp32":
            timer = machine.Timer(self.timer_index * -1)
            timer.init(period=update_period_ms, mode=machine.Timer.ONE_SHOT, callback=lambda t: self.timer(update_period_ms))
        elif sys.platform == "rp2":
            machine.Timer(period=update_period_ms, mode=machine.Timer.ONE_SHOT, callback=lambda t: self.timer(update_period_ms))
        else:
            raise Exception(f"Unsupported platform: {sys.platform}")
