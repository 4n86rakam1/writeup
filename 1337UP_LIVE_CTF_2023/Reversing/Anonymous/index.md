# Anonymous [115 Solves]

## Description

> Anonymous has hidden a message inside this exe, can you extract it?
>
> Author: Mohamed Adil
>
> Password is "infected"
>
> Attachments: Anonymous.zip

## Flag

intigriti{Base_R_Ez?}

## Solution

```console
$ unzip -P infected Anonymous.zip
Archive:  Anonymous.zip
  inflating: Anonymous.exe

$ file Anonymous.exe
Anonymous.exe: PE32 executable (console) Intel 80386 Mono/.Net assembly, for MS Windows, 3 sections
```

Decompiled exe binary with [dnSpy](https://github.com/dnSpy/dnSpy) x86 version.

Compared the input with flag in here:

```csharp
// AnonChallenge (1.0.0.0) > AnonChallenge.exe > {} AnonChallenge > Program
// (snip)
            if (Program.IsBase64String(text2) && text2.Length > 20 && text2.Length <= 30 && Resources.anon.Contains(text2))
            {
                string @string = Encoding.ASCII.GetString(Convert.FromBase64String(text2));
                if (@string[1] == 'n' && @string[3] == 'i')
                {
                    text = "MayBe Your Password Isn't Correct I'm Not Sure : " + @string;
                    for (int i = 0; i < text.Length; i++)
                    {
                        Console.Write(text[i]);
                        Thread.Sleep(30);
                    }
                }
            }
// (snip)
```

```csharp
// AnonChallenge (1.0.0.0) > AnonChallenge.exe > {} AnonChallenge.Properties > Resrouces
// (snip)
        // Token: 0x17000003 RID: 3
        // (get) Token: 0x06000008 RID: 8 RVA: 0x0000223C File Offset: 0x0000043C
        internal static string anon
        {
            get
            {
                return Resources.ResourceManager.GetString("anon", Resources.resourceCulture);
            }
        }
// (snip)
```

```csharp
// AnonChallenge (1.0.0.0) > AnonChallenge.exe > Resources

// 0x00000468: AnonChallenge.Properties.Resources.resources‎ (1809 bytes, Embedded, Public)


// 0x00000531: anon‎ = "                            ````...--...````\r\n                 :s+`   ````````````````````````   -sy/\r\n             --+NN:   `..` ``  ``  ``  ``  `` `..`   +NN//:\r\n           .hssMy/  `.`   .````.``o/sy-`.````.   `.` `+yM/dh`\r\n         `-mN-sod: .`    .    .  `y:/My  .    .    `. /dso:My/`\r\n        `d`MyyNy.`.```` .     `    .y:   `     . ````.`.yNhmd:d\r\n        sM.Nmos. .    `.`````.`````/:`````.`````.     . :o+dh+M+\r\n        hM/ooNo .`     .     .     yy     .     .     `. oNs/sMs\r\n       :sMomN+  .     ``     .     --     .     ``     .  +NNyM/+\r\n      `m`mNd:o ``     ``     . `/`oyyo`/` .     ``     `` y-hNy.N\r\n      `My-d-N/ `.`````..``-:/shNd `hh` dNhs/:-``..`````.` +N:y.dN\r\n       hMo-NN` `.     ```NMMMMMM/ .++. /MMMMMMN```     .` `NM-hMs\r\n       :NMyM+/  .     `.sMMMMMMMs  dd  sMMMMMMMs.`     .  o/MhMd:\r\n      `h-yNm`N. ``     -NMMMMMMMN. MM .NMMMMMMMN-     `` :N`dN+:m\r\n       sNo/s/M+  .` ```+MMMMMMMMMm-MM-mMMMMMMMMM+``` `. `oM:o:yM/\r\n        oMN+/My:- ..`  yMMLjKYleQcOuaspJRvVAKvMMy  `.. /:yM/yMm:\r\n        `/sNdNm`N+ `.  NMMMFxz5\\fxC2FzvnbtMg4XvMN  .` sN NNmm++`\r\n         :y:/yN:hM/  `:MMMMbM90gfG65GcGKsTrfxMMMM:`  +My+do:+d-\r\n          .hNhoo-NN:o.:MMMW4vf2ScKgE5gSzV9o0XgMMM:-s:Nm-oymNs`\r\n           .smMaNhmd:NyyNaW50aWdyaXRpe0Jhc2VfUl9Fej99NdMNho`\r\n            .+o++ooo:yMddNMAzE3tYXvrft43Fh7NdmmNs-ooo++o+`\r\n             -sdMMNNmmNmmMfjVBGe3l4sMcQ9t1QVMdddmNMMMNh+.\r\n               .++//:/odMOW4t1WUJ4otsj7UuNhZWms+://++-\r\n                 :oyddhNB0lABs8YATzKPXmT4oajNyhys+-\r\n                        `2nDxDEXJsYx1aSvN38Ht`\r\n                         -+sydmNNMMMMNNmdys+-`\r\n"
```

The flag, base64 encoded, is included in Resources.anon.
I base64 decode Resources.anon.

[CyberChef](https://gchq.github.io/CyberChef/#recipe=Fork('%5C%5Cn','%5C%5Cn',false)From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=ICAgICAgICAgICAgICAgICAgICAgICAgICAgIGBgYGAuLi4tLS4uLmBgYGAKICAgICAgICAgICAgICAgICA6cytgICAgYGBgYGBgYGBgYGBgYGBgYGBgYGBgYGBgICAgLXN5LwogICAgICAgICAgICAgLS0rTk46ICAgYC4uYCBgYCAgYGAgIGBgICBgYCAgYGAgYC4uYCAgICtOTi8vOgogICAgICAgICAgIC5oc3NNeS8gIGAuYCAgIC5gYGBgLmBgby9zeS1gLmBgYGAuICAgYC5gIGAreU0vZGhgCiAgICAgICAgIGAtbU4tc29kOiAuYCAgICAuICAgIC4gIGB5Oi9NeSAgLiAgICAuICAgIGAuIC9kc286TXkvYAogICAgICAgIGBkYE15eU55LmAuYGBgYCAuICAgICBgICAgIC55OiAgIGAgICAgIC4gYGBgYC5gLnlOaG1kOmQKICAgICAgICBzTS5ObW9zLiAuICAgIGAuYGBgYGAuYGBgYGAvOmBgYGBgLmBgYGBgLiAgICAgLiA6bytkaCtNKwogICAgICAgIGhNL29vTm8gLmAgICAgIC4gICAgIC4gICAgIHl5ICAgICAuICAgICAuICAgICBgLiBvTnMvc01zCiAgICAgICA6c01vbU4rICAuICAgICBgYCAgICAgLiAgICAgLS0gICAgIC4gICAgIGBgICAgICAuICArTk55TS8rCiAgICAgIGBtYG1OZDpvIGBgICAgICBgYCAgICAgLiBgL2BveXlvYC9gIC4gICAgIGBgICAgICBgYCB5LWhOeS5OCiAgICAgIGBNeS1kLU4vIGAuYGBgYGAuLmBgLTovc2hOZCBgaGhgIGROaHMvOi1gYC4uYGBgYGAuYCArTjp5LmROCiAgICAgICBoTW8tTk5gIGAuICAgICBgYGBOTU1NTU1NLyAuKysuIC9NTU1NTU1OYGBgICAgICAuYCBgTk0taE1zCiAgICAgICA6Tk15TSsvICAuICAgICBgLnNNTU1NTU1NcyAgZGQgIHNNTU1NTU1Ncy5gICAgICAuICBvL01oTWQ6CiAgICAgIGBoLXlObWBOLiBgYCAgICAgLU5NTU1NTU1NTi4gTU0gLk5NTU1NTU1NTi0gICAgIGBgIDpOYGROKzptCiAgICAgICBzTm8vcy9NKyAgLmAgYGBgK01NTU1NTU1NTW0tTU0tbU1NTU1NTU1NTStgYGAgYC4gYG9NOm86eU0vCiAgICAgICAgb01OKy9NeTotIC4uYCAgeU1NTGpLWWxlUWNPdWFzcEpSdlZBS3ZNTXkgIGAuLiAvOnlNL3lNbToKICAgICAgICBgL3NOZE5tYE4rIGAuICBOTU1NRnh6NVxmeEMyRnp2bmJ0TWc0WHZNTiAgLmAgc04gTk5tbSsrYAogICAgICAgICA6eToveU46aE0vICBgOk1NTU1iTTkwZ2ZHNjVHY0dLc1RyZnhNTU1NOmAgICtNeStkbzorZC0KICAgICAgICAgIC5oTmhvby1OTjpvLjpNTU1XNHZmMlNjS2dFNWdTelY5bzBYZ01NTTotczpObS1veW1Oc2AKICAgICAgICAgICAuc21NYU5obWQ6Tnl5TmFXNTBhV2R5YVhScGUwSmhjMlZmVWw5RmVqOTlOZE1OaG9gCiAgICAgICAgICAgIC4rbysrb29vOnlNZGROTUF6RTN0WVh2cmZ0NDNGaDdOZG1tTnMtb29vKytvK2AKICAgICAgICAgICAgIC1zZE1NTk5tbU5tbU1malZCR2UzbDRzTWNROXQxUVZNZGRkbU5NTU1OaCsuCiAgICAgICAgICAgICAgIC4rKy8vOi9vZE1PVzR0MVdVSjRvdHNqN1V1TmhaV21zKzovLysrLQogICAgICAgICAgICAgICAgIDpveWRkaE5CMGxBQnM4WUFUektQWG1UNG9hak55aHlzKy0KICAgICAgICAgICAgICAgICAgICAgICAgYDJuRHhERVhKc1l4MWFTdk4zOEh0YAogICAgICAgICAgICAgICAgICAgICAgICAgLStzeWRtTk5NTU1NTk5tZHlzKy1g)

Got the flag: intigriti{Base_R_Ez?}
