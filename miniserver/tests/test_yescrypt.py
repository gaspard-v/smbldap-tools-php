import unittest
from miniserver.linux.crypt import Crypt


class TestYescrypt(unittest.TestCase):
    def setUp(self) -> None:
        self.crypt = Crypt()
        self.password = "123"
        self.yescrypt_hash = (
            "$y$j9T$.nUhEXqsK3NGKot2lsLi0.$laympemwzaSDO29q/TySGRHm34.iYkVp3zaKsKXM1EC"
        )
        return super().setUp()

    def test_correct_password_verification(self):
        verif_yescrypt_hash = self.crypt.crypt(self.password, self.yescrypt_hash)
        self.assertEqual(self.yescrypt_hash, verif_yescrypt_hash)

    def test_incorrect_password_verification(self):
        # password for this hash is "1234"
        yescrypt_hash = (
            "$y$j9T$9HD3.Ho3S0jl8KUFSE0Rv1$m0kuPSS0obD3Re7H5qSA5pJvmcLjgHHJ24yWZ9PF/19"
        )
        verif_yescrypt_hash = self.crypt.crypt(self.password, yescrypt_hash)
        self.assertNotEqual(yescrypt_hash, verif_yescrypt_hash)

    def test_password_generator(self):
        new_hash = self.crypt.crypt_new(self.password, self.yescrypt_hash)
        self.assertEqual(new_hash, self.crypt.crypt(self.password, new_hash))


if __name__ == "__main__":
    unittest.main()
