import sys

UNIT_ID = "PicoW_004"

home_config = {
    "unit_id": f"{UNIT_ID}",
    "description": "Tester boy",
    "display_name": "tester-boy",

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
topics = {
    "desk_motion": "sensors/motion/PicoW_003/1",
    "henry_temp": "sensors/weather/temperature/PicoW_005/1",
    "henry_humidity": "sensors/weather/humidity/PicoW_005/1"
  }
sensors = {

    "weather": {
        "pin": 28,
        "measurement_interval_ms": 10000,
        "timer_n": 1,
        "name_temp": "Bedroom Temperature",
        "name_humidity": "Bedroom Humidity"
    }
}
