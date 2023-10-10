# Dill

## Description

> Originally this was going to be about pickles, but .pyc sounds close enough to "pickles" so I decided to make it about that instead.
>
> Attachment: dill.cpython-38.pyc

## Flag

sun{ZGlsbGxpa2V0aGVwaWNrbGVnZXRpdD8K}

## Solution

Using [rocky/python-uncompyle6](https://github.com/rocky/python-uncompyle6/) to decompile pyc file in Python3.8 environment.


```bash
pyenv global 3.8
pip install uncompyle6
uncompyle6 dill.cpython-38.pyc
```

output:

```python
# uncompyle6 version 3.9.0
# Python bytecode version base 3.8.0 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 19 2023, 16:01:55)
# [GCC 13.1.0]
# Embedded file name: dill.py
# Compiled at: 2023-10-07 04:53:54
# Size of source mod 2**32: 914 bytes


class Dill:
    prefix = 'sun{'
    suffix = '}'
    o = [5, 1, 3, 4, 7, 2, 6, 0]

    def __init__(self) -> None:
        self.encrypted = 'bGVnbGxpaGVwaWNrdD8Ka2V0ZXRpZGls'

    def validate(self, value: str) -> bool:
        return value.startswith(Dill.prefix) and value.endswith(Dill.suffix) or False
        value = value[len(Dill.prefix):-len(Dill.suffix)]
        if len(value) != 32:
            return False
        c = [value[i:i + 4] for i in range(0, len(value), 4)]
        value = ''.join([c[i] for i in Dill.o])
        if value != self.encrypted:
            return False
        return True
# okay decompiling dill.cpython-38.pyc
```

Doing the reverse of `validate` method.

solver.py

```python
def decrypt():
    o = [5, 1, 3, 4, 7, 2, 6, 0]
    encrypted = "bGVnbGxpaGVwaWNrdD8Ka2V0ZXRpZGls"

    decrypted = [_ for _ in range(len(o))]

    for i, o_i in enumerate(o):
        decrypted[o_i] = encrypted[i * 4 : i * 4 + 4]

    return "".join(decrypted)


print("sun{" + decrypt() + "}")
# => sun{ZGlsbGxpa2V0aGVwaWNrbGVnZXRpdD8K}
```
