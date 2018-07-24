from ecdsa.util import number_to_string, string_to_number
from ecdsa import SigningKey, SECP256k1
from ecdsa.ellipticcurve import Point

from .helpers.Util import hexlify
from .crypto.Crypto import sha256

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

    @staticmethod
    def uncompress_public_key(public_key):
        """
        Converts compressed public keys to uncompressed public keys

        Compressed public key:
                   ┌ 0x02 + x, if y mod 2 = 0
         f(x, y) = │
                   └ 0x03 + x, if y mod 2 = 1
        Uncompressed public key:
         f(x,y) = x + y

        https://bitcointalk.org/index.php?topic=644919
        :param public_key: compressed public key (string)
        :return: uncompressed public key (string)
        """

        p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f

        y_parity = int(public_key[: 2]) - 2
        x = int(public_key[2 :], 16)

        a = (pow(x, 3, p) + 7) % p
        y = pow(a, (p + 1) // 4, p)

        y = -y % p if y % 2 != y_parity else y
        return "{:x}{:x}".format(x, y)

    @staticmethod
    def point_from_public_key(public_key):
        C = SECP256k1
        L_n = C.baselen

        x = string_to_number(public_key[:L_n])
        y = string_to_number(public_key[L_n:])

        return Point(C.curve, x, y, C.order)


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
