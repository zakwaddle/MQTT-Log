
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

        self.wifi = WifiConfig(**wifi_config) if wifi_config is not None else None
        self.mqtt = MQTTConfig(**mqtt_config) if mqtt_config is not None else None
        self.ftp = FTPConfig(**ftp_config) if ftp_config is not None else None
        
        self.sensors = config.get('sensors')
