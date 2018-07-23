from bpl_lib.helpers.Constants import TRANSACTION_FEES, TRANSACTION_TYPE
from bpl_lib.transactions.Transaction import Transaction


class Transfer(Transaction):

    def __init__(self, recipient_id, amount, secret, second_secret=None, vendor_field=None, fee=None):
        """
        Creates a transfer transaction

        :param recipient_id: id of user to send to (string)
        :param amount: amount to transfer (integer)
        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param vendor_field: #TODO
        :param fee: fee for transaction
        """

        super().__init__(TRANSACTION_TYPE.TRANSFER, secret)

        self._recipient_id = recipient_id
        self._amount = amount
        self._vendor_field = vendor_field
        self._fee = fee or TRANSACTION_FEES[self._type]

        self._sign(secret)
        if second_secret:
            self._second_sign(second_secret)

        self._id = self._get_id()

    def _handle_transaction_type(self, buffer):
        return buffer

