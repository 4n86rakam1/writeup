# A.R.K. 1 [166 Solves]

## Description

> One sheep, two sheep, three sheep. (Note: to speed up the process, only include entries containing "sheep" in your attempts) Flag is in the format TUCTF{\<password>} (don't include the brackets)
>
> Attachments: sheep

## Flag

TUCTF{baabaablacksheep}

## Solution

Tools:

- [ssh2john](https://github.com/openwall/john/blob/bleeding-jumbo/run/ssh2john.py)
- [John the Ripper](https://github.com/openwall/john)

> Note: to speed up the process, only include entries containing "sheep" in your attempts

As mentioned, it's recommended to use a wordlist containing the term 'sheep' to expedite the process.

```console
$ file sheep
sheep: OpenSSH private key

$ ssh2john sheep > hash.txt

$ grep sheep /usr/share/wordlists/rockyou.txt > sheep-rockyou.txt

$ john hash.txt --wordlist=sheep-rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
baabaablacksheep (sheep)
1g 0:00:00:02 DONE (2023-12-02 02:48) 0.3731g/s 23.88p/s 23.88c/s 23.88C/s blacksheep..sheepp
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

The flag is TUCTF{baabaablacksheep}
