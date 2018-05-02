import logging
import time
import json
import threading

import paho.mqtt.client as mqtt


class Communication:

    def __init__(self, config):
        self._logger = logging.getLogger(self.__class__.__name__)

        self._config = config

        self.client = mqtt.Client()
        self.client.on_message = self._on_message_cb
        self.client.on_connect = self._on_connect_cb

        self._subscriptions = set()

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
            self.client.loop_forever()
            # try:
            #     self.client.loop_forever()
            # except Exception as e:
            #     self._logger.error("MQTT connection broken, reconnecting")
            #     self._logger.error(e)

    def _on_message_cb(self, client, userdata, msg):
        # pass on to every callback fitting
        for topic, func in self._subscriptions:
            # TODO: Properly filter by making wildcard comparisons possible
            # if msg.topic == topic:
            #     func(client, userdata, msg)
            func(client, userdata, msg)

    def _on_connect_cb(self, client, userdata, flags, rc):
        # resubscribe to all topics when reconnecting
        for topic, func in self._subscriptions:
            self.client.subscribe(topic)

    def publish(self, topic, message):
        """
        Publish a message to the topic.
        :param str topic:
        :param message: dict-like object or string, must be json serializable
        """
        self._logger.debug("Publishing topic: %s message: %s", topic, message)
        try:
            # received a dict-like object
            message["timestamp"] = time.time()
        except TypeError as ex:
            # we got a string or something
            message = {"message": message, "timestamp": time.time()}
        self._logger.debug("Message formatted to %s", message)
        self.client.publish(topic=topic, payload=json.dumps(message))

    def register_callback(self, topic, callback):
        cb_tuple = (topic, callback)
        if cb_tuple not in self._subscriptions:
            self._subscriptions.add(cb_tuple)
            self.client.subscribe(topic)
