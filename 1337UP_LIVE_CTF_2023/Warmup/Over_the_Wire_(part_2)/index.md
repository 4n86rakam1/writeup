# Over the Wire (part 2) [166 Solves]

## Description

> Learning the lessons from the previous failed secure file transfer attempts, CryptoCat and 0xM4hm0ud found a new [definitely secure] way to share information 😊
>
> Attachments: otw_pt2.pcapng

## Flag

INTIGRITI{H1dd3n_Crypt0Cat_Purr}

## Solution

1. Open the attached otw_pt2.pcapng file with Wireshark
1. Click on an arbitrary TCP packet
1. In above menu, Analyze > Follow > TCP Stream
1. Increments Stream number
1. In Stream 19, got SMTP packets.

   <details><summary>Stream 19</summary>

   ```text
   220 kali Python SMTP proxy version 0.3
   ehlo 0xM4hm0ud.home
   250-kali
   250-8BITMIME
   250 HELP
   mail FROM:<0xM4hm0ud@example.com>
   250 OK
   rcpt TO:<CryptoCat@example.com>
   250 OK
   data
   354 End data with <CR><LF>.<CR><LF>
   Content-Type: text/plain; charset="us-ascii"
   MIME-Version: 1.0
   Content-Transfer-Encoding: 7bit
   To: Recipient <CryptoCat@example.com>
   From: Author <0xM4hm0ud@example.com>
   
   '
   Hi CryptoCat,
   
   It's been a long time since we last saw each other, and I've been thinking about our friendship. I believe it's important for us to stay connected and share important things in a way that only you and I can understand.
   
   I wanted to remind you that we need to pay more attention to our communications, especially when it comes to discussing crucial matters. Sometimes, we might need to hide our messages in plain sight, using our own secret language. As you know SMTP isn't secure as you think!
   
   It's like we're on a treasure hunt, and the treasure is our bond. You know the drill - for our important stuff, we'll need to hide it somewhere unique, somewhere only we can find it.
   
   Looking forward to hearing from you soon. Let's make our conversations more interesting and secure.
   
   Best,
   0xM4hm0ud
   .
   250 OK
   quit
   221 Bye
   ```

   </details>

1. In Stream 20, SMTP packets. According to these communications, it seems likely that files containing hidden messages will be exchanged.

   <details><summary>Stream 20</summary>

   ```text
   220 kali Python SMTP proxy version 0.3
   ehlo 0xM4hm0ud.home
   250-kali
   250-8BITMIME
   250 HELP
   mail FROM:<CryptoCat@example.com>
   250 OK
   rcpt TO:<0xM4hm0ud@example.com>
   250 OK
   data
   354 End data with <CR><LF>.<CR><LF>
   Content-Type: text/plain; charset="us-ascii"
   MIME-Version: 1.0
   Content-Transfer-Encoding: 7bit
   To: Recipient <0xM4hm0ud@example.com>
   From: Author <CryptoCat@example.com>
   
   '
   Hey 0xM4hm0ud,
   
   It's great to hear from you! I completely agree that we should keep our conversations private and intriguing. Our special bond deserves nothing less. I'm up for the challenge!
   
   I've been thinking about a unique way we can communicate securely. 
   Maybe we could use a combination of our favorite books, movies or pets as a code, or even a simple cipher? Let's brainstorm ideas and keep our messages hidden from prying eyes.
   
   Looking forward to rekindling our friendship in this exciting and mysterious way.
   
   Talk to you soon,
   CryptoCat
   .
   250 OK
   quit
   221 Bye
   ```

   </details>

1. In Stream 114, found SMTP packets. This includes base64 encoded image file.
1. In Stream 150, base64 encoded image file.
   Select `Show data as` to `ASCII` and click `Save as...` to save binary file named as tmp.txt.
1. Clip only the base64 encoded part from tmp.txt, decode it, and save it as tmp.png.

   ```console
   vi tmp.txt
   cat tmp.txt | base64 -d > tmp.jpg
   ```

1. Use [zsteg](https://github.com/zed-0xff/zsteg) to get the flag

   ```console
   $ zsteg tmp.jpg
   imagedata           .. file: Tower/XP rel 2 object not stripped - version 258
   b1,r,msb,xy         .. file: OpenPGP Public Key
   b1,rgb,lsb,xy       .. text: "INTIGRITI{H1dd3n_Crypt0Cat_Purr}\n"
   b1,rgba,lsb,xy      .. text: "YUY{UU[S3}"
   b4,r,lsb,xy         .. text: "34TBEDVF"
   b4,g,lsb,xy         .. text: "hwwhwfwVfVFwh"
   b4,b,lsb,xy         .. text: "#\"3#!#2#EUDEeDvgdR\r"
   b4,rgb,msb,xy       .. text: "O|\"(Bj(\n"
   b4,bgr,msb,xy       .. text: "|L(B\"h\n*"
   b4,rgba,lsb,xy      .. text: "?y/i?h?yOx?x?x?F"
   b4,abgr,msb,xy      .. text: "o</<o|oz/z"
   ```
