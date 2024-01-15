# Voice Changer [206 Solves]

## Description

> I made a cool app that changes your voice.
>
> Author: Ido
>
> `https://uoftctf-voice-changer.chals.io/`

## Short Solution

Argument Injection in [POST] /upload pitch parameter.

## Solution

### Explore functionality

![1.png](img/1.png)

Recording and submitting:

![upload-voice.png](img/upload-voice.png)

The ffmpeg command that appears to have been executed on the server side has been output.
At this time, [POST] /upload request was sent:

![req1.png](img/req1.png)

### Argument Injection

I send the previous request to Burp Repeater and remove unnecessary headers.
And, I inject `id` command in the pitch parameter:

![injection1.png](img/injection1.png)

The result of `id` command is got so exploit Argument Injection.
Now, all that's left is to retrieve the flag.

![flag.png](img/flag.png)

## Flag

uoftctf{Y0UR Pitch IS 70O H!9H}
