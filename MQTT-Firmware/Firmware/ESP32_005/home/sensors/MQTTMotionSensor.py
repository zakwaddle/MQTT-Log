"""
MQTTMotionSensor Class
----------------------
This class handles motion detection functionality for a given pin, and publishes motion updates to an MQTT topic.
It is designed to work with both ESP32 and Raspberry Pi Pico (rp2) platforms.
"""

import machine
import sys
import utime


class MQTTMotionSensor:
    def __init__(self, pin: int, mqtt_client, topic: str, debounce_time: int = 20, timer_index: int = 1):
        """
        Initialize the MQTTMotionSensor object.

        :param pin: The pin number for the motion sensor.
        :param mqtt_client: MQTT client object.
        :param topic: MQTT topic where the motion updates are published.
        :param debounce_time: Debounce time in seconds to avoid false positives.
        :param timer_index: Index for the machine.Timer object.
        """
        self.motion_pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.mqtt_client = mqtt_client
        self.topic = topic

        self.timer_index = timer_index
        self.debounce_time = debounce_time

        self.last_motion = 0
        self.motion_detected_at = 0
        self.publish_last_motion()

    def publish_last_motion(self):
        """Publish the last motion detected to the MQTT topic."""
        self.mqtt_client.publish(self.topic, str(self.last_motion))

    def _motion_detected(self, time: int):
        """Handle motion detection."""
        self.motion_detected_at = time
        if not self.last_motion:
            self.last_motion = 1
            self.publish_last_motion()
            print("Motion detected")

    def _motion_not_detected(self, time: int):
        """Handle the absence of motion."""
        tick_diff = utime.ticks_diff(time, self.motion_detected_at)
        debounce = self.debounce_time * 1000
        is_after_debounce = tick_diff >= debounce
        if is_after_debounce:
            self.last_motion = 0
            self.publish_last_motion()
            print("No motion")

    def update(self):
        """Update motion status."""
        motion = self.motion_pin.value()
        current_time = utime.ticks_ms()
        if motion:
            self._motion_detected(current_time)
        if not motion and self.last_motion:
            self._motion_not_detected(current_time)

    def timer(self, update_period_ms: int):
        """
        Initialize the motion timer.

        :param update_period_ms: Update period in milliseconds.
        """
        self.update()
        platform = sys.platform
        if platform == "esp32":
            timer = machine.Timer(self.timer_index * -1)
            timer.init(
                period=update_period_ms,
                mode=machine.Timer.ONE_SHOT,
                callback=lambda t: self.timer(update_period_ms))
        elif platform == "rp2":
            machine.Timer(
                period=update_period_ms,
                mode=machine.Timer.ONE_SHOT,
                callback=lambda t: self.timer(update_period_ms))
        else:
            raise Exception(f"Unsupported platform: {platform}")
