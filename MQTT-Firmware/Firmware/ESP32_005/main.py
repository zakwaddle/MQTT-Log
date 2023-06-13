import utime
import machine


pin = machine.Pin(13, machine.Pin.IN)
touch = machine.TouchPad(pin)
led = machine.Pin(2, machine.Pin.OUT)

def under_threshold(val):
    return val <= 250


prev_val = False

while True:
    try:
        pad = touch.read()
    except KeyError:
        print('\nkey error\n')
        continue
    except ValueError:
        print('\nvalue error\n')
        continue
    
    is_under = under_threshold(pad)
    if prev_val == is_under:
        utime.sleep_ms(100)
        continue
    
    if is_under:
        led.value(1)
        print("Touched")
    else:
        led.value(0)
        print("Not Touched")
    prev_val = is_under
    utime.sleep_ms(100)