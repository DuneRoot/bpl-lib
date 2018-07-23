from bpl_lib.helpers.Constants import TRANSACTION_FEES, TRANSACTION_TYPE

from bpl_lib.transactions.Transaction import Transaction


class MultiSignature(Transaction):

    def __init__(self, min, lifetime, keysgroup, secret, second_secret=None, fee=None):
        """
        Creates a Multi-Signature transaction

        :param min: #TODO
        :param lifetime: #TODO
        :param keysgroup: #TODO
        :param secret: secret passphrase (string or bytes)
        :param second_secret: second secret passphrase (string or bytes)
        :param fee: fee for transaction (integer)
        """

        super().__init__(TRANSACTION_TYPE.MULTI_SIGNATURE, secret)

        self._asset["multisignature"] = {
            "min": min,
            "lifetime": lifetime,
            "keysgroup": keysgroup
        }
        self._fee = fee or TRANSACTION_FEES[self._type]

        self._sign(secret)
        if second_secret:
            self._second_sign(second_secret)
        self._id = self._get_id()

    def _handle_transaction_type(self, buffer):
        buffer.write_bytes(
            bytes([self._asset["multisignature"]["min"]])
            + bytes([self._asset["multisignature"]["lifetime"]])
            + "".join(self._asset["multisignature"]["keysgroup"]).encode()
        )
        return buffer