import unittest

from utils.base_command import BaseCommand


class Login(BaseCommand):
    def test_login_happy_path(self):
        self.standard_login()

    def test_login_with_locked_out_user(self):
        self.login_locked_out_user()


if __name__ == '__main__':
    unittest.main()
