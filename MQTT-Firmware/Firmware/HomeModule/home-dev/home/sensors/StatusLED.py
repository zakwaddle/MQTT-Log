import machine
import utime

class StatusLED:
    
    def __init__(self, pin):
        self.led_pin = machine.Pin(pin, machine.Pin.OUT)
        self.off()

    def on(self):
        self.led_pin(1)
        
    def off(self):
        self.led_pin(0)
    
#     def on_for(self, on_ms, next_func=None):
#         self.on()
#         cb = lambda t: self.on()
#         timer = machine.Timer(-1)
#         timer.init(period=on_ms, mode=machine.Timer.ONE_SHOT, callback=cb if next_func is None else next_func)
#     
#     def off_for(self, off_ms, next_func=None):
#         self.off()
#         cb = lambda t: self.on()
#         timer = machine.Timer(-1)
#         timer.init(period=off_ms, mode=machine.Timer.ONE_SHOT, callback=cb if next_func is None else next_func)
        
    def blink_light(self):
        self.on()
        utime.sleep_ms(250)
        self.off()
        utime.sleep_ms(250)


if __name__ == "__main__":
    light = StatusLED(21)
    utime.sleep(2)
    light.blink_light()
#     light.on_for(500, lambda t: light.off_for(500)

