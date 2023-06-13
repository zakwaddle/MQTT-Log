import sys

UNIT_ID = "ESP32_002"

home_config = {
    "unit_id": f"{UNIT_ID}",
    "description": "Living Room Temperature/Humidity Sensor",
    "display_name": "living-room",
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

    "weather": {
        "pin": 16,
        "measurement_interval_ms": 10000,
        "timer_n": 1,
        "name_temp": "Living Room Temperature",
        "name_humidity": "Living Room Humidity"
    }
}
