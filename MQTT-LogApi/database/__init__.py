from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import ModelBase, LogEntry, HomeDevice, DeviceSensor, DeviceConfig
import os

engine = create_engine(os.getenv('DATABASE_URI'), pool_size=20)
ModelBase.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


def get_logs():
    with Session() as session:
        entries = session.query(LogEntry).all()
        data = [entry.to_dict() for entry in entries]
    return data


def add_log(log_entry):
    with Session() as session:
        new_log = LogEntry(**log_entry)
        session.add(new_log)
        session.commit()
        data = new_log.to_dict()
    return data


def delete_log(log_id):
    with Session() as session:
        session.query(LogEntry).filter(LogEntry.id == log_id).delete()
        session.commit()


def get_devices():
    with Session() as session:
        devices = session.query(HomeDevice).all()
        data = [device.to_dict() for device in devices]
    return data


def add_device(device):
    with Session() as session:
        new_device = HomeDevice(**device)
        session.add(new_device)
        session.commit()
        data = new_device.to_dict()
    return data


def delete_device(device_id):
    with Session() as session:
        session.query(HomeDevice).filter(HomeDevice.id == device_id).delete()
        session.commit()


def get_device_config(device_id):
    with Session() as session:
        config = session.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).one()
        data = config.to_dict()
    return data


def delete_device_config(device_id):
    with Session() as session:
        session.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).delete()
        session.commit()


def update_device_config(device_id, new_config):
    with Session() as session:
        session.query(DeviceConfig).filter(DeviceConfig.device_id == device_id).update({"config": new_config})
        session.commit()


def add_device_config(device_id, config):
    with Session() as session:
        device_config = DeviceConfig(device_id=device_id, config=config)
        session.add(device_config)
        session.commit()
        data = device_config.to_dict()
    return data


def get_device_sensors(device_config_id):
    with Session() as session:
        sensors = session.query(DeviceSensor).filter(DeviceSensor.device_config_id == device_config_id).all()
        data = [sensor.to_dict() for sensor in sensors]
    return data


def add_sensor(sensor):
    with Session() as session:
        new_sensor = DeviceSensor(**sensor)
        session.add(new_sensor)
        session.commit()
        data = new_sensor.to_dict()
    return data


def update_sensor_config(sensor_id, new_config):
    with Session() as session:
        session.query(DeviceSensor).filter(DeviceSensor.id == sensor_id).update({"sensor_config": new_config})
        session.commit()


def delete_sensor(sensor_id):
    with Session() as session:
        session.query(DeviceSensor).filter(DeviceSensor.id == sensor_id).delete()
        session.commit()


def get_sensor(sensor_id):
    with Session() as session:
        sensor = session.query(DeviceSensor).filter(DeviceSensor.id == sensor_id).one()
        data = sensor.to_dict()
    return data
