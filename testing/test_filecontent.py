import pytest
import secrets_filecontent
import re

#AWS SECRET KEY MATCHES

#the regex for aws secret key test needs to be amended so this matches
def test_aws_secret_key_matches_with_colon_separator():
    aws_secret_key = "aws_secret_access_key:H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA"
    assert secrets_filecontent.detect_secret_in_line(aws_secret_key) == "aws_2"


def test_aws_secret_key_matches_with_equals_sign_separator______NOMATCH_____():
    aws_secret_key = "aws_secret_access_key=H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA"
    assert secrets_filecontent.detect_secret_in_line(aws_secret_key) == None


def test_aws_secret_key_matches_with_whitespace_and_colon_separator():
    aws_secret_key = "aws_secret_access_key :   H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA"
    assert secrets_filecontent.detect_secret_in_line(aws_secret_key) == "aws_2"


def test_aws_secret_key_matches_with_whitespace_and_equals_sign_separator():
    aws_secret_key = "aws_secret_access_key =   H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA"
    assert secrets_filecontent.detect_secret_in_line(aws_secret_key) == "aws_2"


def test_aws_secret_key_does_not_match_40_char_base64_string():
    aws_secret_key = "H5xnFhnR3H/o6nrcfoMLR9VfOlfOY17pa/+PchnA"
    assert secrets_filecontent.detect_secret_in_line(aws_secret_key) == None


def test_aws_secret_key_does_not_match_more_than_40_characters_in_key():
    aws_secret_key = "aws_secret_access_key = X12345MEuati12345ed+voyz/UeJ560Bu0cgJcaac"
    assert secrets_filecontent.detect_secret_in_line(aws_secret_key) == None


def test_aws_secret_key_does_not_match_fewer_than_40_characters_in_key():
    aws_secret_key = "aws_secret_access_key = X12345MEuati12345ed+voyz/UeJ560cgJcaac"
    assert secrets_filecontent.detect_secret_in_line(aws_secret_key) == None


def test_aws_secret_key_does_not_match_with_non_base64_characters():
    aws_secret_key = "aws_secret_access_key = H5xnFhnR3H/o6nrcfoMLR9VfOl*OY17pa/+PchnA"
    assert secrets_filecontent.detect_secret_in_line(aws_secret_key) == None


#CERT 1 RULE MATCHES

def test_cert_1_RSA_header_is_match():
    cert_1 = "-----BEGIN RSA PRIVATE KEY-----"
    assert secrets_filecontent.detect_secret_in_line(cert_1) == "cert_1"


def test_cert_1_RSA_footer_is_match():
    cert_1 = "-----END RSA PRIVATE KEY-----"
    assert secrets_filecontent.detect_secret_in_line(cert_1) == "cert_1"


def test_cert_1_DSA_header_is_match():
    cert_1 = "-----BEGIN DSA PRIVATE KEY----- "
    assert secrets_filecontent.detect_secret_in_line(cert_1) == "cert_1"


def test_cert_1_DSA_footer_is_match():
    cert_1 = "-----END DSA PRIVATE KEY-----"
    assert secrets_filecontent.detect_secret_in_line(cert_1) == "cert_1"


def test_cert_1_RSA_full_match():
    cert_1 = "-----BEGIN RSA PRIVATE KEY----- keycontent -----END RSA PRIVATE KEY-----"
    assert secrets_filecontent.detect_secret_in_line(cert_1) == "cert_1"


def test_cert_1_DSA_full_match():
    cert_1 = "-----BEGIN DSA PRIVATE KEY----- key content -----END RSA PRIVATE KEY-----"
    assert secrets_filecontent.detect_secret_in_line(cert_1) == "cert_1"


def test_cert_1_RSA_pub_key_does_not_match():
    cert_1 = "ssh-rsa public key content"
    assert secrets_filecontent.detect_secret_in_line(cert_1) == None


#APPLICATION SECRET RULE

def test_application_secret_matches_with_colon_separator():
    application_secret = "application.secret:\"helloiamasecret\""
    assert secrets_filecontent.detect_secret_in_line(application_secret) == "application_secret"


def test_application_secret_matches_with_equals_sign_separator():
    application_secret = "application.secret=\"helloiamasecret\""
    assert secrets_filecontent.detect_secret_in_line(application_secret) == "application_secret"


def test_application_secret_matches_with_whitespace_and_colon_separator():
    application_secret = "application.secret : \"helloiamasecret\""
    assert secrets_filecontent.detect_secret_in_line(application_secret) == "application_secret"


def test_application_secret_matches_with_whitespace_and_equals_sign_separator():
    application_secret = "application.secret = \"helloiamasecret\""
    assert secrets_filecontent.detect_secret_in_line(application_secret) == "application_secret"


def test_application_secret_doesnt_match_as_words_in_string():
    application_secret = "application secret."
    assert secrets_filecontent.detect_secret_in_line(application_secret) == None


# PLAY CRYPTO SECRET RULE

def test_play_crypto_secret_matches_with_colon_separator():
    play_crypto_secret = "play.crypto.secret:\"zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k\""
    assert secrets_filecontent.detect_secret_in_line(play_crypto_secret) == "play_crypto_secret"


def test_play_crypto_secret_matches_with_equals_sign_separator():
    play_crypto_secret = "play.crypto.secret=\"zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k\""
    assert secrets_filecontent.detect_secret_in_line(play_crypto_secret) == "play_crypto_secret"


def test_play_crypto_secret_matches_with_whitespace_and_colon_separator():
    play_crypto_secret = "play.crypto.secret :  \"zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k\""
    assert secrets_filecontent.detect_secret_in_line(play_crypto_secret) == "play_crypto_secret"


def test_play_crypto_secret_matches_with_whitespace_and_equals_sign_separator():
    play_crypto_secret = "play.crypto.secret =  \"zLiPolptzA5HLnRG9XAF6hQGP4QGQvEd82W27dzsI8HpFQRToMD7m8f78LQ0Ur7k\""
    assert secrets_filecontent.detect_secret_in_line(play_crypto_secret) == "play_crypto_secret"


def test_play_crypto_secret_matches_with_default_changeme_value():
    play_crypto_secret = "play.crypto.secret = \"changeme\""
    assert secrets_filecontent.detect_secret_in_line(play_crypto_secret) == "play_crypto_secret"


def test_play_crypto_secret_doesnt_match_when_encrypted_with_colon_separator():
    play_crypto_secret = "play.crypto.secret:ENC[GPPencrypted"
    assert secrets_filecontent.detect_secret_in_line(play_crypto_secret) == None


def test_play_crypto_secret_doesnt_match_when_encrypted_with_equals_sign_separator():
    play_crypto_secret = "play.crypto.secret=ENC[GPPencrypted"
    assert secrets_filecontent.detect_secret_in_line(play_crypto_secret) == None


def test_play_crypto_secret_doesnt_match_when_encrypted_with_whitespace_and_colon_separator():
    play_crypto_secret = "play.crypto.secret :  ENC[GPPencrypted"
    assert secrets_filecontent.detect_secret_in_line(play_crypto_secret) == None


def test_play_crypto_secret_doesnt_match_when_encrypted_with_whitespace_and_equals_sign_separator():
    play_crypto_secret = "play.crypto.secret =  ENC[GPPencrypted"
    assert secrets_filecontent.detect_secret_in_line(play_crypto_secret) == None


def test_play_crypto_secret_doesnt_match_as_words_in_string():
    play_crypto_secret = "play crypto secret."
    assert secrets_filecontent.detect_secret_in_line(play_crypto_secret) == None
#cookie_deviceId_secret rule


def test_cookie_deviceId_secret_matches_with_colon_separator():
    cookie_deviceId_secret = "cookie.deviceId.secret:\"helloiamasecret\""
    assert secrets_filecontent.detect_secret_in_line(cookie_deviceId_secret) == "cookie_deviceId_secret"


def test_cookie_deviceId_secret_matches_with_equals_sign_separator():
    cookie_deviceId_secret = "cookie.deviceId.secret=\"helloiamasecret\""
    assert secrets_filecontent.detect_secret_in_line(cookie_deviceId_secret) == "cookie_deviceId_secret"


def test_cookie_deviceId_secret_matches_with_whitespace_and_colon_separator():
    cookie_deviceId_secret = "cookie.deviceId.secret :  \"helloiamasecret\""
    assert secrets_filecontent.detect_secret_in_line(cookie_deviceId_secret) == "cookie_deviceId_secret"


def test_cookie_deviceId_secret_matches_with_whitespace_and_equals_sign_separator():
    cookie_deviceId_secret = "cookie.deviceId.secret =  \"helloiamasecret\""
    assert secrets_filecontent.detect_secret_in_line(cookie_deviceId_secret) == "cookie_deviceId_secret"


def test_cookie_deviceId_secret_doesnt_match_when_encrypted_with_colon_separator():
    cookie_deviceId_secret = "cookie.deviceId.secret:ENC[GPG"
    assert secrets_filecontent.detect_secret_in_line(cookie_deviceId_secret) == None


def test_cookie_deviceId_secret_doesnt_match_when_encrypted_with_equals_sign_separator():
    cookie_deviceId_secret = "cookie.deviceId.secret=ENC[GPG"
    assert secrets_filecontent.detect_secret_in_line(cookie_deviceId_secret) == None


def test_cookie_deviceId_secret_doesnt_match_when_encrypted_with_whitespace_and_colon_separator():
    cookie_deviceId_secret = "cookie.deviceId.secret :  ENC[GPG"
    assert secrets_filecontent.detect_secret_in_line(cookie_deviceId_secret) == None


def test_cookie_deviceId_secret_doesnt_match_when_encrypted_with_whitespace_and_equals_sign_separator():
    cookie_deviceId_secret = "cookie.deviceId.secret =  ENC[GPG"
    assert secrets_filecontent.detect_secret_in_line(cookie_deviceId_secret) == None


def test_cookie_deviceId_secret_doesnt_match_as_words_in_string():
    cookie_deviceId_secret = "cookie deviceId secret."
    assert secrets_filecontent.detect_secret_in_line(cookie_deviceId_secret) == None

#sso_encryption_key rule


def test_sso_encryption_key_matches_with_colon_separator():
    sso_encryption_key = "sso.encryption.key:P5xsJ9Nt+quxDKzB4DeLfw=="
    assert secrets_filecontent.detect_secret_in_line(sso_encryption_key) == "sso_encryption_key"


def test_sso_encryption_key_matches_with_equals_sign_separator():
    sso_encryption_key = "sso.encryption.key=P5xsJ9Nt+quxDKzB4DeLfw=="
    assert secrets_filecontent.detect_secret_in_line(sso_encryption_key) == "sso_encryption_key"


def test_sso_encryption_key_matches_with_whitespace_and_colon_separator():
    sso_encryption_key = "sso.encryption.key :  P5xsJ9Nt+quxDKzB4DeLfw=="
    assert secrets_filecontent.detect_secret_in_line(sso_encryption_key) == "sso_encryption_key"


def test_sso_encryption_key_matches_with_whitespace_and_equals_sign_separator():
    sso_encryption_key = "sso.encryption.key =  P5xsJ9Nt+quxDKzB4DeLfw=="
    assert secrets_filecontent.detect_secret_in_line(sso_encryption_key) == "sso_encryption_key"


def test_sso_encryption_key_doesnt_match_when_encrypted_with_colon_separator():
    sso_encryption_key = "sso.encryption.key:ENC[GPG"
    assert secrets_filecontent.detect_secret_in_line(sso_encryption_key) == None


def test_sso_encryption_key_doesnt_match_when_encrypted_with_equals_sign_separator():
    sso_encryption_key = "sso.encryption.key=ENC[GPG"
    assert secrets_filecontent.detect_secret_in_line(sso_encryption_key) == None


def test_sso_encryption_key_doesnt_match_when_encrypted_with_whitespace_and_colon_separator():
    sso_encryption_key = "sso.encryption.key :  ENC[GPG"
    assert secrets_filecontent.detect_secret_in_line(sso_encryption_key) == None


def test_sso_encryption_key_doesnt_match_when_encrypted_with_whitespace_and_equals_sign_separator():
    sso_encryption_key = "sso.encryption.key =  ENC[GPG"
    assert secrets_filecontent.detect_secret_in_line(sso_encryption_key) == None


def test_sso_encryption_key_doesnt_match_as_words_in_string():
    sso_encryption_key = "sso encryption key."
    assert secrets_filecontent.detect_secret_in_line(sso_encryption_key) == None


#LOGIC TESTS BLEUGH


