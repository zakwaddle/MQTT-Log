import utime
import machine
import sys
import config
from home import Home
from home.sensors import StatusLED, setup_led, setup_motion_sensor, setup_dht22_sensor

status_pin = None
if sys.platform == "rp2":
    status_pin = "LED"
elif sys.platform == "esp32":
    status_pin = 2


def connect_home(home_configs):
    home = Home(home_configs)
    if home:
        utime.sleep(0.5)
        led = StatusLED(status_pin)
        led.blink_light()
        led.on()
    return home


def main():
    home = connect_home(config.home_config)
    sensors = config.sensors
    print(config.device_info)

    # try:
    #     motion = setup_motion_sensor(client=home, **sensors['motion'])
    # except Exception as er:
    #     print("\nMotion Error:\n\t", er, "\n")
    #
    # try:
    #     weather = setup_dht22_sensor(client=home, **sensors['weather'])
    # except Exception as er:
    #     print("\nWeather Error:\n\t", er, "\n")

    # led = None
    # try:
    #     led = setup_led(client=home, **sensors["led"])
    # except Exception as er:
    #     print("\nLED Error:\n\t", er, "\n")

    def on_message(topic, msg):
        home.on_message(topic, msg)
        # led.on_message(topic, msg)

    home.set_callback(on_message)
    home.subscribe(home.command_topic)
    # if led is not None:
    #     home.subscribe(led.command_topic)
    #     home.subscribe(led.brightness_command_topic)

    home.platform_timer(-4, mode=machine.Timer.PERIODIC, period=30000, callback=home.mqtt_ping)

    while True:
        home.check_msg()
        utime.sleep_ms(100)


def run():
    while True:
        try:
            main()
        except Exception as err:
            print('Main Loop Error:', err)
            error_led = StatusLED(status_pin)
            error_led.on()
            utime.sleep(5)
            machine.reset()


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        light = StatusLED(status_pin)
        light.off()
    except Exception as e:
        light = StatusLED(status_pin)
        light.off()
        print('Run Error: ', e)
        utime.sleep(5)
        machine.reset()

