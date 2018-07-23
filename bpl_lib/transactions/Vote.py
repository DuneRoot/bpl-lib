from bpl_lib.helpers.Constants import TRANSACTION_FEES, TRANSACTION_TYPE

from bpl_lib.transactions.Transaction import Transaction


class Vote(Transaction):

    def __init__(self, votes, secret, second_secret=None, fee=None):
        """
        Creates a vote transaction

        :param votes: votes (list)
        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param fee: fee for transaction
        """

        super().__init__(TRANSACTION_TYPE.VOTE, secret)

        self._asset["votes"] = votes
        self._fee = fee or TRANSACTION_FEES[self._type]

        self._sign(secret)
        if second_secret:
            self._second_sign(second_secret)

        self._id = self._get_id()

    def _handle_transaction_type(self, buffer):
        buffer.write_bytes("".join(self._asset["votes"]).encode())
        return buffer
