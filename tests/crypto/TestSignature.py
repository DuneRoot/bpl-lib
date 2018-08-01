import unittest

from bpl_lib.crypto.Signature import Signature
from bpl_lib.crypto.Keys import Keys
from bpl_lib.crypto.Crypto import sha256

class TestSignature(unittest.TestCase):

    def test_signature_1(self):
        signature = Signature("secret").sign(sha256("message".encode()))["signature"]

        self.assertIsNotNone(signature)
        self.assertIsNotNone(signature, str)
        self.assertEqual(signature, "304402202f43daad19f64dd114d55c1488e4ecaee1ce79183008e21e663e24dc882c9b9d022023d0f4e9f63ac43404625b43dbd8df77a774b9e9f33e0d8ff569f6b6b5014e38")

    def test_signature_2(self):
        signature = Signature("secret just to make sure it works").sign(sha256("message data".encode()))["signature"]

        self.assertIsNotNone(signature)
        self.assertIsNotNone(signature, str)
        self.assertEqual(signature, "304402203aef6f3c4aaa0cb597b8e9b80248983641ae909a8700feea8609bdddb0db6bd40220364735b3fed0a4e0b19e78d7c36658bbd36db8658afce4e227f4aad78318407b")

    def test_verify_1(self):
        public_key = Keys("secret").get_public_key()
        message = sha256("message".encode())
        signature = "304402202f43daad19f64dd114d55c1488e4ecaee1ce79183008e21e663e24dc882c9b9d022023d0f4e9f63ac43404625b43dbd8df77a774b9e9f33e0d8ff569f6b6b5014e38"

        self.assertTrue(Signature.verify(public_key, message, signature))

    def test_verify_2(self):
        public_key = Keys("secret just to make sure it works").get_public_key()
        message = sha256("message data".encode())
        signature = "304402203aef6f3c4aaa0cb597b8e9b80248983641ae909a8700feea8609bdddb0db6bd40220364735b3fed0a4e0b19e78d7c36658bbd36db8658afce4e227f4aad78318407b"

        self.assertTrue(Signature.verify(public_key, message, signature))

if __name__ == "__main__":
    unittest.main()
