import bcrypt


def hash_password(password: str) -> str:
    return str(bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt()))
