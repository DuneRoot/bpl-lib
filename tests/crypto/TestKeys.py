import unittest

from bpl_lib.crypto.Keys import Keys

class TestKeys(unittest.TestCase):

    def test_public_key_1(self):
        public_key = Keys("shhItsASecret").get_public_key()

        self.assertIsNotNone(public_key)
        self.assertIsInstance(public_key, str)
        self.assertEqual(public_key, "02966d9d8ecc2fa80ceb1d59ec76e3a318d4b30699a4dd3001d68891f7a3c54ac8")

    def test_public_key_2(self):
        public_key = Keys("secret".encode()).get_public_key()

        self.assertIsNotNone(public_key)
        self.assertIsInstance(public_key, str)
        self.assertEqual(public_key, "03a02b9d5fdd1307c2ee4652ba54d492d1fd11a7d1bb3f3a44c4a05e79f19de933")

    def test_private_key_1(self):
        private_key = Keys("shhItsASecret").get_private_key()

        self.assertIsNotNone(private_key)
        self.assertIsInstance(private_key, str)
        self.assertEqual(private_key, "a1ac5e739d797c2d73ae768dfdb60274832c27ab99400baf8ed8e9514e46ad5d")

    def test_private_key_2(self):
        private_key = Keys("secret".encode()).get_private_key()

        self.assertIsNotNone(private_key)
        self.assertIsInstance(private_key, str)
        self.assertEqual(private_key, "2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b")