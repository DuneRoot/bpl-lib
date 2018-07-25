import setuptools

requires = [
    "base58>=1.0.0",
    "ecdsa"
]

packages = [
    "bpl_lib.address",
    "bpl_lib.crypto",
    "bpl_lib.helpers",
    "bpl_lib.network",
    "bpl_lib.time",
    "bpl_lib.transactions"
]

setuptools.setup(
    name="bpl-lib",
    description="A library for the Blockpool Blockchain.",
    version="0.0.1",
    url="https://github.com/DuneRoot/bpl-lib",
    author="Alistair O'Brien",
    author_email="alistair.o'brien@ellesmere.com",
    packages=packages,
    install_requires=requires
)
