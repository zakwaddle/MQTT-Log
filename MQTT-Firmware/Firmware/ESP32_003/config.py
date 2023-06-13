import sys

UNIT_ID = "ESP32_003"

"""
poo poo poo
"""

home_config = {

    "unit_id": f"{UNIT_ID}",
    "description": "Office Shelf Lights",
    "display_name": "office-shelf-lights",
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

    "led": {
        "pin": 4,
        "freq": 300,
        "timer_n": 1,
        "fade_time_ms": 4,
        "brightness_scale": 255,
        "name": "Shelf Lights"
    }

}
