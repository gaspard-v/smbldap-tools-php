import ctypes
import re
import secrets
import string


class Crypt:
    def __init__(self):
        upper_case = [char for char in string.ascii_uppercase]
        lower_case = [char for char in string.ascii_lowercase]
        numbers = [str(char) for char in range(10)]
        self.standard_char_array = upper_case + lower_case + numbers
        self.extended_char_array = self.standard_char_array + [".", "/"]
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
        array_size = len(self.extended_char_array)
        return_str = ""
        for bytes in salt_bytes:
            return_str += self.extended_char_array[int(bytes) % array_size]
        return return_str

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
        while True:
            id_algo, is_prefix, rounds_or_prefix, salt, hashed_password = (
                self._parse_shadow_hash(shadow_hash)
            )
            new_salt = self._gen_salt(len(salt))
            new_shadow_hash = f"${id_algo}${new_salt}$"
            if rounds_or_prefix:
                if is_prefix:
                    new_shadow_hash = f"${id_algo}${rounds_or_prefix}${new_salt}$"
                else:
                    new_shadow_hash = (
                        f"${id_algo}$rounds={rounds_or_prefix}${new_salt}$"
                    )
            hash = self.crypt(plain_password, new_shadow_hash)
            if hash == "*0":
                continue
            return hash
