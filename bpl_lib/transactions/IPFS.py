from bpl_lib.helpers.Constants import TRANSACTION_FEES, TRANSACTION_TYPE
from bpl_lib.transactions.Transaction import Transaction

class IPFS(Transaction):

    def __init__(self, ipfs_hash, secret, second_secret=None, fee=None):
        """
        Creates a IPFS transaction

        :param ipfs_hash: ipfs hash (string)
        :param secret: secret passphrase (stirng or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param fee: fee for transaciton (integer)
        """

        super().__init__(TRANSACTION_TYPE.IPFS, secret)

        self._vendor_field = ipfs_hash
        self._fee = fee or TRANSACTION_FEES[self._type]

        self._sign(secret)
        if second_secret:
            self._second_sign(second_secret)
        self._id = self._get_id()

    def _handle_transaction_type(self, buffer):
        raise buffer
