from .transactions.Transaction import Transaction
from .helpers.Constants import TRANSACTION_TYPE
from .crypto.Keys import Keys

class IPFS(Transaction):

    def __init__(self, fee, _error_use_class_method=True):
        """
        Create a IPFS transaction

        :param fee: fee for transaction
        :param _error_use_class_method: boolean flag, used to indicate if the transaction
                                        was created from generate or from_dict
        """

        if _error_use_class_method:
            raise TypeError("Please use IPFS.generate(args) or IPFS.from_dict(args) to construct me.")

        super().__init__(TRANSACTION_TYPE.IPFS, fee)


    @classmethod
    def generate(cls, ipfs_hash, secret, second_secret=None, fee=None):
        """
        Create a IPFS transaction

        :param ipfs_hash: ipfs_hash (string)
        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param fee: fee for transaction
        :return: (IPFS)
        """

        self = cls(fee, _error_use_class_method=False)
        self._sender_public_key = Keys(secret).get_public_key()

        self._vendor_field = ipfs_hash

        self.sign(secret, second_secret)
        return self

    @classmethod
    def from_dict(cls, transaction):
        """
        Create a IPFS transaction

        :param transaction: transaction (dict)
        :return: (IPFS)
        """

        self = cls(transaction["fee"], _error_use_class_method=False)
        self._sender_public_key = transaction["senderPublicKey"]
        self._timestamp = transaction["timestamp"]

        self._vendor_field = transaction["vendorField"]

        self.sign_from_dict(transaction)
        return self

    def _handle_transaction_type(self, buffer):
        raise buffer
