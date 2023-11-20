# Obfuscation [213 Solves]

## Description

> I think I made my code harder to read. Can you let me know if that's true?
>
> Author: 0xM4hm0ud
>
> Attachments: obfuscation.zip

## Flag

INTIGRITI{Z29vZGpvYg==}

## Solution

chall.c is obfuscated C code, but compiled it and executed with argument as output, got flag.

```console
$ unzip -P infected obfuscation.zip
Archive:  obfuscation.zip
   creating: chall/
  inflating: chall/chall.c
 extracting: chall/output

$ cd chall

$ make chall
cc     chall.c   -o chall

$ ./chall
Not enough arguments provided!

$ ./chall AAAAAAAAA
Error opening file: No such file or directory

$ ./chall output

$ cat output
INTIGRITI{Z29vZGpvYg==}q 

$ echo -ne Z29vZGpvYg== | base64 -d
goodjob
```
