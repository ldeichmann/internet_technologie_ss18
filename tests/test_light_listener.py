import unittest
from unittest import mock
from src.that_automation_tool.light_listener import LightListener


class LightListenerTest(unittest.TestCase):

    @staticmethod
    def _create_message(timestamp):
        mock_message = mock.MagicMock()
        mock_message.timestamp = float(timestamp)
        return mock_message

    def test_queue(self):
        # low number of messages for testing purposes
        num_msg = 3

        config_mock = mock.MagicMock()
        config_mock.getint.return_value = num_msg

        listener = LightListener(mock.MagicMock(), config_mock)
        self.assertEqual(listener._size, num_msg)

        msg1, msg2, msg3 = self._create_message(1000), self._create_message(1001), self._create_message(1002)

        msg4, msg5, msg6 = self._create_message(4000), self._create_message(5000), self._create_message(6000)

        # initialize with some values
        listener._add_message(msg3, None)
        listener._add_message(msg2, None)
        listener._add_message(msg1, None)

        # make sure queue is filled as expected
        self.assertEqual(listener._recent_values.qsize(), 3)
        self.assertEqual(listener._recent_values.queue[0], (msg1.timestamp, None),
                         "Oldest message isn't first element in queue")

        # make sure oldest entry gets dropped
        listener._add_message(msg4, None)
        self.assertEqual(listener._recent_values.queue[0], (msg2.timestamp, None),
                         "Oldest message isn't first element in queue")

        # make sure an old entry doesn't drop a new one
        listener._add_message(msg1, None)
        self.assertEqual(listener._recent_values.queue[0], (msg2.timestamp, None),
                         "Oldest message isn't first element in queue")

        # now test an element between min and max
        listener._add_message(msg6, None)
        self.assertEqual(listener._recent_values.queue[0], (msg3.timestamp, None),
                         "Oldest message isn't first element in queue")
        listener._add_message(msg5, None)
        self.assertEqual(listener._recent_values.queue[0], (msg4.timestamp, None),
                         "Oldest message isn't first element in queue")

        # rotate all messages older than 6 out of the queue
        listener._add_message(msg6, None)
        self.assertEqual(listener._recent_values.queue[0], (msg5.timestamp, None),
                         "Oldest message isn't first element in queue")
        listener._add_message(msg6, None)
        self.assertEqual(listener._recent_values.queue[0], (msg6.timestamp, None),
                         "Oldest message isn't first element in queue")
        self.assertListEqual(list(listener._recent_values.queue),
                             [(msg6.timestamp, None), (msg6.timestamp, None), (msg6.timestamp, None)])
