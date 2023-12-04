# A.R.K. 4 [98 Solves]

## Description

> What does the fox say?
>
> Attachments: fox

## Flag

TUCTF{B3w4R3_7h3_f1r3_4nd_7h3_f0x}

## Solution

Tools:

- [firefox_decrypt](https://github.com/unode/firefox_decrypt)

```console
$ file fox
fox: Zip archive data, at least v1.0 to extract, compression method=store

$ mv fox{,.zip}

$ unzip -q fox.zip

$ ~/tools/firefox_decrypt/firefox_decrypt.py fox
2023-12-02 03:25:04,764 - WARNING - profile.ini not found in fox
2023-12-02 03:25:04,765 - WARNING - Continuing and assuming 'fox' is a profile location

Website:   https://www.example.com
Username: 'fox'
Password: 'TUCTF{B3w4R3_7h3_f1r3_4nd_7h3_f0x}'
```
