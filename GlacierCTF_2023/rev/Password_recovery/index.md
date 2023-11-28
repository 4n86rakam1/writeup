# Password recovery [264 Solves]

## Description

> Our infra admin "LosCapitan" stores all of his passwords in a self-hosted password manager. Shortly before the CTF, he forgot his password and now he can't access his passwords anymore. The keys to the underlying server are stored in the password manager as well. Luckily, he never changed his password and we still have the old password checker for one of our servers. Can you help us recover his password for the "LosCapitan" user? Wrap the correct password in gctf{}. Flag format is gctf{.*}.
>
> author: Xer0
>
> Attachments: app

## Flag

gctf{]^WR\\lcTI}

## Solution

```gdb
gdb-peda$ b *main+590
Breakpoint 1 at 0x1494
gdb-peda$ r
Starting program: /root/ctf/GlacierCTF_2023/rev/Password recovery/app
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Enter your name: LosCapitan
Enter your password: AAAA
[----------------------------------registers-----------------------------------]
RAX: 0x7fffffffdba0 ("]^WR\\\\lcTI")
RBX: 0x272c8fe355ddd8e8
RCX: 0x149
RDX: 0x7fffffffdbe0 --> 0x41414141 ('AAAA')
RSI: 0x7fffffffdbe0 --> 0x41414141 ('AAAA')
RDI: 0x7fffffffdba0 ("]^WR\\\\lcTI")
RBP: 0x7fffffffdc30 --> 0x1
RSP: 0x7fffffffdb70 --> 0xc00000
RIP: 0x555555555494 (<main+590>:        call   0x5555555550e0 <strcmp@plt>)
R8 : 0x5
R9 : 0x7ffff7f91aa0 --> 0xfbad2288
R10: 0x0
R11: 0x7ffff7f92580 --> 0x7ffff7f8e820 --> 0x7ffff7f555f7 --> 0x5a5400544d470043 ('C')
R12: 0x0
R13: 0x7fffffffdd58 --> 0x7fffffffe12e ("COLORFGBG=15;0")
R14: 0x555555557d98 --> 0x5555555551a0 (<__do_global_dtors_aux>:        endbr64)
R15: 0x7ffff7ffd000 --> 0x7ffff7ffe2d0 --> 0x555555554000 --> 0x10102464c457f
EFLAGS: 0x246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x555555555487 <main+577>:   lea    rax,[rbp-0x90]
   0x55555555548e <main+584>:   mov    rsi,rdx
   0x555555555491 <main+587>:   mov    rdi,rax
=> 0x555555555494 <main+590>:   call   0x5555555550e0 <strcmp@plt>
   0x555555555499 <main+595>:   test   eax,eax
   0x55555555549b <main+597>:   jne    0x5555555554ae <main+616>
   0x55555555549d <main+599>:   lea    rax,[rip+0xb8b]        # 0x55555555602f
   0x5555555554a4 <main+606>:   mov    rdi,rax
Guessed arguments:
arg[0]: 0x7fffffffdba0 ("]^WR\\\\lcTI")
arg[1]: 0x7fffffffdbe0 --> 0x41414141 ('AAAA')
arg[2]: 0x7fffffffdbe0 --> 0x41414141 ('AAAA')
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffdb70 --> 0xc00000
0008| 0x7fffffffdb78 --> 0x6100000000c00000
0016| 0x7fffffffdb80 --> 0xa ('\n')
0024| 0x7fffffffdb88 --> 0xa ('\n')
0032| 0x7fffffffdb90 --> 0x555555558019 --> 0x1337deadbeefc0
0040| 0x7fffffffdb98 --> 0x2
0048| 0x7fffffffdba0 ("]^WR\\\\lcTI")
0056| 0x7fffffffdba8 --> 0x4954 ('TI')
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
```


- name: LosCapitan
- password: `]^WR\\lcTI`

```console
$ ./app
Enter your name: LosCapitan
Enter your password: ]^WR\\lcTI
Valid!
```

Therefore, the flag is `gctf{]^WR\\lcTI}`.
