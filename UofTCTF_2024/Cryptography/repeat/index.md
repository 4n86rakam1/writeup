# repeat [317 Solves]

## Description

> I'm a known repeat offender when it comes to bad encryption habits. But the secrets module is secure, so you'll never be able to guess my key!
>
> Author: SteakEnthusiast
>
> Attachments: flag.enc, gen.py

## Source Code

flag.enc

```text
Flag: 982a9290d6d4bf88957586bbdcda8681de33c796c691bb9fde1a83d582c886988375838aead0e8c7dc2bc3d7cd97a4 
```

gen.py

```python
import os
import secrets

flag = "REDACATED"
xor_key = secrets.token_bytes(8)

def xor(message, key):
    return bytes([message[i] ^ key[i % len(key)] for i in range(len(message))])

encrypted_flag = xor(flag.encode(), xor_key).hex()

with open("flag.enc", "w") as f:
    f.write("Flag: "+encrypted_flag)
```

## Solution

The flag in flag.enc is encrypted XOR encryption by 8 length XOR key.
The flag format is starting with `uoftctf{` and this is 8 length.
I calculate XOR key by first 8 bytes and decrypt it.

```python
from pwn import xor, unhex

with open("flag.enc", "rb") as f:
    f.read(6)
    encrypted = unhex(f.read())

xor_key = xor(encrypted[0:8], b"uoftctf{")
print(xor(encrypted, xor_key))
```

Result:

```console
$ python3 solver.py
b'uoftctf{x0r_iz_r3v3rs1bl3_w17h_kn0wn_p141n73x7}'
```

## Flag

uoftctf{x0r_iz_r3v3rs1bl3_w17h_kn0wn_p141n73x7}
