# whataxor

- source code: [CSAW-CTF-2023-Quals/rev/whataxor at main · osirislab/CSAW-CTF-2023-Quals](https://github.com/osirislab/CSAW-CTF-2023-Quals/tree/main/rev/whataxor)

## Flag

csawctf{0ne_sheeP_1wo_sheWp_2hree_5heeks_____z___zzz_____zzzzzz____xor}

## Solution

`main` decompiled with Ghidra:

```c
  // (snip)
  printf("Enter your password: ");
  __isoc99_scanf(&DAT_00100b1a,local_78);
  xor_transform(local_78,0xffffffaa);
  local_c8 = -0x37;
  // (snip)
  local_82 = 0xd7;
  iVar1 = strcmp(local_78,&local_c8);
  if (iVar1 == 0) {
    puts("Correct!");
  }
  else {
    puts("Access denied.");
  }
  // (snip)
```

- The following are compared.
  - input value is exclusived OR (XORed) with 0xaa
  - Values starting from a variable defined as `local_c8 = -0x37`
  
Thus, I should XOR 0xc9 (= -0x37 + 0x100), 0xd9, 0xcb, etc... with 0xaa.

```python
>>> org = [-0x37+0x100, 0xd9, 0xcb, 0xdd, 0xc9, 0xde, 0xcc, 0xd1, 0x9a, 0xc4, 0xcf, 0xf5, 0xd9, 0xc2, 0xcf, 0xcf, 0xfa, 0xf5, 0x9b, 0xdd, 0xc5, 0xf5, 0xd9, 0xc2, 0xcf, 0xfd, 0xda, 0xf5, 0x98, 0xc2, 0xd8, 0xcf, 0xcf, 0xf5, 0x9f, 0xc2, 0xcf, 0xcf, 0xc1, 0xd9, 0xf5, 0xf5, 0xf5, 0xf5, 0xf5, 0xd0, 0xf5, 0xf5, 0xf5, 0xd0, 0xd0, 0xd0, 0xf5, 0xf5, 0xf5, 0xf5, 0xf5, 0xd0, 0xd0, 0xd0, 0xd0, 0xd0, 0xd0, 0xf5, 0xf5, 0xf5, 0xf5, 0xd2, 0xc5, 0xd8, 0xd7]
>>> key = 0xaa
>>> ''.join([chr(x ^ key) for x in org])
'csawctf{0ne_sheeP_1wo_sheWp_2hree_5heeks_____z___zzz_____zzzzzz____xor}'
```

```console
root@kali:~/ctf/CSAW-CTF-2023-Quals/rev/whataxor# echo -ne 'csawctf{0ne_sheeP_1wo_sheWp_2hree_5heeks_____z___zzz_____zzzzzz____xor}' | ./whataxor
Enter your password: Correct!
```
