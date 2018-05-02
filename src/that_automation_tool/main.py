import time
import platform
import configparser
import argparse
import logging

from .communication import Communication
from .ldr_arduino import LDRArduinoHandler
from .gpio import GPIOHandler

DEBUGGING = True

if __name__ == "__main__":

    if DEBUGGING:
        logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    if platform.machine() == "armv7l":
        logger.info("This is being executed on the raspi")
    else:
        logger.warning("Probably not running on the raspi")

    # get configuration path from arguments
    parser = argparse.ArgumentParser(description="Do some IoT things")
    parser.add_argument("-c", "--config", help="path to configuration file")
    args = parser.parse_args()

    # read config file
    config = configparser.ConfigParser()
    config.read(args.config)

    mqtt_handler = None
    if "MQTT" in config.sections():
        logger.info("Enabling MQTT")
        mqtt_handler = Communication(config["MQTT"])

        def on_mqtt_message(client, userdata, msg):
            logger.debug("%s - %s", msg.topic, str(msg.payload))

        mqtt_handler.connect_async()

        if DEBUGGING:
            # register debug handler
            def dbg_cb(client, userdata, message):
                logger.debug("topic: %s message: %s", message.topic, str(message.payload))

            mqtt_handler.register_callback("/sensornetwork/group3/#", dbg_cb)

    gpio_handler = GPIOHandler()

    if "LDR" in config.sections():
        logger.info("Enabling LDR")
        ldr_arduino_handler = LDRArduinoHandler(gpio=gpio_handler, config=config["LDR"], mqtt=mqtt_handler)
        ldr_arduino_handler.run_async()

    while True:
        time.sleep(5)
        logger.debug("Still alive")
