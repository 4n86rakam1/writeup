# SimonProgrammer 3

## Description

> **SimonProgrammer 3: Now You C♭ Me... Now You Don't**
>
> **Bandwidth notice:**
>
> Please only download the audio you need to complete the challenge. You can use the audio files from Simon Programmer 1 to calibrate your solver, if required. Thanks! - CTF Organizers
>
> **Music to my ears!**
>
> ...
>
> Really?
>
> You solved it that way?
>
> Why?
>
> I mean, the old way was broken, so I guess it makes sense, but...
>
> It's so much easier to just solve it with the right tools!
>
> Ok ok, this time, I give you a working challenge.
>
> And don't try to solve it manually! I have a ticking clock this time, so you better solve these fast!
>
> As Mr. Schmitt says, there are a whole lot of techniques to answer back with a pitch, but his is the best!
>
> WAIT... NOOOOOO 🤖🤖🤖🤖🤖🤖🤖🤖
>
> robots have taken over this challenge
>
> Visit <https://simon3.web.2023.sunshinectf.games>, if you dare, human!
>
> But don't worry that this game will get old! The flags in this game are split into three octaves, with one flag in each... you'll never find them all! And since it's random, no two games will ever be alike!
>
> Flag will be given by our backend in the standard sun{} format!
>
> **Notes**
>
> We are not unreasonable.
>
> All we ask is you listen to the music with 99.9% accuracy.
>
> Should be easy for you, human.
>
> <https://simon3.web.2023.sunshinectf.games>

## Flag

sun{simon_says_automated_solve_or_bust}

## Solution

- This solution is based on using <https://stackoverflow.com/a/66892766>
- It's didn't work by extracting `Rough   frequency:` in [SoX](https://sox.sourceforge.net/sox.html) output

```python
import numpy as np
from scipy.fft import *
from scipy.io import wavfile

import requests

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://simon3.web.2023.sunshinectf.games"

s = requests.Session()
# s.proxies = {"https": "http://127.0.0.1:8080"}
s.headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


# https://stackoverflow.com/a/66892766
def wav2frequency(file):
    # Open the file and convert to mono
    sr, data = wavfile.read(file)
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    # Fourier Transform
    N = len(data)
    yf = rfft(data)
    xf = rfftfreq(N, 1 / sr)

    # Get the most dominant frequency and return it
    idx = np.argmax(np.abs(yf))
    freq = xf[idx]
    return freq


def paths2frequencies(paths: list[str]) -> list[float]:
    frequencies = []

    for path in paths:
        filename = path.replace("/static/", "")
        resp = s.get(f"{BASE_URL}/{path}")

        # save wav
        with open(f"wavs/{filename}", "wb") as f:
            f.write(resp.content)

        frequencies.append(wav2frequency(f"wavs/{filename}"))

    return frequencies


def get_frequencies() -> dict:
    resp = s.get(f"{BASE_URL}/frequencies", verify=False)
    return resp.json()


def get_flag(frequencies: list[str]) -> None:
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
