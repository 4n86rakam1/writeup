# rebug 2
## Flag

csawctf{01011100010001110000}

## Solution

execute gdb and set breakpoint, run.

```
b *printbinchar+117
r
```


```gdb
gdb-peda$ c
Continuing.
[----------------------------------registers-----------------------------------]
RAX: 0x0
RBX: 0x7fffffffdd78 --> 0x7fffffffe120 ("/root/ctf/CSAW-CTF-2023-Quals/rev/rebug 2/bin.out")
RCX: 0x7
RDX: 0x555555558030 ("01011100010001110000")
RSI: 0x28 ('(')
RDI: 0x7fffffffdc00 --> 0x100000000
RBP: 0x7fffffffdc30 --> 0x7fffffffdc60 --> 0x1
RSP: 0x7fffffffdbf0 --> 0x10
RIP: 0x5555555552a1 (<printbinchar+117>:        nop)
R8 : 0x400
R9 : 0x410
R10: 0x1000
R11: 0x3f ('?')
R12: 0x0
R13: 0x7fffffffdd88 --> 0x7fffffffe152 ("COLORFGBG=15;0")
R14: 0x555555557dd8 --> 0x5555555550f0 (<__do_global_dtors_aux>:        endbr64)
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2c0 --> 0x555555554000 --> 0x10102464c457f
EFLAGS: 0x202 (carry parity adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x555555555295 <printbinchar+105>:   lea    rax,[rbp-0x30]
   0x555555555299 <printbinchar+109>:   mov    rdi,rax
   0x55555555529c <printbinchar+112>:   call   0x555555555139 <xoring>
=> 0x5555555552a1 <printbinchar+117>:   nop
   0x5555555552a2 <printbinchar+118>:   leave
   0x5555555552a3 <printbinchar+119>:   ret
   0x5555555552a4 <main>:       push   rbp
   0x5555555552a5 <main+1>:     mov    rbp,rsp
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdbf0 --> 0x10
0008| 0x7fffffffdbf8 --> 0x7700000040 ('@')
0016| 0x7fffffffdc00 --> 0x100000000
0024| 0x7fffffffdc08 --> 0x100000001
0032| 0x7fffffffdc10 --> 0x100000000
0040| 0x7fffffffdc18 --> 0x100000001
0048| 0x7fffffffdc20 --> 0x1ffffdd78
0056| 0x7fffffffdc28 --> 0x877ffe2c0
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x00005555555552a1 in printbinchar ()
```
