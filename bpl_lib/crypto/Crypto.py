import hashlib

def create_hash(algorithm, bytes):
    h = hashlib.new(algorithm)
    h.update(bytes)
    return h

def ripemd160(bytes):
    return create_hash("ripemd160", bytes).digest()

def sha1(bytes):
    return create_hash("sha1", bytes).digest()

def sha256(bytes):
    return create_hash("sha256", bytes).digest()

def hash160(bytes):
    return ripemd160(sha256(bytes))

def hash256(bytes):
    return sha256(sha256(bytes))
