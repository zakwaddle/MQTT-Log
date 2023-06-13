import utime
import machine
import config
from home import Home
from home.sensors import setup_led, setup_motion_sensor
from home.sensors.StatusLED import StatusLED

"""
poo poo pa-choo
"""

home_client = Home(config.home_config, use_ping=True)
sensors = config.sensors
device_info = config.device_info


def status_led_off():
    light = StatusLED(home_client.status_pin)
    light.off()


def restart_on_error(error_message):
    print(error_message)
    home_client.log(error_message)
    status_led_off()
    utime.sleep(5)
    machine.reset()


def main():
    home_client.connect(led_on_after_connect=True)

    try:
        motion = setup_motion_sensor(client=home_client, device_info=device_info, **sensors['motion'])
    except Exception as er:
        home_client.log(f"Motion Error: {er}")
        print("\nMotion Error:\n\t", er, "\n")

    led1 = None
    try:
        led1 = setup_led(client=home_client, device_info=device_info, **sensors["led1"])
    except Exception as er:
        home_client.log(f"LED1 Error: {er}")
        print("\nLED1 Error:\n\t", er, "\n")
        
    led2 = None
    try:
        led2 = setup_led(client=home_client, device_info=device_info, **sensors["led2"])
    except Exception as er:
        home_client.log(f"LED2 Error: {er}")
        print("\nLED2 Error:\n\t", er, "\n")

    def on_message(topic, msg):
        home_client.on_message(topic, msg)
        led1.on_message(topic, msg)
        led2.on_message(topic, msg)

    home_client.set_callback(on_message)
    home_client.subscribe(home_client.command_topic)
    if led1 is not None:
        home_client.subscribe(led1.command_topic)
        home_client.subscribe(led1.brightness_command_topic)
    if led2 is not None:
        home_client.subscribe(led2.command_topic)
        home_client.subscribe(led2.brightness_command_topic)

    while True:
        home_client.check_msg()
        utime.sleep_ms(100)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        status_led_off()
    except Exception as e:
        restart_on_error(f'Main Loop Error: \n\t{e}')
