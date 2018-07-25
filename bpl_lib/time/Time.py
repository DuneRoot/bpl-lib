from datetime import datetime

from bpl_lib.helpers.Constants import INTERVAL
from bpl_lib.network.Network import Network

class Time:


    @staticmethod
    def get_time(time=None):
        """
        Gets timestamp for current network

        :return: blockchain timestamp (integer)
        """

        if not time:
            time = datetime.utcnow()

        return int((time - Network.get_begin_epoch()).total_seconds())

    @staticmethod
    def get_real_time(timestamp=None):
        """
        Converts timestamp into datetime

        :param timestamp: blockchain timestamp (integer)
        :return: (datetime)
        """

        if not timestamp:
            timestamp = Time.get_time()

        return datetime.utcfromtimestamp(timestamp + Network.get_begin_epoch().timestamp()).strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_slot_number(timestamp=None):
        """
        Calculates slot number

        :param timestamp: blockchain timestamp (integer)
        :return: slot number (integer)
        """

        if not timestamp:
            timestamp = Time.get_time()

        return timestamp // INTERVAL

    @staticmethod
    def get_slot_time(slot_number=None):
        """
        Calculates timestamp of network from slot

        :param slot_number: slot number (integer)
        :return: blockchain timestamp (integer)
        """

        if not slot_number:
            slot_number = Time.get_slot_time()

        return slot_number * INTERVAL
