import base58

from bpl_lib.helpers.Util import Buffer, unhexlify, hexlify
from bpl_lib.helpers.Constants import TRANSACTION_FEES
from bpl_lib.crypto.Signature import Signature
from bpl_lib.crypto.Crypto import sha256
from bpl_lib.time.Time import Time

class Transaction:

    def __init__(self, type, fee):
        """
        Parent Class for all transactons

        :param type: transaction type (TRANSACTION_TYPE)
        :param fee: fee for transaction (integer)
        """

        self._id = None
        self._type = type
        self._recipient_id = None

        self._amount = 0
        self._fee = fee or TRANSACTION_FEES[self._type]
        self._asset = {}

        self._vendor_field = None
        self._timestamp = Time.get_time()

        self._requester_public_key = None
        self._sender_public_key = None

        self._signature = None
        self._sign_signature = None

    @classmethod
    def generate(cls, *args):
        raise NotImplementedError

    def sign(self, secret, second_secret=False):
        """
        Signs the transaction with signatures and an id

        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        """

        self._sign(secret)
        if second_secret:
            self._second_sign(second_secret)
        self._id = hexlify(sha256(self._to_bytes(False, False)))

    def sign_from_dict(self, transaction):
        """
        Signs the transaction with signatures and an id from a dictionary

        :param transaction: (dict)
        """

        self._signature = transaction["signature"]
        if transaction.get("signSignature", False):
            self._sign_signature = transaction["signSignature"]
        self._id = transaction["id"]

    def _get_hash(self, skip_signature=True, skip_second_signature=True):
        """
        Computes the hash for the transaction

        :param skip_signature: boolean
        :param skip_second_signature: boolean
        :return: hash (bytes)
        """

        return sha256(self._to_bytes(skip_signature, skip_second_signature))

    def to_dict(self):
        """Converts Transaction to a dictionary representation

        :return: (dict)
        """

        return {
            "type": self._type,
            "amount": self._amount,
            "fee": self._fee,
            "asset": self._asset,
            "id": self._id,
            "recipientId": self._recipient_id,
            "venderField": self._vendor_field,
            "timestamp": self._timestamp,
            "senderPublicKey": self._sender_public_key,
            "signature": self._signature,
            "signSignature": self._sign_signature
        }

    @classmethod
    def from_dict(cls, transaction):
        raise NotImplementedError

    def _to_bytes(self, skip_signature=True, skip_second_signature=True):
        """
        Calculates the bytes of the transaction (See bpl_lib-js for initial algorithm)

        :param skip_signature: boolean
        :param skip_second_signature: boolean
        :return: (bytes)
        """

        buffer = Buffer()

        buffer.write_byte(int(self._type))
        buffer.write_int(self._timestamp)

        buffer.write_bytes(unhexlify(self._sender_public_key))

        if self._requester_public_key:
            buffer.write_bytes(unhexlify(self._requester_public_key))

        buffer.write_bytes(
            base58.b58decode_check(self._recipient_id) \
            if self._recipient_id else bytes(21)
        )


        if self._vendor_field:
            vendor_field = self._vendor_field.encode()
            buffer.write_bytes(vendor_field + bytes(64 - len(vendor_field)))
        else:
            buffer.write_bytes(bytes(64))


        buffer.write_long(self._amount)
        buffer.write_long(self._fee)


        buffer = self._handle_transaction_type(buffer)
        buffer = self._handle_signature(buffer, skip_signature, skip_second_signature)

        return buffer.to_bytes()

    def _handle_signature(self, buffer, skip_signature, skip_second_signature):
        """
        Handles the signatures stored in the transaction when calculating bytes.
        Adds signatures to buffer if signatures have been calculated and if they aren't
        being skipped

        :param buffer: stores currently calculated bytes of transaction (Buffer)
        :param skip_signature: boolean
        :param skip_second_signature: boolean
        :return: buffer (Buffer)
        """

        if not skip_signature and self._signature:
            buffer.write_bytes(unhexlify(self._signature))

        if not skip_second_signature and self._sign_signature:
            buffer.write_bytes(unhexlify(self._sign_signature))

        return buffer

    def _handle_transaction_type(self, buffer):
        """
        Abstract method for handling transaction types

        :param buffer: stores currently calculated bytes of transaction (buffer)
        :return: buffer (Buffer)
        """

        raise NotImplementedError

    def _sign(self, secret):
        """
        Signs the transaction with a signature generated from the self._sender_public_key of the transaction

        :param secret: secret passphrase used to generate self._sender_public_key (string or bytes)
        """
        signature = Signature(secret).sign(self._get_hash())
        self._signature = signature["signature"]

    def _second_sign(self, secret):
        """
        Signs the transaction with a second signature generated from a provided secret passphrase

        :param secret: secret passphrase (string or bytes)
        """

        signature = Signature(secret).sign(self._get_hash(False, True))
        self._sign_signature = signature["signature"]

    def verify(self):
        """
        Verifies the transaction using first signature
        #TODO produce from_json method to allow transactions to be constructed from json objects,
        this will allow api's to quickly verify transactions

        :return: is valid (boolean)
        """

        return Signature.verify(self._sender_public_key, self._get_hash(), self._signature)

    def second_verify(self, public_key):
        """
        Verifies the transaction using both signatures
        #TODO produce from_json method to allow transactions to be constructed from json objects,
        this will allow api's to quickly verify transactions

        :return: is valid (boolean)
        """

        return Signature.verify(public_key, self._get_hash(False, True), self._sign_signature)
