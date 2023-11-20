# Over the Wire (part 1) [251 Solves]

## Description

> I'm not sure how secure this protocol is but as long as we update the password, I'm sure everything will be fine 😊
>
> Attachments: otw_pt1.pcapng

## Flag

INTIGRITI{1f_0nly_7h3r3_w45_4_53cur3_FTP}

## Solution

1. Open the attached otw_pt1.pcapng file with Wireshark
1. Click on an arbitrary TCP packet
1. In above menu, Analyze > Follow > TCP Stream
1. Increments Stream number
1. In Stream 8, got pyftpdlib credential

   ```text
   220 pyftpdlib 1.5.9 ready.
   USER cat
   331 Username ok, send password.
   PASS 5up3r_53cur3_p455w0rd_2022
   230 Login successful.
   ```

1. In Stream 22, found the directory listing result

   ```text
   -rwxrw-rw-   1 crypto   crypto       7616 Oct 29 12:50 README.md
   -rwxrw-rw-   1 crypto   crypto        236 Oct 29 12:49 flag.zip
   -rwxrw-rw-   1 crypto   crypto        190 Oct 29 12:50 reminder.txt
   ```

1. In Stream 24, found the starting with `PK..` packet.
1. Select `Show data as` to `Hex Dump` and found that this packet signature is 50 4b 03 04. This is zip file [^1].
1. Select `Show data as` to `Raw` and click `Save as...` to save binary file named as flag.zip.
1. Extract the saved file. Note: the password suffix is `2023`, not `2022`, as this year is 2023.

   ```console
   $ unzip -P 5up3r_53cur3_p455w0rd_2022 flag.zip
   Archive:  flag.zip
      skipping: flag.txt                incorrect password
   
   $ unzip -P 5up3r_53cur3_p455w0rd_2023 flag.zip
   Archive:  flag.zip
    extracting: flag.txt
   
   $ cat flag.txt
   INTIGRITI{1f_0nly_7h3r3_w45_4_53cur3_FTP}
   ```

## Footnots

[^1]: [List of file signatures - Wikipedia](https://en.wikipedia.org/wiki/List_of_file_signatures)
    > 50 4B 03 04 zip
