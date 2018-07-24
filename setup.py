import sys

import setuptools

requires = [
    "base58",
    "ecdsa"
]

tests_require = []

extras_require = {
    'test': tests_require,
    'dev': requires + tests_require
}

setup_requires = ['pytest-runner'] if {'pytest', 'test', 'ptr'}.intersection(sys.argv) else []

setuptools.setup(
    name="bpl-lib",
    description="A library for the Blockpool Blockchain.",
    version="0.0.1",
    author="Alistair O'Brien",
    author_email="alistair.o'brien@ellesmere.com",
    packes=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=requires,
    extras_require=extras_require,
    tests_require=tests_require,
    setup_requires=setup_requires
)
