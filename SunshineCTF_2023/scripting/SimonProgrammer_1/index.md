# SimonProgrammer 1

## Description

> **Bandwidth notice:**
>
> This specific challenge is exempted from the do-not-download-everything request that SimonProgrammer 2 and SimonProgrammer 3 have. Feel free to download all audio files from this challenge if it helps you on the other challenges for calibration. Thanks! - CTF Organizers
>
> **Music to my ears!**
>
> Have you ever played "Simon Says?"
>
> You know, "Simon says, go make a CTF challenge and forget to fix a bug in the first challenge but fix a bug in all the other challenges!"
>
> No? Well good! Turns out... last year... I may have procrastinated... I mean predicted... that something like that would have happened 😂.
>
> This year we're breaking out of the pattern for the *programmer series.
>
> The robots are taking our jobs writing articles about the robots taking our jobs!
>
> Now, automation is the name of the game, and Simon Says... automate!
>
> As Mr. Schmitt says, there are a whole lot of techniques to answer back with a pitch, but his is the best!
>
> Visit <https://simon1.web.2023.sunshinectf.games>, and play a game of listening to the present!
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
> <https://simon1.web.2023.sunshinectf.games>

## Flag

sun{simon_says_wait_that_was_a_mistake_what_do_you_mean_i_gave_all_the_frequencies}

## Solution

1. Extract frequencies from response to `/frequencies`
2. Request`/flag` with frequencies in order.

solver.py

```python
import requests

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://simon1.web.2023.sunshinectf.games"

s = requests.Session()
# s.proxies = {"https": "http://127.0.0.1:8080"}
s.headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}


def get_correct_frequencies():
    resp = s.get(f"{BASE_URL}/frequencies", verify=False)
    return resp.json()


def parse_frequencies(frequencies: list[str]) -> list[str]:
    frequencies = [
        f.replace("/static/", "").replace(".wav", "")
        for f in frequencies["frequencies"]
    ]

    return frequencies


def get_flag(frequencies: list[str]) -> None:
    resp = s.post(
        f"{BASE_URL}/flag",
        json=frequencies,
        verify=False,
    )

    return resp.text


def main():
    correct = parse_frequencies(get_correct_frequencies())
    resp = get_flag(correct)
    print(resp)


if __name__ == "__main__":
    main()
```

```console
root@kali:~/ctf/SunshineCTF_2023/scripting/SimonProgrammer 1# python3 solver.py
{"msg":"sun{simon_says_wait_that_was_a_mistake_what_do_you_mean_i_gave_all_the_frequencies}"}
```
