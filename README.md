# Proquints in Python

Proquint is an encoding scheme to transform 16-bit sequences into readable, spellable and pronouncable identifier.

The original proposal can be found here: https://arxiv.org/html/0901.4016


## CLI Usage

```shell
$ python3 proquint.py encode 7f000001
lusab-babad

$ echo -n "\x7f\x00\x00\x01" | python3 proquint.py encode -
lusab-babad

$ python3 proquint.py decode lusab-babad | xxd -p
7f000001

$ echo -n "lusab-babad" | python3 proquint.py decode - | xxd -p
7f000001
```

## Library Usage

```python-repl
>>> from proquint import Proquint

>>> Proquint.encode(bytes.fromhex("7f000001"))
'lusab-babad'

>>> Proquint.decode("lusab-babad")
b'\x7f\x00\x00\x01'

>>> Proquint.encode_uint16(0x7f00)
'lusab'

>>> Proquint.decode_uint16("babad")
1
```

It is also possible to use another encoding scheme or other alphabets, using the following interface:

```python-repl
>>> Proquint.ALPHABET
{'C': ('bdfghjklmnprstvz', 4), 'V': ('aiou', 2)}

>>> Proquint.CONSTRUCTION
'CVCVC'
```

The keys of `Proquint.ALPHABET` are those used in `Proquint.CONSTRUCTION`, and the values are tuples containing the alphabet and the length of bits that are encoded using a symbol of the alphabets.

## Installation

It's possible to use `pip` to install this library. Example to install `proquint` inside a python virtual environment:

```shell
$ python3 -m venv /tmp/venv

$ source /tmp/venv/bin/activate

$ pip install .
Processing /code/proquint
  Preparing metadata (setup.py) ... done
Installing collected packages: Proquint
  Running setup.py install for Proquint ... done
Successfully installed Proquint-1.0
```

