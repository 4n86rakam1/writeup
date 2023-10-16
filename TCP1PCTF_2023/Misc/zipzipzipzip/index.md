# zipzipzipzip

## Description

> unzip me pls
>
> Attachment: password.txt, zip-25000.zip

## Flag

TCP1P{1_TH1NK_U_G00D_4T_SCR1PT1N9_botanbell_1s_h3r3^_^}

## Solution

Extracting provided zip file recursively.

solver.sh

```bash
#!/bin/bash

test ! -e zip-25000.zip && echo 'Not found zip-25000.zip.' && exit 1

for i in $(seq 25000 -1 1); do
    password=$(tr -d '\r\n' < password.txt)

    unzip -oqqP "${password}" "zip-${i}.zip"
    rm "zip-${i}.zip"
done
```

```console
root@kali:~/ctf/TCP1PCTF_2023/misc/zipzipzipzip# time ./solver.sh

real    4402.76s
user    4078.29s
sys     298.16s
cpu     99%

root@kali:~/ctf/TCP1PCTF_2023/misc/zipzipzipzip# cat flag.txt
TCP1P{1_TH1NK_U_G00D_4T_SCR1PT1N9_botanbell_1s_h3r3^_^}
```

## References

- `man unzip`
