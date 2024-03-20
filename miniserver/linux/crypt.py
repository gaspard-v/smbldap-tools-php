import ctypes

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
        
    def crypt(
        self, 
        plain_password: str, 
        old_password_string: str|bytes
    ):
        encoded_password = plain_password.encode()
        if type(old_password_string) == str:
            old_password_string = old_password_string.encode()
        self.libcrypt.crypt(encoded_password, old_password_string)