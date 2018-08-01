import unittest
from datetime import datetime

from bpl_lib.network.Network import Network
from bpl_lib.time.Time import Time

class TestTime(unittest.TestCase):

    def test_get_time_1(self):
        Network.use("mainnet")
        time = Time.get_time(datetime.utcfromtimestamp(1533122273))

        self.assertIsNotNone(time)
        self.assertIsInstance(time, int)
        self.assertEqual(time, 43021073)

    def test_get_real_time_1(self):
        Network.use("mainnet")

        date_time = datetime.utcfromtimestamp(1533122273)
        time = Time.get_real_time(43021073)

        self.assertIsNotNone(time)
        self.assertIsInstance(time, str)
        self.assertEqual(time, date_time.strftime("%Y-%m-%d %H:%M:%S"))

    def test_get_slot_number(self):
        timestamp = 43021073
        slot_number = Time.get_slot_number(timestamp)

        self.assertIsNotNone(slot_number)
        self.assertIsInstance(slot_number, int)
        self.assertEqual(slot_number, 2868071)

    def test_get_slot_time(self):
        slot_number = 2868071
        slot_time = Time.get_slot_time(slot_number)

        self.assertIsNotNone(slot_time)
        self.assertIsInstance(slot_time, int)
        self.assertEqual(slot_time, 43021065)

if __name__ == "__main__":
    unittest.main()
