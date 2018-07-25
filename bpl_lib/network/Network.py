from datetime import datetime

from bpl_lib.helpers.Exceptions import BPLNetworkException
from bpl_lib.helpers.Util import hexlify
from bpl_lib.network.DDL import DDL
from bpl_lib.helpers.Database import Database

network = {}
DDL.ddl()

class Network:

    @staticmethod
    def _get_networks():
        """
        Gets a list of valid network identifiers

        :return: list (string)
        """

        database = Database()
        networks = database.query("SELECT Identifier FROM Networks;")
        database.close()

        return [identifier[0] for identifier in networks]

    @staticmethod
    def use(identifier):
        """
        Loads the configuration of a network from networks.db

        :param identifier: valid network identifer (string)
        """

        if identifier not in Network._get_networks():
            raise BPLNetworkException({
                "message": "Invalid network identifier.",
                "network": identifier,
                "networks": Network._get_networks()
            })

        database = Database()
        network_result_set = database.query(
            "SELECT BeginEpoch, Version FROM Networks WHERE Identifier = ?;",
            (identifier, )
        )[0]

        global network
        network = {
            "begin_epoch": datetime.strptime(network_result_set[0], "%Y-%m-%d %H:%M:%S"),
            "version": int(network_result_set[1], base=16)
        }

        database.close()

    @staticmethod
    def use_custom(identifier, begin_epoch, version):
        """
        Writes custom configuration into network and networks.db

        :param begin_epoch:
        :param version:
        """

        if identifier in Network._get_networks():
            raise BPLNetworkException({
                "message": "Network identifier UNIQUE CONSTRAINT.",
                "network": identifier,
                "networks": Network._get_networks()
            })

        database = Database()
        database.insert(
            "INSERT INTO Networks(Identifier, BeginEpoch, Version) "
          + "VALUES (?, ?, ?);",
            (identifier, begin_epoch.strftime("%Y-%m-%d %H:%M:%S"),
            "0x" + hexlify(bytes([version])))
        )
        database.close()

        global network
        network = {
            "begin_epoch": begin_epoch,
            "version": version
        }

    @staticmethod
    def get_begin_epoch():
        """
        Gets the begin epoch time stored in networks

        :return: begin epoch time (datetime)
        """

        if not network:
            raise BPLNetworkException({
                "message": "network has not yet been set. Please use Network.use."
            })

        return network["begin_epoch"]

    @staticmethod
    def get_version():
        """
        Gets the network version stored in networks

        :return: network version (integer)
        """

        if not network:
            raise BPLNetworkException({
                "message": "network has not yet been set. Please use Network.use."
            })

        return network["version"]
