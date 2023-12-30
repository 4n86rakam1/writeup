# ERROR REPORTING PROTOCOL [MODERATE]

## Description

> Can you identify the flag hidden within the error messages of this ICMP traffic?

## Solution

```console
$ tshark -r error_reporting.pcap -T json 'icmp.type == 0' | jq -r  '.[]._source.layers.icmp.data."data.data"' | tr -d '\n' | tr -d ':' | xxd -r -p > tmp.data

$ file tmp.data
tmp.data: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 500x500, components 3
```
