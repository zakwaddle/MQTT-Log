import home
import machine
import utime


if __name__ == '__main__':
    print('Home Version: ', home.__version__)
    h = home.Home()
    try:
        while True:
            h.run()
    except KeyboardInterrupt:
        print('exiting')
        h.status_led_off()
    except Exception as e:
        print("Run Error: ", e)
        utime.sleep(10)
        machine.reset()

    
    