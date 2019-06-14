import pytest
import secrets_filecontent
import re


"""All comments at beginning of test sets correspond to id of leak detection rules per
https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf"""


# aws_2


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("aws_secret_access_key:H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA", "aws_2"),
        ("aws_secret_access_key :   H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA", "aws_2"),
        ("aws_secret_access_key =   H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA", "aws_2"),
        ("aws_secret_access_key=H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA", None),
        ("H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA", None),
        ("aws_secret_access_key = X12345MEuati12345ed+voyz/UeJ560Bu0cgJcaac", None),
        ("aws_secret_access_key = X12345MEuati12345ed+voyz/UeJ560cgJcaac", None),
        ("aws_secret_access_key = H5xnFhnR3H/o6nrcfoMLR9VfOl*OY17pa/+PchnA", None),
    ],
)
def test_aws_2(test_input, expected):
    assert secrets_filecontent.detect_secret_in_line(test_input) == expected


# cert_1


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("-----BEGIN RSA PRIVATE KEY-----", "cert_1"),
        ("-----END RSA PRIVATE KEY-----", "cert_1"),
        ("-----BEGIN DSA PRIVATE KEY-----", "cert_1"),
        ("-----END DSA PRIVATE KEY-----", "cert_1"),
        (
            "-----BEGIN RSA PRIVATE KEY----- \n keycontent \n -----END RSA PRIVATE KEY-----",
            "cert_1",
        ),
        (
            "-----BEGIN DSA PRIVATE KEY----- \n keycontent \n -----END RSA PRIVATE KEY-----",
            "cert_1",
        ),
        ("ssh-rsa public key content", None),
        ("ssh-dsa public key content", None),
    ],
)
def test_cert_1(test_input, expected):
    assert secrets_filecontent.detect_secret_in_line(test_input) == expected


# application_secret


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ('application.secret:"helloiamasecret"', "application_secret"),
        ('application.secret="helloiamasecret"', "application_secret"),
        ('application.secret : "helloiamasecret"', "application_secret"),
        ('application.secret = "helloiamasecret"', "application_secret"),
        ("application secret", None),
        ("application.secret", None),
        ("application_secret", None),
    ],
)
def test_application_secret(test_input, expected):
    assert secrets_filecontent.detect_secret_in_line(test_input) == expected


# play_crypto_secret


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            'play.crypto.secret:"zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k"',
            "play_crypto_secret",
        ),
        (
            'play.crypto.secret="zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k"',
            "play_crypto_secret",
        ),
        (
            'play.crypto.secret :  "zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k"',
            "play_crypto_secret",
        ),
        (
            'play.crypto.secret =  "zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k"',
            "play_crypto_secret",
        ),
        ('play.crypto.secret = "changeme"', "play_crypto_secret"),
        ("play.crypto.secret:ENC[GPPencrypted", None),
        ("play.crypto.secret=ENC[GPPencrypted", None),
        ("play.crypto.secret :  ENC[GPPencrypted", None),
        ("play.crypto.secret =  ENC[GPPencrypted", None),
        ("play crypto secret.", None),
    ],
)
def test_play_crypto_secret(test_input, expected):
    assert secrets_filecontent.detect_secret_in_line(test_input) == expected


# cookie_deviceId_secret


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ('cookie.deviceId.secret:"helloiamasecret"', "cookie_deviceId_secret"),
        ('cookie.deviceId.secret="helloiamasecret"', "cookie_deviceId_secret"),
        ('cookie.deviceId.secret :  "helloiamasecret"', "cookie_deviceId_secret"),
        ('cookie.deviceId.secret =  "helloiamasecret"', "cookie_deviceId_secret"),
        ("cookie.deviceId.secret:ENC[GPG", None),
        ("cookie.deviceId.secret=ENC[GPG", None),
        ("cookie.deviceId.secret :  ENC[GPG", None),
        ("cookie.deviceId.secret =  ENC[GPG", None),
        ("cookie deviceId secret.", None),
    ],
)
def test_cookie_deviceId_secret(test_input, expected):
    assert secrets_filecontent.detect_secret_in_line(test_input) == expected


# sso_encryption_key


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ('sso.encryption.key:"P5xsJ9Nt+quxDKzB4DeLfw=="', "sso_encryption_key"),
        ("sso.encryption.key=P5xsJ9Nt+quxDKzB4DeLfw==", "sso_encryption_key"),
        ("sso.encryption.key :  P5xsJ9Nt+quxDKzB4DeLfw==", "sso_encryption_key"),
        ("sso.encryption.key =  P5xsJ9Nt+quxDKzB4DeLfw==", "sso_encryption_key"),
        ("sso.encryption.key:ENC[GPG", None),
        ("sso.encryption.key=ENC[GPG", None),
        ("sso.encryption.key :  ENC[GPG", None),
        ("sso.encryption.key =  ENC[GPG", None),
        ("sso encryption key.", None),
    ],
)
def test_sso_encrpytion_key(test_input, expected):
    assert secrets_filecontent.detect_secret_in_line(test_input) == expected
