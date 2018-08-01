import unittest

from bpl_lib.network import Network
from bpl_lib.transactions import Transfer

class TestKeys(unittest.TestCase):

    def test_generate_without_second_signature_1(self):
        Network.use("mainnet")

        transaction = Transfer.generate("AJWRd23HNEhPLkK1ymMnwnDBX2a7QBZqff", 1000, "secret")

        self.assertIsNotNone(transaction)
        self.assertIsInstance(transaction, Transfer)

    def test_generate_with_vendor_field_1(self):
        Network.use("mainnet")

        transaction = Transfer.generate(
            "AJWRd23HNEhPLkK1ymMnwnDBX2a7QBZqff", 1000, "secret",
            vendor_field="0123456789ABCDEF"
        )

        self.assertIsNotNone(transaction)
        self.assertIsInstance(transaction, Transfer)
        self.assertIsNotNone(transaction._vendor_field)

    def test_generate_with_vendor_field_2(self):
        Network.use("mainnet")

        transaction = Transfer.generate(
            "AJWRd23HNEhPLkK1ymMnwnDBX2a7QBZqff", 1000, "secret",
            vendor_field="A" * 64
        )

        self.assertIsNotNone(transaction)
        self.assertIsInstance(transaction, Transfer)
        self.assertIsNotNone(transaction._vendor_field)

    def test_generate_with_invalid_vendor_field_1(self):
        Network.use("mainnet")

        transaction = Transfer.generate(
            "AJWRd23HNEhPLkK1ymMnwnDBX2a7QBZqff", 1000, "secret",
            vendor_field="A" * 128
        )

        self.assertIsNotNone(transaction)
        self.assertIsInstance(transaction, Transfer)
        self.assertIsNone(transaction._vendor_field)


    def test_from_dict_1(self):
        Network.use("mainnet")

        transaction_json = {
            "amount": 10,
            "signSignature": None,
            "id": "264715578ae6dafb86f2a37c9b2bbafb559a5bbfec7e0551f5a8d967dbf3f1b9",
            "fee": 10000000,
            "type": 0,
            "timestamp": 42948327,
            "senderPublicKey": "0306fd3edc0404565174bacd690e601ec5aa03d589bf56979b5adc97912dccda36",
            "signature": "304502210090641586dae4347967541e19560a8b6bae65e5f95dada8b7dbc89cbee0e74bbd0220230"
                       + "40498f5a29462dcccfe315997bccf8bbe15f68414e526aff55fa1bdeb3cb7",
            "venderField": None,
            "recipientId": "BFCKaUEkmG8ULYitaharStcdn7ijuDxxpK",
            "asset": {}
        }

        transaction = Transfer.from_dict(transaction_json)

        self.assertIsNotNone(transaction)
        self.assertIsInstance(transaction, Transfer)
        self.assertTrue(transaction.verify())

        transaction._amount = 100
        self.assertFalse(transaction.verify())


if __name__ == "__main__":
    unittest.main()