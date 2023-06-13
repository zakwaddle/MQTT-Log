"""
This module contains the `MQTTDimmableLED` class, which provides an interface for controlling
an LED connected to a microcontroller (either Raspberry Pi Pico or ESP32) using MQTT messages.

The `MQTTDimmableLED` class allows you to control the brightness of an LED, adjusting its intensity
based on messages received over MQTT. The class works by creating a PWM (Pulse Width Modulation)
object on a specified pin, which is then used to control the LED's brightness.

The class also supports a fading effect, where the LED's brightness gradually changes from one level
to another over a specified period of time.

This class requires an MQTT client object, the pin number where the LED is connected, and the MQTT topic
to listen for messages.

Dependencies:
    machine, sys

Usage:
    import MQTTClient
    mqtt_client = MQTTClient(...)
    led = MQTTDimmableLED(mqtt_client, pin=2, light_topic='home/room/light')
    ...
"""
import machine
import sys


class MQTTDimmableLED:
    """
    Class to control a dimmable LED via MQTT messages. Supports both 'rp2' and 'esp32' platforms.
    """

    def __init__(self, mqtt_client, pin: int, light_topic: str,
                 freq: int = 1000, timer_index: int = 1, fade_time_ms: int = 1):
        """
        Initialize the MQTTDimmableLED.

        Args:
            :param mqtt_client: MQTT client instance to use for communication.
            :param pin: The GPIO pin number where the LED is connected.
            :param light_topic: The MQTT topic to listen for light control messages.
            :param freq: The frequency for the PWM signal. Default is 1000.
            :param timer_index: Index of the timer to be used for fading. Default is 1.
            :param fade_time_ms: Fade time in milliseconds. Default is 1.
        """
        self._platform = sys.platform
        if self._platform not in ['rp2', 'esp32']:
            raise ValueError(f"Unsupported platform: {self._platform}")

        self.mqtt_client = mqtt_client
        self.light_topic = light_topic
        self.pwm = machine.Pin(pin)
        self.freq = freq
        self._timer_index = timer_index
        self._fade_time_ms = fade_time_ms

        if self._platform == "rp2":
            self.light = machine.PWM(self.pwm)
            self.light.freq(freq)
        elif self._platform == "esp32":
            self.light = machine.PWM(self.pwm, freq=self.freq)

        self.brightness = 0
        self._set_duty(self.brightness)
        self.publish_brightness()

    def _set_duty(self, value: int):
        """
        Set the PWM duty cycle.

        :param value: The duty cycle value to set.
        """
        if self._platform == "rp2":
            self.light.duty_u16(value)
        elif self._platform == "esp32":
            self.light.duty(value)

    def percent_to_duty(self, value: int) -> int:
        """
        Convert a percentage value to a duty cycle value.

        :param value: The percentage value to convert.
        :return: The converted duty cycle value.
        """
        if self._platform == "rp2":
            return round((65535 / 100) * value)
        elif self._platform == "esp32":
            return round((1023 / 100) * value)
        else:
            return value

    def publish_brightness(self):
        """
        Publish the current brightness value to the MQTT topic.
        """
        self.mqtt_client.publish(self.light_topic, str(self.brightness))

    def fade(self, brightness: int):
        """
        Gradually change the brightness to a new value.

        :param brightness: The new brightness value to fade to.
        """
        duty = self.percent_to_duty(self.brightness)
        self._set_duty(duty)

        if self._platform == 'rp2':
            machine.Timer(period=self._fade_time_ms, mode=machine.Timer.ONE_SHOT, callback=lambda t: self.set_brightness(brightness))
        else:
            timer = machine.Timer(self._timer_index * -1)
            timer.init(period=self._fade_time_ms, mode=machine.Timer.ONE_SHOT, callback=lambda t: self.set_brightness(brightness))

    def set_brightness(self, brightness: int):
        """
        Set the brightness to a new value.

        :param brightness: The new brightness value.
        """
        if not 0 <= brightness <= 100:
            raise ValueError("Brightness must be a value between 0 and 100")

        print("setting brightness: ", self.brightness)
        if self.brightness < brightness:
            self.brightness += 1
            self.fade(brightness)
        elif self.brightness > brightness:
            self.brightness -= 1
            self.fade(brightness)
        else:
            self.brightness = brightness
            duty = self.percent_to_duty(self.brightness)
            self._set_duty(duty)

    def on_message(self, topic, msg):
        """
        Handle a received MQTT message.

        :param topic: The topic of the received message.
        :param msg: The received message.
        """
        topic = topic.decode('utf-8')
        msg = msg.decode('utf-8')

        if topic == self.light_topic:
            try:
                self.set_brightness(int(msg))
            except ValueError:
                print(f"Invalid brightness value received: {msg}")
