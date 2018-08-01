import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

requires = [
    "base58>=1.0.0",
    "ecdsa"
]

packages = [
    "bpl_lib",
    "bpl_lib.address",
    "bpl_lib.crypto",
    "bpl_lib.helpers",
    "bpl_lib.network",
    "bpl_lib.time",
    "bpl_lib.transactions"
]

setuptools.setup(
    name="bpl-lib",
    version="0.0.12",
    author="Alistair O'Brien",
    author_email="alistair.o'brien@ellesmere.com",
    description="A library for the Blockpool Blockchain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DuneRoot/bpl-lib",
    packages=packages,
    install_requires=requires
)
