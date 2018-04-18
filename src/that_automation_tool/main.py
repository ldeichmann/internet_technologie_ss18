import time

from .communication import Communication
from .gpio import ldr_high, led_on, led_off

if __name__ == "__main__":
    print("This is being executed on the raspi")
    i = 0
    while True:
        time.sleep(1)
        if ldr_high():
            print(i, "LDR is high")
            led_on()
            # led_off()
        else:
            print(i, "LDR is low")
            # led_on()
            led_off()
        i += 1