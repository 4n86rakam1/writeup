# IrrORversible [222 Solves]

## Description

> So reversible it's practically irreversible
>
> `nc irrorversible.ctf.intigriti.io 1330`

## Flag

INTIGRITI{b451c_x0r_wh47?}

## Solution

```console
$ echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA | nc irrorversible.ctf.intigriti.io 1330
 ___            ___  ____                     _ _     _
|_ _|_ __ _ __ / _ \|  _ \__   _____ _ __ ___(_) |__ | | ___
 | || '__| '__| | | | |_) \ \ / / _ \ '__/ __| | '_ \| |/ _ \
 | || |  | |  | |_| |  _ < \ V /  __/ |  \__ \ | |_) | |  __/
|___|_|  |_|   \___/|_| \_\ \_/ \___|_|  |___/_|_.__/|_|\___|

 _____                             _   _
| ____|_ __   ___ _ __ _   _ _ __ | |_(_) ___  _ __
|  _| | '_ \ / __| '__| | | | '_ \| __| |/ _ \| '_ \
| |___| | | | (__| |  | |_| | |_) | |_| | (_) | | | |
|_____|_| |_|\___|_|   \__, | .__/ \__|_|\___/|_| |_|
                       |___/|_|
Welcome to the military grade cryptosystem!
Please enter the text you would like to encrypt:

Your encrypted ciphertext (hex format):
082f61190e136136246135333432356d612f2e612f24242561352e6127282629356d610328353261272d283161202f256125202f22246d61282f61252038612e33612f282629356f61152e61223320222a6135292832612a24386d61382e34612c343235612439312d2e33246d61080f150806130815083a23757470221e3971331e362975767e3c6d6129282525242f6120356128353261222e33246f61122928273561202f256135362832356d613529332e34262961232835326126202d2e33246d610e2f2d38613529246123332037246136282d2d61322e2d372461190e136632612d2e33246f082f611945
Thank you for playing!
```

[XOR - CyberChef](https://gchq.github.io/CyberChef/#recipe=XOR%2528%7B'option':'Hex','string':'082f61190e136136246135333432356d612f2e612f24242561352e6127282629356d610328353261272d283161202f256125202f22246d61282f61252038612e33612f282629356f61152e61223320222a6135292832612a24386d61382e34612c343235612439312d2e33246d61080f150806130815083a23757470221e3971331e362975767e3c6d6129282525242f6120356128353261222e33246f61122928273561202f256135362832356d613529332e34262961232835326126202d2e33246d610e2f2d38613529246123332037246136282d2d61322e2d372461190e136632612d2e33246f082f611945'%7D,'Standard',false%2529&input=QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB)

```text
In XOR we trust, no need to fight, Bits flip and dance, in day or night. To crack this key, you must explore, INTIGRITI{b451c_x0r_wh47?}, hidden at its core. Shift and twist, through bits galore, Only the brave will solve XOR's lore.In XIn XOR we trust, no need to fight, Bits flip and dance, in day or night. To crack this key, you must explore,
```
