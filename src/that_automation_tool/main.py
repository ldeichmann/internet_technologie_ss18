import time
import platform

from .communication import Communication
from .gpio import GPIOHandler


led_channel_no = 40
led2_channel_no = 38
ldr_channel_no = 37


if __name__ == "__main__":
    if platform.machine() == "armv7l":
        print("This is being executed on the raspi")
    else:
        print("Probably not running on the raspi")
    gpio_handler = GPIOHandler()
    gpio_handler.set_output(led_channel_no)
    gpio_handler.set_output(led2_channel_no)
    gpio_handler.set_input(ldr_channel_no)


    def ldr_on_cb():
        gpio_handler.turn_on(led_channel_no)
        gpio_handler.turn_off(led2_channel_no)

    def ldr_off_cb():
        gpio_handler.turn_off(led_channel_no)
        gpio_handler.turn_on(led2_channel_no)


    def ldr_cb(channel, value):
        if value:
            ldr_on_cb()
        else:
            ldr_off_cb()

    gpio_handler.enable_callback(ldr_channel_no)
    gpio_handler.register_callback(ldr_channel_no, ldr_cb)

    while True:
        time.sleep(5)
        print("Still alive")
