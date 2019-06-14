# Overview

## ID: aws_2
This is the explanation of the regex.

### Regular expression
| Python | LDS (Java) |
|--------|------|
|`(?:aws).{0,100}?(:|=|=>|->)\s*\"?(?<![A-Za-z0-9\/+=])[A-Za-z0-9\/+=]{40}(?![A-Za-z0-9\/+=])\"?`   |`"""(?i:aws).{0,100}?(:|=|=>|->)\s*"?(?<![A-Za-z0-9\/+=])[A-Za-z0-9\/+=]{40}(?![A-Za-z0-9\/+=])"?"""` |

### Notes
Reliant on codestyle. Requires `aws` in the 100 chars preceding fixed length 40 char base64 string, and whitespace surrounding `:`,`=`,`=>`,or `->`.
### Improvements
### Should match

#leak-detection-ignore
`aws_secret_access_key = H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA`
`aws_secret_access_key="H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA"`
`aws_secret_access_key = "H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA"`


### Should not match

`secret_key: H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA`
`amazon_secret_key = H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA`
`access_key = H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA`
`secret_access_key = H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA`
`aws_secret_access_key=H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA`
`wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`
`wJalrXUtnFEMI/K7MDENG/bPxRfiCY4e+TESTKEY(?i:aws).{0,100}?(:|=|=>|->)\s*"?(?<![A-Za-z0-9\/+=])[A-Za-z0-9\/+=]{40}(?![A-Za-z0-9\/+=])"?`
`aws_secret_access_key = X12345MEuati12345ed+voyz/UeJ560Bu0cgJcaac` - more than 40 chars
`aws_secret_access_key = X12345MEuati12345ed+voyz/UeJ560cgJcaac` - fewer than 40 chars
`aws_secret_access_key = H5xnFhnR3H/o6nrcfoMLR9VfOl*OY17pa/+PchnA` - contains non-base64 chars



## id = cert_1:

### Regular expression
| Python | LDS (Java) |
|--------|------|
|`-----(BEGIN|END).*?PRIVATE.*?-----`   |`"""-----(BEGIN|END).*?PRIVATE.*?-----"""` |

### Notes
Case sensitive.

### Should match

`-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCqGKlkO1De2zhZj6+H0qtjTkVxwTCpvKe4eCZ0FPqri0cb2JZfXJ/DgYSF6vUp
wmJG8wVQZKjeGcjDOL5UlsuusFncCzWBQ7RKNUSesmQRMSGkVb1/3j+skZ6UtW+5u09lHNsj6tQ5
1sfSPrCBkedbNf0Tp0GbMJDyG4e9T04ZZwIDAQABAoGAFijko56+qGyN8M0RVyaRAXz++xTqHBLh
3tx4VgMtrQ+WEgCjhoTwo23KMBAuJGSYnRmoBZM3lMfTKevIkAidPExvYCdm5dYq3XToLkkLv5L2
pIDVOFMDG+KESnAFV7l2c+cnsRKW0+b6f8mR1CJzZuxVLL6Q02fvLi55/mbSYxECQQDeAw6fiIQX
GukBI4eMZZt4nscy2o12KyYner3VpoeE+Np2q+Z3pvAMd/aNzQ/W9WaI+NRfcxUJrmfPwIGm63il
AkEAxCL5HQb2bQr1ByorcMWm/hEP2MZzROV73yF41hPsRC9m66KrheO9HPTJuo3/9s5p+sqGxOlF
L0NDt4SkosjgGwJAFeryR1uZ/wPJjj611cdBcztlPdqoxssQGnh85BzCj/u3WqBpE2vjvyyvyI5k
X6zk7S0ljKtt2jny2+00VsBerQJDQJGC1Mg5Oydo5NwD6BiROrPxGo2bpTbu/fhrT8ebHkTz2epl
f4AQQSQzY1oZMVX8i1j5WUTLPz2yLJIBQVdXqhMCQBGoiuSoSjafUhV7i1cEGpb88h5NBYZzWXGZ
37sJ5QsW+sJyoNdy3xH8vdXhzU7eT82D6X/scw9RZz+/6rCJ4p0=
-----END RSA PRIVATE KEY-----`

`-----BEGIN DSA PRIVATE KEY-----
MIIBvAIBAAKBgQDzKBcwISunTYfBjqmSRi+3REP3KXtxZm+sl+iyGnXNdLxMqsDR
Z6T1FxaReGkL2oqrv0ERNHO/UUriZA6wFJD8OJvUIeFPtZx30zFIB6b5E/ogDP7C
IE2sdfE0sTdMygllSJsjOscH1UIbEmp6GUljZAyQXRoGzRFTd9olvefyEQIVAPBE
dsdXY0jpDThzsbxhvnU14w+3AoGBANFAAwwF9UpDRlIWU1TAYzqVu3EPCL/uoMVv
7OzU/VE9ZldqqiAAEmc4LocwzbVJ2x1cTQ1wPGElfxDm6r8ej0nDGFBnWKfp5Svl
1rOIW77Xh3tSxZo4zkFOHNzLkiL1hRe9J4xR3+Es6h9KwbkUxqyscGnhrSjE9Urk
IdsUPMfUAoGAJFiR2z0FfGUMKTFc80PJQrXArvBwIzrg4y+013LDabtoej9b+RFh
7OJfY9o3C98iUvKcs/zE8AW+cSPz9kZpWXDQcueNWH0CucihpryPT5OboQnFky6j
3pea2ShzvJukJDXFU9fjOFg0vMgrsDWS9BHEUUy6+ba6RF8KBCCZjyoCFQCwAJyw
UFnpGR+DXojYIbA5s7lhgw==
-----END DSA PRIVATE KEY-----`

### Should not match

`ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6db7f3QFvoDSiaMq/vzvarl/6
nNxeK0y+FTt9FGAkD0Ew7JfdkKI7a0uhWRysaBebadZoTvmMFSr74U1hU8he4ehg
EO3dMmQOasw0PEaLjeNA1woK4WbqyzGUsZYN1IpjqDPurcUFj8GyDwqUukdDfJxS
kcWj0O0W5ddPQ4vR/gHPvd1XsHELRp9Awx2dbjuUnsVu5$`

## id = application_secret:

### Regular expression
| Python | LDS (Java) |
|--------|------|
|`application\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))`   |`“""application\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))"""` |

### Notes

_application.secret is deprecated as of Play 2.5, and was replaced by play.crypto.secret_

### Should match

`application.secret:"helloiamasecret"`
`application.secret:helloiamasecret`
`application.secret = "helloiamasecret"`
`application.secret = helloiamasecret`

### Should not match

`A sentence containing the words application secret.`
`A sentence containing the words application secret and also containing more words.`
`application.secret  :    ENC[GPPencrypted`
`application.secret:ENC[GPPencrypted`

## id = play_crypto_secret:

### Regular expression
| Python | LDS (Java) |
|--------|------|
|`play\.crypto\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))`   |`"""play\.crypto\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))"""` |

### Notes

_play.crypto.secret is deprecated as of Play 2.7, and is replaced by play.http.secret.key_

### Should match

`play.crypto.secret="QCY?tAnfk?aZ?iwrNwnxIlR6CTf:G3gf:90Latabg@5241AB:R5W:1uDFN];Ik@n"`
`play.crypto.secret:"zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k"`
`play.crypto.secret= "yNhI04vHs9<_HWbCl]20uT37=NGKJYY5:0Tg5?y<W<NoKnXWqmjcgZBec@rOxb^G"`
`play.crypto.secret -> "aPONxpsQVeaGGxhw9OnloQ"`
`play.crypto.secret="$!SECRET_KEY!$"`
`play.crypto.secret = "changeme"`

### Should not match

`A sentence containing the words play crypto secret. Then some more words.`
`play.crypto.secret  :    ENC[GPPencrypted`
`play.crypto.secret:ENC[GPPencrypted`
`play.crypto.secret=ENC[GPPencrypted`
`play.crypto.secret =   ENC[GPPencrypted`

`play.http.secret.key="QCY?tAnfk?aZ?iwrNwnxIlR6CTf:G3gf:90Latabg@5241AB:R5W:1uDFN];Ik@n"`


## id = cookie_deviceId_secret:

### Regular expression
| Python | LDS (Java) |
|--------|------|
|`cookie\.deviceId\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))`   |`"""cookie\.deviceId\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))"""` |

### Notes

### Should match

`cookie.deviceId.secret="helloiamasecret"`
`cookie.deviceId.secret = "helloiamasecret"`
`cookie.deviceId.secret:"helloiamasecret"`
`cookie.deviceId.secret ->    "helloiamasecret"`


### Should not match

`cookie.deviceId.secret: ENC[GPG`
`cookie.deviceId.secret = ENC[GPG`
`cookie.deviceId.secret -> ENC[GPG`
`A sentence with the words cookie deviceId secret.`


## id = sso_encryption_key:

### Regular expression
| Python | LDS (Java) |
|--------|------|
|`sso\.encryption\.key\s*(=|:|->)\s*(?!(\s*ENC\[))`   |`"""sso\.encryption\.key\s*(=|:|->)\s*(?!(\s*ENC\[))"""` |

### Notes

### Should match

`"sso.encryption.key  =     P5xsJ9Nt+quxDKzB4DeLfw=="`
`"sso.encryption.key=P5xsJ9Nt+quxDKzB4DeLfw=="`
`"sso.encryption.key = P5xsJ9Nt+quxDKzB4u4k2=33DeLfw=="`

### Should not match

`ssoEncryptionKey = "P5xsJ9Nt+quxDKzB4DeLfw=="`
`ssoEncryptionKey="L5xsJ4Nt+quxGZzB4DzLmw=="`
`"sso.encryption.key = ENC[GPG"`

## Other Values for Test Purposes
### Should not match

`privatekeys.p12`
`privatekeys.pfx`
`privatekeys.pkcs12`
`privatekeys.pem`
`privatekeys.jks`
`.bashrc`
`.zshrc`
`.bash_profile`
`.zsh_profile`
`.bash_aliases`
`.zsh_aliases`
`.credential`
`.credentials`
`_rsa`
`_dsa`
`_rsa.pub`
`_dsa.pub`

"privatekeys.p12"
"privatekeys.pfx"
"privatekeys.pkcs12"
"privatekeys.pem"
"privatekeys.jks"

SHA1: 752034292627FF19B2E7827C428C825D94882500
SHA256: 80e77c9c8dc2b91898f8c9a622116413afda889c3f9ac8ed31e85afd41e182ec
SHA512: 9c36dc25250e73d395cbeb117019cb1287611b01fdec69d04462f7ab7d236b457276d4ecf23702148e0dad8a097c07bca2ebff8e5fa1266792ad21a189f9e043
