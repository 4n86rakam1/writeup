# Take some Bytes

## Description

> I think some code is need some effort to read
>
> Attachment: byte.txt

## Flag

TCP1P{byte_code_is_HuFtt}

## Solution

attached byte.txt is Python disassembled code (`dis` function outout).

<https://docs.python.org/3/library/dis.html>

Looking at these code.

```text
15           0 LOAD_FAST                0 (flag)
              2 LOAD_CONST               0 (None)
              4 LOAD_CONST               1 (6)
              6 BUILD_SLICE              2
              8 BINARY_SUBSCR
             10 LOAD_CONST               2 ('TCP1P{')
             12 COMPARE_OP               3 (!=)
             14 POP_JUMP_IF_FALSE       38
             16 LOAD_FAST                0 (flag)
             18 LOAD_CONST               3 (-1)
             20 LOAD_CONST               0 (None)
             22 BUILD_SLICE              2
             24 BINARY_SUBSCR
             26 LOAD_CONST               4 ('}')
             28 COMPARE_OP               3 (!=)
             30 POP_JUMP_IF_FALSE       38
```

- `flag[0:6] = "TCP1P{"`

```text
 18     >>   38 LOAD_FAST                0 (flag)
             40 LOAD_CONST               1 (6)
             42 LOAD_CONST               5 (10)
             44 BUILD_SLICE              2
             46 BINARY_SUBSCR
             48 LOAD_CONST               6 ('byte')
             50 COMPARE_OP               2 (==)
             52 POP_JUMP_IF_FALSE       60
```

- `flag[6:10] = "byte"`

```text
 21     >>   60 LOAD_FAST                0 (flag)
             62 LOAD_CONST               5 (10)
             64 BINARY_SUBSCR
             66 POP_JUMP_IF_FALSE       98
             68 LOAD_FAST                0 (flag)
             70 LOAD_CONST               7 (15)
             72 BINARY_SUBSCR
             74 POP_JUMP_IF_FALSE       98
             76 LOAD_FAST                0 (flag)
             78 LOAD_CONST               8 (18)
             80 BINARY_SUBSCR
             82 LOAD_GLOBAL              2 (chr)
             84 LOAD_CONST               9 (95)
             86 CALL_FUNCTION            1
             88 COMPARE_OP               3 (!=)
             90 POP_JUMP_IF_FALSE       98
```

`char(95)` is `_` so

- `flag[10] = "_"`
- `flag[15] = "_"`
- `flag[18] = "_"`

```text
 24     >>   98 LOAD_FAST                0 (flag)
            100 LOAD_CONST              10 (11)
            102 LOAD_CONST               7 (15)
            104 BUILD_SLICE              2
            106 BINARY_SUBSCR
            108 LOAD_CONST              11 ('code')
            110 COMPARE_OP               3 (!=)
            112 POP_JUMP_IF_FALSE      120
```

- `flag[11:15] = "code"`

```text
 27     >>  120 LOAD_FAST                0 (flag)
            122 LOAD_CONST              10 (11)
            124 BINARY_SUBSCR
            126 LOAD_FAST                0 (flag)
            128 LOAD_CONST              12 (19)
            130 BINARY_SUBSCR
            132 COMPARE_OP               2 (==)
            134 POP_JUMP_IF_FALSE      142
```

- check `flag[11] == flag[19]`
- `flag[19] = flag[11] = "c"`

```text
 30     >>  142 LOAD_FAST                0 (flag)
            144 LOAD_CONST              13 (12)
            146 BINARY_SUBSCR
            148 LOAD_FAST                0 (flag)
            150 LOAD_CONST              14 (20)
            152 BINARY_SUBSCR
            154 COMPARE_OP               2 (==)
            156 POP_JUMP_IF_FALSE      164
```

- check `flag[12] == flag[20]`
- `flag[20] = "o"`

```text
 33     >>  164 LOAD_GLOBAL              3 (ord)
            166 LOAD_FAST                0 (flag)
            168 LOAD_CONST              15 (16)
            170 BINARY_SUBSCR
            172 CALL_FUNCTION            1
            174 LOAD_CONST              16 (105)
            176 COMPARE_OP               3 (!=)
            178 POP_JUMP_IF_FALSE      202
            180 LOAD_GLOBAL              3 (ord)
            182 LOAD_FAST                0 (flag)
            184 LOAD_CONST              17 (17)
            186 BINARY_SUBSCR
            188 CALL_FUNCTION            1
            190 LOAD_CONST              18 (115)
            192 COMPARE_OP               3 (!=)
            194 POP_JUMP_IF_FALSE      202
```

- check `ord(flag[16]) != 105` and `ord(flag[17]) != 115`
- `flag[16] = chr(105) = "i"`
- `flag[17] = chr(115) = "s"`

```text
 36     >>  202 LOAD_FAST                0 (flag)
            204 LOAD_CONST              12 (19)
            206 BINARY_SUBSCR
            208 LOAD_CONST              19 ('H')
            210 COMPARE_OP               3 (!=)
            212 POP_JUMP_IF_FALSE      220
```

- check `flag[19] != 'H'`
- `flag[19] = "H"`

```text
 39     >>  220 LOAD_GLOBAL              3 (ord)
            222 LOAD_FAST                0 (flag)
            224 LOAD_CONST              14 (20)
            226 BINARY_SUBSCR
            228 CALL_FUNCTION            1
            230 LOAD_CONST              20 (117)
            232 COMPARE_OP               2 (==)
            234 POP_JUMP_IF_FALSE      242
```

- check `ord(flag[20]) == 117`
- `flag[20] = chr(117) = "u"`

```text
 42     >>  242 LOAD_GLOBAL              3 (ord)
            244 LOAD_FAST                0 (flag)
            246 LOAD_CONST              21 (21)
            248 BINARY_SUBSCR
            250 CALL_FUNCTION            1
            252 LOAD_GLOBAL              3 (ord)
            254 LOAD_FAST                0 (flag)
            256 LOAD_CONST              22 (2)
            258 BINARY_SUBSCR
            260 CALL_FUNCTION            1
            262 LOAD_CONST               5 (10)
            264 BINARY_SUBTRACT
            266 COMPARE_OP               3 (!=)
            268 EXTENDED_ARG             1
            270 POP_JUMP_IF_FALSE      278
```

- check `ord(flag[21]) != (ord(flag[2]) - 10)`
  - `ord(flag[2]) = ord('P') = 80`
  - `80 - 10 = 70`
- `flag[21] = chr(70) = "F"`

```text
 45     >>  278 LOAD_FAST                0 (flag)
            280 LOAD_CONST              23 (22)
            282 BINARY_SUBSCR
            284 LOAD_FAST                0 (flag)
            286 LOAD_CONST              24 (0)
            288 BINARY_SUBSCR
            290 LOAD_METHOD              4 (lower)
            292 CALL_METHOD              0
            294 COMPARE_OP               3 (!=)
            296 EXTENDED_ARG             1
            298 POP_JUMP_IF_FALSE      306
```

- check `flag[22] != lower(flag[0])`
- `flag[22] = "t"`

```text
 48     >>  306 LOAD_FAST                0 (flag)
            308 LOAD_CONST              23 (22)
            310 BINARY_SUBSCR
            312 LOAD_FAST                0 (flag)
            314 LOAD_CONST              25 (23)
            316 BINARY_SUBSCR
            318 COMPARE_OP               2 (==)
            320 EXTENDED_ARG             1
            322 POP_JUMP_IF_FALSE      330

 49         324 LOAD_GLOBAL              1 (yeayy)
            326 CALL_FUNCTION            0
            328 POP_TOP
        >>  330 LOAD_CONST               0 (None)
            332 RETURN_VALUE
```

- if `flag[22] == flag[23]`, then call `yeayy` function. else nothing.
  so it is expected `flag[22]` is same to `flag[23]`

Thus, implemented solver.py

```python
flag = [" " for _ in range(25)]

flag[0:6] = "TCP1P{"
flag[6:10] = "byte"

flag[10] = "_"
flag[15] = "_"
flag[18] = "_"

flag[11:15] = "code"
flag[19] = "c"

flag[20] = "o"

flag[16] = "i"
flag[17] = "s"

flag[19] = "H"

flag[20] = "u"

flag[21] = "F"

flag[22] = "t"
flag[23] = "t"

flag[24] = "}"

print("".join(flag))
```

```console
root@kali:~/ctf/TCP1PCTF_2023/rev/Take_some_Byte# python3 solver.py
TCP1P{byte_code_is_HuFtt}
```
