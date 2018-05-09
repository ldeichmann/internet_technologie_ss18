import logging
from queue import PriorityQueue
import json
import datetime
import time


class LightListener:

    def __init__(self, mqtt_handler, config):
        """
        Listener calculating an average Lux value over all groups values
        :param Communication mqtt_handler: mqtt handler object for callbacks
        :param config: ConfigParser Section for this Object
        """
        self._logger = logging.getLogger(__name__)
        self._mqtt = mqtt_handler
        self._size = config.getint("num_msg", 20)

        self._recent_values = PriorityQueue(maxsize=self._size)

    def message_callback(self, client, userdata, msg):
        try:
            fmsg = json.loads(msg.payload)
            self._logger.debug("%s: %s", datetime.datetime.fromtimestamp(fmsg['timestamp']).strftime('%H:%M:%S'), fmsg)
            if "value" not in fmsg:
                raise Exception("value missing from message")

            if self._recent_values.qsize() == self._recent_values.maxsize:
                # remove "lowest" value
                val = self._recent_values.get()
                self._logger.debug("Removed oldest element from queue, element was: %s", val)

            self._recent_values.put((msg.timestamp, fmsg))

            # our values might've changed, inform the user about the new average
            self._print_average()
        except Exception as e:
            self._logger.error("%s: Received invalid message: %s", datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S'), msg.topic + " " + str(msg.payload))
            self._logger.error(e)

    def _print_average(self):
        if self._recent_values.qsize():
            total = 0
            # create a copy of all values here to allow simple iteration
            for timestamp, value in list(self._recent_values.queue):
                total += value["value"]
            self._logger.info("Average measurement value is: %.2f", total / self._recent_values.qsize())
            self._logger.debug("Queue for average was: %s", list(self._recent_values.queue))

    def run(self):
        self._mqtt.register_callback("/sensornetwork/+/sensor/brightness", self.message_callback)
