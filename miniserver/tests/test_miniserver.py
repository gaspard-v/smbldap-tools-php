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

    def test_wrong_old_password(self):
        message = self.message.copy()
        message["old_password"] = "1234"
        recv_message = self.miniclient.connect().send_message(message).recv_message()
        self.miniclient.close()
        self.assertNotEqual(dict(self.success_message), dict(recv_message))
        self.assertEqual(recv_message["status_code"], 400)
        self.assertEqual(recv_message["error"]["error_message"], "Invalid Credentials")


if __name__ == "__main__":
    unittest.main()
