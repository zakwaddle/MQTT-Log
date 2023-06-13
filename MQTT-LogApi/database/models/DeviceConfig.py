from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .ModelBase import ModelBase


class DeviceConfig(ModelBase):
    __tablename__ = 'device-configs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String, ForeignKey('home-devices.id'), unique=True)  # one-to-one relationship
    config = Column(JSON)

    device = relationship("HomeDevice", back_populates="config")  # one-to-one relationship
    sensors = relationship("DeviceSensor", back_populates="device_config")  # one-to-many relationship

    def __repr__(self):
        return f"<DeviceConfig - {self.id} | {self.device_id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "device_id": self.device_id,
            "config": self.config,
            "sensors": [s.to_dict() for s in self.sensors if self.sensors]
        }
