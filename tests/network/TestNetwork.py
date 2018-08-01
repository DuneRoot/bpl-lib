import unittest

from bpl_lib.network.Network import Network
from datetime import datetime


class TestNetwork(unittest.TestCase):

    def test_use_1(self):
        Network.use("mainnet")

        self.assertEqual(Network.get_begin_epoch(), datetime.strptime("2017-03-21 13:00:00", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(Network.get_version(), 0x17)

    def test_use_2(self):
        Network.use("testnet")

        self.assertEqual(Network.get_begin_epoch(), datetime.strptime("2017-03-21 13:00:00", "%Y-%m-%d %H:%M:%S"))
        self.assertEqual(Network.get_version(), 0x17)

    def test_use_custom_1(self):
        begin_epoch = datetime.strptime("2018-07-25 13:00:00", "%Y-%m-%d %H:%M:%S")
        version = 0x19

        Network.use_custom("test_use_custom_1", begin_epoch, version)

        self.assertEqual(Network.get_begin_epoch(), begin_epoch)
        self.assertEqual(Network.get_version(), version)

if __name__ == "__main__":
    unittest.main()