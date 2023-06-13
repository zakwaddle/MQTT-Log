import utime
import machine
import sys
import json
from display import display, settings, update_numbers, setup_labels, on_display_message

from home import Home
from home.sensors import StatusLED

status_pin = None
if sys.platform == "rp2":
    status_pin = "LED"
elif sys.platform == "esp32":
    status_pin = 2


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


def connect_home(home_configs):
    home = Home(home_configs)
    if home:
        utime.sleep(0.5)
        led = StatusLED(status_pin)
        led.blink_light()
        led.on()
    return home



def main():

    display.sleep(False)
    setup_labels()

    config = load_config()
    home = connect_home(config)
    
#     pins = config.get("pins")
    topics = config.get("topics")
#     timers = config.get("timers")


    def on_message(topic, msg):
        home.on_message(topic, msg)
        on_display_message(topic, msg, topics)



    home.set_callback(on_message)
    
    home.subscribe(home.command_topic)
    home.subscribe(topics["desk_motion"])
    home.subscribe(topics["henry_temp"])
    home.subscribe(topics["henry_humidity"])
    
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
        display.sleep(True)
    except Exception as e:
        light = StatusLED(status_pin)
        light.off()
        display.sleep(True)

        print('Run Error: ', e)
        utime.sleep(5)
        machine.reset()
