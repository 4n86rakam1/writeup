# Flag Extraction [411 Solves]

## Description

> They told me I just need to extract flag but I don't know what that means?!
>
> Attachments: flag.rar

## Flag

INTIGRITI{fl46_3x7r4c710n_c0mpl373}

## Solution

Keep on trying to use the appropriate extracting tool and use `strings` command.

```console
$ unrar e flag.rar

UNRAR 7.00 beta 1 freeware      Copyright (c) 1993-2023 Alexander Roshal


Extracting from flag.rar

Extracting  flag.tar.xz                                               OK
All OK

$ tar Jxvf flag.tar.xz
flag.tar.bz2

$ tar jxvf flag.tar.bz2
flag.tar.gz

$ tar zxvf flag.tar.gz
flag.zip

$ unzip flag.zip
Archive:  flag.zip
  inflating: flag.gif

$ strings flag.gif | grep INTIGRITI
INTIGRITI{fl46_3x7r4c710n_c0mpl373}
```
