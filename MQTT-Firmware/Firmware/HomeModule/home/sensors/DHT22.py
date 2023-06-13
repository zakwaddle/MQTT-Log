import machine
# import sys
import dht
import json
from ..Timer import Timer


class DHT22Sensor:

    def __init__(self, pin):
        self.pin = machine.Pin(pin)
        self.sensor = dht.DHT22(self.pin)

    def measure(self):
        self.sensor.measure()

    def temperature(self):
        return self.sensor.temperature()

    def humidity(self):
        return self.sensor.humidity()


class MQTTDHT22Sensor:
    def __init__(self, dht22_sensor: DHT22Sensor, mqtt_client, name_temp=None, name_humidity=None, timer_n=1):
        self.dht22_sensor = dht22_sensor
        self.mqtt_client = mqtt_client
        self.sensor_index = timer_n

        self.name_temp = f"temp-{self.sensor_index}" if name_temp is None else name_temp
        self.name_humidity = f"humidity-{self.sensor_index}" if name_humidity is None else name_humidity

        self.base_topic = f"homeassistant/sensor/{self.mqtt_client.unit_id}"
        self.temp_topic = f"{self.base_topic}/{self.name_temp.lower().replace(' ', '_')}"
        self.temp_discovery_topic = f"{self.temp_topic}/config"
        self.humidity_topic = f"{self.base_topic}/{self.name_humidity.lower().replace(' ', '_')}"
        self.humidity_discovery_topic = f"{self.humidity_topic}/config"

        self.timer = None
        self.measurement_errors = 0
        self.active = True

    def measure(self):
        try:
            self.dht22_sensor.measure()
            temperature = self.dht22_sensor.temperature()
            humidity = self.dht22_sensor.humidity()
            # self.publish_measurement(temperature, humidity)
            self.measurement_errors = 0
            self.active = True
            return temperature, humidity
        except Exception as e:
            print(f"Weather Measurement Error: {e}")
            self.mqtt_client.log(f"Weather Measurement Error: {e}")
            self.measurement_errors += 1
            if self.measurement_errors > 5:
                if self.timer is not None:
                    self.timer.stop()
                    print("Disabled Weather Timer")
                    self.mqtt_client.log("Disabled Weather Timer")
                    self.active = False
            return None, None

    def publish_measurement(self, temperature, humidity):
        """Publish the last measurement to the MQTT topic."""
        self.mqtt_client.publish(self.temp_topic, str(temperature))
        self.mqtt_client.publish(self.humidity_topic, str(humidity))

    def measure_and_publish(self):
        temperature, humidity = self.measure()
        if temperature is not None and humidity is not None:
            print(f"Temperature: {temperature}    Humidity: {humidity}%")
            self.publish_measurement(temperature, humidity)

    def enable_interrupt(self, measurement_interval_ms):
        """Enable timer for regular measurements."""
        print(f"Weather Timer Started")
        self.timer = Timer(timer_number=self.sensor_index,
                           mode=Timer.PERIODIC,
                           period=measurement_interval_ms,
                           callback=self.measure_and_publish)

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
    sensor = DHT22Sensor(pin=pin)
    dht22 = MQTTDHT22Sensor(
        dht22_sensor=sensor,
        mqtt_client=client,
        name_temp=name_temp,
        name_humidity=name_humidity,
        timer_n=timer_n
    )
    dht22.publish_discovery(device_info)
    dht22.enable_interrupt(measurement_interval_ms)
    return dht22
