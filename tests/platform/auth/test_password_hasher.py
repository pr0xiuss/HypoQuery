from backend.platform.auth.infra.password_hasher_impl import (
    PasswordHasherImpl,
)


def test_hash_password():
    """
    Passwords are hashed successfully.
    """

    hasher = PasswordHasherImpl()

    hashed = hasher.hash("super-secret-password")

    assert hashed != "super-secret-password"


def test_verify_password():
    """
    A valid password is verified successfully.
    """

    hasher = PasswordHasherImpl()

    password = "super-secret-password"
    hashed = hasher.hash(password)

    assert hasher.verify(password, hashed)


def test_invalid_password():
    """
    Invalid passwords fail verification.
    """

    hasher = PasswordHasherImpl()

    hashed = hasher.hash("correct-password")

    assert not hasher.verify(
        "wrong-password",
        hashed,
    )