from .transactions.Transaction import Transaction
from .helpers.Constants import TRANSACTION_TYPE
from .crypto.Keys import Keys

class MultiSignature(Transaction):

    def __init__(self, fee, _error_use_class_method=True):
        """
        Creates a Multi-Signature transaction

        :param fee: fee for transaction
        :param _error_use_class_method: boolean flag, used to indicate if the transaction
                                        was created from generate or from_dict
        """

        if _error_use_class_method:
            raise TypeError("Please use MultiSignature.generate(args) or MultiSignature.from_dict(args) to construct me.")

        super().__init__(TRANSACTION_TYPE.MULTI_SIGNATURE, fee=fee)


    @classmethod
    def generate(cls, min, lifetime, keysgroup, secret, second_secret=None, fee=None):
        """
        Create a Multi-Signature transaction

        :param min: #TODO
        :param lifetime: #TODO
        :param keysgroup: #TODO
        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param fee: fee for transaction (integer)
        :return: (MultiSignature)
        """
        self = cls(fee, _error_use_class_method=False)
        self._sender_public_key = Keys(secret).get_public_key()

        self._asset["multisignature"] = {
            "min": min,
            "lifetime": lifetime,
            "keysgroup": keysgroup
        }

        self.sign(secret, second_secret)
        return self

    @classmethod
    def from_dict(cls, transaction):
        """
        Create a Multi-Signature transaction

        :param transaction: transaction (dict)
        :return: (MultiSignature)
        """

        self = cls(transaction["fee"], _error_use_class_method=False)
        self._sender_public_key = transaction["senderPublicKey"]
        self._timestamp = transaction["timestamp"]

        self._asset["multisignature"] = transaction["asset"]["multisignature"]

        self.sign_from_dict(transaction)
        return self

    def _handle_transaction_type(self, buffer):
        buffer.write_bytes(
            bytes([self._asset["multisignature"]["min"]])
            + bytes([self._asset["multisignature"]["lifetime"]])
            + "".join(self._asset["multisignature"]["keysgroup"]).encode()
        )
        return buffer
