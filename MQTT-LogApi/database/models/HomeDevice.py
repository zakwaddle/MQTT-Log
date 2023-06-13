from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship
from .ModelBase import ModelBase


class HomeDevice(ModelBase):
    __tablename__ = 'home-devices'

    id = Column(String, primary_key=True)
    platform = Column(String)
    display_name = Column(String)
    device_info = Column(JSON)

    log_entries = relationship("LogEntry", back_populates="device")
    config = relationship("DeviceConfig", uselist=False, back_populates="device")  # one-to-one relationship

    def __repr__(self):
        return f"<HomeDevice - {self.id} | {self.display_name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "platform": self.platform,
            "display_name": self.display_name
        }
