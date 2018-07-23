from bpl_lib.helpers.Util import hexlify
from bpl_lib.crypto.Crypto import sha256

from ecdsa import SigningKey, SECP256k1
from ecdsa.util import number_to_string

class Keys:

    def __init__(self, secret):
        """
        Initializes Keys object

        :param secret: secret passphrase (bytes or string)
        """

        if not isinstance(secret, bytes):
            secret = secret.encode()

        self._private_key = self._private_key_from_secret(secret)
        self._public_key = self._public_key_from_secret(secret)

    def _private_key_from_secret(self, secret):
        """
        Get a private key from a provided secret passphrase

        :param secret: secret passphrase (bytes)
        :return: private key (string)
        """

        return hexlify(sha256(secret))

    def _public_key_from_secret(self, secret):
        """
        Get a public key from a provided secret passphrase

        :param secret: secret passphrase (bytes)
        :return: public key (string)
        """

        return self._compress_public_key(sha256(secret))

    def _compress_public_key(self, private_key):
        """
        Compute ECDSA compressed public key

        :param private_key: private key (bytes)
        :return: compressed public key (string)
        """

        order = SigningKey.from_string(private_key, curve=SECP256k1).curve.generator.order()
        point = SigningKey.from_string(private_key, curve=SECP256k1).get_verifying_key().pubkey.point
        return hexlify(chr(2 + (point.y() & 1)).encode() + number_to_string(point.x(), order))

    def to_dict(self):
        """
        Converts Keys to a dictionary representation

        :return: (dict) containing public key and private key
        """

        return {
            "private_key": self._private_key,
            "public_key": self._public_key
        }

    def get_private_key(self):
        """
        Gets the computed private key

        :return: private key (string)
        """

        return self._private_key

    def get_public_key(self):
        """
        Gets the computed public key

        :return: public key (string)
        """

        return self._public_key

    def __repr__(self):
        return str(self.to_dict())

