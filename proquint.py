#!/usr/bin/env python3

""" Proquint is an encoding scheme, used to handle 16-bit words aiming at generating
human-readable, spellable and pronouncable identifier.

Proquint uses two distinct alphabets (alphabet #1 named "consonants" contains 16 symbols,
alphabet #2 named "vocals" contains 4 symbols) with well-selected symbols (according to the
goals - human-readable...).

The scheme for a proquint [_pronouncable quintuple_] is "CVCVC" - where C is a symbol from
alphabet #1 and V is a symbol from alphabet #2. With that you can gently encode 16 bits
(log2(16 * 4 * 16 * 4 * 16)).

Proposal: https://arxiv.org/html/0901.4016
"""

import argparse
import sys

class Proquint:
    """ Proquint Encoding and Decoding Implementation """

    # construction key -> (alphabet, length of covered bits)
    ALPHABET = {
        "C": ("bdfghjklmnprstvz", 4),
        "V": ("aiou", 2)
    }

    CONSTRUCTION = "CVCVC"

    @staticmethod
    def encode_uint16(double: int) -> str:
        """ Proquint-encode 16-bit, returning resulting proquint.

        A non-iterative implementation would be:

        result = ""

        c1 = (double & 0b1111000000000000) >> 12
        v1 = (double & 0b0000110000000000) >> 10
        c2 = (double & 0b0000001111000000) >> 6
        v2 = (double & 0b0000000000110000) >> 4
        c3 = (double & 0b0000000000001111) >> 0

        result += Proquint.ALPHABET["C"][0][c1]
        result += Proquint.ALPHABET["V"][0][v1]
        result += Proquint.ALPHABET["C"][0][c2]
        result += Proquint.ALPHABET["V"][0][v2]
        result += Proquint.ALPHABET["C"][0][c3]

        return result
        """

        result = ""

        for position in reversed(Proquint.CONSTRUCTION):
            alphabet, bits = Proquint.ALPHABET[position]

            result += alphabet[double & (pow(2, bits) - 1)]
            double = double >> bits

        return ''.join(reversed(result))

    @staticmethod
    def encode(data: bytes, sep: str = '-') -> str:
        """ Proquint-encode data, returning proquints seperated using the given
        seperator. data must be a multiple of 16 bits.
        """

        assert len(data) % 2 == 0

        proquints = []

        for chunk in [data[i:i+2] for i in range(0, len(data), 2)]:
            uint16 = int.from_bytes(chunk, "big")
            proquints.append(Proquint.encode_uint16(uint16))

        return sep.join(proquints)

    @staticmethod
    def decode_uint16(proquint: str) -> int:
        """ Decode a proquint, returns decoded uint16. """

        # ensure proquing length, and ensure that all character are part of the alphabets:
        assert len(proquint) == 5
        assert all(c in ''.join(a[0] for a in Proquint.ALPHABET.values()) for c in proquint)

        result = 0

        for position, char in zip(Proquint.CONSTRUCTION, proquint):
            alphabet, bits = Proquint.ALPHABET[position]

            result = result << bits
            result = result | alphabet.index(char)

        return result

    @staticmethod
    def decode(proquints: str, sep: str = '-') -> bytes:
        """ Decode a string of proquints and returns the corresponding bytes. """

        result = b""

        for proquint in proquints.split(sep):
            result += Proquint.decode_uint16(proquint).to_bytes(2, byteorder="big")

        return result

def run_tests():
    """ Run various tests to ensure that this Proquint implementation for encoding and decoding
    works according to the proposal.
    """

    from ipaddress import IPv4Address

    # all examples from https://arxiv.org/html/0901.4016:
    assert "lusab-babad" == Proquint.encode(IPv4Address("127.0.0.1").packed)
    assert "gutih-tugad" == Proquint.encode(IPv4Address("63.84.220.193").packed)
    assert "gutuk-bisog" == Proquint.encode(IPv4Address("63.118.7.35").packed)
    assert "mudof-sakat" == Proquint.encode(IPv4Address("140.98.193.141").packed)
    assert "haguz-biram" == Proquint.encode(IPv4Address("64.255.6.200").packed)
    assert "mabiv-gibot" == Proquint.encode(IPv4Address("128.30.52.45").packed)
    assert "natag-lisaf" == Proquint.encode(IPv4Address("147.67.119.2").packed)
    assert "tibup-zujah" == Proquint.encode(IPv4Address("212.58.253.68").packed) 
    assert "tobog-higil" == Proquint.encode(IPv4Address("216.35.68.215").packed)
    assert "todah-vobij" == Proquint.encode(IPv4Address("216.68.232.21").packed)
    assert "sinid-makam" == Proquint.encode(IPv4Address("198.81.129.136").packed)
    assert "budov-kuras" == Proquint.encode(IPv4Address("12.110.110.204").packed)

    assert Proquint.decode("lusab-babad") == IPv4Address("127.0.0.1").packed
    assert Proquint.decode("gutih-tugad") == IPv4Address("63.84.220.193").packed
    assert Proquint.decode("gutuk-bisog") == IPv4Address("63.118.7.35").packed
    assert Proquint.decode("mudof-sakat") == IPv4Address("140.98.193.141").packed
    assert Proquint.decode("haguz-biram") == IPv4Address("64.255.6.200").packed
    assert Proquint.decode("mabiv-gibot") == IPv4Address("128.30.52.45").packed
    assert Proquint.decode("natag-lisaf") == IPv4Address("147.67.119.2").packed
    assert Proquint.decode("tibup-zujah") == IPv4Address("212.58.253.68").packed
    assert Proquint.decode("tobog-higil") == IPv4Address("216.35.68.215").packed
    assert Proquint.decode("todah-vobij") == IPv4Address("216.68.232.21").packed
    assert Proquint.decode("sinid-makam") == IPv4Address("198.81.129.136").packed
    assert Proquint.decode("budov-kuras") == IPv4Address("12.110.110.204").packed

    print("[*] all tests passed.")

def cli():
    """ Provides a command-line-interface using argparse """

    parser = argparse.ArgumentParser()

    parser.add_argument("action", choices=["encode", "decode"])

    parser.add_argument(
        "data",
        help="proquints to decode, or hexstring to encode (use '-' for passing bytes via stdin)"
    )

    args = parser.parse_args()

    if args.action == "encode":
        data = sys.stdin.buffer.read() if args.data == '-' else bytes.fromhex(args.data)
        proquints = Proquint.encode(data)
        print(proquints)
    elif args.action == "decode":
        data = sys.stdin.read() if args.data == '-' else args.data
        payload = Proquint.decode(data)
        sys.stdout.buffer.write(payload)

if __name__ == "__main__":
    cli()
