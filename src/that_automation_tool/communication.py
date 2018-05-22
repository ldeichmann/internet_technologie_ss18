import logging
import time
import json
import threading
from collections import namedtuple

import paho.mqtt.client as mqtt


class Communication:

    def __init__(self, config):
        self._logger = logging.getLogger(self.__class__.__name__)

        self._config = config

        self.client = mqtt.Client()
        self.client.on_message = self._on_message_cb
        self.client.on_connect = self._on_connect_cb

        self._subscriptions = set()
        self._will = None

        self._thread = None
        self._lock = threading.Lock()

        if config.getboolean("ssl"):
            self.client.tls_set(self._config["ca_certs"], self._config["certfile"], self._config["keyfile"])
            if self._config.getboolean("unsafe_hostname", True):
                self.client.tls_insecure_set(True)

        if self._config.get("username"):
            self.client.username_pw_set(self._config["username"], password=self._config.get("password", None))

    def connect_async(self):
        with self._lock:
            if not self._thread:
                self._thread = threading.Thread(target=self._connect)
                self._thread.setDaemon(True)
                self._thread.start()

    def _connect(self):
        self.client.connect(host=self._config["hostname"], port=self._config.getint("port"))
        while True:
            try:
                self.client.loop_forever()
            except Exception as e:
                self._logger.error("MQTT connection broken, reconnecting")
                self._logger.error(e)

    def _on_message_cb(self, client, userdata, msg):
        # pass on to every callback fitting
        for topic, func in self._subscriptions:
            if self.is_subscription(topic, msg.topic):
                func(client, userdata, msg)

    def _on_connect_cb(self, client, userdata, flags, rc):
        # resubscribe to all topics when reconnecting
        for topic, func in self._subscriptions:
            self.client.subscribe(topic)
        # set last will
        if self.will:
            self.client.will_set(*self.will)

    def publish(self, topic, message, qos=0, retain=False):
        """
        Publish a message to the topic.
        :param str topic:
        :param message: dict-like object or string, must be json serializable
        :param int qos: quality of service for message
        :param bool retain: retain messages on broker
        """
        self._logger.debug("Publishing topic: %s message: %s qos: %s retain: %s", topic, message, qos, retain)
        try:
            # received a dict-like object
            message["timestamp"] = time.time()
        except TypeError:
            # we got a string or something
            message = {"message": message, "timestamp": time.time()}
        self._logger.debug("Message formatted to %s", message)
        self.client.publish(topic=topic, payload=json.dumps(message), qos=qos, retain=retain)

    def register_callback(self, topic, callback):
        cb_tuple = (topic, callback)
        if cb_tuple not in self._subscriptions:
            self._subscriptions.add(cb_tuple)
            self.client.subscribe(topic)

    @property
    def will(self):
        return self._will

    @will.setter
    def will(self, value):
        """
        Set value as our will
        :param value: Tuple[str, str, int, bool] where [topic, payload, qos, retain]
        """
        self._will = value
        self.client.will_set(*value)

    @staticmethod
    def is_subscription(sub, msg):
        sub = sub.split("/")
        msg = msg.split("/")
        # if the subscription topic is longer than the actual message topic, it ain't never gonna work
        if len(sub) > len(msg):
            return False

        for i, part in enumerate(msg):
            # catch all wildcard
            if sub[i] == "#":
                return True
            # one level wildcard or exact match
            elif sub[i] == "+" or sub[i] == part:
                continue
            else:
                return False
        return True
