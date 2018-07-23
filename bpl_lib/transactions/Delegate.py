from bpl_lib.helpers.Constants import TRANSACTION_FEES, TRANSACTION_TYPE

from bpl_lib.transactions.Transaction import Transaction


class Delegate(Transaction):

    def __init__(self, username, secret, second_secret=None, fee=None):
        """
        Create Delegate transaction

        :param username: username of delegate (string)
        :param secret: secret passphrase (string)
        :param second_secret: second secret passphrase (string)
        :param fee: fee for transaction (integer)
        """

        super().__init__(TRANSACTION_TYPE.DELEGATE, secret)

        self._asset["delegate"] = {
            "username": username,
            "publicKey": self._sender_public_key
        }
        self._fee = fee or TRANSACTION_FEES[self._type]

        self._sign(secret)
        if second_secret:
            self._second_sign(second_secret)
        self._id = self._get_id()

    def _handle_transaction_type(self, buffer):
        buffer.write_bytes(self._asset["username"].encode())
        return buffer

