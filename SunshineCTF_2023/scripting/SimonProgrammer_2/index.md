# SimonProgrammer 2

## Description

> **SimonProgrammer 2: The Next Octave**
>
> **Bandwidth notice:**
>
> Please only download the audio you need to complete the challenge. You can use the audio files from Simon Programmer 1 to calibrate your solver, if required. Thanks! - CTF Organizers
>
> **Music to my ears!**
>
> Ok, ok. Yeah. That was a mistake.
>
> An intentional mistake laughs in evil genius.
>
> I... uh... intended to... uh...
>
> ...
>
> I patched it now! And now uh... the old way of doing the challenge seems broken... uh...
>
> ...
>
> Ok, ok. We'll say the previous challenge was so folks could calibrate... automated solvers... cause...
>
> The robots are taking our jobs writing articles about the robots taking our jobs!
>
> Now, automation is the name of the game, and Simon Says... automate!
>
> As Mr. Schmitt says, there are a whole lot of techniques to answer back with a pitch, but his is the best!
>
> Visit <https://simon2.web.2023.sunshinectf.games>, and play a game of listening to the present!
>
> But don't worry that this game will get old! The flags in this game are split into three octaves, with one flag in each... you'll never find them all! And since it's random, no two games will ever be alike!
>
> Flag will be given by our backend in the standard sun{} format!
>
> **Notes**
>
> I am not unreasonable.
>
> All I ask is you listen to the music with 99.9% accuracy.
>
> That's better than last year, which required 100% accuracy! Much better.
>
> <https://simon2.web.2023.sunshinectf.games>

## Flag

sun{simon_says_wait_that_was_a_mistake_what_do_you_mean_the_filenames_were_frequencies}

## Solution

- This solution is based on using [Base64 URL](https://gchq.github.io/CyberChef/#recipe=Fork('%5C%5Cn','',false)From_Base64('A-Za-z0-9-_',true,false)&input=OEota2xqRXdOamZ3bjZTV0NnPT0KOEota2xqVTROdkNmcEpZSwo4Si1rbGpFME5qSHduNlNXQ2c9PQo4Si1rbGpFeE5fQ2ZwSllLCjhKLWtsalUxTlBDZnBKWUsKOEota2xqRTBNVFR3bjZTV0NnPT0KOEota2xqRTBOemJ3bjZTV0NnPT0KOEota2xqazJPZkNmcEpZSwo4Si1rbGpZNE5QQ2ZwSllLCjhKLWtsakV4TURqd242U1dDZz09CjhKLWtsakV3TWpEd242U1dDZz09CjhKLWtsak0zTmZDZnBKWUsKOEota2xqa3dOX0NmcEpZSwo4Si1rbGpFME1QQ2ZwSllLCjhKLWtsamczTV9DZnBKWUsKOEota2xqRTFOemZ3bjZTV0NnPT0KOEota2xqRTJORFh3bjZTV0NnPT0KOEota2xqRXlNemJ3bjZTV0NnPT0KOEota2xqRTBNRFR3bjZTV0NnPT0KOEota2xqRXlNakR3bjZTV0NnPT0KOEota2xqUTVPUENmcEpZSwo4Si1rbGpNd052Q2ZwSllLCjhKLWtsamt4T2ZDZnBKWUsKOEota2xqY3lPZkNmcEpZSwo4Si1rbGpReE5mQ2ZwSllLCjhKLWtsakU1TkRid242U1dDZz09CjhKLWtsak13TV9DZnBKWUsKOEota2xqa3dNUENmcEpZSwo4Si1rbGpFeE1UanduNlNXQ2c9PQo4Si1rbGpFNE1EVHduNlNXQ2c9PQo4Si1rbGpFd016UHduNlNXQ2c9PQo4Si1rbGpjMU1mQ2ZwSllLCjhKLWtsakV3Tnpid242U1dDZz09CjhKLWtsakU1TWZDZnBKWUsKOEota2xqRTRNRGp3bjZTV0NnPT0KOEota2xqRTBOZkNmcEpZSwo4Si1rbGpnME1QQ2ZwSllLCjhKLWtsakUzTWpYd242U1dDZz09CjhKLWtsakV4TlRYd242U1dDZz09CjhKLWtsalEzTmZDZnBKWUs) not standard Base64
- It didn't work by using <https://stackoverflow.com/a/66892766>

```python
import requests
import string
import base64

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://simon2.web.2023.sunshinectf.games"

s = requests.Session()
# s.proxies = {"https": "http://127.0.0.1:8080"}
s.headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def paths2frequencies(path_list: list[str]) -> list[str]:
    frequencies = []

    for path in path_list:
        base64encoded = path.replace("/static/", "").replace(".wav", "")
        freq = "".join(
            [
                chr(s)
                for s in base64.urlsafe_b64decode(base64encoded)
                if chr(s) in string.printable
            ]
        ).strip()

        frequencies.append(freq)

    return frequencies


def get_frequencies() -> dict:
    resp = s.get(f"{BASE_URL}/frequencies", verify=False)
    return resp.json()


def get_flag(frequencies: list[str]) -> str:
    resp = s.post(
        f"{BASE_URL}/flag",
        json=frequencies,
        verify=False,
    )

    return resp.text


def main():
    frequencies = paths2frequencies(get_frequencies()["frequencies"])
    resp = get_flag(frequencies)
    print(resp)


if __name__ == "__main__":
    main()
```
