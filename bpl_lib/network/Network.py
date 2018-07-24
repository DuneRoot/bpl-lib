from datetime import datetime
import json
import os

from .helpers.Constants import NETWORK_CONFIG, NETWORKS_PATH
from .helpers.Exceptions import BPLNetworkException
from .helpers.Util import hexlify

class Network:

    @staticmethod
    def _get_networks():
        """
        Gets a list of valid network identifiers

        :return: list (string)
        """

        return [network.split(".")[0] for network in os.listdir(NETWORKS_PATH)]

    @staticmethod
    def use(identifier):
        """
        Loads the configuration of a network into config.json

        :param identifier: valid network identifer (string)
        """

        if identifier not in Network._get_networks():
            raise BPLNetworkException({
                "message": "Invalid network identifier.",
                "network": identifier,
                "networks": Network._get_networks()
            })

        with open(os.path.join(NETWORKS_PATH, "{0}.json".format(identifier)), "r") as network, \
             open(NETWORK_CONFIG, "w") as config:
            json.dump(json.load(network), config, indent=4, sort_keys=True)

    @staticmethod
    def use_custom(begin_epoch, version):
        """
        Writes a custom configuration into config.json

        :param begin_epoch:
        :param version:
        """

        with open(NETWORK_CONFIG, "w") as config:
            json.dump({
                "begin_epoch": begin_epoch.strftime("%Y-%m-%d %H:%M:%S"),
                "version": "0x" + hexlify(bytes([version]))
            }, config, indent=4, sort_keys=True)

    @staticmethod
    def get_begin_epoch():
        """
        Gets the begin epoch time stored in config.json

        :return: begin epoch time (datetime)
        """

        with open(NETWORK_CONFIG, "r") as config:
            return datetime.strptime(json.load(config)["begin_epoch"], "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_version():
        """
        Gets the network version stored in config.json

        :return: network version (integer)
        """

        with open(NETWORK_CONFIG, "r") as config:
            return int(json.load(config)["version"], 16)
