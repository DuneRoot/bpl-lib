# BPL lib

> A simple Python package for the Blockpool Blockchain

This is an easy-to-use Python package for interacting with a Blockpool Blockchain. This package provided the majority of the functionality provided by [BPL-JS](https://github.com/blockpool-io/BPL-js)

## Features

### Address
- [x] from_secret
- [x] from_public_key
- [ ] from_private_key
- [x] validate

### Network
- [x] use
- [x] use_custom
- [x] get_begin_epoch
- [x] get_version

### Transaction Entity
- [x] generate
- [x] get_id
- [x] get_hash
- [x] sign
- [x] second_sign
- [x] to_bytes
- [x] to_dict
- [x] from_dict
- [x] verify
- [x] second_verify

### Transaction Types
- [x] Transfer Transaction
- [x] Vote Transaction
- [x] Second Signature Transaction
- [x] Multi-Signature Transaction
- [x] Delegate Transaction
- [x] IPFS Transaction

### Time
- [x] get_time
- [x] get_real_time
- [x] get_slot_number
- [x] get_slot_time

## Installation

```sh
python -m pip install bpl-lib
```

## Usage

There are 6 main sub-packages in bpl-lib:

- ``bpl_lib.address``
- ``bpl_lib.crypto``
- ``bpl_lib.helpers``
- ``bpl_lib.network``
- ``bpl_lib.time``
- ``bpl_lib.transactions``

***

### Addresses

#### Generating an Address

There are currently 2 methods for generating an address:
- ``from_public_key``
- ``from_secret``

Note: Addresses are dependent on the ``version`` of the network, therefore to generate an address you must first select a network (see network section).
##### from_public_key

To generate a unique Blockpool address from a given public key:
```python
from bpl_lib.address import Address
from bpl_lib.network import Network

Network.use("mainnet")
public_key = "03aacac6c98daaf3d433fe90e9295ce380916946f850bcdc6f6880ae6503ca1e40"
address = Address.from_public_key(public_key)

print(address)
```

Printing:

```python
b'AdzCBJt2F2Q2RYL7vnp96QhTeGdDZNZGeJ'
```

##### from_secret

To generate a unique Blockpool address from a given secret passphrase:
```python
from bpl_lib.address import Address
from bpl_lib.network import Network

Network.use("mainnet")
address = Address.from_secret("secret passphrase")

print(address)
```

Printing:

```python
b'AdzCBJt2F2Q2RYL7vnp96QhTeGdDZNZGeJ'
```

#### Validation

Note: Addresses are dependent on the ``version`` of the network, therefore to validate an address you must first select a network (see network section).

```python
from bpl_lib.address import Address
from bpl_lib.network import Network

Network.use("mainnet")
address = "AdzCBJt2F2Q2RYL7vnp96QhTeGdDZNZGeJ"
is_valid = Address.validate(address)

print(is_valid)
```

Printing:

```python
True
```

***

### Cryptography

#### Generating Keys
```python
from bpl_lib.crypto import Keys

keys = Keys("secret passphrase").to_dict()

print(keys)
```

Printing:

```python
{
    "public_key": "03aacac6c98daaf3d433fe90e9295ce380916946f850bcdc6f6880ae6503ca1e40",
    "private_key": "b6a2b12beb4179538bfb42423cce2e98ccdebcc684145ba977f2f80630eb278e"
}
```

#### Signatures
 ```python
from bpl_lib.crypto import Signature, sha256

message = sha256("message".encode())
signature = Signature("secret passphrase").sign(message)["signature"]

print(signature)
```

Printing:
```python
"30440220622b8edf8fc5cf4522a13489a9b710b1bf94b6e37722d2278a0069ae3c67088b0220206e202dcad8e4ee2100716ce0d2c7d08a685f983c21dfbccdd6ecec50268b6f"
```

#### Hashing
The ``crypto`` sub-package also provides common hashing algorithms such as:
- ``sha1(bytes)``
- ``sha256(bytes)``
- ``ripemd160(bytes)``
- ``hash160(bytes)``
- ``hash256(bytes)``

***

### Helpers
The helpers package contains useful contains and classes:
- ``TRANSACTION_TYPE`` - Enum Class containing all 6 transaction types
- ``TRANSACTION_FEES`` - Transaction fees depending on `TRANSACTION_TYPE`
- ``NETWORKS_DB`` - Networks database file location

***

### Network
The networks sub-package is an interface for network configurations.  The networks sub-package makes use of a local SQLite database, which stores the network identifier, begin epoch time and network version. These setting / fields are require for calculations such as addresses and timestamps.

#### Using a network
There are current 2 methods that allows a client to use a network:
- ``use``
- ``use_custom``

##### use
The `use` method requires a network ``identifier`` and queries the local network database for the specified configuration. The method then stores the configuration in memory.

```python
from bpl_lib.network import Network

Network.use("mainnet")

print(Network.get_begin_epoch())
print(Network.get_version())
```

Printing:

```python
"2017-03-21 13:00:00"
23
```

##### use_custom
The `use_custom` method requires a network `identifier`, `begin_epoch` and `version`. The method first inserts this custom configuration into the local network database, this will allow you to make use of the custom configuration in other applications. After that the method stores the custom configuration in memory.

Note: ``identifier`` is used as the primary key in the database, this implies that the identifier for the network must be unique. If the identifier is not unique a `BPLNetworkException` is raised.
```python
from datetime import datetime

from bpl_lib.network import Network

identifier = "test_use_custom_method"
begin_epoch = datetime.strptime("2018-07-25 15:30:00", "%Y-%m-%d %H:%M:%S")
version = 0x19

Network.use_custom(identifier, begin_epoch, version)

print(Network.get_begin_epoch())
print(Network.get_version())
```

Printing:

```python
"2018-07-25 15:30:00"
25
```

#### Accessing the current configuration
After loading a network configuration into memory, there are 2 settings that can be accessed via the `Network` interface:
- `begin_epoch`
- `version`

##### Accessing begin_epoch
To access `begin_epoch` the `Network.get_begin_epoch` method must be used.
```python
from bpl_lib.network import Network

Network.use("testnet")

print(Network.get_begin_epoch())
```

Printing:

```python
"2017-03-21 13:00:00"
```

##### Accessing version
To access `version` the `Network.get_version` method must be used.
```python
from bpl_lib.network import Network

Network.use("testnet")

print(Network.get_version())
```

Printing:
```python
82
```

***

### Time
The time sub-package contains 4 methods:
- `get_time` - returns the timestamp for the blockchain
- `get_real_time` - converts blockchain timestamp to datetime
- `get_slot_number` - converts blockchain timestamp to slot number
- `get_slot_time` - converts slot number to blockchain timestamp

#### get_time
The `get_time` method converts a datetime object to a blockchain timestamp. The method has an optional argument `time`. If `time` is not provided then the current time will be used. (See code)
```python
from bpl_lib.time import Time

print(Time.get_time())
```

Printing:

```python
42429391
```

#### get_real_time
The `get_real_time` method converts a blockchain timestamp into a datetime object. The method has an optional argument `timestamp`. If `timestamp` is not provided then the current timestamp will be used. (See code)
```python
from bpl_lib.time import Time

print(Time.get_real_time(42429391))
```

Printing:

```python
"2018-07-25 14:56:31"
```

#### get_slot_number
The `get_slot_number` method converts a blockchain timestamp into a slot number. The method has an optional argument `timestamp`. If `timestamp` is not provided then the current timestamp will be used. (See code)
```python
from bpl_lib.time import Time

print(Time.get_slot_number())
```

Printing:

```python
5303721
```

#### get_slot_time
The `get_slot_time` method converts a slot number into a blockchain timestamp. The method has an optional argument `slot_number`. If `slot_number` is not provided then the current slot number will be used. (See code)
```python
from bpl_lib.time import Time

print(Time.get_slot_time(5303721))
```

Printing:

```python
42429768
```

***

### Transactions
Each transaction is built from the Transaction Entity (See Features). There are 2 currently possible ways of building a BPL transaction:
 - `Transaction.generate`
 - `Transaction.from_dict`

#### Buidling a transaction using generate
`Transaction.generate` automatically calculates the timestamp for the transaction, therefore a network must be selected before a transaction can be built. (See network)

```python
from bpl_lib.transactions.Transfer import Transfer
from bpl_lib.network import Network

Network.use("mainnet")
transaction = Transfer.generate("BCU4rocsgw2GNihtnzAgFzRfx7XebZRpRi", 1000, "passphrase")

print(transaction.to_dict())
```
Printing:

```python
{  
   'recipientId': 'BCU4rocsgw2GNihtnzAgFzRfx7XebZRpRi',
   'senderPublicKey': '02e012f0a7cac12a74bdc17d844cbc9f637177b470019c32a53cef94c7a56e2ea9',
   'type': "<TRANSACTION_TYPE.TRANSFER: 0>",
   'id': '9bfa3aee9ed984f856c6268b0b03dd908d3541c4c94f614fdae5c66c587560b2',
   'asset': {},
   'venderField': None,
   'fee': 10000000,
   'signature': '3045022100faf1e2bb7388caf0ba4ca26d6bddf9ea39197365d369f63efe271ad183745a77022047865c97baa925369ee099594010f7e7912772febbb83bcb9512f9b2759ac97d',
   'timestamp': 42430405,
   'amount': 1000,
   'signSignature': None
}
```

To see how each transaction is built see the documentation in the code.

***

## Security or Errors

If you discover a security vulnerability or error within this package, please email [me](mailto:alistair.o'brien@ellesmere.com) or message me on the [BPL discord](https://discordapp.com/invite/67HxSKq).

***

## Credits

- [Alistair O'Brien](https://github.com/johnyob)
