from datetime import datetime
from bpl_lib.network.Network import Network


def get_time():
    """
    Gets the current time for the blockchain

    :return: time in seconds (integer)
    """

    now = datetime.utcnow()
    return int((now - Network.get_begin_epoch()).total_seconds())