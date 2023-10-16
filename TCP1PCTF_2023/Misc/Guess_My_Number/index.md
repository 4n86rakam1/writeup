# Guess My Number

## Description

> My friend said if i can guess the right number, he will give me something. Can you help me?
>
> nc ctf.tcp1p.com 7331
>
> Attachment: dist.zip

## Flag

TCP1P{r4nd0m_1s_n0t_th4t_r4nd0m_r19ht?_946f38f6ee18476e7a0bff1c1ed4b23b}

## Solution

`vuln` function decompiled with Ghidra:

```c
void vuln(void)

{
  int iVar1;
  
  key = 0;
  srand(0x539);
  iVar1 = rand();
  printf("Your Guess : ");
  fflush(stdout);
  __isoc99_scanf(&DAT_001020cb,&key);
  if ((key ^ iVar1 + 0x1467f3U) == 0xcafebabe) {
    puts("Correct! This is your flag :");
    system("cat flag.txt");
  // (snip)
```

Calculating correct number:

```python
>>> from ctypes import CDLL  # https://stackoverflow.com/a/66937717
>>> libc = CDLL("libc.so.6")
>>> libc.srand(0x539)
1
>>> print(libc.rand())
292616681
>>> (292616681 + 0x1467f3) ^ 0xcafebabe
3682327394
```

```console
root@kali:~/ctf/TCP1PCTF_2023/misc/Guess_My_Number/dist# echo '3682327394' | nc ctf.tcp1p.com 7331
=======              WELCOME TO GUESSING GAME               =======
======= IF YOU CAN GUESS MY NUMBER, I'LL GIVE YOU THE FLAG  =======

Your Guess : TCP1P{r4nd0m_1s_n0t_th4t_r4nd0m_r19ht?_946f38f6ee18476e7a0bff1c1ed4b23b}
Correct! This is your flag :
```
