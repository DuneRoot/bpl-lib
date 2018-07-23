from bpl_lib.crypto.Keys import Keys
from bpl_lib.helpers.Constants import TRANSACTION_FEES, TRANSACTION_TYPE

from bpl_lib.helpers.Util import unhexlify
from bpl_lib.transactions.Transaction import Transaction


class SecondSignature(Transaction):

    def __init__(self, secret, second_secret, fee=None):
        """
        Creates a Second Signature transaction

        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param fee: fee for transaction
        """

        super().__init__(TRANSACTION_TYPE.SECOND_SIGNATURE, secret)

        self._asset["signature"] = {
            "publicKey": Keys(second_secret).get_public_key()
        }
        self._fee = fee or TRANSACTION_FEES[self._type]

        self._sign(secret)
        if second_secret:
            self._second_sign(second_secret)
        self._id = self._get_id()

    def _handle_transaction_type(self, buffer):
        buffer.write_bytes(unhexlify(self._asset["signature"]))
        return buffer
