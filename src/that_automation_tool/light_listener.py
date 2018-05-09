import logging
import collections
import json
import datetime


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

        self._recent_values = {}

    def _add_group_value(self, group, value):
        if group not in self._recent_values:
            self._recent_values[group] = collections.deque(maxlen=self._size)
        self._recent_values[group].append(value)

    def message_callback(self, client, userdata, msg):
        try:
            fmsg = json.loads(msg.payload)
            self._logger.debug("%s: %s", datetime.datetime.fromtimestamp(fmsg['timestamp']).strftime('%H:%M:%S'), fmsg)
            if "measurement_value" not in fmsg:
                raise Exception("measurement_value missing from message")

            grp = msg.topic.split("/")[1]
            self._add_group_value(group=grp, value=fmsg)

            # our values might've changed, inform the user about the new average
            self._print_average()
        except Exception as e:
            self._logger.error("%s: Received invalid message: %s", datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S'), msg.topic + " " + str(msg.payload))
            self._logger.error(e)

    def _print_average(self):
        for grp, values in self._recent_values.items():
            total = 0
            for val in self._recent_values:
                total += val["measurement_value"]
            self._logger.info("%s: Average measurement value is: %s", grp, total / len(self._recent_values))

    def run(self):
        self._mqtt.register_callback("/sensornetwork/+/sensor/brightness", self.message_callback)
