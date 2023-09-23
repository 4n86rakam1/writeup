# rebug 1
## Flag

csawctf{c20ad4d76fe97759aa27a0c99bff6710}

## Solution

main decompiled with Ghidra:

```c
undefined8 main(void)
(snip)
  printf("Enter the String: ");
  __isoc99_scanf(&DAT_00102017,local_408);
  for (local_c = 0; local_408[local_c] != '\0'; local_c = local_c + 1) {
  }
  if (local_c == 0xc) {
    puts("that\'s correct!");
```

- It loops over the length of the input value and increments `local_c`.
- If `local_c` is 0xc (12), output `that's correct!`.

Thus, I should enter the length of 12 characters.

```console
root@kali:~/ctf/CSAW-CTF-2023-Quals/rev/rebug 1# echo -ne '123456789012' | ./test.out
Enter the String: that's correct!
csawctf{c20ad4d76fe97759aa27a0c99bff6710}
```
