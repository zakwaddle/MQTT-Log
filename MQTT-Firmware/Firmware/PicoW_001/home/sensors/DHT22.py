import machine
import sys
import dht
import json


class DHT22Sensor:

    def __init__(self, pin, timer_n=1, measurement_interval_ms=5000):
        self.pin = machine.Pin(pin)
        self.sensor = dht.DHT22(self.pin)

        self.measurement_interval_ms = measurement_interval_ms
        self.on_measurement = None

        self.timer_n = timer_n
        self.timer = None

    def enable_interrupt(self):
        """Enable timer for regular measurements."""
        platform = sys.platform
        if platform == "esp32":
            self.timer = machine.Timer(self.timer_n * -1)
            self.timer.init(mode=machine.Timer.PERIODIC,
                            period=self.measurement_interval_ms,
                            callback=self.measure)
        elif platform == "rp2":
            self.timer = machine.Timer(mode=machine.Timer.PERIODIC,
                                       period=self.measurement_interval_ms,
                                       callback=self.measure)
        else:
            raise Exception(f"Unsupported platform: {platform}")

    def set_on_measurement(self, func):
        self.on_measurement = func

    def measure(self, _):
        self.sensor.measure()
        print(self.sensor.temperature(), self.sensor.humidity())
        if self.on_measurement is not None:
            self.on_measurement(self.sensor.temperature(), self.sensor.humidity())


class MQTTDHT22Sensor:
    def __init__(self, dht22_sensor: DHT22Sensor, mqtt_client, name_temp=None, name_humidity=None):
        self.dht22_sensor = dht22_sensor
        self.mqtt_client = mqtt_client
        self.sensor_index = self.dht22_sensor.timer_n

        self.name_temp = f"temp-{self.sensor_index}" if name_temp is None else name_temp
        self.name_humidity = f"humidity-{self.sensor_index}" if name_humidity is None else name_humidity

        self.base_topic = f"homeassistant/sensor/{self.mqtt_client.unit_id}"
        self.temp_topic = f"{self.base_topic}/{self.name_temp.lower().replace(' ', '_')}"
        self.temp_discovery_topic = f"{self.temp_topic}/config"
        self.humidity_topic = f"{self.base_topic}/{self.name_humidity.lower().replace(' ', '_')}"
        self.humidity_discovery_topic = f"{self.humidity_topic}/config"

        self.dht22_sensor.set_on_measurement(self.publish_measurement)

    def enable_interrupt(self):
        self.dht22_sensor.enable_interrupt()

    def publish_measurement(self, temperature, humidity):
        """Publish the last measurement to the MQTT topic."""
        self.mqtt_client.publish(self.temp_topic, str(temperature))
        self.mqtt_client.publish(self.humidity_topic, str(humidity))

    def publish_discovery(self, device_info):
        print(f"\n{self.name_temp} Discovery Topic: {self.temp_discovery_topic}")
        print(f"{self.name_temp} State Topic: {self.temp_topic}\n")
        print(f"\n{self.name_humidity} Discovery Topic: {self.humidity_discovery_topic}")
        print(f"{self.name_humidity} State Topic: {self.humidity_topic}\n")

        config_temp = {
            "name": self.name_temp,
            "device_class": "temperature",
            "unit_of_measurement": chr(176) + "C",
            "state_topic": self.temp_topic,
            "device": device_info,
            "unique_id": f"{self.mqtt_client.unit_id}-{self.sensor_index}_temp",
        }

        config_humidity = {
            "name": self.name_humidity,
            "device_class": "humidity",
            "unit_of_measurement": "%",
            "state_topic": self.humidity_topic,
            "device": device_info,
            "unique_id": f"{self.mqtt_client.unit_id}-{self.sensor_index}_humidity",
        }

        self.mqtt_client.publish(self.temp_discovery_topic, json.dumps(config_temp).encode("utf-8"), retain=True)
        self.mqtt_client.publish(self.humidity_discovery_topic, json.dumps(config_humidity), retain=True)


def setup_dht22_sensor(pin, timer_n, measurement_interval_ms, client, name_temp, name_humidity, device_info):
    sensor = DHT22Sensor(pin=pin, timer_n=timer_n, measurement_interval_ms=measurement_interval_ms)
    dht22 = MQTTDHT22Sensor(
        dht22_sensor=sensor,
        mqtt_client=client,
        name_temp=name_temp,
        name_humidity=name_humidity

    )
    dht22.publish_discovery(device_info)
    dht22.enable_interrupt()
    return dht22
