# First Date

## Description

> I'm Excited, this is my first date in years but this time it's a Play Date!
>
> Sadly I'm locked out of it so if you could help me get in that would be great!
>
> **Note**
>
> Your .pdx.zip file should have this SHA256 hash: 27628909e164ac4c61eaf3bc2583282e9bebbb6d23871b6043614703492d6cf0. If it doesn't you're not on the correct build and should redownload the .pdx.zip file
>
> Attachment: first_date.pdx.zip

## Flag

sun{MIEANBLVFPZJTDOA}

## Solution

```console
root@kali:~/ctf/SunshineCTF_2023/Reversing/First Date# unzip first_date.pdx.zip
Archive:  first_date.pdx.zip
   creating: first_date.pdx/
 extracting: first_date.pdx/main.pdz
 extracting: first_date.pdx/pdxinfo

root@kali:~/ctf/SunshineCTF_2023/Reversing/First Date# file first_date.pdx/*
first_date.pdx/main.pdz: Playdate executable package
first_date.pdx/pdxinfo:  ASCII text
```

[Playdate (console) - Wikipedia](https://en.wikipedia.org/wiki/Playdate_%28console%29)

> Playdate is a handheld video game console developed by Panic. The device features a mechanical crank and a black-and-white screen.

I guess `main.pdz` file is the executable file which is executed in [Playdate](https://play.date/).
I see what

Decompiled Step:

1. .pdz -> .luac: [pdz.py in cranksters/playdate-reverse-engineering](https://github.com/cranksters/playdate-reverse-engineering/blob/main/tools/pdz.py)

   ```bash
   git clone https://github.com/cranksters/playdate-reverse-engineering.git
   python3 ./playdate-reverse-engineering/tools/pdz.py first_date.pdx/main.pdz output
   ```

2. .luac -> .lua: [scratchminer/unluac](https://github.com/scratchminer/unluac)

   ```bash
   curl -sLO https://github.com/scratchminer/unluac/releases/download/v2023.03.22/unluac.jar
   mkdir decompiled
   java -jar unluac.jar output/main.luac -o decompiled/main.lua
   ```

main.lua

```lua
-- (snip)
function generateOrder()
 local pinSeed = ""
 for i = 1, 20 do
  pinSeed = pinSeed .. i
 end
 return pinSeed
end
-- (snip)
function clean(input)
 local cleaned = ""
 for i = 1, #input, 2 do
  local pair = input:sub(i, i + 1)
  local num = tonumber(pair)
  num = num % 26 + 65
  cleaned = cleaned .. string.char(num)
 end
 return cleaned
end
-- (snip)
function playdate.update()
-- (snip)
 if pressedButtons == generateOrder() then
  print("Pin entered correctly!")
  gfx.setFont(gfx.font.kVariantBold)
  cleaned = clean(pressedButtons)
  print("Flag: sun{" .. cleaned .. "}")
  gfx.drawTextAligned([[
Flag: 
sun{]] .. cleaned .. "}", 200.0, 80.0, kTextAlignment.center)
 end
end
```

flag is generated in there and output, so I implement same script.

solver.lua

```lua
function clean(input)
 local cleaned = ""
 for i = 1, #input, 2 do
  local pair = input:sub(i, i + 1)
  local num = tonumber(pair)
  num = num % 26 + 65
  cleaned = cleaned .. string.char(num)
 end
 return cleaned
end

function generateOrder()
 local pinSeed = ""
 for i = 1, 20 do
  pinSeed = pinSeed .. i
 end
 return pinSeed
end

pressedButtons = generateOrder()
cleaned = clean(pressedButtons)
print("sun{" .. cleaned .. "}")
-- => sun{MIEANBLVFPZJTDOA}
```
