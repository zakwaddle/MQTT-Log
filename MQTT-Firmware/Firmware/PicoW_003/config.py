import sys

UNIT_ID = "PicoW_003"

home_config = {
    "unit_id": f"{UNIT_ID}",
    "description": "Office Weather and Motion",
    "display_name": "office-motion",
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
    "motion1": {
        "pin": 17,
        "retrigger_delay_ms": 120000,
        "timer_n": 1,
        "name": "Shelf Motion"
    },
    "motion2": {
        "pin": 16,
        "retrigger_delay_ms": 120000,
        "timer_n": 2,
        "name": "Desk Motion"
    },
    "weather": {
        "pin": 13,
        "measurement_interval_ms": 10000,
        "timer_n": 3,
        "name_temp": "Office Temperature",
        "name_humidity": "Office Humidity"
    }
}
