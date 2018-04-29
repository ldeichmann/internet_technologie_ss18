import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)


class _GPIOCallback:
    """
    Container to allow returning actual values to the callback func
    """

    def __init__(self, func):
        self.func = func

    def __call__(self, channel):
        value = GPIO.input(channel)
        self.func(channel, value)


class GPIOHandler:

    @staticmethod
    def enable_callback(channel):
        GPIO.add_event_detect(channel, GPIO.BOTH)

    @staticmethod
    def register_callback(channel, callback):
        GPIO.add_event_callback(channel, _GPIOCallback(callback))

    @staticmethod
    def set_input(channel):
        GPIO.setup(channel, GPIO.IN)

    @staticmethod
    def set_output(channel):
        GPIO.setup(channel, GPIO.OUT)

    @staticmethod
    def turn_on(channel):
        GPIO.output(channel, 1)

    @staticmethod
    def turn_off(channel):
        GPIO.output(channel, 0)
