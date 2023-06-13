import sys

UNIT_ID = "ESP32_004"

home_config = {

    "unit_id": UNIT_ID,
    "description": "Nook/Printer lights w/ Motion Sensor",
    "display_name": "nook-esp",
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
        "pin": 27,
        "retrigger_delay_ms": 120000,
        "timer_n": 1,
        "name": "Nook Motion",
    },
    "led1": {
        "pin": 25,
        "freq": 300,
        "timer_n": 2,
        "fade_time_ms": 4,
        "brightness_scale": 255,
        "name": "Printer Lights"
    },
    "led2": {
        "pin": 26,
        "freq": 300,
        "timer_n": 3,
        "fade_time_ms": 4,
        "brightness_scale": 255,
        "name": "Nook Lights"
    }

}
