from FTPUploader import FTPUploader
import paho.mqtt.client as mqtt
import json
import os
import time

firmware_folder = os.path.abspath(f"{os.path.dirname(__file__)}/../Firmware")


class Unit:
    # local_firmware_folder = "/Users/zakwaddle/MQTT-HomeKit-ESP32/Firmware"
    local_firmware_folder = firmware_folder
    local_home_path = f"{local_firmware_folder}/HomeModule"

    ftp_home_folder = f"/upload/Firmware/HomeModule"

    @classmethod
    def create_message(cls, command, file_list=None):
        if file_list is None:
            file_list = []
        info = {
            "command": command,
            "file_list": file_list
        }
        return json.dumps(info)

    def __init__(self, unit_id):
        self.ftp_uploader = FTPUploader(
            host="homeassistant.local",
            user="microcontrollers",
            password="microcontrollers"
        )
        self.ftp_uploader.set_excluded_files([".gitignore", ".gitattributes", ".git"])
        self.mqtt_client = mqtt.Client()

        self.unit_id = unit_id
        self.command_topic = f"command/{self.unit_id}"
        self.local_folder = f"{self.local_firmware_folder}/{self.unit_id}"
        self.ftp_folder = f"/upload/Firmware/{self.unit_id}"

    def connect_mqtt(self):
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_publish = self.on_publish

        self.mqtt_client.username_pw_set(
            username="Zak", password="935Ravine"
        )
        self.mqtt_client.connect(
            host="homeassistant.local", port=1883, keepalive=60
        )

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT server")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_publish(self, *args):
        print("Message published")
        self.mqtt_client.disconnect()

    def upload(self):
        print("uploading unit folder")
        self.ftp_uploader.upload_folder(self.local_folder, self.ftp_folder)

    def clear(self):
        self.ftp_uploader.connect()
        self.ftp_uploader.clear_folder(self.ftp_folder)
        self.ftp_uploader.disconnect()

    def create_home_package_folder(self):
        self.ftp_uploader.connect()
        self.ftp_uploader.create_directory(self.ftp_home_folder)
        self.ftp_uploader.disconnect()

    def upload_home_package(self):
        print("uploading home folder")
        self.create_home_package_folder()
        self.ftp_uploader.clear_folder(self.ftp_home_folder)
        self.ftp_uploader.upload_folder(self.local_home_path, self.ftp_home_folder)

    def create_root(self):
        self.ftp_uploader.connect()
        self.ftp_uploader.create_directory(self.ftp_folder)
        self.ftp_uploader.disconnect()

    def refresh_fpt(self):
        self.create_root()
        print("clearing folder")
        self.clear()
        print("uploading unit configs")
        self.upload()

    def send_mqtt_message(self, mqtt_topic, mqtt_message):
        self.connect_mqtt()
        self.mqtt_client.publish(mqtt_topic, mqtt_message, qos=1)

    def send_command(self, command, **kwargs):
        self.send_mqtt_message(self.command_topic, json.dumps({"command": command, **kwargs}))

    def restart(self):
        self.send_command("restart")

    def update_files(self, file_list, refresh=True):
        if refresh:
            self.refresh_fpt()
        self.send_command("update_all", file_list=file_list)

    def check_in(self):
        self.send_command("check-in")
