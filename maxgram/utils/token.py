class TokenValidationError(Exception):
    pass


def validate_token(token: str) -> bool:
    """Validate MAX API token."""
    if not isinstance(token, str):
        msg = f"Token is invalid! It must be 'str' type instead of {type(token)} type."
        raise TokenValidationError(msg)

    if not token.strip():
        msg = "Token is invalid! It can't be empty."
        raise TokenValidationError(msg)

    return True
