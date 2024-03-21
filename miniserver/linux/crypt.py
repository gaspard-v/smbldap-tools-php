import ctypes
import re
import secrets
import codecs


class Crypt:
    # Size in bytes
    YESCRYPT_SALT_LENGTH = 32
    BCRYPT_SALT_LENGTH = 16
    SHA_512_SALT_LENGTH = 12
    SHA_256_SALT_LENGTH = 12
    MD5_SALT_LENGTH = 6

    def __init__(self):
        self.libcrypt = ctypes.CDLL("libcrypt.so.1")
        self.libcrypt.crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        self.libcrypt.crypt.restype = ctypes.c_char_p

    def crypt(self, plain_password: str | bytes, shadow_hash: str | bytes):
        if isinstance(plain_password, str):
            plain_password = plain_password.encode()
        if isinstance(shadow_hash, str):
            shadow_hash = shadow_hash.encode()
        hashed_password = self.libcrypt.crypt(plain_password, shadow_hash)
        return hashed_password.decode()

    def _gen_salt(self, length_bytes: int) -> str:
        salt_bytes = secrets.token_bytes(length_bytes)
        return codecs.encode(salt_bytes, "hex").decode()

    def _parse_shadow_hash(self, shadow_hash: str):
        old_pattern = r"^\$(\d+)\$(?:rounds=(\d+)\$)?([./\w]+)\$([./\w]+)$"
        new_pattern = r"^\$(\w+)\$?([./\w]+)\$([./\w]+)\$([./\w]+)$"
        is_prefix = False
        pattern = old_pattern
        if shadow_hash.startswith("$y$"):
            pattern = new_pattern
        match = re.search(pattern, shadow_hash)
        if not match:
            raise ValueError("Incorrect shadow hash")
        id_algo, rounds_or_prefix, salt, hashed_password = match.groups()
        if pattern != old_pattern:
            is_prefix = True
        else:
            rounds_or_prefix = int(rounds_or_prefix) if rounds_or_prefix else None
        return (id_algo, is_prefix, rounds_or_prefix, salt, hashed_password)

    def crypt_new(self, plain_password: str, shadow_hash: str):
        id_algo, is_prefix, rounds_or_prefix, salt, hashed_password = (
            self._parse_shadow_hash(shadow_hash)
        )
        new_salt = self._gen_salt(len(salt))
        new_shadow_hash = f"${id_algo}${new_salt}$"
        if rounds_or_prefix:
            if is_prefix:
                new_shadow_hash = f"${id_algo}${rounds_or_prefix}${new_salt}$"
            else:
                new_shadow_hash = f"${id_algo}$rounds={rounds_or_prefix}${new_salt}$"
        return self.crypt(plain_password, new_shadow_hash)
