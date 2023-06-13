import utime
import machine
import sys
import json
from home import Home
from home.sensors import StatusLED, MQTTTemperatureHumidity

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
        # led.on()
    return home


def main():
    config = load_config()
    home = connect_home(config)
    pins = config.get("pins")
    
    try:
        weather = MQTTTemperatureHumidity(
            pin=pins["dht22"],
            client=home,
            sensor_index=1
            )
        weather.timer(5000)
    except Exception as e:
        print("\nWeather Error: \n\t", e, "\n")

    def on_message(topic, msg):
        home.on_message(topic, msg)

    home.set_callback(on_message)
    home.subscribe(home.command_topic)

    while True:
        home.check_msg()
        utime.sleep_ms(100)


def run():
    while True:
        try:
            main()
        except Exception as e:
            print('Main Loop Error:', e)
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
