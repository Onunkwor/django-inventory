from django.test import TestCase
from django.contrib.auth.password_validation import validate_password
import os


class TryDjangoConfigTest(TestCase):
    def test_secret_key_string(self):
        SECRET_KEY = os.environ.get('SECRET_KEY')
        # self.assertIsNotNone(SECRET_KEY)
        try:
            is_strong = validate_password(SECRET_KEY)
        except Exception as e:
            self.fail(f'Bad Secret Key {e.messages}')
