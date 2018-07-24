from bpl_lib.transactions.Transaction import Transaction
from bpl_lib.helpers.Constants import TRANSACTION_TYPE
from bpl_lib.helpers.Util import unhexlify
from bpl_lib.crypto.Keys import Keys

class SecondSignature(Transaction):

    def __init__(self, fee, _error_use_class_method=True):
        """
        Creates a Second Signature transaction

        :param fee: fee for transaction
        :param _error_use_class_method: boolean flag, used to indicate if the transaction
                                        was created from generate or from_dict
        """

        if _error_use_class_method:
            raise TypeError("Please use SecondSignature.generate(args) or SecondSignature.from_dict(args) to construct me.")

        super().__init__(TRANSACTION_TYPE.SECOND_SIGNATURE, fee)

    @classmethod
    def generate(cls, secret, second_secret, fee=None):
        """
        Create a Second Signature transaction

        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param fee: fee for transaction
        :return: (SecondSignature)
        """

        self = cls.__init__(fee, _error_use_class_method=False)
        self._sender_public_key = Keys(secret).get_public_key()

        self._asset["signature"] = {
            "publicKey": Keys(second_secret).get_public_key()
        }

        self.sign(secret, second_secret)
        return self

    @classmethod
    def from_dict(cls, transaction):
        """
        Create a Second Signature transaction

        :param transaction: transaction (dict)
        :return: (SecondSignature)
        """

        self = cls.__init__(transaction["fee"], _error_use_class_method=False)
        self._sender_public_key = transaction["senderPublicKey"]
        self._timestamp = transaction["timestamp"]

        self._asset["signature"] = transaction["asset"]["signature"]

        self.sign_from_dict(transaction)
        return self

    def _handle_transaction_type(self, buffer):
        buffer.write_bytes(unhexlify(self._asset["signature"]))
        return buffer
