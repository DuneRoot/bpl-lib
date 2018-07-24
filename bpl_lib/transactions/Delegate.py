from bpl_lib.transactions.Transaction import Transaction
from bpl_lib.helpers.Constants import TRANSACTION_TYPE
from bpl_lib.crypto.Keys import Keys

class Delegate(Transaction):

    def __init__(self, fee, _error_use_class_method=True):
        """
        Create a delegate transaction

        :param fee: fee for transaction
        :param _error_use_class_method: boolean flag, used to indicate if the transaction
                                        was created from generate or from_dict
        """

        if _error_use_class_method:
            raise TypeError("Please use Delegate.generate(args) or Delegate.from_dict(args) to construct me.")

        super().__init__(TRANSACTION_TYPE.DELEGATE, fee)

    @classmethod
    def generate(cls, username, secret, second_secret=None, fee=None):
        """
        Create a delegate transaction

        :param username: username of delegate (string)
        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param fee: fee for transaction (integer)
        :return: (Delegate)
        """

        self = cls(fee, _error_use_class_method=False)
        self._sender_public_key = Keys(secret).get_public_key()

        self._asset["delegate"] = {
            "username": username,
            "publicKey": self._sender_public_key
        }

        self.sign(secret, second_secret)
        return self

    @classmethod
    def from_dict(cls, transaction):
        """
        Create a delegate transaction

        :param transaction: transaction (dict)
        :return: (Delegate)
        """

        self = cls(transaction["fee"], _error_use_class_method=False)
        self._sender_public_key = transaction["senderPublicKey"]
        self._timestamp = transaction["timestamp"]

        self._asset["delegate"] = transaction["asset"]["delegate"]

        self.sign_from_dict(transaction)
        return self

    def _handle_transaction_type(self, buffer):
        buffer.write_bytes(self._asset["username"].encode())
        return buffer
