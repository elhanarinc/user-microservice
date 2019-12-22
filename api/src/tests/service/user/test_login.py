import unittest
import sys

from unittest.mock import Mock, ANY

sys.path.append("./..")
from app import app

from tests.builder.user_builder import UserBuilder
from service.user import login
from entity.user import User


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.user_repo = Mock()
        self.jwt = Mock()
        self.user = self.get_user()

        self.app_context = app.app_context()
        self.app_context.push()

        self.user = self.get_user()

        self.last_login_ip = ["127.0.0.1"]

    def tearDown(self):
        self.app_context.pop()

    @staticmethod
    def get_user():
        return User(
            UserBuilder()
                .with_username("elhanarinc")
                .with_name("Arinc")
                .with_surname("Elhan")
                .with_age(27)
                .with_email("elhanarinc@gmail.com")
                .with_password("$2b$12$3OKDxg/kpTvneu.3kmu96epgeY.kwPZPoBcE8F0xe.iAqina7hEgS")
                .build()
        )

    def test_user_repo_find_by_email_method_should_be_called_with_correct_params(self):
        email = "elhanarinc@gmail.com"
        password = "123456"

        self.user_repo.find_by_email.return_value = self.user

        login(email, password, self.last_login_ip, self.user_repo)

        self.user_repo.find_by_email.assert_called_with(email)

    def test_if_user_not_found_in_db(self):
        email = "elhanarinc123@gmail.com"
        password = "123456"

        self.user_repo.find_by_email.return_value = None

        with self.assertRaises(Exception) as context:
            login(email, password, self.last_login_ip, self.user_repo)

        exception = context.exception
        self.assertTrue("Wrong mail or password." in str(exception.message))
        self.assertTrue("401" in str(exception.status_code))

    def test_if_user_password_does_not_match(self):
        email = "elhanarinc@gmail.com"
        password = "1234567"

        self.user_repo.find_by_email.return_value = self.user

        with self.assertRaises(Exception) as context:
            login(email, password, self.last_login_ip, self.user_repo)

        exception = context.exception
        self.assertTrue("Wrong mail or password." in str(exception.message))
        self.assertTrue("401" in str(exception.status_code))

    def test_user_repo_update_last_login_data_method_should_be_called_with_correct_params(self):
        email = "elhanarinc@gmail.com"
        password = "123456"

        user = self.get_user()

        self.user_repo.find_by_email.return_value = user

        login(email, password, self.last_login_ip, self.user_repo)

        self.user_repo.update_last_login_data.assert_called_with(user, ANY)

    def test_if_user_login_successfully(self):
        email = "elhanarinc@gmail.com"
        password = "123456"

        self.user_repo.find_by_email.return_value = self.user

        login(email, password, self.last_login_ip, self.user_repo)

        self.assertEqual(self.user.last_login_ip, self.last_login_ip)

    def test_successful_login_must_return_jwt_token(self):
        email = "elhanarinc@gmail.com"
        password = "123456"

        self.user_repo.find_by_email.return_value = self.user

        result = login(email, password, self.last_login_ip, self.user_repo)

        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
