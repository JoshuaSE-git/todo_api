import bcrypt


def hash_password(password: str) -> str:
    return str(bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt()))


def valid_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        bytes(password, "utf-8"), hashed_password=bytes(hashed_password, "utf-8")
    )
