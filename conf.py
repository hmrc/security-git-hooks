_FILE_NAME_REGEXES = {
    "p12": r"\.p12$",
    "pfx": r"\.pfx$",
    "pkcs12": r"\.pkcs12$",
    "pem": r"\.pem$",
    "rsa": r"_rsa$",
    "dsa": r"_dsa$",
    "ed25519": r"_ed25519$",
    "ecdsa": r"_ecdsa$",
    "jks": r"\.jks$",
    "bash/zsh rc file": r"^\.?(bash|zsh)?rc$",
    "bash/zsh profile": r"^\.?(bash|zsh)_profile$",
    "bash/zsh aliases file": r"^\.?(bash|zsh)_aliases$",
    "credential(s) file": r"^\.credential(s)?$",
    "Github Enterprise file": r"^\.githubenterprise$",
    "Apple Keychain file": r"^\.*keychain$",
    "Keystore/Keyring file": r"^key(store|ring)$",
}

_FILE_CONTENT_REGEXES = {
    "aws_2": r"(?:aws).{0,100}?(:|=|=>|->)\s*\"?(?<![A-Za-z0-9\/+=])[A-Za-z0-9\/+=]{40}(?![A-Za-z0-9\/+=])\"?",
    "cert_1": r"-----(BEGIN|END).*?PRIVATE.*?-----",
    "application_secret": r"application\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))",
    "play_crypto_secret": r"play\.crypto\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))",
    "cookie_deviceId_secret": r"cookie\.deviceId\.secret\s*(=|:|->)\s*(?!(\s*ENC\[))",
    "sso_encryption_key": r"sso\.encryption\.key\s*(=|:|->)\s*(?!(\s*ENC\[))",
}