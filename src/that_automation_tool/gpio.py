import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD)

led_channel_no = 40
led2_channel_no = 38
ldr_channel_no = 36

ldr_channel = gpio.setup(ldr_channel_no, gpio.IN, pull_up_down=gpio.PUD_DOWN)
led_channel = gpio.setup(led_channel_no, gpio.OUT)
led2_channel = gpio.setup(led2_channel_no, gpio.OUT)


def ldr_high():
    return gpio.input(ldr_channel_no)


def led_on():
    gpio.output(led_channel_no, 1)
    gpio.output(led2_channel_no, 0)

def led_off():
    gpio.output(led_channel_no, 0)
    gpio.output(led2_channel_no, 1)


# do stuff here
