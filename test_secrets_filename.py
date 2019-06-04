import pytest
import secrets_filename
import re

'''All comments at beginning of test sets correspond to id of leak detection rules per
https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf'''


# filename_private_key_1

def test_p12_extension_match():
    filename = "fake.p12"
    assert secrets_filename.detect_match_against_filename(filename) == "\.p12$"


def test_p12_in_filename_does_not_match():
    filename = "p12.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None

# filename_private_key_2

def test_pfx_extension_match():
    filename = "fake.pfx"
    assert secrets_filename.detect_match_against_filename(filename) == "\.pfx$"


def test_pfx_in_filename_does_not_match():
    filename = "pfx.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None


# filename_private_key_3

def test_pkcs12_extension_match():
    filename = "fake.pkcs12"
    assert secrets_filename.detect_match_against_filename(filename) == "\.pkcs12$"


def test_pkcs12_in_filename_does_not_match():
    filename = "pkcs12.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None


# filename_private_key_5

def test_pem_extension_match():
    filename = "fake.pem"
    assert secrets_filename.detect_match_against_filename(filename) == "\.pem$"


def test_pem_in_filename_does_not_match():
    filename = "pem.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None


# filename_private_key_7

def test_rsa_extension_match():
    filename = "fake_rsa"
    assert secrets_filename.detect_match_against_filename(filename) == "_rsa$"


def test_rsa_public_key_does_not_match():
    filename = "fake_rsa.pub"
    assert secrets_filename.detect_match_against_filename(filename) is None


# filename_private_key_8

def test_dsa_extension_match():
    filename = "fake_dsa"
    assert secrets_filename.detect_match_against_filename(filename) == "_dsa$"


def test_dsa_public_key_does_not_match():
    filename = "fake_dsa.pub"
    assert secrets_filename.detect_match_against_filename(filename) is None


# filename_private_key_9

def test_ed25519_extension_match():
    filename = "fake_ed25519"
    assert secrets_filename.detect_match_against_filename(filename) == "_ed25519$"


def test_ed25519_public_key_does_not_match():
    filename = "fake_ed25519.pub"
    assert secrets_filename.detect_match_against_filename(filename) is None


# filename_private_key_10

def test_ecdsa_extension_match():
    filename = "fake_ecdsa"
    assert secrets_filename.detect_match_against_filename(filename) == "_ecdsa$"


def test_ecdsa_public_key_does_not_match():
    filename = "fake_ecdsa.pub"
    assert secrets_filename.detect_match_against_filename(filename) is None


# filename_private_key_11
@pytest.mark.skip(reason="add to dict")
def test_jks_extension_match():
    filename = "fake.jks"
    assert secrets_filename.detect_match_against_filename(filename) == "jks"


def test_jks_in_filename_does_not_match():
    filename = "jks.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None


def test_bash_config_bashrc_match():
    filename = ".bashrc"
    assert secrets_filename.detect_match_against_filename(filename) == "^\.?(bash|zsh)?rc$"


def test_bashrc_in_filename_does_not_match():
    filename = ".bashrc.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None 


def test_zsh_config_zshrc_match():
    filename = ".zshrc"
    assert secrets_filename.detect_match_against_filename(filename) == "^\.?(bash|zsh)?rc$"


def test_zshrc_in_filename_does_not_match():
    filename = ".zshrc.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None 


def test_bash_config_bash_profile_match():
    filename = ".bash_profile"
    assert secrets_filename.detect_match_against_filename(filename) == "^\.?(bash|zsh)_profile$"


def test_bash_profile_in_filename_does_not_match():
    filename = ".bash_profile.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None 


def test_zsh_config_zsh_profile_match():
    filename = ".zsh_profile"
    assert secrets_filename.detect_match_against_filename(filename) == "^\.?(bash|zsh)_profile$"


def test_zsh_profile_in_filename_does_not_match():
    filename = ".zsh_profile.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None 


def test_bash_config_bash_aliases_match():
    filename = ".bash_aliases"
    assert secrets_filename.detect_match_against_filename(filename) == "^\.?(bash|zsh)_aliases$"


def test_bash_aliases_in_filename_does_not_match():
    filename = ".bash_aliases.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None 


def test_zsh_config_zsh_aliases_match():
    filename = ".zsh_aliases"
    assert secrets_filename.detect_match_against_filename(filename) == "^\.?(bash|zsh)_aliases$"


def test_zsh_aliases_in_filename_does_not_match():
    filename = ".zsh_aliases.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None 


def test_credential_extension_match():
    filename = ".credential"
    assert secrets_filename.detect_match_against_filename(filename) == "^\.credential(s)?$"


def test_credential_in_filename_does_not_match():
    filename = "credential.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None


def test_credentials_extension_match():
    filename = ".credentials"
    assert secrets_filename.detect_match_against_filename(filename) == "^\.credential(s)?$"


def test_credentials_in_filename_does_not_match():
    filename = "credentials.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None


def test_github_enterprise_extension_match():
    filename = ".githubenterprise"
    assert secrets_filename.detect_match_against_filename(filename) == "^\.githubenterprise$"


def test_github_enterprise_in_filename_does_not_match():
    filename = "githubenterprise.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None


def test_apple_keychain_extension_match():
    filename = ".keychain"
    assert secrets_filename.detect_match_against_filename(filename) == "^\.*keychain$"


def test_apple_keychain_in_filename_does_not_match():
    filename = "keychain.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None


def test_apple_login_keychain_in_filename_does_not_match___TO_REVIEW():
    filename = "login.keychain"
    assert secrets_filename.detect_match_against_filename(filename) is None


def test_keystore_match___TO_REVIEW():
    filename = "keystore"
    assert secrets_filename.detect_match_against_filename(filename) == "^key(store|ring)$"


def test_keystore_in_filename_does_not_match():
    filename = "keystore.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None


def test_keyring_match___TO_REVIEW():
    filename = "keyring"
    assert secrets_filename.detect_match_against_filename(filename) == "^key(store|ring)$"


def test_keyring_in_filename_does_not_match():
    filename = "keyring.txt"
    assert secrets_filename.detect_match_against_filename(filename) is None