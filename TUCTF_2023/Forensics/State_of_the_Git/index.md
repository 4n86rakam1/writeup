# State of the Git [89 Solves]

## Description

> All the cool kids are embracing state of the art IAC technology, and we are rushing to catch up! We have a new system that we are testing out, but we are not sure how secure it is. Can you check it out for us?
>
> Attachments: tuctf-devops-2023.tar.gz

## Flag

TUCTF{73rr4f0rm_S7A73-1y_53cr375}

## Solution

Looking at branch and commit log.

```console
$ tar zxf tuctf-devops-2023.tar.gz

$ cd tuctf-devops-2023

$ git branch
  bugfix
  dev
  feature
  hotfix
* main
  release

$ git log --oneline release
(snip)
3122ad4 add - variables.tf
dafd396 add - do-ctf.tf
729267a add - token.md
c7ac66f jqnljvtngtrtpqdkvccfpqyskwnayzgdhurvuwdkxjtcldzhjcksiaagimzdyoflpodbgzfimxumbouesdkivaolamntydqtmwwj
410e87f release - variables.tf
f0ecec2 release - do-ctf.tf
0840e07 release - token.yml
(snip)
```

Most commit messages typically start with `add`, `release`, `delete`, or `modify`, but I found the commit that doesn't follow this pattern in release branch.

```console
$ git --no-pager show c7ac66f
commit c7ac66fbd99c8850706c99b27475222f8dfe3d29
Author: MrLadas <97653268+MrLadas@users.noreply.github.com>
Date:   Tue Nov 21 23:28:37 2023 +0000

    jqnljvtngtrtpqdkvccfpqyskwnayzgdhurvuwdkxjtcldzhjcksiaagimzdyoflpodbgzfimxumbouesdkivaolamntydqtmwwj

diff --git a/terraform.tfstate b/terraform.tfstate
new file mode 100644
index 0000000..955de90
--- /dev/null
+++ b/terraform.tfstate
@@ -0,0 +1,103 @@
+{
+  "version": 4,
+  "terraform_version": "1.6.4",
+  "serial": 3,
+  "lineage": "0d21a79d-34f7-89e7-57f4-9266570147f4",
+  "outputs": {},
+  "resources": [
+    {
+      "mode": "managed",
+      "type": "droplet",
+      "name": "ctfd-dev-01",
+      "provider": "provider[\"registry.terraform.io/digitalocean/digitalocean\"]",
+      "instances": [
+        {
+          "schema_version": 0,
+          "attributes": {
+            "arch": "amd64",
+            "bwlimit": 0,
+            "clone": null,
+            "clone_storage": null,
+            "cmode": "tty",
+            "console": true,
+            "cores": 1,
+            "cpulimit": 0,
+            "cpuunits": 1024,
+            "description": "",
+            "features": [],
+            "force": false,
+            "full": null,
+            "hagroup": "",
+            "hastate": "",
+            "hookscript": "",
+            "hostname": "ctfd-dev-01",
+            "id": "aws/ctfd-dev-01",
+            "ignore_unpack_errors": false,
+            "lock": "",
+            "memory": 512,
+            "mountpoint": [],
+            "nameserver": "",
+            "network": [
+              {
+                "bridge": "vmbr0",
+                "firewall": true,
+                "gw": "192.168.1.1",
+                "gw6": "",
+                "hwaddr": "BC:24:11:15:79:0A",
+                "ip": "192.168.5.250/16",
+                "ip6": "",
+                "mtu": 0,
+                "name": "eth0",
+                "rate": 0,
+                "tag": 0,
+                "trunks": "",
+                "type": "veth"
+              }
+            ],
+            "onboot": true,
+            "ostemplate": "",
+            "ostype": "ubuntu",
+            "password": "VFVDVEZ7NzNycjRmMHJtX1M3QTczLTF5XzUzY3IzNzV9Cg==", // ZG9wX3YxXzA3ZmJjODgwY2YwNTNhOTE5Nzk4MDdkZmFhZjhhZDVjOTg4MGFiYWUxZjhkZjJjY2VjZTk2Njk0MmFmNDE0MDgK < Change this before going !
+            "pool": "Production",
+            "protection": false,
+            "restore": false,
+            "rootfs": [
+              {
+                "acl": false,
+                "quota": false,
+                "replicate": false,
+                "ro": false,
+                "shared": false,
+                "size": "8G",
+                "storage": "do-block-storage",
+                "volume": "do-block-storage:ctfd-dev-01/rootfs"
+              }
+            ],
+            "searchdomain": "",
+            "ssh_public_keys": null,
+            "start": true,
+            "startup": "",
+            "swap": 512,
+            "tags": "",
+            "template": false,
+            "timeouts": null,
+            "tty": 2,
+            "unique": false,
+            "unprivileged": true,
+            "unused": []
+          },
+          "sensitive_attributes": [
+            [
+              {
+                "type": "get_attr",
+                "value": "password"
+              }
+            ]
+          ],
+          "private": "sdkawewgfjfakqpwoqpretwenfwejweahwhuqhewdfhewf"
+        }
+      ]
+    }
+  ],
+  "check_results": null
+}

$ echo -n VFVDVEZ7NzNycjRmMHJtX1M3QTczLTF5XzUzY3IzNzV9Cg== | base64 -d
TUCTF{73rr4f0rm_S7A73-1y_53cr375}

$ echo -n ZG9wX3YxXzA3ZmJjODgwY2YwNTNhOTE5Nzk4MDdkZmFhZjhhZDVjOTg4MGFiYWUxZjhkZjJjY2VjZTk2Njk0MmFmNDE0MDgK | base64 -d
dop_v1_07fbc880cf053a91979807dfaaf8ad5c9880abae1f8df2ccece966942af41408
```
