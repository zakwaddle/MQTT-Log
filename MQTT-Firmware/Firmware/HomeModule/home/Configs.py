import json



class WifiConfig:
    def __init__(self, id, ssid, password, is_default):
        self.ssid = ssid
        self.password = password


class MQTTConfig:
    def __init__(self, id, host_address, port, username, password, is_default):
        self.host = host_address
        self.port = port
        self.username = username
        self.password = password


class FTPConfig:
    def __init__(self, id, host_address, username, password, is_default):
        self.host = host_address
        self.username = username
        self.password = password


class DeviceConfig:
    wifi = None
    mqtt = None
    ftp = None
    led_on_after_connect = True
    use_ping = True

    @classmethod
    def parse_config(cls, device_config):
        if device_config is not None:
            return DeviceConfig(device_config)

    def __init__(self, device_config):
        self.device_id = device_config.get('id')
        self.platform = device_config.get('platform')
        self.name = device_config.get('display_name')
        self.device_info = device_config.get('device_info')

        config = device_config.get('config')
        wifi_config = config.get('wifi_network')
        mqtt_config = config.get('mqtt_broker')
        ftp_config = config.get('ftp_server')

        device_settings = config.get('device_settings')
        if device_settings is not None:
            led_on = device_settings.get('led_on_after_connect')
            self.led_on_after_connect = led_on if led_on is not None else self.led_on_after_connect
            use_ping = device_settings.get('use_ping')
            self.use_ping = use_ping if use_ping is not None else self.use_ping

        self.wifi = WifiConfig(**wifi_config) if wifi_config is not None else None
        self.mqtt = MQTTConfig(**mqtt_config) if mqtt_config is not None else None
        self.ftp = FTPConfig(**ftp_config) if ftp_config is not None else None

        self.sensors = config.get('sensors')


class DeviceSettings:
    config_path = '/config.json'

    def __save_config(self, data):
        with open(self.config_path, 'w') as f:
            json.dump(data, f)

    def __load_config(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def __init__(self):
        configs = self.__load_config()
        self.host = configs['host']
        self.name = configs['name']
        self.ssid = configs['wifi_ssid']
        self.password = configs['wifi_password']

    def save(self):
        self.__save_config({
            "host": self.host,
            "name": self.name,
            "wifi_ssid": self.ssid,
            "wifi_password": self.password
        })

    def save_new_config(self, new_config):
        self.__save_config(new_config)
