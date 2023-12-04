# Plenty O Fish in the Sea [249 Solves]

## Description

> You have embarked on a quest to find the One Bit! Your first step is to find the scattered pieces of the treasure map on this here abandoned island!
>
> Attachments: lost_map.zip

## Flag

TUCTF{83h!Nd_7h3_W@73rF@11}

## Solution

```console
$ unzip lost_map.zip
Archive:  lost_map.zip
  inflating: lost_map.log

$ sort lost_map.log | uniq -c
      1 1Nd_7h3_
      1 %4011%7D
      1 %7B83h%2
   1805 At the top of this cliff
   3469 Behind this foliage
    602 Inside this burrow
    175 Inside this coastal cave
    167 Inside this coastal cave
   5421 Inside this shipwreck
     92 In this here tree trunk
    288 In this old rum stash
   3471 In this stream
      1 TUCTF
   1748 Under this big rock
    681 Under this palm tree
    277 Under this skeleton
    330 Under ye feet
      1 W%4073rF

$ sort lost_map.log | uniq -c | nkf --url-input
      1 1Nd_7h3_
      1 @11}
      1 {83h%
2   1805 At the top of this cliff
   3469 Behind this foliage
    602 Inside this burrow
    175 Inside this coastal cave
    167 Inside this coastal cave
   5421 Inside this shipwreck
     92 In this here tree trunk
    288 In this old rum stash
   3471 In this stream
      1 TUCTF
   1748 Under this big rock
    681 Under this palm tree
    277 Under this skeleton
    330 Under ye feet
      1 W@73rF
```

concat `TUCTF`, `%7B83h%2`, `1Nd_7h3_`, `W@73rF`, `%4011%7D` and urldecode.

```console
$ echo TUCTF%7B83h%21Nd_7h3_W@73rF%4011%7D | nkf --url-input
TUCTF{83h!Nd_7h3_W@73rF@11}
```

Also, CyberChef is useful.

[CyberChef: URL Decode](https://gchq.github.io/CyberChef/#recipe=URL_Decode()&input=VFVDVEYlN0I4M2glMjFOZF83aDNfVyU0MDczckYlNDAxMSU3RAoK)
