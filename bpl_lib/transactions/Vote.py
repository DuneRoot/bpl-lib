from bpl_lib.transactions.Transaction import Transaction
from bpl_lib.helpers.Constants import TRANSACTION_TYPE
from bpl_lib.crypto.Keys import Keys

class Vote(Transaction):

    def __init__(self, fee, _error_use_class_method=True):
        """
        Creates a vote transaction

        :param fee: fee for transaction
        :param _error_use_class_method: boolean flag, used to indicate if the transaction
                                        was created from generate or from_dict
        """

        if _error_use_class_method:
            raise TypeError("Please use Vote.generate(args) or Vote.from_dict(args) to construct me.")

        super().__init__(TRANSACTION_TYPE.VOTE, fee)

    @classmethod
    def generate(cls, votes, secret, second_secret=None, fee=None):
        """
        Creates a vote transaction

        :param votes: votes (list)
        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param fee: fee for transaction
        :return: (Vote)
        """

        self = cls(fee, _error_use_class_method=False)
        self._sender_public_key = Keys(secret).get_public_key()

        self._asset["votes"] = votes

        self.sign(secret, second_secret)
        return self

    @classmethod
    def from_dict(cls, transaction):
        """
        Creates a vote transaction

        :param transaction: transaction (dict)
        :return: (Vote)
        """

        self = cls(transaction["fee"], _error_use_class_method=False)
        self._sender_public_key = transaction["senderPublicKey"]
        self._timestamp = transaction["timestamp"]

        self._asset["votes"] = transaction["asset"]["votes"]

        self.sign_from_dict(transaction)
        return self

    def _handle_transaction_type(self, buffer):
        buffer.write_bytes("".join(self._asset["votes"]).encode())
        return buffer
