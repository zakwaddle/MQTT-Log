from Unit import Unit


main_files = [
    "/main.py",
    "/config.py"
]
sensor_files = [
    "/home/sensors/__init__.py",
    "/home/sensors/MQTTMotionSensor.py",
    "/home/sensors/MQTTDimmableLED.py",
    "/home/sensors/MQTTTemperatureHumidity.py",
    "/home/sensors/StatusLED.py",
]
sensor_files_v2 = [
    "/home/sensors/__init__.py",
    "/home/sensors/DHT22.py",
    "/home/sensors/DimmableLED.py",
    "/home/sensors/MotionSensor.py",
    "/home/sensors/StatusLED.py",
]
home_files = [
    "/home/__init__.py",
    "/home/Home.py",
    "/home/MQTTManager.py",
    "/home/UpdateManager.py",
    "/home/WiFiManager.py",
    "/home/Timer.py",
]

c = [
    "/home/Home.py",
    "/config.py",
    "/home/UpdateManager.py",
    "/home/sensors/DHT22.py",
    "/home/Timer.py",
    # "/main.py",
]

kitchen = Unit("PicoW_001")  # |W-M-L-L| Firmware Ready
bedroom = Unit("PicoW_002")  # |W|           current home version/homeassistant ftp/mqtt-logger
office_motion = Unit("PicoW_003")  # |W-M-M| current home version/homeassistant ftp/mqtt-logger
henry = Unit("PicoW_005")  # |W|   current home version/homeassistant ftp/mqtt-logger

living_room = Unit("ESP32_002")  # -   |W| current home version/homeassistant ftp/mqtt-logger
shelf_lights = Unit("ESP32_003")  # -  |L| current home version/homeassistant ftp/mqtt-logger
nook_esp = Unit("ESP32_004")  # -  |M-L-L| current home version/homeassistant ftp/mqtt-logger

display_pico = Unit("PicoW_004")
unused_esp_1 = Unit("ESP32_001")
touch_esp = Unit("ESP32_005")
test_esp = Unit("TESTESP")

tester_boy = Unit("PicoW_004")  # |W-M-M| current home version/homeassistant ftp/mqtt-logger
all_units = Unit("all-units")


def check_in():
    henry.check_in()
    shelf_lights.check_in()
    nook_esp.check_in()
    office_motion.check_in()
    living_room.check_in()
    bedroom.check_in()
    kitchen.check_in()


# shelf_lights.restart()
# office_motion.restart()
# kitchen.restart()
# nook_esp.restart()

# bedroom.restart()

# shelf_lights.update_files(home_files)
# shelf_lights.update_files(main_files)

# shelf_lights.update_files(c)
# nook_esp.update_files(c)
# office_motion.update_files(c)
# living_room.update_files(c)
# bedroom.update_files(c)
# henry.update_files(c)
# henry.restart()
# henry.check_in()
# check_in()
tester_boy.update_files([
    "/home/Timer.py",
    "/config.py"
])
# all_units.upload_home_package()
# all_units.update_files(c, refresh=False)