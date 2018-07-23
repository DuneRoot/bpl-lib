import binascii

def hexlify(data):
    """
    Converts binary data to hexadecimal

    :param data: data (bytes)
    :return: hexadecimal string (string)
    """

    return binascii.hexlify(data).decode()

def unhexlify(data):
    """
    Converts hexadecimal to binary data

    :param data: hexadecimal string (string)
    :return: data (bytes)
    """

    if len(data) % 2:
        data = "0" + data
    return binascii.unhexlify(data)

class Buffer:

    def __init__(self):
        """
        Buffer Class

        Used to mimic Buffer in javascript
        """

        self._bytearray = bytearray()

    def write_byte(self, data):
        """
        Writes a byte to the buffer

        :param data: integer between 0 and 255
        """

        self.write_bytes(bytes([data]))

    def write_int(self, data):
        """
        Write a 32bit integer to the buffer

        :param data: 32 bit integer
        """

        try:
            bytesData = self._int_to_bytes(32, data)
        except Exception:
            raise ValueError({
                "message": "data must be less than 32 bits"
            })

        self.write_bytes(bytesData)

    def write_long(self, data):
        """
        Writes a 64bit integer to the buffer

        :param data: 64 bit integer
        """

        try:
            bytesData = self._int_to_bytes(64, data)
        except Exception:
            raise ValueError({
                "message": "data must be less than 64 bits"
            })

        self.write_bytes(bytesData)

    def write_bytes(self, data):
        """
        Writes a series of bytes to the buffer

        :param data: data (bytes)
        """

        self._bytearray.extend(data)

    def _int_to_bytes(self, bits, data):
        """
        Converts integers to bytes

        :param bits: number of bits used to encode (integer)
        :param data: data (integer)
        :return: converted bytes
        """

        return bytes(bytearray.fromhex(
           ("{" + ":0{0}x".format(bits // 4) + "}").format(data)
        )[::-1])

    def to_bytes(self):
        """
        Converts buffer to bytes

        :return: (bytes)
        """

        return bytes(self._bytearray)

    def __repr__(self):
        return hexlify(self.to_bytes())

    def __len__(self):
        return len(self._bytearray)

