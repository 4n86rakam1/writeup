# Skribl

## Description

> The modern paste service for the New World.
>
> <https://skribl.chall.pwnoh.io>
>
> Downloads: dist.zip

## Flag

bctf{wHy_d0_w3_Ne3d_s0_m@ny_N0T3$_aNyW@y}

## solver.py

```python
import math
import re
import random
import string
from datetime import datetime, timezone

import requests


def generate_seed():
    resp = requests.get(
        "https://skribl.chall.pwnoh.io/",
    )

    pattern = r"stime = moment.duration\(([0-9]+), 'seconds'\)"
    duration = re.findall(pattern, resp.text)[0]
    duration = int(duration)

    created_datetime = math.floor((datetime.now().timestamp() - duration))

    # or I can calculate as considering the timezone from 'Date' response header
    # current_datetime = datetime.strptime(
    #     resp.headers["Date"], "%a, %d %b %Y %H:%M:%S %Z"
    # ).timestamp()
    # created_datetime = math.floor((current_datetime - duration)) + (60 * 60 * 9)

    return created_datetime


def create_key(seed):
    random.seed(seed)

    alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return "".join([random.choice(alphabet) for i in range(40)])


def main():
    created_datetime = generate_seed()

    for i in range(-1, 2):
        key = create_key(created_datetime + i)
        print(f"{key=}")

        resp = requests.get(
            f"https://skribl.chall.pwnoh.io/view/{key}",
        )
        if len((m := re.findall(r"bctf{.*}", resp.text))) != 0:
            print("flag found.")
            print(m[0])
            return


if __name__ == "__main__":
    main()
```

```console
root@kali:~/ctf/buckeyectf-2023/rev/Skribl# python3 solver-skribl.py
key='CYf2HTsftHWx3cG1k9Evi9hlphHdWvBv9DqLwUsp'
key='fXwza3Jls7pmhYNQ1U72ZFNU8AOvJAiyg4MZI9Mq'
key='n8ukS9mypdZ2mtxZj9Vq81nEqtzYmXsF00GSlqJV'
flag found.
bctf{wHy_d0_w3_Ne3d_s0_m@ny_N0T3$_aNyW@y}
```

## Solution

provided stuff:

```console
root@kali:~/ctf/buckeyectf-2023/rev/Skribl# unzip -q dist.zip

root@kali:~/ctf/buckeyectf-2023/rev/Skribl# tree dist
dist
├── chal
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── backend.cpython-313.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   └── skribl.cpython-313.pyc
│   ├── setup.py
│   ├── skribl.py
│   └── templates
│       ├── about.html
│       ├── base.html
│       ├── index.html
│       └── view.html
└── Dockerfile

4 directories, 11 files

root@kali:~/ctf/buckeyectf-2023/rev/Skribl# pyenv global 3.13-dev
```

dist/Dockerfile:

```dockerfile
(snip)
ENV FLAG "bctf{fAk3_f1@g}"
(snip)
```

Flag is set to enviornment variable, however, it is not used in any Python code.

Since backend.py is not included in dist.zip, compile `__pycache__/backend.cpython-313.pyc` to see the process in backend.py.

I see `__pycache__/backend.cpython-313.pyc` was generated with Python 3.13 since it's staretd from `eb 0d 0d 0a`,

```console
root@kali:~/ctf/buckeyectf-2023/rev/Skribl# hexdump -C -n 4 dist/chal/__pycache__/backend.cpython-313.pyc
00000000  eb 0d 0d 0a                                       |....|
00000004

root@kali:~/ctf/buckeyectf-2023/rev/Skribl# python3 -V
Python 3.13.0a0

root@kali:~/ctf/buckeyectf-2023/rev/Skribl# touch test.py; python3 -m py_compile test.py; hexdump -C -n 4 __pycache__/test.cpython-313.pyc
00000000  eb 0d 0d 0a                                       |....|
00000004
```

Install Python 3.13-dev and I can decompile by using [`show_pyc.py`](https://github.com/nedbat/coveragepy/blob/coverage-5.6b1/lab/show_pyc.py) in the coveragepy repository.

<details><summary>decompile with coveragepy in Python 3.13-dev</summary>

[coveragepy/lab/show_pyc.py at coverage-5.6b1 · nedbat/coveragepy](https://github.com/nedbat/coveragepy/blob/coverage-5.6b1/lab/show_pyc.py)

```console
root@kali:~/ctf/buckeyectf-2023/rev/Skribl# git clone https://github.com/nedbat/coveragepy.git && cd coveragepy
(snip)
root@kali:~/ctf/buckeyectf-2023/rev/Skribl/coveragepy# git checkout coverage-5.6b1
(snip)
root@kali:~/ctf/buckeyectf-2023/rev/Skribl/coveragepy# python3 lab/show_pyc.py ../dist/chal/__pycache__/backend.cpython-313.pyc
magic b'eb0d0d0a'
flags 0x00000000
moddate b'76a31365' (Wed Sep 27 12:37:26 2023)
pysize b'f6010000' (502)
code
    name '<module>'
    argcount 0
    nlocals 0
    stacksize 2
    flags 0000:
    code
       9500530053014b007200530053014b017201530053014b02720253005301
       4b037203530053014b04720453025c05340253031a006a04720653041a00
       72076701
  0           0 RESUME                   0

  1           2 LOAD_CONST               0 (0)
              4 LOAD_CONST               1 (None)
              6 IMPORT_NAME              0 (string)
              8 STORE_NAME               0 (string)

  2          10 LOAD_CONST               0 (0)
             12 LOAD_CONST               1 (None)
             14 IMPORT_NAME              1 (random)
             16 STORE_NAME               1 (random)

  3          18 LOAD_CONST               0 (0)
             20 LOAD_CONST               1 (None)
             22 IMPORT_NAME              2 (time)
             24 STORE_NAME               2 (time)

  4          26 LOAD_CONST               0 (0)
             28 LOAD_CONST               1 (None)
             30 IMPORT_NAME              3 (math)
             32 STORE_NAME               3 (math)

  5          34 LOAD_CONST               0 (0)
             36 LOAD_CONST               1 (None)
             38 IMPORT_NAME              4 (os)
             40 STORE_NAME               4 (os)

  8          42 LOAD_CONST               2 ('return')
             44 LOAD_NAME                5 (str)
             46 BUILD_TUPLE              2
             48 LOAD_CONST               3 (<code object create_skribl at 0x7f8ed37aa3d0, file "/home/rene/Documents/Java/OSUCyberSecurityClub/buckeyectf23/buckeyectf-challenges/chals/rev-pycache/dist/chal/backend.py", line 8>)
             50 MAKE_FUNCTION
             52 SET_FUNCTION_ATTRIBUTE   4 (annotations)
             54 STORE_NAME               6 (create_skribl)

 18          56 LOAD_CONST               4 (<code object init_backend at 0x7f8ed33368d0, file "/home/rene/Documents/Java/OSUCyberSecurityClub/buckeyectf23/buckeyectf-challenges/chals/rev-pycache/dist/chal/backend.py", line 18>)
             58 MAKE_FUNCTION
             60 STORE_NAME               7 (init_backend)
             62 RETURN_CONST             1 (None)
    consts
        0: 0
        1: None
        2: 'return'
        3: code
            name 'create_skribl'
            argcount 3
            nlocals 7
            stacksize 6
            flags 0003: CO_OPTIMIZED, CO_NEWLOCALS
            code
               95005b010000000000000000530155010e00330235010000000000002000
               5b0200000000000000005204000000000000000000000000000000000000
               5b0200000000000000005206000000000000000000000000000000000000
               2d0000005b02000000000000000052080000000000000000000000000000
               000000002d0000006e035b0b000000000000000053023501000000000000
               1300560473022f007302481900006e045b0c0000000000000000520e0000
               000000000000000000000000000000002200550335010000000000005002
               4d1b00000b006e056e045303521100000000000000000000000000000000
               0000550535010000000000006e0658123402580627000000550624007302
               200073026e046600
   8           0 RESUME                   0

   9           2 LOAD_GLOBAL              1 (print + NULL)
              12 LOAD_CONST               1 ('Creating skribl ')
              14 LOAD_FAST                1 (message)
              16 FORMAT_SIMPLE
              18 BUILD_STRING             2
              20 CALL                     1
              28 POP_TOP

  11          30 LOAD_GLOBAL              2 (string)
              40 LOAD_ATTR                4 (ascii_lowercase)
              60 LOAD_GLOBAL              2 (string)
              70 LOAD_ATTR                6 (ascii_uppercase)
              90 BINARY_OP                0 (+)
              94 LOAD_GLOBAL              2 (string)
             104 LOAD_ATTR                8 (digits)
             124 BINARY_OP                0 (+)
             128 STORE_FAST               3 (alphabet)

  12         130 LOAD_GLOBAL             11 (range + NULL)
             140 LOAD_CONST               2 (40)
             142 CALL                     1
             150 GET_ITER
             152 LOAD_FAST_AND_CLEAR      4 (i)
             154 SWAP                     2
             156 BUILD_LIST               0
             158 SWAP                     2
         >>  160 FOR_ITER                25 (to 214)
             164 STORE_FAST               4 (i)
             166 LOAD_GLOBAL             12 (random)
             176 LOAD_ATTR               14 (choice)
             196 PUSH_NULL
             198 LOAD_FAST                3 (alphabet)
             200 CALL                     1
             208 LIST_APPEND              2
             210 JUMP_BACKWARD           27 (to 160)
         >>  214 END_FOR
             216 STORE_FAST               5 (key_list)
             218 STORE_FAST               4 (i)

  14         220 LOAD_CONST               3 ('')
             222 LOAD_ATTR               17 (join + NULL|self)
             242 LOAD_FAST                5 (key_list)
             244 CALL                     1
             252 STORE_FAST               6 (key)

  15         254 LOAD_FAST_LOAD_FAST     18 (message, author)
             256 BUILD_TUPLE              2
             258 LOAD_FAST_LOAD_FAST      6 (skribls, key)
             260 STORE_SUBSCR

  16         264 LOAD_FAST                6 (key)
             266 RETURN_VALUE

None     >>  268 SWAP                     2
             270 POP_TOP

  12         272 SWAP                     2
             274 STORE_FAST               4 (i)
             276 RERAISE                  0
ExceptionTable:
  156 to 214 -> 268 [2]
            consts
                0: None
                1: 'Creating skribl '
                2: 40
                3: ''
            names ('print', 'string', 'ascii_lowercase', 'ascii_uppercase', 'digits', 'range', 'random', 'choice', 'join')
            varnames ('skribls', 'message', 'author', 'alphabet', 'i', 'key_list', 'key')
            freevars ()
            cellvars ()
            filename '/home/rene/Documents/Java/OSUCyberSecurityClub/buckeyectf23/buckeyectf-challenges/chals/rev-pycache/dist/chal/backend.py'
            firstlineno 8
/root/ctf/buckeyectf-2023/rev/Skribl/coveragepy/lab/show_pyc.py:116: DeprecationWarning: co_lnotab is deprecated, use co_lines instead.
  show_hex("lnotab", code.co_lnotab, indent=indent)
            lnotab 02011c0264015a0222010a0108fc
/root/ctf/buckeyectf-2023/rev/Skribl/coveragepy/lab/show_pyc.py:145: DeprecationWarning: co_lnotab is deprecated, use co_lines instead.
  byte_increments = bytes_to_ints(code.co_lnotab[0::2])
/root/ctf/buckeyectf-2023/rev/Skribl/coveragepy/lab/show_pyc.py:146: DeprecationWarning: co_lnotab is deprecated, use co_lines instead.
  line_increments = bytes_to_ints(code.co_lnotab[1::2])
                8:0, 9:2, 11:30, 12:130, 14:220, 15:254, 16:264, 12:272
            linetable
               8000dc0409d00c1c98579849d00a26d40427e40f15d70f25d10f25ac06d7
               283ed1283ed10f3ec416c71dc11dd10f4e8048dc3136b072b319d60f3ba8
               419406970d920d9868d61027d00f3b8048d00f3be00a0c8f2789279028d3
               0a1b8043d8141bd013248047814cd80b0e804af9f20900103c
                co_lines 8:0-2, 9:2-30, 11:30-130, 12:130-220, 14:220-254, 15:254-264, 16:264-268, None:268-272, 12:272-278
        4: code
            name 'init_backend'
            argcount 1
            nlocals 1
            stacksize 6
            flags 0003: CO_OPTIMIZED, CO_NEWLOCALS
            code
               95005b000000000000000000520200000000000000000000000000000000
               000022005b04000000000000000052060000000000000000000000000000
               0000000022005b0800000000000000005208000000000000000000000000
               000000000000220035000000000000003501000000000000350100000000
               000020005b0b000000000000000055005b0c0000000000000000520e0000
               000000000000000000000000000000005301050000005302350300000000
               000020006700
 18           0 RESUME                   0

 19           2 LOAD_GLOBAL              0 (random)
             12 LOAD_ATTR                2 (seed)
             32 PUSH_NULL
             34 LOAD_GLOBAL              4 (math)
             44 LOAD_ATTR                6 (floor)
             64 PUSH_NULL
             66 LOAD_GLOBAL              8 (time)
             76 LOAD_ATTR                8 (time)
             96 PUSH_NULL
             98 CALL                     0
            106 CALL                     1
            114 CALL                     1
            122 POP_TOP

 21         124 LOAD_GLOBAL             11 (create_skribl + NULL)
            134 LOAD_FAST                0 (skribls)
            136 LOAD_GLOBAL             12 (os)
            146 LOAD_ATTR               14 (environ)
            166 LOAD_CONST               1 ('FLAG')
            168 BINARY_SUBSCR
            172 LOAD_CONST               2 ('rene')
            174 CALL                     3
            182 POP_TOP
            184 RETURN_CONST             0 (None)
            consts
                0: None
                1: 'FLAG'
                2: 'rene'
            names ('random', 'seed', 'math', 'floor', 'time', 'create_skribl', 'os', 'environ')
            varnames ('skribls',)
            freevars ()
            cellvars ()
            filename '/home/rene/Documents/Java/OSUCyberSecurityClub/buckeyectf23/buckeyectf-challenges/chals/rev-pycache/dist/chal/backend.py'
            firstlineno 18
            lnotab 02017a02
                18:0, 19:2, 21:124
            linetable
               8000dc040a874b824b9404970a920a9c349f399a399b3bd31027d40428e4
               041190279c329f3a993aa066d11b2da876d50436
                co_lines 18:0-2, 19:2-124, 21:124-186
    names ('string', 'random', 'time', 'math', 'os', 'str', 'create_skribl', 'init_backend')
    varnames ()
    freevars ()
    cellvars ()
    filename '/home/rene/Documents/Java/OSUCyberSecurityClub/buckeyectf23/buckeyectf-challenges/chals/rev-pycache/dist/chal/backend.py'
    firstlineno 1
    lnotab 00ff0201080108010801080108030e0a
        0:0, 1:2, 2:10, 3:18, 4:26, 5:34, 8:42, 18:56
    linetable
       f003010101db000ddb000ddb000bdb000bdb0009f00608010fa873f40008
       010ff314030137
        co_lines 0:0-2, 1:2-10, 2:10-18, 3:18-26, 4:26-34, 5:34-42, 8:42-56, 18:56-64
```

</details>

backend.py processing:

- `create_skribl` function: generate key

  ```python
  alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits
  key = "".join([random.choice(alphabet) for i in range(40)])
  ```

- `init_backend` function:
  - `random.seed(math.floor(time.time()))`: the server startup datetime is used as seed
  - I guess there is dictionary `{key: [os.environ['FLAG'], 'rene'}`

I can calculate the server startup datetime from `stime = moment.duration(11606, 'seconds');` in <https://skribl.chall.pwnoh.io/>:

```html
   <script>
        stime = moment.duration(11606, 'seconds');
        stime_text = document.getElementById("stime");

        stime_text.outerHTML = stime.humanize()
    </script>
```

![skribl-server-start.png](./img/skribl-server-start.png )

Thus, I can retrieve the flag by determining the server startup datetime, implementing a Python script that does the same thing, generating and accessing the key.

## Refenrences

- [The structure of .pyc files \| Ned Batchelder](https://nedbatchelder.com/blog/200804/the_structure_of_pyc_files.html)
- [nedbat/coveragepy: The code coverage tool for Python](https://github.com/nedbat/coveragepy/tree/master)
