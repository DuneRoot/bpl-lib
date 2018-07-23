from bpl_lib.crypto.Keys import Keys
from bpl_lib.helpers.Util import hexlify, unhexlify
import hashlib

from ecdsa import SigningKey, VerifyingKey, SECP256k1
from ecdsa.keys import BadDigestError, BadSignatureError
from ecdsa.util import sigencode_der_canonize, sigdecode_der

class Signature(Keys):
    """
    Signatures are currently not working, I have yet to figure this out.
    """

    def __init__(self, secret):
        super().__init__(secret)


    def sign(self, message):
        """
        Sign a message

        :param message: message used to compute signature (bytes)
        :return: (dict) containing message, public key, private key and signature
        """

        signing_key = SigningKey.from_string(unhexlify(self._private_key), curve=SECP256k1, hashfunc=hashlib.sha256)
        signature = hexlify(signing_key.sign_deterministic(
            message, hashfunc=hashlib.sha256,
            sigencode=sigencode_der_canonize
        ))
        return {
            "public_key": self._public_key,
            "private_key": self._private_key,
            "message": message,
            "signature": signature
        }

    @staticmethod
    def verify(public_key, message, signature):
        """
        Verify a message

        :param public_key: public key used to verify message (string)
        :param message: message used to verify (string)
        :param signature: signature of signed message (string)
        :return: boolean used to indicate if message is valid
        """

        uncompressed_public_key = Keys.uncompressed_public_key(public_key)
        verifying_key = VerifyingKey.from_string(
            unhexlify(uncompressed_public_key),
            curve=SECP256k1,
            hashfunc=hashlib.sha256
        )

        try:
            is_valid = verifying_key.verify(
                unhexlify(signature),
                message,
                hashfunc=hashlib.sha256,
                sigdecode=sigdecode_der
            )
        except BadSignatureError:
            raise BadSignatureError({
                "message": "Signature was invalid",
                "signature": signature
            })
        except BadDigestError as error:
            raise BadDigestError({
                "message": "Bad digest",
                "error": error
            })

        return is_valid


