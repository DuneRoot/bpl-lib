import hashlib

from ecdsa.util import sigencode_der_canonize
from ecdsa.numbertheory import inverse_mod
from ecdsa.rfc6979 import generate_k
from ecdsa import SECP256k1

from bpl_lib.helpers.Util import hexlify, unhexlify, verify_point, sigdecode_der_canonize
from bpl_lib.crypto.Keys import Keys

class Signature(Keys):

    def __init__(self, secret):
        super().__init__(secret)


    def sign(self, message):
        """
        Sign a message - https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm

        :param message: message used to compute signature (bytes)
        :return: (dict) containing message, public key, private key and signature
        """

        G = SECP256k1.generator
        n = G.order()
        #Skip step 1, e is provided by :param message

        #Step 2
        L_n = n.bit_length()
        z = int(hexlify(message[:L_n]), base=16)

        #Step3
        d_a = int(self._private_key, base=16)
        k = generate_k(n, d_a, hashlib.sha256, message)
        assert 1 <= k <= n - 1

        #Step 4
        p1 = k * G

        #Step 5
        r = p1.x() % n
        assert r != 0

        #Step 6
        s = (inverse_mod(k, n) * ((z + (r * d_a)) % n)) % n
        assert s != 0

        #Step 7
        signature = hexlify(sigencode_der_canonize(r, s, n))

        return {
            "public_key": self._public_key,
            "private_key": self._private_key,
            "message": message,
            "signature": signature
        }

    @staticmethod
    def verify(public_key, message, signature):
        """
        Verifies a message - https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm

        :param public_key: public key (string)
        :param message: message used to verify signature (bytes)
        :param signature: signature (string)
        :return: boolean
        """

        G = SECP256k1.generator
        n = G.order()

        uncompressed_public_key = Keys.uncompress_public_key(public_key)
        try:
            Q_a = Keys.point_from_public_key(unhexlify(uncompressed_public_key))
            return verify_point(G, Q_a) and Signature.verify_signature(G, n, Q_a, message, unhexlify(signature))
        except AssertionError:
            return False

    @staticmethod
    def verify_signature(G, n, Q_a, message, signature):
        r, s = sigdecode_der_canonize(signature, n)
        print(r, s)
        # Step 1
        if not (1 <= r <= n - 1 and 1 <= s <= n - 1):
            return False

        # Skip step 2, e is provided by :param: message

        # Step 3
        L_n = n.bit_length()
        z = int(hexlify(message[:L_n]), base=16)

        # Step 4
        w = inverse_mod(s, n)

        # Step 5
        u_1, u_2 = (z * w) % n, (r * w) % n

        # Step 6
        p1 = u_1 * G + u_2 * Q_a
        print(p1)
        if not verify_point(G, p1):
            return False

        # Step 7
        print(r == p1.x() % n)
        return r == p1.x() % n
