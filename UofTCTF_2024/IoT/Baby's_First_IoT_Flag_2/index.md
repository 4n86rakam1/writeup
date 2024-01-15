# Baby's First IoT Flag 2 [314 Solves]

## Description

> See introduction for complete context.
>
> - Part 2 - What company makes the processor for this device? <https://fccid.io/Q87-WRT54GV81/Internal-Photos/Internal-Photos-861588>. Submit the answer to port 6318.

## Solution

The top of the processor is labeled with Bloadcom.

```console
$ printf 'Broadcom\n\0' | nc 35.225.17.48 6318
Enter the company that manufactures the processor for the FCC ID Q87-WRT54GV81 Access granted! The Flag is {Processor_Recon}! 
```

## Flag

{Processor_Recon}
