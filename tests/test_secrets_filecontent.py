import pytest
import os

from security_git_hooks import secrets_filecontent

"""All comments at beginning of test sets 
correspond to id of leak detection rules per 
 https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf"""

my_path = os.path.abspath(os.path.dirname(__file__))

minimal = os.path.join(my_path, "resources/minimal.yaml")

# aws_secret_access_key


@pytest.mark.parametrize(
    "line, file, expected",
    [
        (
            "aws_secret_access_key:H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA",
            "afile.py",
            "aws_secret_access_key",
        ),
        (
            "aws_secret_access_key :   H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA",
            "afile.txt",
            "aws_secret_access_key",
        ),
        (
            "aws_secret_access_key =   H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA",
            "afile.md",
            "aws_secret_access_key",
        ),
        (
            "aws_secret_access_key=H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA",
            "afile.py",
            None,
        ),
        ("H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA", "afile.py", None),
        (
            "aws_secret_access_key = X12345MEuati12345ed+voyz/UeJ560Bu0cgJcaac",
            "afile.py",
            None,
        ),
        (
            "aws_secret_access_key = X12345MEuati12345ed+voyz/UeJ560cgJcaac",
            "afile.py",
            None,
        ),
        (
            "aws_secret_access_key = H5xnFhnR3H/o6nrcfoMLR9VfOl*OY17pa/+PchnA",
            "afile.py",
            None,
        ),
    ],
)
def test_aws_secret_access_key(line, file, expected):
    assert secrets_filecontent.detect_secret_in_line(line, file) == expected


# cert_1


@pytest.mark.parametrize(
    "line, file, expected",
    [
        ("-----BEGIN RSA PRIVATE KEY-----", "filename.txt", "cert_1"),
        ("-----END RSA PRIVATE KEY-----", "filename.md", "cert_1"),
        ("-----BEGIN DSA PRIVATE KEY-----", "filename.py", "cert_1"),
        ("-----END DSA PRIVATE KEY-----", "filename.js", "cert_1"),
        ("-----BEGIN RSA PRIVATE KEY-----", "kitchen.yml", None),
        ("-----BEGIN RSA PRIVATE KEY-----", "kitchen.yaml", None),
        (
            "-----BEGIN RSA PRIVATE KEY----- \n keycontent \n -----END RSA PRIVATE KEY-----",
            "filename.txt",
            "cert_1",
        ),
        (
            "-----BEGIN DSA PRIVATE KEY----- \n keycontent \n -----END RSA PRIVATE KEY-----",
            "filename.txt",
            "cert_1",
        ),
        ("ssh-rsa public key content", "filename.txt", None),
        ("ssh-dsa public key content", "filename.txt", None),
    ],
)
def test_cert_1(line, file, expected):
    assert secrets_filecontent.detect_secret_in_line(line, file) == expected


# application_secret


@pytest.mark.parametrize(
    "line, file, expected",
    [
        ('application.secret:"helloiamasecret"', "filename.txt", "application_secret"),
        ('application.secret="helloiamasecret"', "filename.txt", "application_secret"),
        (
            'application.secret : "helloiamasecret"',
            "filename.txt",
            "application_secret",
        ),
        (
            'application.secret = "helloiamasecret"',
            "filename.txt",
            "application_secret",
        ),
        ('application.secret = "helloiamasecret"', "filename.scala", None),
        ('application.secret = "helloiamasecret"', " /conf/application.conf", None),
        ("application secret", "filename.txt", None),
        ("application.secret", "filename.txt", None),
        ("application_secret", "filename.txt", None),
    ],
)
def test_application_secret(line, file, expected):
    assert secrets_filecontent.detect_secret_in_line(line, file) == expected


# play_crypto_secret


@pytest.mark.parametrize(
    "line, file, expected",
    [
        (
            'play.crypto.secret:"zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k"',
            "filename.txt",
            "play_crypto_secret",
        ),
        (
            'play.crypto.secret="zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k"',
            "filename.txt",
            "play_crypto_secret",
        ),
        (
            'play.crypto.secret :  "zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k"',
            "filename.txt",
            "play_crypto_secret",
        ),
        (
            'play.crypto.secret =  "zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k"',
            "filename.txt",
            "play_crypto_secret",
        ),
        ('play.crypto.secret = "changeme"', "filename.txt", "play_crypto_secret"),
        ('play.crypto.secret = "changeme"', "filename.scala", None),
        ('play.crypto.secret = "changeme"', " /conf/application.conf", None),
        ("play.crypto.secret:ENC[GPPencrypted", "filename.txt", None),
        ("play.crypto.secret=ENC[GPPencrypted", "filename.txt", None),
        ("play.crypto.secret :  ENC[GPPencrypted", "filename.txt", None),
        ("play.crypto.secret =  ENC[GPPencrypted", "filename.txt", None),
        ("play crypto secret.", "filename.txt", None),
    ],
)
def test_play_crypto_secret(line, file, expected):
    assert secrets_filecontent.detect_secret_in_line(line, file) == expected


# cookie_deviceId_secret


@pytest.mark.parametrize(
    "line, file, expected",
    [
        (
            'cookie.deviceId.secret:"helloiamasecret"',
            "filename.txt",
            "cookie_deviceId_secret",
        ),
        (
            'cookie.deviceId.secret="helloiamasecret"',
            "filename.txt",
            "cookie_deviceId_secret",
        ),
        (
            'cookie.deviceId.secret :  "helloiamasecret"',
            "filename.txt",
            "cookie_deviceId_secret",
        ),
        (
            'cookie.deviceId.secret =  "helloiamasecret"',
            "filename.txt",
            "cookie_deviceId_secret",
        ),
        ("cookie.deviceId.secret:ENC[GPG", "filename.txt", None),
        ("cookie.deviceId.secret=ENC[GPG", "filename.txt", None),
        ("cookie.deviceId.secret :  ENC[GPG", "filename.txt", None),
        ("cookie.deviceId.secret =  ENC[GPG", "filename.txt", None),
        ("cookie deviceId secret.", "filename.txt", None),
    ],
)
def test_cookie_deviceId_secret(line, file, expected):
    assert secrets_filecontent.detect_secret_in_line(line, file) == expected


# sso_encryption_key


@pytest.mark.parametrize(
    "line, file, expected",
    [
        (
            'sso.encryption.key:"P5xsJ9Nt+quxDKzB4DeLfw=="',
            "filename.txt",
            "sso_encryption_key",
        ),
        (
            "sso.encryption.key=P5xsJ9Nt+quxDKzB4DeLfw==",
            "filename.txt",
            "sso_encryption_key",
        ),
        (
            "sso.encryption.key :  P5xsJ9Nt+quxDKzB4DeLfw==",
            "filename.txt",
            "sso_encryption_key",
        ),
        (
            "sso.encryption.key =  P5xsJ9Nt+quxDKzB4DeLfw==",
            "filename.txt",
            "sso_encryption_key",
        ),
        ("sso.encryption.key:ENC[GPG", "filename.txt", None),
        ("sso.encryption.key=ENC[GPG", "filename.txt", None),
        ("sso.encryption.key :  ENC[GPG", "filename.txt", None),
        ("sso.encryption.key =  ENC[GPG", "filename.txt", None),
        ("sso encryption key.", "filename.txt", None),
    ],
)
def test_sso_encrpytion_key(line, file, expected):
    assert secrets_filecontent.detect_secret_in_line(line, file) == expected


def test_main():
    assert secrets_filecontent.main([minimal]) == 0
