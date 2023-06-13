from machine import Pin, SPI
import sh1106

# Create an SPI interface
spi = SPI(0, baudrate=1000000, sck=Pin(18), mosi=Pin(19))

# The exact pins will depend on your setup
dc = Pin(20)     # data/command
res = Pin(21)    # reset
cs = Pin(17)     # chip select

# Create a SH1106 object
display = sh1106.SH1106_SPI(128, 64, spi, dc, res, cs)


class Settings:
    def __init__(self):
        self.temperature = 0
        self.humidity = 0
        self.motion = 0
        
    def update_temp(self, val):
        self.temperature = round(val * 9/5 + 32, 1)

    def update_humidity(self, val):
        self.humidity = val
    
    def update_motion(self, val):
        self.motion = val

settings = Settings()


def setup_labels():
    display.fill(0)
    display.fill_rect(0,0,128, 14, 1)
    display.text("Henryman", 32, 4, 0)
    display.text("Temp", 13, 28, 1)
    display.text("Humidity", 60, 28, 1)
    

def update_numbers():
    display.fill_rect(0,40,128, 14, 0)
    display.text(f"{settings.temperature}", 12, 44, 1)
    display.rect(48, 43, 4, 4, 1)
    display.text(f"{settings.humidity}%", 73, 44, 1)
    display.show()


def on_display_message(topic, msg, topics):
    topic = topic.decode("utf-8")
    msg = msg.decode("utf-8")
    
    if topic == topics["desk_motion"]:
        settings.update_motion(int(msg))
        
        if settings.motion:
            display.sleep(False)
        elif not settings.motion:
            display.sleep(True)
        
        
    elif topic == topics["henry_temp"]:
        settings.update_temp(float(msg))
        update_numbers()

    elif topic == topics["henry_humidity"]:
        settings.update_humidity(float(msg))
        update_numbers()
