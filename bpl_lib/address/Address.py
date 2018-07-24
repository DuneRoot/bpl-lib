import base58

from .helpers.Util import Buffer, unhexlify
from .network.Network import Network
from .crypto.Crypto import ripemd160
from .crypto.Keys import Keys

class Address:

    @staticmethod
    def from_public_key(public_key):
        """
        Create address from public key

        :param public_key: public key used to create address (string)
        :return: BPL address (string)
        """

        buffer = Buffer()
        buffer.write_byte(Network.get_version())
        buffer.write_bytes(ripemd160(unhexlify(public_key)))
        return base58.b58encode_check(buffer.to_bytes())

    @staticmethod
    def from_secret(secret):
        """
        Create address from secret passphrase

        :param secret: secret passphrase (bytes)
        :return: BPL address (string)
        """

        return Address.from_public_key(Keys(secret).get_public_key())

    @staticmethod
    def validate(address):
        """
        Validate BPL address

        :param address: BPL address (string)
        :return: is valid (boolean)
        """

        try:
            return base58.b58decode_check(address)[0] == Network.get_version()
        except Exception:
            return False
