import utime
import machine
import config
from home import Home
from home.sensors import setup_dht22_sensor

home_client = Home(config.home_config, use_ping=True)
sensors = config.sensors
device_info = config.device_info


def main():	
    weather = None
    home_client.connect(led_on_after_connect=True)

    def on_message(topic, msg):
        home_client.on_message(topic, msg)

    home_client.set_callback(on_message)
    home_client.subscribe(home_client.command_topic)

    while True:
        home_client.check_msg()
    

        utime.sleep_ms(100)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        home_client.status_led_off()
    except Exception as e:
        home_client.restart_on_error(f'Main Loop Error: \n\t{e}')
