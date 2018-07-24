from bpl_lib.transactions.Transaction import Transaction
from bpl_lib.helpers.Constants import TRANSACTION_TYPE
from bpl_lib.crypto.Keys import Keys

class Transfer(Transaction):

    def __init__(self, fee, _error_use_class_method=True):
        """
        Creates a transfer transaction

        :param fee: fee for transaction
        :param _error_use_class_method: boolean flag, used to indicate if the transaction
                                        was created from generate or from_dict
        """

        if _error_use_class_method:
            raise TypeError("Please use Transfer.generate(args) or Transfer.from_dict(args) to construct me.")

        super().__init__(TRANSACTION_TYPE.TRANSFER, fee)

    @classmethod
    def generate(cls, recipient_id, amount, secret, second_secret=None, vendor_field=None, fee=None):
        """
        Creates a transfer transaction

        :param recipient_id: id of user to send to (string)
        :param amount: amount to transfer (integer)
        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param vendor_field: #TODO
        :param fee: fee for transaction
        :return: (Transfer)
        """

        self = cls(fee, _error_use_class_method=False)
        self._sender_public_key = Keys(secret).get_public_key()

        self._recipient_id = recipient_id
        self._amount = amount
        self._vendor_field = vendor_field

        self.sign(secret, second_secret)
        return self

    @classmethod
    def from_dict(cls, transaction):
        """
        Creates a transfer transaction

        :param transaction: transaction (dict)
        :return: (Transfer)
        """

        self = cls(transaction["fee"], _error_use_class_method=False)
        self._sender_public_key = transaction["senderPublicKey"]
        self._timestamp = transaction["timestamp"]

        self._recipient_id = transaction["recipientId"]
        self._amount = transaction["amount"]
        self._vendor_field = transaction.get("vendorField", None)

        self.sign_from_dict(transaction)
        return self

    def _handle_transaction_type(self, buffer):
        return buffer
