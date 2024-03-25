from miniclient import Miniclient
import unittest


class TestMiniserver(unittest.TestCase):
    def setUp(self) -> None:
        self.miniclient = Miniclient()
        self.message = {
            "username": "loled",
            "old_password": "123",
            "new_password": "123",
        }
        self.success_message = {
            "status_code": 200,
            "message": "Password modified successfully",
        }
        return super().setUp()

    def test_password_modification(self):
        recv_message = (
            self.miniclient.connect().send_message(self.message).recv_message()
        )
        self.miniclient.close()
        self.assertTrue(dict(self.success_message) == dict(recv_message))


if __name__ == "__main__":
    unittest.main()
