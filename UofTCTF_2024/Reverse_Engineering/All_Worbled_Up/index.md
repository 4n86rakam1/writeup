# All Worbled Up [86 Solves]

## Description

> last time we had a worbler, it failed miserably and left everyone sad, and no one got their flags.
> now we have another one, maybe it'll work this time?
>
> output:
>
> ```text
>                       _     _             
>                      | |   | |            
>   __      _____  _ __| |__ | | ___ _ __   
>   \ \ /\ / / _ \| '__| '_ \| |/ _ \ '__|  
>    \ V  V / (_) | |  | |_) | |  __/ |     
>     \_/\_/ \___/|_|  |_.__/|_|\___|_|     
>                                           
> ==========================================
> Enter flag: *redacted*
> Here's your flag:  a81c0750d48f0750
> ```
>
> Author: cartoonraccoon
>
> Attachments: worbler

## Source Code

<details><summary>worbler</summary>

```asm
  1           0 RESUME                   0

  2           2 LOAD_CONST               1 (0)
              4 LOAD_CONST               0 (None)
              6 IMPORT_NAME              0 (re)
              8 STORE_FAST               0 (re)

  4          10 LOAD_FAST                0 (re)
             12 LOAD_METHOD              1 (compile)
             34 LOAD_CONST               2 ('^uoftctf\\{([bdrw013]){9}\\}$')
             36 PRECALL                  1
             40 CALL                     1
             50 STORE_FAST               1 (pattern)

  6          52 LOAD_CONST               3 (<code object worble at 0x7fca0cbe0f50, line 6>)
             54 MAKE_FUNCTION            0
             56 STORE_FAST               2 (worble)

 16          58 LOAD_CONST               4 (<code object shmorble at 0x7fca0cbae6f0, line 16>)
             60 MAKE_FUNCTION            0
             62 STORE_FAST               3 (shmorble)

 23          64 LOAD_CONST               5 (<code object blorble at 0x7fca0ca61630, line 23>)
             66 MAKE_FUNCTION            0
             68 STORE_FAST               4 (blorble)

 26          70 LOAD_GLOBAL              5 (NULL + print)
             82 LOAD_CONST               6 ('                      _     _             ')
             84 PRECALL                  1
             88 CALL                     1
             98 POP_TOP

 27         100 LOAD_GLOBAL              5 (NULL + print)
            112 LOAD_CONST               7 ('                     | |   | |            ')
            114 PRECALL                  1
            118 CALL                     1
            128 POP_TOP

 28         130 LOAD_GLOBAL              5 (NULL + print)
            142 LOAD_CONST               8 ('  __      _____  _ __| |__ | | ___ _ __   ')
            144 PRECALL                  1
            148 CALL                     1
            158 POP_TOP

 29         160 LOAD_GLOBAL              5 (NULL + print)
            172 LOAD_CONST               9 ("  \\ \\ /\\ / / _ \\| '__| '_ \\| |/ _ \\ '__|  ")
            174 PRECALL                  1
            178 CALL                     1
            188 POP_TOP

 30         190 LOAD_GLOBAL              5 (NULL + print)
            202 LOAD_CONST              10 ('   \\ V  V / (_) | |  | |_) | |  __/ |     ')
            204 PRECALL                  1
            208 CALL                     1
            218 POP_TOP

 31         220 LOAD_GLOBAL              5 (NULL + print)
            232 LOAD_CONST              11 ('    \\_/\\_/ \\___/|_|  |_.__/|_|\\___|_|     ')
            234 PRECALL                  1
            238 CALL                     1
            248 POP_TOP

 32         250 LOAD_GLOBAL              5 (NULL + print)
            262 LOAD_CONST              12 ('                                          ')
            264 PRECALL                  1
            268 CALL                     1
            278 POP_TOP

 33         280 LOAD_GLOBAL              5 (NULL + print)
            292 LOAD_CONST              13 ('==========================================')
            294 PRECALL                  1
            298 CALL                     1
            308 POP_TOP

 35         310 LOAD_GLOBAL              7 (NULL + input)
            322 LOAD_CONST              14 ('Enter flag: ')
            324 PRECALL                  1
            328 CALL                     1
            338 STORE_FAST               5 (flag)

 36         340 LOAD_FAST                1 (pattern)
            342 LOAD_METHOD              4 (match)
            364 LOAD_FAST                5 (flag)
            366 PRECALL                  1
            370 CALL                     1
            380 POP_JUMP_FORWARD_IF_TRUE    17 (to 416)

 37         382 LOAD_GLOBAL              5 (NULL + print)
            394 LOAD_CONST              15 ('Incorrect format!')
            396 PRECALL                  1
            400 CALL                     1
            410 POP_TOP
            412 LOAD_CONST               0 (None)
            414 RETURN_VALUE

 39     >>  416 PUSH_NULL
            418 LOAD_FAST                2 (worble)
            420 LOAD_FAST                5 (flag)
            422 PRECALL                  1
            426 CALL                     1
            436 STORE_FAST               6 (a)

 40         438 PUSH_NULL
            440 LOAD_FAST                2 (worble)
            442 LOAD_FAST                5 (flag)
            444 LOAD_CONST               0 (None)
            446 LOAD_CONST               0 (None)
            448 LOAD_CONST              16 (-1)
            450 BUILD_SLICE              3
            452 BINARY_SUBSCR
            462 PRECALL                  1
            466 CALL                     1
            476 STORE_FAST               7 (b)

 42         478 LOAD_GLOBAL              5 (NULL + print)
            490 LOAD_CONST              17 ("Here's your flag:")
            492 PUSH_NULL
            494 LOAD_FAST                3 (shmorble)
            496 PUSH_NULL
            498 LOAD_FAST                4 (blorble)
            500 LOAD_FAST                6 (a)
            502 LOAD_FAST                7 (b)
            504 PRECALL                  2
            508 CALL                     2
            518 PRECALL                  1
            522 CALL                     1
            532 PRECALL                  2
            536 CALL                     2
            546 POP_TOP
            548 LOAD_CONST               0 (None)
            550 RETURN_VALUE

Disassembly of <code object worble at 0x7fca0cbe0f50, line 6>:
  6           0 RESUME                   0

  7           2 LOAD_CONST               1 (5)
              4 STORE_FAST               1 (s1)

  8           6 LOAD_CONST               2 (31)
              8 STORE_FAST               2 (s2)

 10          10 LOAD_GLOBAL              1 (NULL + range)
             22 LOAD_GLOBAL              3 (NULL + len)
             34 LOAD_FAST                0 (s)
             36 PRECALL                  1
             40 CALL                     1
             50 PRECALL                  1
             54 CALL                     1
             64 GET_ITER
        >>   66 FOR_ITER                40 (to 148)
             68 STORE_FAST               3 (n)

 11          70 LOAD_FAST                1 (s1)
             72 LOAD_GLOBAL              5 (NULL + ord)
             84 LOAD_FAST                0 (s)
             86 LOAD_FAST                3 (n)
             88 BINARY_SUBSCR
             98 PRECALL                  1
            102 CALL                     1
            112 BINARY_OP                0 (+)
            116 LOAD_CONST               3 (7)
            118 BINARY_OP                0 (+)
            122 LOAD_CONST               4 (65521)
            124 BINARY_OP                6 (%)
            128 STORE_FAST               1 (s1)

 12         130 LOAD_FAST                1 (s1)
            132 LOAD_FAST                2 (s2)
            134 BINARY_OP                5 (*)
            138 LOAD_CONST               4 (65521)
            140 BINARY_OP                6 (%)
            144 STORE_FAST               2 (s2)
            146 JUMP_BACKWARD           41 (to 66)

 14     >>  148 LOAD_FAST                2 (s2)
            150 LOAD_CONST               5 (16)
            152 BINARY_OP                3 (<<)
            156 LOAD_FAST                1 (s1)
            158 BINARY_OP                7 (|)
            162 RETURN_VALUE

Disassembly of <code object shmorble at 0x7fca0cbae6f0, line 16>:
 16           0 RESUME                   0

 17           2 LOAD_CONST               1 ('')
              4 STORE_FAST               1 (r)

 18           6 LOAD_GLOBAL              1 (NULL + range)
             18 LOAD_GLOBAL              3 (NULL + len)
             30 LOAD_FAST                0 (s)
             32 PRECALL                  1
             36 CALL                     1
             46 PRECALL                  1
             50 CALL                     1
             60 GET_ITER
        >>   62 FOR_ITER                29 (to 122)
             64 STORE_FAST               2 (i)

 19          66 LOAD_FAST                1 (r)
             68 LOAD_FAST                0 (s)
             70 LOAD_FAST                2 (i)
             72 LOAD_GLOBAL              3 (NULL + len)
             84 LOAD_FAST                0 (s)
             86 PRECALL                  1
             90 CALL                     1
            100 BINARY_OP               10 (-)
            104 BINARY_SUBSCR
            114 BINARY_OP               13 (+=)
            118 STORE_FAST               1 (r)
            120 JUMP_BACKWARD           30 (to 62)

 21     >>  122 LOAD_FAST                1 (r)
            124 RETURN_VALUE

Disassembly of <code object blorble at 0x7fca0ca61630, line 23>:
 23           0 RESUME                   0

 24           2 LOAD_GLOBAL              1 (NULL + format)
             14 LOAD_FAST                0 (a)
             16 LOAD_CONST               1 ('x')
             18 PRECALL                  2
             22 CALL                     2
             32 LOAD_GLOBAL              1 (NULL + format)
             44 LOAD_FAST                1 (b)
             46 LOAD_CONST               1 ('x')
             48 PRECALL                  2
             52 CALL                     2
             62 BINARY_OP                0 (+)
             66 RETURN_VALUE
```

</details>

## Solution

Decompile manually worbler file Python byte code along with ChatGPT.
And then, brute force until the a81c0750d48f0750 is matched to a calculated flag.

decompiled.py

```python
import dis
import itertools
import re


ENCRYPTED = "a81c0750d48f0750"
POSSIBLE = "bdrw013"
PATTERN = re.compile(r"^uoftctf\{([" + POSSIBLE + "]){9}\}$")


def worble(s):
    s1 = 5
    s2 = 31

    for n in range(len(s)):
        s1 = (s1 + ord(s[n]) + 7) % 65521

        s2 = (s1 * s2) % 65521

    return (s2 << 16) | s1


def shmorble(s):
    r = ""
    for i in range(len(s)):
        r += s[i - len(s)]

    return r


def blorble(a, b):
    return format(a, "x") + format(b, "x")


def main():
    for c in itertools.product(POSSIBLE, repeat=9):
        flag = "uoftctf{" + "".join(c) + "}"

        assert (m := PATTERN.match(flag)), f"not matched: {m}."

        a = worble(flag)
        b = worble(flag[::-1])
        result = shmorble(blorble(a, b))

        print(f"{flag=}, {result=}", end="\r", flush=True)
        if result == ENCRYPTED:
            print(f"\nfound flag: {flag}")
            return


if __name__ == "__main__":
    main()
    # dis.dis(worble)
    # dis.dis(shmorble)
    # dis.dis(blorble)
```

Result:

```console
$ python3 decompiled.py
flag='uoftctf{d3w0rb13d}', result='a81c0750d48f0750'
found flag: uoftctf{d3w0rb13d}
```

## Flag

uoftctf{d3w0rb13d}
