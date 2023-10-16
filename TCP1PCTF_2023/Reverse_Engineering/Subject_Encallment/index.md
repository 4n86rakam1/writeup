# Subject Encallment

## Description

> If there's something strange. In your neighborhood. Who you gonna call?
>
> Attachment: chall

## Flag

TCP1P{here_my_number_so_call_me_maybe}

## Solution

Running `chall` binary with gdb, set breakpoint main+34, change RIP to jump `printFlag` function.

```asm
0000000000001ba5 <printFlag>:
    1ba5:       55                      push   rbp
    1ba6:       48 89 e5                mov    rbp,rsp
    1ba9:       48 81 ec b0 00 00 00    sub    rsp,0xb0
(snip)

00000000000011a9 <secretFunction>:
    11a9:       55                      push   rbp
    11aa:       48 89 e5                mov    rbp,rsp
    11ad:       48 83 ec 10             sub    rsp,0x10
(snip)

0000000000001e22 <main>:
    1e22:       55                      push   rbp
    1e23:       48 89 e5                mov    rbp,rsp
    1e26:       48 8d 05 73 05 00 00    lea    rax,[rip+0x573]        # 23a0 <_IO_stdin_used+0x3a0>
    1e2d:       48 89 c7                mov    rdi,rax
    1e30:       e8 0b f2 ff ff          call   1040 <puts@plt>
    1e35:       bf 02 00 00 00          mov    edi,0x2
    1e3a:       e8 51 f2 ff ff          call   1090 <sleep@plt>
    1e3f:       b8 00 00 00 00          mov    eax,0x0
    1e44:       e8 60 f3 ff ff          call   11a9 <secretFunction>
    1e49:       bf 02 00 00 00          mov    edi,0x2
    1e4e:       e8 3d f2 ff ff          call   1090 <sleep@plt>
    1e53:       b8 00 00 00 00          mov    eax,0x0
    1e58:       5d                      pop    rbp
    1e59:       c3                      ret
```

input in gdb:

```text
disas main
b *main+34
r
tele 0x555555555ba5
set $rip=0x555555555ba5
c
```

```gdb
gdb-peda$ c
Continuing.
TCP1P{here_my_number_so_call_me_maybe}

Program received signal SIGSEGV, Segmentation fault.
[----------------------------------registers-----------------------------------]
RAX: 0x1
RBX: 0x7fffffffdd58 --> 0x7fffffffe10e ("/root/ctf/TCP1PCTF_2023/rev/Subject_Encallment/chall")
RCX: 0x7ffff7eb8b00 (<__GI___libc_write+16>:    cmp    rax,0xfffffffffffff000)
RDX: 0x0
RSI: 0x5555555592a0 ("TCP1P{here_my_number_so_call_me_maybe}\n")
RDI: 0x7ffff7f96a30 --> 0x0
RBP: 0x7fffffffdc40 --> 0x1
RSP: 0x7fffffffdc48 --> 0x7ffff7de86ca (<__libc_start_call_main+122>:   mov    edi,eax)
RIP: 0x1
R8 : 0x400
R9 : 0x410
R10: 0x7ffff7dcedc8 --> 0x10001200003292
R11: 0x202
R12: 0x0
R13: 0x7fffffffdd68 --> 0x7fffffffe143 ("COLORFGBG=15;0")
R14: 0x555555557dd8 --> 0x555555555160 (<__do_global_dtors_aux>:        endbr64)
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2d0 --> 0x555555554000 --> 0x10102464c457f
EFLAGS: 0x10202 (carry parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
Invalid $PC address: 0x1
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdc48 --> 0x7ffff7de86ca (<__libc_start_call_main+122>:  mov    edi,eax)
0008| 0x7fffffffdc50 --> 0x7fffffffdd40 --> 0x7fffffffdd48 --> 0x7ffff7fc3160 --> 0x7ffff7dc1000 --> 0x3010102464c457f
0016| 0x7fffffffdc58 --> 0x555555555e22 (<main>:        push   rbp)
0024| 0x7fffffffdc60 --> 0x155554040
0032| 0x7fffffffdc68 --> 0x7fffffffdd58 --> 0x7fffffffe10e ("/root/ctf/TCP1PCTF_2023/rev/Subject_Encallment/chall")
0040| 0x7fffffffdc70 --> 0x7fffffffdd58 --> 0x7fffffffe10e ("/root/ctf/TCP1PCTF_2023/rev/Subject_Encallment/chall")
0048| 0x7fffffffdc78 --> 0x50c157b89c9dbf5
0056| 0x7fffffffdc80 --> 0x0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x0000000000000001 in ?? ()
gdb-peda$
```
