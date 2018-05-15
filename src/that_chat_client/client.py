import argparse
import configparser
import threading
import json
import datetime
import time
import logging
import os

from that_automation_tool.communication import Communication

DEBUGGING = True


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        fmsg = json.loads(msg.payload)
        print("{}: {}".format(datetime.datetime.fromtimestamp(fmsg['timestamp']).strftime('%H:%M:%S'), fmsg['message']))
    except Exception as e:
        print(e)
        print("{}: {} {}".format(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S'), msg.topic,
                                 str(msg.payload)))


if __name__ == "__main__":

    if DEBUGGING:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # get configuration path from arguments
    parser = argparse.ArgumentParser(description="Do some IoT things")
    parser.add_argument("-c", "--config", help="path to configuration file")
    args = parser.parse_args()

    cfg_pth = os.path.abspath(args.config)
    logger.debug("Configuration path is %s", cfg_pth)

    # read config file
    config = configparser.ConfigParser()
    config.read(cfg_pth)

    if "MQTT" not in config.sections():
        raise Exception("MQTT missing from configuration file")

    mqtt_handler = Communication(config["MQTT"])
    mqtt_handler.register_callback("/chat/#", on_message)


    def threaded_thing():
        while True:
            msg = input()
            # since we're group 3, this value is hardcoded
            mqtt_handler.publish("/chat/group3", msg)


    thrd = threading.Thread(target=threaded_thing)
    thrd.setDaemon(True)
    thrd.start()

    mqtt_handler.connect_async()
    while True:
        # since our handler doesn't have a blocking run, we'll do it ourselves
        pass
