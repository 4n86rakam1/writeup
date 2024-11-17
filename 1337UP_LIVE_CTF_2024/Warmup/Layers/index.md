# Layers [126 Solves]

## Description

> Weird way to encode your data, but OK! 🤷‍♂️
>
> Attachments: layers.zip

## Flag

INTIGRITI{7h3r35_l4y3r5_70_7h15_ch4ll3n63}

## Solution

```console
$ unzip -t layers.zip
Archive:  layers.zip
    testing: 48                       OK
    testing: 45                       OK
    testing: 6                        OK
    testing: 25                       OK
    testing: 55                       OK
    testing: 39                       OK
    testing: 29                       OK
    testing: 32                       OK
    testing: 24                       OK
    testing: 12                       OK
    testing: 8                        OK
    testing: 31                       OK
    testing: 52                       OK
    testing: 15                       OK
    testing: 46                       OK
    testing: 54                       OK
    testing: 1                        OK
    testing: 36                       OK
    testing: 43                       OK
    testing: 50                       OK
    testing: 13                       OK
    testing: 30                       OK
    testing: 28                       OK
    testing: 21                       OK
    testing: 3                        OK
    testing: 23                       OK
    testing: 47                       OK
    testing: 16                       OK
    testing: 18                       OK
    testing: 44                       OK
    testing: 9                        OK
    testing: 49                       OK
    testing: 7                        OK
    testing: 35                       OK
    testing: 42                       OK
    testing: 37                       OK
    testing: 33                       OK
    testing: 0                        OK
    testing: 20                       OK
    testing: 5                        OK
    testing: 11                       OK
    testing: 22                       OK
    testing: 51                       OK
    testing: 38                       OK
    testing: 17                       OK
    testing: 14                       OK
    testing: 4                        OK
    testing: 19                       OK
    testing: 34                       OK
    testing: 53                       OK
    testing: 41                       OK
    testing: 10                       OK
    testing: 26                       OK
    testing: 40                       OK
    testing: 27                       OK
    testing: 2                        OK
No errors detected in compressed data of layers.zip.

$ for i in 48 45 6 25 55 39 29 32 24 12 8 31 52 15 46 54 1 36 43 50 13 30 28 21 3 23 47 16 18 44 9 49 7 35 42 37 33 0 20 5 11 22 51 38 17 14 4 19 34 53 41 10 26 40 27 2; do a=$(cat $i); python3 -c "print(chr(0b${a}),end='')";done
SU5USUdSSVRJezdoM3IzNV9sNHkzcjVfNzBfN2gxNV9jaDRsbDNuNjN9

$ echo SU5USUdSSVRJezdoM3IzNV9sNHkzcjVfNzBfN2gxNV9jaDRsbDNuNjN9 | base64 -d
INTIGRITI{7h3r35_l4y3r5_70_7h15_ch4ll3n63}
```
