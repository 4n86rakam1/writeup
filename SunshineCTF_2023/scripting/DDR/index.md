# DDR

## Description

> All the cool robots are playing Digital Dance Robots, a new rythmn game that... has absolutely no sound! Robots are just that good at these games... until they crash because they can't count to 256. Can you beat the high score and earn a prize?
>
> nc chal.2023.sunshinectf.games 23200

## Flag

sun{d0_r0b0t5_kn0w_h0w_t0_d4nc3}

## Solution

```console
root@kali:~/ctf/SunshineCTF_2023/scripting/DDR# nc chal.2023.sunshinectf.games 23200
Welcome to DIGITAL DANCE ROBOTS!

       -- INSTRUCTIONS --
 Use the WASD keys to input the
 arrow that shows up on screen.
 If you beat the high score of
     255, you win a FLAG!

   -- Press ENTER To Start --


⇧⇦⇨⇨⇧⇨⇩⇦⇨⇩⇦⇦⇧⇦⇨⇦⇨⇦⇩⇩⇧⇧⇩⇩⇩⇩⇩⇧⇧⇦⇩⇦⇨⇧⇧⇧⇦⇧⇦⇨⇨⇧⇨⇩⇨⇦⇩⇧⇩⇨
You lose... better luck next time!
Score: 1
```

Connecting to the host with netcat (`nc`), I receive some arrow.
e.g. `⇧⇦⇨⇨⇧⇨⇩⇦⇨⇩⇦⇦⇧⇦⇨⇦⇨⇦⇩⇩⇧⇧⇩⇩⇩⇩⇩⇧⇧⇦⇩⇦⇨⇧⇧⇧⇦⇧⇦⇨⇨⇧⇨⇩⇨⇦⇩⇧⇩⇨`.

So I send request which replaces `WASD` e.g. `⇧` to `W` and `⇦` to `A`, etc... .
And repeat it 255 times.

solver-ddr.py

```python
from pwn import *

io = remote("chal.2023.sunshinectf.games", 23200)

io.sendlineafter(b"-- Press ENTER To Start --", b"")

io.recvline()
io.recvline()

mapping = {ord("⇦"): b"A", ord("⇧"): b"W", ord("⇨"): b"D", ord("⇩"): b"S"}


def ddr():
    ddr_recv = io.recvlineS()
    log.debug(ddr_recv)

    payload = b""
    for c in ddr_recv:
        if c in ["\r", "\n"]:
            continue

        payload += mapping[ord(c)]

    log.debug(payload.decode())

    io.sendline(payload)


for i in range(255):
    print(f"{i}", end="\r", flush=True)
    ddr()

log.info(io.recvallS())
```

```console
root@kali:~/ctf/SunshineCTF_2023/scripting/DDR# python3 solver-ddr.py
[+] Opening connection to chal.2023.sunshinectf.games on port 23200: Done
[+] Receiving all data: Done (61B)
[*] Closed connection to chal.2023.sunshinectf.games port 23200
[*]
    YOU WIN!!!
    Your prize is sun{d0_r0b0t5_kn0w_h0w_t0_d4nc3}
```
