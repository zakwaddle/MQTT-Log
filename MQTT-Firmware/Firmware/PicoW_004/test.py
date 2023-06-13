from display import display
import time

display.sleep(False)
display.fill(0)

def setup_labels():
    display.fill(0)
    display.fill_rect(0,0,128, 14, 1)
    display.text("Henryman", 30, 4, 0)
    display.text("Temp", 10, 25, 1)
    display.text("Humidity", 55, 25, 1)
    

def change_numbers(temp, hum):
    display.fill_rect(0,40,128, 14, 0)
    display.text(f"{temp}", 18, 40, 1)
    display.text(f"{hum}%", 78, 40, 1)
    display.show()


setup_labels()
change_numbers(13, 40)
time.sleep(1)

change_numbers(32, 15)
time.sleep(1)

change_numbers(346, 48)
time.sleep(1)