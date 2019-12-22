import unittest
import sys

from unittest.mock import Mock

sys.path.append("./..")
from app import app

from tests.builder.user_builder import UserBuilder
from service.user import register
from entity.user import User


class TestRegister(unittest.TestCase):
    def setUp(self):
        self.user_repo = Mock()
        self.jwt = Mock()
        self.user = self.get_user()

        self.app_context = app.app_context()
        self.app_context.push()

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
                .with_password("123456")
                .build()
        )

    def test_user_repo_should_be_called_with_correct_params(self):
        register(self.user, self.user_repo)

        self.user_repo.insert.assert_called_with(self.user)

    def test_successful_register_must_return_jwt_token(self):
        result = register(self.user, self.user_repo)

        self.assertIsInstance(result, str)

    def test_fields_of_user_should_be_set_correctly(self):
        register(self.user, self.user_repo)

        assert self.user.username == "elhanarinc"
        assert self.user.name == "Arinc"
        assert self.user.surname == "Elhan"
        assert self.user.email == "elhanarinc@gmail.com"
        assert self.user.age == 27
        self.assertIsInstance(self.user.ts_registration, int)
        self.assertIsInstance(self.user.ts_last_login, int)
        self.assertIsInstance(self.user.password, bytes)


if __name__ == '__main__':
    unittest.main()
