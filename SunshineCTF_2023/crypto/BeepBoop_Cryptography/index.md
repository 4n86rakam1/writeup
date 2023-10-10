# BeepBoop Cryptography

## Description

> **Help! My IOT device has gone sentient!**
>
> All I wanted to know was the meaning of 42!
>
> It's also waving its arms up and down, and I...
>
> oh no! It's free!
>
> AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
>
> **Automated Challenge Instructions**
>
> Detected failure in challenge upload. Original author terminated. Please see attached file BeepBoop for your flag... human.
>
> Attachment: BeepBoop

## Flag

sun{exterminate-exterminate-exterminate}

## Solution

solver.py

```python
import codecs

with open("BeepBoop", "r") as f:
    data = f.read()

bin_str = data.replace("beep", "0").replace("boop", "1").replace(" ", "")
n = int(bin_str, base=2)
decoded = n.to_bytes((n.bit_length() + 7) // 8, "big").decode()
flag = codecs.encode(decoded, "rot13")

print(flag)
```

```console
root@kali:~/ctf/SunshineCTF_2023/crypto/BeepBoop Cryptography# python3 solver.py

sun{exterminate-exterminate-exterminate}
```
