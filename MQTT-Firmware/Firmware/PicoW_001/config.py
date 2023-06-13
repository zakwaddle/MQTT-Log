import sys

UNIT_ID = "PicoW_001"

home_config = {

    "unit_id": f"{UNIT_ID}",
    "description": "Kitchen Controller - Cabinet Light/Motion Sensor/Weather Sensor",
    "display_name": "kitchen-pico",

    "wifi": {
        "ssid": "the_interwebs",
        "password": "935Ravine"
    },

    "mqtt": {
        "server": "homeassistant.local",
        "port": 1883,
        "username": "Zak",
        "password": "935Ravine"
    },

    "ftp": {
        "host": "homeassistant.local",
        "user": "microcontrollers",
        "password": "microcontrollers"
    }

}

device_info = {

    "name": f"{UNIT_ID}",
    "manufacturer": "ZRW",
    "model": f"{sys.platform.upper()}-Circuit",
    "identifiers": f"{UNIT_ID}"

}

sensors = {

    "motion": {
        "pin": 18,
        "retrigger_delay_ms": 120000,
        "timer_n": 1,
        "name": "Kitchen Motion",
    },

    "weather": {
        "pin": 26,
        "measurement_interval_ms": 10000,
        "timer_n": 2,
        "name_temp": "Kitchen Temperature",
        "name_humidity": "Kitchen Humidity"
    },

    "led1": {
        "pin": 22,
        "freq": 300,
        "timer_n": 3,
        "fade_time_ms": 4,
        "brightness_scale": 255,
        "name": "Cabinet Lights"
    },

    "led2": {
        "pin": 21,
        "freq": 300,
        "timer_n": 4,
        "fade_time_ms": 4,
        "brightness_scale": 255,
        "name": "Sink Light"
    }

}
