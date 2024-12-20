import unittest
import string
from unittest.mock import MagicMock, patch
from password_app import PasswordApp
from PyQt5.QtWidgets import QApplication

app = QApplication([])

class TestPasswordApp(unittest.TestCase):
    def setUp(self):
        self.window = PasswordApp()

    def test_generate_password(self):
        self.window.spinBox_length.setValue(12)
        self.window.checkBox_numbers.setChecked(True)
        self.window.checkBox_uppercase.setChecked(True)
        self.window.checkBox_symbols.setChecked(True)
        self.window.generate_password()

        generated_passwords = self.window.textEdit_password.toPlainText().split('\n')
        self.assertTrue(any(char in string.ascii_uppercase for char in generated_passwords[0]))
        self.assertTrue(any(char in string.digits for char in generated_passwords[0]))      
        self.assertTrue(any(char in "!@#$%^&*()-_=+<>?" for char in generated_passwords[0]))


    def test_evaluate_password_strength(self):
        test_cases = {
            "abc123": "Слабый", 
            "A1b@1234": "Очень сильный", 
            "password": "Слабый", 
            "PASSWORD123!": "Очень сильный",
            "Passw0rd": "Очень сильный", 
        }

        for password, expected_strength in test_cases.items():
            with self.subTest(password=password):
                self.window.lineEdit_evaluate.setText(password)
                self.window.evaluate_password_strength()
                self.assertEqual(self.window.label_result.text(), f"Надёжность: {expected_strength}")



if __name__ == "__main__":
    unittest.main()
