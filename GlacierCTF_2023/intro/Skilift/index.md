# Skilift [366 Solves]

## Description

> You arrive at the base station of a ski lift. Unfortunately for you, the lift is not in operation but you have to reach the next summit somehow. You enter the control room to find a control terminal with the words "Please input your key:"
>
> author: mole99
>
> `nc chall.glacierctf.com 13375`
>
> Attachments: top.v

top.v:

```verilog
module top(
    input [63:0] key,
    output lock
);
  
    reg [63:0] tmp1, tmp2, tmp3, tmp4;

    // Stage 1
    always @(*) begin
        tmp1 = key & 64'hF0F0F0F0F0F0F0F0;
    end
    
    // Stage 2
    always @(*) begin
        tmp2 = tmp1 <<< 5;
    end
    
    // Stage 3
    always @(*) begin
        tmp3 = tmp2 ^ "HACKERS!";
    end

    // Stage 4
    always @(*) begin
        tmp4 = tmp3 - 12345678;
    end

    // I have the feeling "lock" should be 1'b1
    assign lock = tmp4 == 64'h5443474D489DFDD3;

endmodule
```

## Flag

gctf{V3r1log_ISnT_SO_H4rd_4fTer_4ll_!1!}

## Solution

The attached top.v file is [Verilog](https://en.wikipedia.org/wiki/Verilog).

In the top.v script:

- stores an input value to `key` variable
- Stage 1: logical AND by 0xF0F0F0F0F0F0F0F0
- Stage 2: bit shift to the left by 5
- Stage 3: exclusive OR by `HACKERS!`
- Stage 4: subtract by 12345678
- Final: compares to 0x5443474D489DFDD3

Reverse Operation in Python Console:

```python
>>> 0x5443474D489DFDD3 + 12345678  # Reverse Stage 4
6071775119894273825
>>> import binascii
>>> 6071775119894273825 ^ int(binascii.hexlify(b'HACKERS!'), base=16)  # Reverse Stage 3
2018180007033572352
>>> hex(2018180007033572352 >> 5)  # Reverse Stage 2
'0xe0102030604060'
>>> # Stage 1:
>>> # 0xe0102030604060 is the correct key, as it only needs alignment with the bits that are set (the positions of 'F' in 0xF0F0F0F0F0F0F0F0). e.g. 0xe0102030604061 is correct too.
>>> # 0x00e0102030604060: 0x0 padding
>>> # 0xF0F0F0F0F0F0F0F0
```

```console
$ echo 0xe0102030604060 | nc chall.glacierctf.com 13375
  ∗               ∗        ∗               ∗          ∗
         ∗
                                ∗                     ◦◦╽◦◦
   ∗               ∗                      ∗          ◦◦ █  ◦
                                ∗                   ◦◦  █
            ∗                         ∗         ∗  ◦◦   █
     ∗              ∗    ◦╽◦◦                   ◦◦◦◦    █
                       ◦◦ █ ◦◦◦         ◦◦╽◦◦◦◦◦◦       █
                      ◦◦  █   ◦◦◦◦◦◦◦◦◦◦◦ █             █
      ■■■■■■■■     ◦◦◦◦   █        ▛      █  ∗          █  ∗
     ▟        ▙ ◦◦◦       █  ∗     ▌      █         ∗   █
 ∗  ▟          ▙          █     ██████  ∗ █             █
   ▟            ▙     ∗   █     █    █    █             █
   ▛▀▀▀▀▀▀▀▀▀▀▀▀▜         █     ██████    █             █░░░
   ▌            ▐         █               █    ∗       ░░░░░
   ▌            ▐  ∗      █               █          ░░░░░▒▒
   ▌  ▛▀▀▀▜     ▐         █   ∗           █        ░░░░░▒░░░
∗  ▌  ▌   ▐     ▐      ∗  █          ∗   ░░░░░░░▓░░░░░░▒▒░░░
   ▌  ▌ ╾ ▐     ▐         █░░░░░      ░░░░▒░░░░▓░░░░░░░░░░░░
   ▌  ▌   ▐     ▐     ░░░░░▒▒▒░░░░░░░░░░░░░░░░░▒▒▒░░░░░░░▓▓▓
   ▙▄▄▙▄▄▄▟▄▄▄▄▄▟     ░░░░▒▒░░░░▓▓░░░░░░░░░▓░░░░░░░░░░░░░░░░
░░░░░░░░░░░▒▒▒░░░░▒░░░░░░░░░░░░░░░░░░░░▓▓░░░░░░░░░▓▓░░▒▒░░░░
░░▓░░▒░░░▓░░░░░░░░░░░░░░░░░▒░▓░░░▒░░░░▓░░░░░▒░░░░▓▓░▒▒░░░░░░
░▓▓░░▒░░░░░░▒░░░░░░░░░░░░░░░▓▓▓░░░▒░░░░░░░░░▒▒░▒░░░░░░░░▒░░░
░░░░░░░▒░░░░░░░░▓▓▓░░░░▒▒░░▒░░░░░░▒▓▓░░▒▒░░░░░░▓░░▓░░░░▓▒░░░
░░░▒░░░▓░░░░░▒░░░░░░▒▓░░░░░░░░░░░░░▓░░░░░░░▓░░▓░▓░░░░░░▓░░░░
░░░░░░▓▓░░░▒▒▒░░░░░░░▓▓▓▓▓░░░░▒░░░░░▒░░░░░░░░░░▒░░░░▒░░░░░░░
░░░░▓░▒▒▒░░░░░░░░░░▒░░░░░░░░░░▓▓▓▒░░░░░░░░░▒░░░░▓░░░░░▓▓░░▒░
░░▓▓░░░░░░░▓░░▒░░░░░░░░░▒▒▒▒▒░░░░░░░░▒░▒▒░░░░░▓▓░░░░▓▓░░░░░░


               ╔═════════════════════════════╗
               ║ > Welcome to SkiOS v1.0.0   ║
               ║                             ║
               ║ > Please provide the        ║
               ║   master key to start       ║
               ║   the ski lift              ║
               ║                             ║
               ║ (format 0x1234567812345678) ║
               ║                             ║
               ╚═════════════════════════════╝

                    Please input your key
                    > gctf{V3r1log_ISnT_SO_H4rd_4fTer_4ll_!1!}
```
