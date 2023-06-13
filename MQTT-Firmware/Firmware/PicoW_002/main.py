import utime
import config
from home import Home
from home.sensors import setup_dht22_sensor

home_client = Home(config.home_config, use_ping=True)
sensors = config.sensors
device_info = config.device_info


def main():
    weather = None
    home_client.connect(led_on_after_connect=False)

    try:
        weather = setup_dht22_sensor(client=home_client, device_info=device_info, **sensors['weather'])
    except Exception as er:
        home_client.log(f"Weather Error: {er}", log_type='error')
        print("\nWeather Error:\n\t", er, "\n")

    def on_message(topic, msg):
        home_client.on_message(topic, msg)

    home_client.set_callback(on_message)
    home_client.subscribe(home_client.command_topic)

    while True:
        home_client.check_msg()

        if weather is not None and not weather.active:
            raise Exception("Weather Sensor Failure")

        utime.sleep_ms(100)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        home_client.status_led_off()
    except Exception as e:
        home_client.restart_on_error(f'Main Loop Error: \n\t{e}')
