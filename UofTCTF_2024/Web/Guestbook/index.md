# Guestbook [97 Solves]

## Description

> I made this cool guestbook for the CTF. Please sign it.
>
> Author: Ido
>
> Attachments: index.html

## Source Code

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Guestbook</title>
    <script async=false defer=false>
        fetch("https://script.google.com/macros/s/AKfycbyMdMLPsRtvXmcQN1V2yR3Zv_HYI1jvVqOCNAZpx7xgXqSflgwrtcveyUaGB8eTZwkM/exec?sheetId=1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ").then(x=>x.json()).then(x=>{
            x.slice(x.length-11).forEach(entry =>{
                const el = document.createElement("li");
                el.innerText = entry.Name + " - " + entry.Message
                document.getElementById("entries").appendChild(el)
            })
            document.getElementById("loading")?.remove();
        })
    </script>
</head>
<body>
<h1>
    Hi! I made this guestbook for my site, please sign it.
</h1>
<iframe name="dummyframe" id="dummyframe" style="display: none;"></iframe>
<h3 style="margin: 0">Last 10 user entries in the guestbook:</h3>
<p id="loading" style="margin: 0">Loading...</p>
<ul id="entries" style="margin: 0">
</ul>

<h3>Sign the guestbook:</h3>
<form method="POST" action="https://script.google.com/macros/s/AKfycbyMdMLPsRtvXmcQN1V2yR3Zv_HYI1jvVqOCNAZpx7xgXqSflgwrtcveyUaGB8eTZwkM/exec?sheetId=1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ">
  <input id="name" name="name" type="text" placeholder="Name" required>
  <input id="message" name="message" type="text" placeholder="Message" required>
  <button type="submit">Send</button>
</form>
</body>
</html> 
```

## Solution

The API URL is <https://script.google.com/macros/s/AKfycbyMdMLPsRtvXmcQN1V2yR3Zv_HYI1jvVqOCNAZpx7xgXqSflgwrtcveyUaGB8eTZwkM/exec?sheetId=1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ>.
This is the URL hosted by GAS (Google Apps Script) Web Apps.

The query parameter of the URL includes sheetId, which is believed to be the ID of a Google Spreadsheet.
So we can access the spreadsheet by <https://docs.google.com/spreadsheets/d/1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ/edit> URL.
Also, we can open GAS project attached the Spreadsheet: File > Make a copy > Open Attached Apps Script file named as `Untitled project`.
And get the source code of this GAS API.

This API returns values in a sheet named `sorted`.
Instead, I will try to get values from a sheet named `raw`.
Create a GAS project in my account and execute the following code:

```javascript
function doGet(e) {
  let file;
  try{
    file = SpreadsheetApp.openById("1PGFh37vMWFrdOnIoItnxiGAkIqSxlJDiDyklp9OVtoQ");  // change here: hard cording
  }
  finally{
    if(!file){
      return ContentService.createTextOutput(JSON.stringify({status:404, message:"invalid sheet ID"})).setMimeType(ContentService.MimeType.JSON);
    }
  }
  const sheet = file.getSheetByName('raw');  // change here: sorted -> raw
  const [headers, ...rows] = sheet.getDataRange().getValues();
  const res = rows.map(row => headers.reduce((a,x, i)=> {a[x] = row[i]; return a;},{}))
  return ContentService.createTextOutput(JSON.stringify(res)).setMimeType(ContentService.MimeType.JSON);
}
```

## Flag

uoftctf{@PP 5cRIP7 !5 s0 coOL}

## References

- [Web Apps  \|  Apps Script  \|  Google for Developers](https://developers.google.com/apps-script/guides/web)
