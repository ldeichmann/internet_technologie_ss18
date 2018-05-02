import threading
import serial


class LDRArduinoHandler:

    def __init__(self, gpio, config, mqtt=None):

        self.serial = serial.Serial(config['serial_port'])
        self._mqtt = mqtt
        self._led_pin = config.getint('led_pin')
        self._ldr_threshold = config.getint('brightness_threshold', 50)
        self._gpio = gpio
        self._gpio.set_output(self._led_pin)
        self.thread = None
        self.lock = threading.Lock()

    def ldr_high(self):
        self._gpio.turn_on(self._led_pin)

    def ldr_low(self):
        self._gpio.turn_off(self._led_pin)

    def run_async(self):
        with self.lock:
            if not self.thread:
                self.thread = threading.Thread(target=self._run)
                self.thread.setDaemon(True)
                self.thread.start()

    def _run(self):
        while True:
            lux_value = int(self.serial.readline())
            if self._mqtt:
                self._mqtt.publish('/sensornetwork/group3/sensor/brightness', {"brightness": lux_value, "unit": "Lux"})
            if lux_value < self._ldr_threshold:
                self.ldr_high()
            else:
                self.ldr_low()
