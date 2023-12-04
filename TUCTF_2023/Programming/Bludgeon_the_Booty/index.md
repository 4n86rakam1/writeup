# Bludgeon the Booty [173 Solves]

## Description

> You have found me treasure chest, but can you crack its code?
>
> ```text
>   ___________
>  /           \
> /__|0|0|0|0|__\
> |      @      |
> |_____________|
> ```
>
> "This here lock be cursed by the shaman of the swamp to change keys for each attempt"
>
> `nc chal.tuctf.com 30002`

## Flag

TUCTF{h3R3_1!3_M3_800Ty}

## Solution

```console
$ nc chal.tuctf.com 30002
  ___________
 /           \
/___|0|0|0|___\
|      @      |
|_____________|
Enter 1 to rotate the lock, or 2 to exit
1
Which wheel would you like to rotate? (1-3)
1
Which direction would you like to rotate the wheel? (+/-)
+
  ___________
 /           \
/___|1|0|0|___\
|      @      |
|_____________|
The chest is still locked!
Enter 1 to rotate the lock, or 2 to exit
1
Which wheel would you like to rotate? (1-3)
2
Which direction would you like to rotate the wheel? (+/-)
+
  ___________
 /           \
/___|1|1|0|___\
|      @      |
|_____________|
The chest is still locked!
Enter 1 to rotate the lock, or 2 to exit
...
```

Try from 000 to 999.

```python
# solver.py
from pwn import remote, context, log

context.log_level = "ERROR"

io = remote("chal.tuctf.com", 30002)

"""
  ___________
 /           \
/___|1|2|3|___\
|      @      |
|_____________|

digit order:
1st | 2nd | 3rd
"""


def rotate(digit):
    io.sendlineafter(b"or 2 to exit", b"1")
    io.sendlineafter(b"rotate? (1-3)", digit.encode())
    io.sendlineafter(b"(+/-)", b"+")

    [io.recvline() for _ in range(6)]
    res = io.recvlineS()

    if "The chest is still locked!" not in res:
        io.interactive()


def main():
    for i in range(1, 1000):
        rotate("1")

        # 2nd digit
        if i % 10 == 0:
            rotate("2")

        # 3rd digit
        if i % 10 == 0 and i % 100 == 0:
            rotate("3")


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py
[+] Opening connection to chal.tuctf.com on port 30002: Done[
[*] The chest is still locked!
(snip)
[*] The chest is still locked!
[*] You have unlocked the treasure chest!
[*] Switching to interactive mode
You have found the Flag!
--------------------------\
|   .        .             \
|    .  . .     .           \
|                  X         |
>                            |
|  TUCTF{h3R3_1!3_M3_800Ty}  |
|                            |
>                            <
|                            |
-----^-----------------^------
[*] Got EOF while reading in interactive
$
```
