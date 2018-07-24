from datetime import datetime

from .helpers.Constants import INTERVAL
from .network.Network import Network

def get_time(time=None):
    """
    Gets the current time for the blockchain

    :return: time in seconds (integer)
    """
    if not time:
        time = datetime.utcnow()

    return int((time - Network.get_begin_epoch()).total_seconds())

def get_real_time(epoch_time=None):
    if not epoch_time:
        epoch_time = get_time()

    return datetime.utcfromtimestamp(epoch_time + Network.get_begin_epoch().timestamp()).strftime("%Y-%m-%d %H:%M:%S")

def get_slot_number(epoch_time=None):
    if not epoch_time:
        epoch_time = get_time()

    return epoch_time / INTERVAL

def get_slot_time(slot_number=None):
    if not slot_number:
        slot_number = get_slot_time()

    return slot_number * INTERVAL
