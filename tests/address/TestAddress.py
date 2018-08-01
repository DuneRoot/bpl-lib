import unittest

from bpl_lib.network.Network import Network
from bpl_lib.address.Address import Address
from bpl_lib.crypto.Keys import Keys

class TestAddress(unittest.TestCase):

    def test_from_public_key_1(self):
        Network.use("mainnet")
        public_key = Keys("secret").get_public_key()
        address = Address.from_public_key(public_key)

        self.assertTrue(isinstance(address, bytes))
        self.assertEqual(address, b"AJWRd23HNEhPLkK1ymMnwnDBX2a7QBZqff")

    def test_from_public_key_2(self):
        Network.use("mainnet")
        public_key = Keys("secret second test to be sure it works correctly").get_public_key()
        address = Address.from_public_key(public_key)

        self.assertTrue(isinstance(address, bytes))
        self.assertEqual(address, b"AQSqYnjmwj1GBL5twD4K9EBXDaTHZognox")

    def test_from_secret_1(self):
        Network.use("mainnet")
        address = Address.from_secret("secret")

        self.assertTrue(isinstance(address, bytes))
        self.assertEqual(address, b"AJWRd23HNEhPLkK1ymMnwnDBX2a7QBZqff")

    def test_from_secret_2(self):
        Network.use("mainnet")
        address = Address.from_secret("secret second test to be sure it works correctly")

        self.assertTrue(isinstance(address, bytes))
        self.assertEqual(address, b"AQSqYnjmwj1GBL5twD4K9EBXDaTHZognox")

    def test_validate_1(self):
        Network.use("mainnet")
        self.assertTrue(Address.validate("AQSqYnjmwj1GBL5twD4K9EBXDaTHZognox"))

    def test_validate_2(self):
        Network.use("mainnet")
        self.assertFalse(Address.validate("totally not valid address"))

if __name__ == "__main__":
    unittest.main()
