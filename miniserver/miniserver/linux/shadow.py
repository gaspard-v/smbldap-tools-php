import spwd
from .crypt import Crypt
import io
from ..exceptions.shadow import WrongPasswordException, UnknowUserException
from ..utils.logger import log
from typing import Optional
import time


class Chpasswd:
    user_entry: Optional[spwd.struct_spwd]

    def __init__(self, username: str, old_password: str, new_password: str) -> None:
        self.username = username
        self.old_password = old_password
        self.new_password = new_password
        self.crypt = Crypt()
        self.user_entry = None

    def _get_user_entry(self):
        if self.user_entry:
            return
        try:
            self.user_entry = spwd.getspnam(self.username)
        except FileNotFoundError as err:
            raise UnknowUserException(self.username) from err

    def verify_password(self):
        self._get_user_entry()
        if not self.user_entry:
            raise Exception("No user entry!")
        encrypted_password = self.user_entry.sp_pwdp
        hash = self.crypt.crypt(self.old_password, encrypted_password)
        if hash != encrypted_password:
            raise WrongPasswordException(self.username)
        return self

    def _create_new_hash(self):
        self._get_user_entry()
        if not self.user_entry:
            raise Exception("No user entry!")
        encrypted_password = self.user_entry.sp_pwdp
        return self.crypt.crypt_new(self.new_password, encrypted_password)

    @staticmethod
    def _get_days_since_epoch():
        today = time.time()
        epoch_time = time.mktime(time.strptime("1970-01-01", "%Y-%m-%d"))
        days_since_epoch = (today - epoch_time) / (24 * 60 * 60)
        return int(days_since_epoch)

    def _new_shadow_file(
        self, shadow_file: io.TextIOWrapper, hashed_password: str
    ) -> list[str]:
        new_lines: list[str] = []
        username_idx = 0
        password_idx = 1
        days_epoch_idx = 2
        days_epoch = self._get_days_since_epoch()

        # TODO Add check for min and max password age and warning days!
        for line in shadow_file.readlines():
            fields = line.split(":")
            if fields[username_idx] != self.username:
                new_lines.append(line)
                continue
            fields[password_idx] = hashed_password
            fields[days_epoch_idx] = str(days_epoch)
            new_line = ":".join(fields)
            new_lines.append(new_line)
        return new_lines

    def _modify_shadow_file(self, hashed_password: str) -> list[str]:
        shadow_path = "/etc/shadow"
        new_lines: list[str] = []
        with io.open(shadow_path, "r") as shadow_file:
            new_lines = self._new_shadow_file(shadow_file, hashed_password)
        with io.open(shadow_path, "w") as shadow_file:
            shadow_file.writelines(new_lines)
        return new_lines

    def modify_password(self):
        hashed_password = self._create_new_hash()
        self._modify_shadow_file(hashed_password)
        log().info(f"{self.username} has modified its password!")
        return self
