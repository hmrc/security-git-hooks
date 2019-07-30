import pytest
from security_git_hooks import secrets_filename

"""All comments at beginning of test sets correspond to id of leak detection rules per
https://github.com/hmrc/app-config-base/blob/master/leak-detection.conf"""


# filename_private_key_1


@pytest.mark.parametrize(
    "test_input,expected",
    [("fake.p12", r"\.p12$"), ("p12.txt", None), ("fake.p12.txt", None)],
)
def test_private_key_1_p12(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# filename_private_key_2


@pytest.mark.parametrize(
    "test_input,expected",
    [("fake.pfx", r"\.pfx$"), ("pfx.txt", None), ("fake.pfx.txt", None)],
)
def test_private_key_1_pfx(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# filename_private_key_3


@pytest.mark.parametrize(
    "test_input,expected",
    [("fake.pkcs12", r"\.pkcs12$"), ("pkcs12.txt", None), ("fake.pkcs12.txt", None)],
)
def test_private_key_3_pkcs12(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# filename_private_key_5


@pytest.mark.parametrize(
    "test_input,expected",
    [("fake.pem", r"\.pem$"), ("pem.txt", None), ("fake.pem.txt", None)],
)
def test_private_key_5_pem(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# filename_private_key_7


@pytest.mark.parametrize(
    "test_input,expected",
    [("fake_rsa", r"_rsa$"), ("rsa.txt", None), ("fake.rsa.pub", None)],
)
def test_private_key_7_rsa(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# filename_private_key_8


@pytest.mark.parametrize(
    "test_input,expected",
    [("fake_dsa", r"_dsa$"), ("dsa.txt", None), ("fake.dsa.pub", None)],
)
def test_private_key_8_dsa(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# filename_private_key_9


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("fake_ed25519", r"_ed25519$"),
        ("_ed25519.txt", None),
        ("fake_ed25519.pub", None),
    ],
)
def test_private_key_9_ed25519(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# filename_private_key_10


@pytest.mark.parametrize(
    "test_input,expected",
    [("fake_ecdsa", r"_ecdsa$"), ("_ecdsa.txt", None), ("fake_ecdsa.pub", None)],
)
def test_private_key_9_ed25519(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# filename_private_key_11


@pytest.mark.parametrize(
    "test_input,expected",
    [("fake.jks", r"\.jks$"), ("jks.txt", None), ("fake.jks.txt", None)],
)
def test_private_key_11_jks(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# shell_1


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (".bashrc", r"^\.?(bash|zsh)?rc$"),
        (".zshrc", r"^\.?(bash|zsh)?rc$"),
        (".bashrc.txt", None),
        (".zshrc.txt", None),
    ],
)
def test_shell_1_rc_config___REVIEW(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# shell_2


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (".bash_profile", r"^\.?(bash|zsh)_profile$"),
        (".zsh_profile", r"^\.?(bash|zsh)_profile$"),
        (".bash_profile.txt", None),
        (".zshrc.txt", None),
    ],
)
def test_shell_2_profile_config___REVIEW(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# shell_3


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (".bash_aliases", r"^\.?(bash|zsh)_aliases$"),
        (".zsh_aliases", r"^\.?(bash|zsh)_aliases$"),
        (".bash_aliases.txt", None),
        (".zsh_aliases.txt", None),
    ],
)
def test_shell_3_aliases_config___REVIEW(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# credential_1


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (".credential", r"^\.credential(s)?$"),
        (".credentials", r"^\.credential(s)?$"),
        ("credentials.txt", None),
        ("fake.credential.txt", None),
    ],
)
def test_credential_1_credential_credentials(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# credential_2


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (".githubenterprise", r"^\.githubenterprise$"),
        ("githubenterprise.txt", None),
        ("fake.githubenterprise.txt", None),
    ],
)
def test_credential_2_githubenterprise(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# credential_3


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (".keychain", r"^\.*keychain$"),
        ("keychain.txt", None),
        ("fake.keychain.txt", None),
    ],
)
def test_credential_3_keychain__REVIEW(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


# credential_4


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("keystore", r"^key(store|ring)$"),
        ("keyring", r"^key(store|ring)$"),
        ("keyring.txt", None),
        ("keystore.txt", None),
        ("fake.keyring.txt", None),
        ("fake.keystore.txt", None),
    ],
)
def test_credential_4_keystore_keyring(test_input, expected):
    assert secrets_filename.detect_match_against_filename(test_input) == expected


def test_main_pos():
    assert secrets_filename.main(["lol.txt"]) == 0


def test_main_neg():
    assert secrets_filename.main(["lol.pem"]) != 0
