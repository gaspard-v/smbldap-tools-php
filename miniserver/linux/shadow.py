import spwd
import crypt
import io
from ..exceptions.shadow import WrongPasswordException, UnknowUserException

class Chpasswd:

    def __init__(
            self,
            username: str,
            old_password: str,
            new_password: str
    ) -> None:
        self.username = username
        self.old_password = old_password
        self.new_password = new_password


    def verify_password(self):
        try:
            user_entry = spwd.getspnam(self.username)
        except FileNotFoundError as err:
            raise UnknowUserException(self.username) from err
        encrypted_password = user_entry.sp_pwdp
        hash  = crypt.crypt(self.old_password, encrypted_password)
        if hash != encrypted_password:
            raise WrongPasswordException(self.username)
        return self

    def _create_new_hash(self):
        return crypt.crypt(self.new_password)
    
    def _new_shadow_file(self, shadow_file: io.TextIOWrapper, hashed_password: str) -> list[str]:
        new_lines: list[str] = []
        for line in shadow_file.readlines():
            fields = line.split(':')
            if fields[0] != self.username:
                new_lines.append(line)
                continue
            fields[1] = hashed_password
            new_line = ':'.join(fields)
            new_lines.append(new_line)
        return new_lines
            
    
    def _modify_shadow_file(self, hashed_password: str) -> list[str]:
        shadow_path = '/etc/shadow'
        new_lines: list[str] = []
        with io.open(shadow_path, 'r') as shadow_file:
            new_lines = self._new_shadow_file(shadow_file, hashed_password)
        with io.open(shadow_path, 'w') as shadow_file:
            shadow_file.writelines(new_lines)
        return new_lines
    
    def modify_password(self):
        hashed_password = self._create_new_hash()
        self._modify_shadow_file(hashed_password)
        return self
        