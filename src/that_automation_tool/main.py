import time
import platform
import serial

from .communication import Communication
from .gpio import GPIOHandler


led_channel_no = 40
led2_channel_no = 38
ldr_channel_no = 37


if __name__ == "__main__":
    if platform.machine() == "armv8":
        print("This is being executed on the raspi")
    else:
        print("Probably not running on the raspi")
    gpio_handler = GPIOHandler()
    gpio_handler.set_output(led_channel_no)
    gpio_handler.set_output(led2_channel_no)
    gpio_handler.set_input(ldr_channel_no)

    ser = serial.Serial('/dev/ttyACM0')  # open serial port


    def ldr_on_cb():
        gpio_handler.turn_on(led_channel_no)
        gpio_handler.turn_off(led2_channel_no)

    def ldr_off_cb():
        gpio_handler.turn_off(led_channel_no)
        gpio_handler.turn_on(led2_channel_no)


    while True:
        lux_value = int(ser.readline())
        if lux_value < 50:
            ldr_on_cb()
        else:
            ldr_off_cb()
