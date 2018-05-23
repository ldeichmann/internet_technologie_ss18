import logging

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

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    @staticmethod
    def enable_callback(channel):
        GPIO.add_event_detect(channel, GPIO.BOTH)

    @staticmethod
    def register_callback(channel, callback):
        GPIO.add_event_callback(channel, _GPIOCallback(callback))

    def set_input(self, channel):
        self._logger.debug("Setting pin %s to input" % channel)
        GPIO.setup(channel, GPIO.IN)

    def set_output(self, channel):
        self._logger.debug("Setting pin %s to output" % channel)
        GPIO.setup(channel, GPIO.OUT)

    def turn_on(self, channel):
        self._logger.debug("Turning on output on Pin %s" % channel)
        GPIO.output(channel, 1)

    def turn_off(self, channel):
        self._logger.debug("Turning off output on Pin %s" % channel)
        GPIO.output(channel, 0)
