# A.R.K. 3 [121 Solves]

## Description

> Meowdy. (Note: to speed up the process, only include entries containing "meow" in your attempts)
>
> Attachments: meow

## Flag

TUCTF{k3YCh41ns_AR3_sUp3r_c00L}

## Solution

Tools:

- [keychain2john](https://github.com/openwall/john/blob/bleeding-jumbo/run/keychain2john.py)
- [chainbreaker](https://github.com/n0fate/chainbreaker) - Mac OS X Keychain Forensic Tool is useful tool for this challenge. Linux user can use this tool, too.

```console
$ keychain2john meow > hash.txt

$ grep meow /usr/share/wordlists/rockyou.txt > meow.txt

$ john hash.txt --wordlist=meow.txt
Note: This format may emit false positives, so it will keep trying even after finding a possible candidate.
Using default input encoding: UTF-8
Loaded 1 password hash (keychain, Mac OS X Keychain [PBKDF2-SHA1 3DES 256/256 AVX2 8x])
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
coolcatmeow      (meow)
1g 0:00:00:00 DONE (2023-12-02 03:03) 9.090g/s 11700p/s 11700c/s 11700C/s leslie-meow..!#%&meow12345
Session completed.

$ git clone https://github.com/n0fate/chainbreaker.git && cd chainbreaker

$ python setup.py bdist_wheel -d dist
running bdist_wheel
(snip)
removing build/bdist.linux-x86_64/wheel

$ pip install -e .
(snip)
Successfully installed argparse-1.4.0 chainbreaker-3.0.3

$ python3 -m chainbreaker ../meow --dump-all --password coolcatmeow
2023-12-02 03:14:52,219 - INFO - Version - 3.0.3
2023-12-02 03:14:52,219 - INFO - Chainbreaker : https://github.com/n0fate/chainbreaker
2023-12-02 03:14:52,219 - INFO - Version: 3.0.3
2023-12-02 03:14:52,220 - INFO - Runtime Command: /root/ctf/TUCTF 2023/Misc/A.R.K. 3/chainbreaker/chainbreaker/__main__.py ../meow --dump-all --password coolcatmeow
2023-12-02 03:14:52,220 - INFO - Keychain: ../meow
2023-12-02 03:14:52,220 - INFO - Keychain MD5: c0bbdc431e82ceb82c6c62ae4571a52a
2023-12-02 03:14:52,220 - INFO - Keychain 256: 0653458b0fc08b21b1cbd91c8434320edc0063efbaea221d0723c1e75df927b3
2023-12-02 03:14:52,220 - INFO - Dump Start: 2023-12-02 03:14:52.219805
2023-12-02 03:14:52,227 - WARNING - [!] Certificate Table is not available
2023-12-02 03:14:52,227 - INFO - 1 Keychain Password Hash
2023-12-02 03:14:52,227 - INFO -        $keychain$*b'9196324d59f13ef6b20331e2e6d81da8993a02db'*b'34d065407b48d418'*b'976cb9617ec4e656d7fdbb097c525c9fc7502908aab1dc9aefbf40b24368ee8e78af756e91cc960a65d90f9be62e4240'
2023-12-02 03:14:52,227 - INFO -
2023-12-02 03:14:52,227 - INFO - 1 Generic Passwords
2023-12-02 03:14:52,227 - INFO -        [+] Generic Password Record
2023-12-02 03:14:52,227 - INFO -         [-] Create DateTime: 2023-11-27 22:43:23
2023-12-02 03:14:52,227 - INFO -         [-] Last Modified DateTime: 2023-11-27 22:43:23
2023-12-02 03:14:52,227 - INFO -         [-] Description:
2023-12-02 03:14:52,227 - INFO -         [-] Creator:
2023-12-02 03:14:52,227 - INFO -         [-] Type:
2023-12-02 03:14:52,227 - INFO -         [-] Print Name: b'flag'
2023-12-02 03:14:52,227 - INFO -         [-] Alias:
2023-12-02 03:14:52,227 - INFO -         [-] Account: b'flag'
2023-12-02 03:14:52,228 - INFO -         [-] Service: b'flag'
2023-12-02 03:14:52,228 - INFO -         [-] Password: TUCTF{k3YCh41ns_AR3_sUp3r_c00L}
2023-12-02 03:14:52,228 - INFO -
2023-12-02 03:14:52,228 - INFO -
2023-12-02 03:14:52,228 - INFO - 0 Internet Passwords
2023-12-02 03:14:52,228 - INFO - 0 Appleshare Passwords
2023-12-02 03:14:52,228 - INFO - 0 Private Keys
2023-12-02 03:14:52,228 - INFO - 0 Public Keys
2023-12-02 03:14:52,228 - INFO - 0 x509 Certificates
2023-12-02 03:14:52,228 - INFO - Chainbreaker : https://github.com/n0fate/chainbreaker
2023-12-02 03:14:52,228 - INFO - Version: 3.0.3
2023-12-02 03:14:52,228 - INFO - Runtime Command: /root/ctf/TUCTF 2023/Misc/A.R.K. 3/chainbreaker/chainbreaker/__main__.py ../meow --dump-all --password coolcatmeow
2023-12-02 03:14:52,228 - INFO - Keychain: ../meow
2023-12-02 03:14:52,228 - INFO - Keychain MD5: c0bbdc431e82ceb82c6c62ae4571a52a
2023-12-02 03:14:52,228 - INFO - Keychain 256: 0653458b0fc08b21b1cbd91c8434320edc0063efbaea221d0723c1e75df927b3
2023-12-02 03:14:52,228 - INFO - Dump Start: 2023-12-02 03:14:52.219805
2023-12-02 03:14:52,228 - INFO -        1 Keychain Password Hash
2023-12-02 03:14:52,228 - INFO -        1 Generic Passwords
2023-12-02 03:14:52,228 - INFO -        0 Internet Passwords
2023-12-02 03:14:52,228 - INFO -        0 Appleshare Passwords
2023-12-02 03:14:52,228 - INFO -        0 Private Keys
2023-12-02 03:14:52,228 - INFO -        0 Public Keys
2023-12-02 03:14:52,228 - INFO -        0 x509 Certificates
2023-12-02 03:14:52,228 - INFO - Dump End: 2023-12-02 03:14:52.228363
```
