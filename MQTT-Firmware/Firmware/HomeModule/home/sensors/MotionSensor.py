import machine
import sys
import json


class MotionSensor:

    def __init__(self, pin, retrigger_delay_ms, timer_n=1):
        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.retrigger_delay_ms = retrigger_delay_ms

        self.on_motion_detected = None
        self.on_motion_not_detected = None

        self.timer_n = timer_n
        self.timer = None
        self.last_motion = 0

    def enable_interrupt(self):
        """Enable interrupt for motion pin."""
        self.pin.irq(trigger=machine.Pin.IRQ_RISING, handler=self.motion_change)

    def set_on_motion_detected(self, func):
        self.on_motion_detected = func

    def set_on_motion_not_detected(self, func):
        self.on_motion_not_detected = func

    def set_timer_n(self, timer_n):
        self.timer_n = timer_n

    def motion_change(self, _):
        self._motion_detected()
        if self.timer is not None:
            self.timer.deinit()
            self.timer = None

        platform = sys.platform
        if platform == "esp32":
            self.timer = machine.Timer(self.timer_n * -1)
            self.timer.init(mode=machine.Timer.ONE_SHOT,
                            period=self.retrigger_delay_ms,
                            callback=self._no_motion_detected)
        elif platform == "rp2":
            self.timer = machine.Timer(mode=machine.Timer.ONE_SHOT,
                                       period=self.retrigger_delay_ms,
                                       callback=self._no_motion_detected)
        else:
            raise Exception(f"Unsupported platform: {platform}")

    def _motion_detected(self):
        if not self.last_motion:
            self.last_motion = 1
            if self.on_motion_detected is not None:
                self.on_motion_detected()

    def _no_motion_detected(self, _):
        self.last_motion = 0
        if self.on_motion_not_detected is not None:
            self.on_motion_not_detected()


class MQTTMotionSensor:
    def __init__(self, motion_sensor: MotionSensor, mqtt_client, name=None):
        self.motion_sensor = motion_sensor
        self.mqtt_client = mqtt_client
        self.sensor_index = self.motion_sensor.timer_n

        self.name = f"motion_{self.sensor_index}" if name is None else name
        self.topic = f"homeassistant/binary_sensor/{self.mqtt_client.unit_id}/{self.name.lower().replace(' ', '_')}"
        self.state_topic = f"{self.topic}/state"
        self.motion_sensor.set_on_motion_detected(self.publish_last_motion)
        self.motion_sensor.set_on_motion_not_detected(self.publish_last_motion)

    def enable_interrupt(self):
        self.motion_sensor.enable_interrupt()

    def publish_last_motion(self):
        """Publish the last motion detected to the MQTT topic."""
        self.mqtt_client.publish(self.state_topic, str(self.motion_sensor.last_motion))

    def set_name(self, name):
        self.name = name
        self.topic = f"homeassistant/binary_sensor/{self.mqtt_client.unit_id}/{self.name.lower().replace(' ', '_')}"

    def publish_discovery(self, device_info):
        discovery_topic = f"{self.topic}/config"
        print("Motion Sensor Discovery Topic: ", discovery_topic)
        print("Motion Sensor State Topic: ", self.state_topic)
        config = {
            "name": self.name,
            "device_class": "motion",
            "device": device_info,
            "unique_id": f"{self.mqtt_client.unit_id}_{self.sensor_index}",
            "payload_off": "0",
            "payload_on": "1",
            "state_topic": f"{self.topic}/state"
        }
        self.mqtt_client.publish(discovery_topic, json.dumps(config), retain=True)


def setup_motion_sensor(pin, retrigger_delay_ms, timer_n, client, name, device_info):
    motion = MQTTMotionSensor(
        motion_sensor=MotionSensor(pin=pin, retrigger_delay_ms=retrigger_delay_ms, timer_n=timer_n),
        mqtt_client=client,
        name=name
    )
    print(device_info)
    motion.publish_discovery(device_info)
    motion.enable_interrupt()
    return motion

# if __name__ == "__main__":
#
#     def load_config():
#         with open("config.json", "r") as f:
#             return json.load(f)
#
#
#     def setup_motion_sensor(p, d, tn, client, name):
#         motion = MQTTMotionSensor(
#             motion_sensor=MotionSensor(pin=p, retrigger_delay_ms=d, timer_n=tn),
#             mqtt_client=client
#         )
#         motion.set_topic("homeassistant/" + motion.topic)
#         motion.set_name(name)
#         motion.publish_discovery()
#         motion.enable_interrupt()
#         return motion
#
#
#     home = Home(load_config())
#     m1 = setup_motion_sensor(17, 10000, 1, home, "OfficeMotion1")
#     m2 = setup_motion_sensor(16, 10000, 2, home, "OfficeMotion2")
#
#     while 1:
#         machine.idle()
