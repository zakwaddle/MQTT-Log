from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .ModelBase import ModelBase


class WifiNetwork(ModelBase):
    __tablename__ = 'wifi-networks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ssid = Column(String)
    password = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "ssid": self.ssid,
            "password": self.password
        }


class FTPServer(ModelBase):
    __tablename__ = 'ftp-servers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_address = Column(String)
    username = Column(String)
    password = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "host_address": self.host_address,
            "username": self.username,
            "password": self.password
        }


class MQTTBroker(ModelBase):
    __tablename__ = 'mqtt-brokers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_address = Column(String)
    port = Column(Integer)
    username = Column(String)
    password = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "host_address": self.host_address,
            "port": self.port,
            "username": self.username,
            "password": self.password
        }


class DeviceConfig(ModelBase):
    __tablename__ = 'device-configs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String, ForeignKey('home-devices.id'), unique=True)  # one-to-one relationship
    # config = Column(JSON)
    wifi_network_id = Column(Integer, ForeignKey('wifi-networks.id'))
    ftp_server_id = Column(Integer, ForeignKey('ftp-servers.id'))
    mqtt_broker_id = Column(Integer, ForeignKey('mqtt-brokers.id'))

    wifi_network = relationship("WifiNetwork", uselist=False)
    ftp_server = relationship("FTPServer", uselist=False)
    mqtt_broker = relationship("MQTTBroker", uselist=False)

    device = relationship("HomeDevice", back_populates="config")  # one-to-one relationship
    sensors = relationship("DeviceSensor", back_populates="device_config")  # one-to-many relationship

    def __repr__(self):
        return f"<DeviceConfig - {self.id} | {self.device_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            # "config": self.config,
            "wifi_network": self.wifi_network.to_dict() if self.wifi_network else None,
            "ftp_server": self.ftp_server.to_dict() if self.ftp_server else None,
            "mqtt_broker": self.mqtt_broker.to_dict() if self.mqtt_broker else None,
            "sensors": [s.to_dict() for s in self.sensors if self.sensors]
        }
