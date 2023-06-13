import machine
import sys


class MQTTFan:
    """
    A class to control a fan using MQTT.

    Attributes
    ----------
    on_off_pin : Pin
        Pin object associated with the fan's on-off switch.
    pwm_pin : Pin
        Pin object associated with the fan's PWM.
    pwm : PWM
        PWM object associated with the fan.
    mqtt_client : MQTTClient
        MQTT client for publishing and receiving messages.
    set_speed_topic : str
        Topic to set fan speed.
    get_speed_topic : str
        Topic to get fan speed.
    set_on_topic : str
        Topic to turn on the fan.
    get_on_topic : str
        Topic to get fan on state.
    state : bool
        State of the fan (on/off).
    speed : int
        Speed of the fan.

    Methods
    -------
    map_percentage_to_duty_cycle(percentage):
        Maps percentage to duty cycle.
    set_speed(speed):
        Sets fan speed.
    on():
        Turns the fan on.
    off():
        Turns the fan off.
    publish_speed():
        Publishes fan speed.
    publish_on_state():
        Publishes fan on state.
    on_message(topic, msg):
        Handles received MQTT messages.
    """

    def __init__(self, pwm_pin, on_off_pin, freq, mqtt_client, set_speed_topic, get_speed_topic, set_on_topic,
                 get_on_topic):
        self.on_off_pin = machine.Pin(on_off_pin, machine.Pin.OUT)
        self.pwm_pin = machine.Pin(pwm_pin)
        self.pwm = machine.PWM(self.pwm_pin, freq=freq)
        self.mqtt_client = mqtt_client
        self.set_speed_topic = set_speed_topic
        self.get_speed_topic = get_speed_topic
        self.set_on_topic = set_on_topic
        self.get_on_topic = get_on_topic

        self.state = False
        self.speed = 50
        self.off()
        self.publish_speed()

    def map_percentage_to_duty_cycle(self, percentage: int) -> int:
        """
        Maps a percentage to the corresponding duty cycle.

        Args:
            percentage: The desired percentage (0-100).

        Returns:
            The duty cycle that corresponds to the given percentage.
        """
        input_range = (0, 100)

        # Scale the input percentage to the 0-1 range
        scaled_input = (percentage - input_range[0]) / (input_range[1] - input_range[0])

        # Apply a quadratic curve
        curved_output = scaled_input ** 1.5

        if sys.platform == "rp2":
            output_range = (0, 65535)
        elif sys.platform == "esp32":
            output_range = (0, 1023)
        else:
            raise Exception(f"Unsupported platform: {sys.platform}")

        # Scale the output back to the appropriate duty cycle range
        duty_cycle = int(output_range[0] + curved_output * (output_range[1] - output_range[0]))

        return duty_cycle

    def set_speed(self, speed: int):
        """
        Set the speed of the fan.

        Args:
            speed: The desired speed percentage (0-100).
        """
        print('Setting fan speed: ', speed, '%')
        duty_cycle = self.map_percentage_to_duty_cycle(speed)

        if sys.platform == "rp2":
            self.pwm.duty_u16(duty_cycle)
        elif sys.platform == "esp32":
            self.pwm.duty(duty_cycle)
        else:
            raise Exception(f"Unsupported platform: {sys.platform}")

        self.speed = speed

    def on(self):
        """Turns the fan on."""
        self.state = True
        self.on_off_pin(1)
        self.publish_on_state()
        self.set_speed(self.speed)

    def off(self):
        """Turns the fan off."""
        self.state = False
        self.on_off_pin(0)
        self.pwm.duty(0)
        self.publish_on_state()

    def publish_speed(self):
        """Publishes fan speed."""
        self.mqtt_client.publish(self.get_speed_topic, str(self.speed))

    def publish_on_state(self):
        """Publishes fan on state."""
        self.mqtt_client.publish(self.get_on_topic, 'true' if self.state else 'false')
        print('Fan is now', 'on' if self.state else 'off')

    def on_message(self, topic, msg):
        """
        Handles received MQTT messages.
        """
        topic = topic.decode('utf-8')
        msg = msg.decode('utf-8')

        if topic == self.set_speed_topic:
            speed = int(msg)
            if speed == 0:
                self.speed = 0
                self.off()
            else:
                if not self.state:
                    self.on()
                self.set_speed(speed)
                self.publish_speed()

        elif topic == self.set_on_topic:
            if msg == 'true':
                self.on()
            elif msg == 'false':
                self.off()


# import machine
#
#
# class MQTTFan:
#     def __init__(self, pwm_pin, on_off_pin, freq, mqtt_client, set_speed_topic, get_speed_topic, set_on_topic, get_on_topic, get_online_topic):
#         self.on_off_pin = machine.Pin(on_off_pin, machine.Pin.OUT)
#         self.pwm_pin = machine.Pin(pwm_pin)
#         self.pwm = machine.PWM(self.pwm_pin, freq=freq)
#         self.pwm.duty(0)
#         self.mqtt_client = mqtt_client
#         self.set_speed_topic = set_speed_topic
#         self.get_speed_topic = get_speed_topic
#         self.set_on_topic = set_on_topic
#         self.get_on_topic = get_on_topic
#         self.get_online_topic = get_online_topic
#
#         self.state = False
#         self.speed = 50
#         self.off()
#         self.mqtt_client.publish(self.get_speed_topic, str(self.speed))
#
#
#     def map_percentage_to_duty_cycle(self, percentage):
#         max_duty = 1023
#         input_range = (0, 100)
#         output_range = (0, max_duty)
#
#         # Scale the input percentage to the 0-1 range
#         scaled_input = (percentage - input_range[0]) / (input_range[1] - input_range[0])
#
#         # Apply a quadratic curve
#         curved_output = scaled_input ** 1.5
#
#         # Scale the output back to the appropriate duty cycle range
#         duty_cycle = int(output_range[0] + curved_output * (output_range[1] - output_range[0]))
#
#         return duty_cycle
#
#
#     def set_speed(self, speed):
# #         if speed == 0:
# #             self.off()
# #         else:
#         print('setting fan speed: ', speed, '%')
#         duty_cycle = self.map_percentage_to_duty_cycle(speed)
#         self.pwm.duty(duty_cycle)
#         self.speed = speed
#
#     def on(self):
#         self.state = True
#         self.on_off_pin(1)
# #         print('fan on')
# #
# #         if self.speed == 0:
# #             self.speed = 1
#         self.mqtt_client.publish(self.get_on_topic, 'true')
#         self.set_speed(self.speed)
#
#     def off(self):
#         self.state = False
#         self.on_off_pin(0)
#         self.pwm.duty(0)
#         self.mqtt_client.publish(self.get_on_topic, 'false')
#         print('fan off')
#
#
#     def mqtt_callback(self, topic, msg):
#         topic = topic.decode('utf-8')
#         msg = msg.decode('utf-8')
#
#         if topic == self.set_speed_topic:
#             speed = int(msg)
#             if speed == 0:
#                 self.speed = 0
#                 self.off()
#             else:
#                 if not self.state:
#                     self.on()
#                 self.set_speed(speed)
#                 self.mqtt_client.publish(self.get_speed_topic, str(self.speed))
#
#         elif topic == self.set_on_topic:
#             if msg == 'true':
#                 self.on()
#             elif msg == 'false':
#                 self.off()
#
# #             self.mqtt_client.publish(self.get_on_topic, 'true' if self.state else 'false')
#
#
#     def setup(self):
#         self.mqtt_client.publish(self.get_online_topic, 'true')
# #         self.mqtt_client.set_last_will(self.get_online_topic, 'false')
#         self.mqtt_client.set_callback(self.mqtt_callback)
#         self.mqtt_client.subscribe(self.set_speed_topic)
#         self.mqtt_client.subscribe(self.set_on_topic)
#
#     def update(self):
#         self.mqtt_client.check_msg()
#
