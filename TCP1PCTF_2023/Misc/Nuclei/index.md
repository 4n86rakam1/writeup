# Nuclei

## Description

> Nuclei is a fast, template based vulnerability scanner focusing on extensive configurability, massive extensibility and ease of use.
>
> <http://ctf.tcp1p.com:45689>
>
> Attachment: dist.zip

## Flag

TCP1P{W00h00_nuclei_can_detect_my_website!!!}

## Solution

Creating vulnerable application to match Nuclei template.

app.py

```python
from flask import Flask

app = Flask(__name__)

resp = """
"version":"10.0.5"
"Name":"TCP1P"
"msg":"success"
<script>alert(1)</script>
TCP1P{a}
"""


@app.route("/api/v1/version/")
def hello_world():
    return resp


@app.route("/api/v2/echo/")
def test():
    return resp
```

```console
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install Flask
(snip)
$ flask --app app run --host 0.0.0.0 --port 8080
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.0.104:8080
Press CTRL+C to quit
34.126.162.59 - - [15/Oct/2023 12:33:44] "GET /api/v1/version/ HTTP/1.1" 200 -
34.126.162.59 - - [15/Oct/2023 12:33:44] "GET /api/v2/echo/?name=<script>alert(1)</script>&file=/etc/passwd HTTP/1.1" 200 -
```

In my case, when using Ngrok, Nuclei on the server could not connect to Vulnerable Application in my machine due to Ngrok Browser Warning.
So, I used the port forwarding function of my home router to temporarily connect to the local machine and access it from Nuclei.
