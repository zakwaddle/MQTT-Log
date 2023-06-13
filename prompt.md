
I've been working on a project to create a system for creating devices for
home automation using Raspberry Pi Pico W and ESP32 microcontrollers and a Raspberry Pi 4
running HomeAssistant. 
In HomeAssistant I've installed add-on's for Mosquitto (an MQTT broker to handle 
communication with the microcontrollers), and FTP (to handle OTA updates, triggered by MQTT, for the microcontrollers).
I've writen a package in micropython which I've simply called 'home'. 
The structure of this package, and the `main.py` and `config.py` present on the microcontrollers is as follows:
### Microcontroller File Structure
```
- home/
    - sensors/
        - __init.py
        - DHT22.py  // Temperature/Humidity Sensor 
        - MotionSensor.py  // Motion Sensor
        - DimmableLED.py  // Dimmable LED 
        - StatusLED.py  // On Board LED to indicate Status
    - lib/
        - umqtt/
            - simple.py  // MQTT Client Library 
        - __init__.py
        - ftplib.py  // FTP Client Library
    - __init__.py
    - Home.py  //  main coordiator and interface
    - UpdateManager.py  // handles FTP connection and local filesystem interactions
    - MQTTManager.py  // handles MQTT connection and interactions
    - WiFiManager.py  // handles WiFi connection and interactions
    - Timer.py  // handles platform differences for machine.Timer
- main.py  //  loads configuration specifics from `config.py`, initializes the home client and runs main loop
- config.py  //  device specific configurations
```

This system works well. However, after a few weeks I began to notice that if something went wrong during
an update, or even if a controller reconnected to the Wifi or MQTT broker, I had no idea. 

My solution was:
- Update the Home package to send log messages to an MQTT topic unrelated to HomeAssistant
- On a second Raspberry Pi 4 (which I'll call by it's local network host name: yawntsum):
  - Create a Flask app which uses SQLAlchemy to save/serve log entries to/from a database.
  - Create a script to listen to the above mentioned log topic and make a POST request to the Flask app when a log entry is received 
  - Create a React app to request log entries from the Flask app and view log messages on the the local network
  - Install redis
  - using flask-sse and redis, stream new log entries to the React app (refreshing the page to view new entries got annoying really fast) 

While developing this solution I began to see it potential to do more that just view logs.
On each microcontroller, the home package is identical while `main.py` and `config.py` are structurally the
same, but contain information unique to that devices configuration. However, they are also just variations on the same thing.

My idea is to centralize the configuration of these devices using as much of the existing code structure as possible,
including MQTT communication, Flask app and database. I've added tables to the database, added endpoints to the Flask app.


### Database Tables
```python
from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class LogEntry(Base):
    __tablename__ = 'log_entries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String)
    log = Column(JSON)
    time = Column(DateTime, default=datetime.datetime.now)
    device_id = Column(String, ForeignKey('home-devices.id'))

    device = relationship("HomeDevice", back_populates="log_entries")


class HomeDevice(Base):
    __tablename__ = 'home-devices'

    id = Column(String, primary_key=True, autoincrement=False)
    platform = Column(String)
    display_name = Column(String)
    device_info = Column(JSON)

    log_entries = relationship("LogEntry", back_populates="device")
    config = relationship("DeviceConfig", uselist=False, back_populates="device")  # one-to-one relationship


class DeviceConfig(Base):
    __tablename__ = 'device-configs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String, ForeignKey('home-devices.id'), unique=True)  # one-to-one relationship
    config = Column(JSON)

    device = relationship("HomeDevice", back_populates="config")  # one-to-one relationship
    sensors = relationship("DeviceSensor", back_populates="config")  # one-to-many relationship


class DeviceSensor(Base):
    __tablename__ = 'device-sensors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_type = Column(String)
    name = Column(String)
    sensor_config = Column(JSON)
    device_config_id = Column(String, ForeignKey('device-configs.id'))

    device_config = relationship("DeviceConfig", back_populates="sensors")  # one-to-many relationship


```
### Flask Endpoints
**GET** `/api/home/devices`\
**GET** `/api/home/devices/<device_id>/sensors`\
**POST** `/api/home/devices/add`\
**DELETE** `/api/home/devices/<device_id>`

**GET** `/api/home/logs`\
**POST** `/api/home/logs/add`\
**DELETE** `/api/home/logs/entries/<log_id>`

**GET** `/api/home/devices/<device_id>/config`\
**POST** `/api/home/devices/<device_id>/config`\
**PUT** `/api/home/devices/<device_id>/config`\
**DELETE** `/api/home/devices/<device_id>/config`\

**GET** `/api/home/sensors/<sensor_id>'`\
**POST** `/api/home/sensors/add`\
**PUT** `/api/home/sensors/<sensor_id>/config`\
**DELETE** `/api/home/sensors/<sensor_id>`


I think I have most of what is needed for the backend. 
I believe the next step is to begin modifying the React app to use these endpoints. Once new devices can be added 
and modified from the app, it should be time to begin modifying the device firmware to listen for, and react to,
messages sent by the app.
There are still some decisions to be made as for how to handle these configuration messages, but until the React app is
actually able to make, modify, and notify these devices, those decisions don't seem very important.
Before I begin to actually work on next step, do you see anything I may have missed? Or have advice on how to proceed?

