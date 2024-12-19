from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
import random
import string

class PasswordApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("password_generator.ui", self)

        self.centralwidget.setContentsMargins(20, 20, 20, 20)

        self.pushButton_generate.clicked.connect(self.generate_password)
        self.pushButton_copy.clicked.connect(self.copy_password)
        self.pushButton_evaluate.clicked.connect(self.evaluate_password_strength)

    def generate_password(self):
        try:
            length = self.spinBox_length.value()
            use_numbers = self.checkBox_numbers.isChecked()
            use_uppercase = self.checkBox_uppercase.isChecked()
            use_symbols = self.checkBox_symbols.isChecked()

            char_pool = string.ascii_lowercase
            if use_numbers:
                char_pool += string.digits
            if use_uppercase:
                char_pool += string.ascii_uppercase
            if use_symbols:
                char_pool += "!@#$%^&*()-_=+<>?"

            password = ''.join(random.choice(char_pool) for _ in range(length))
            current_text = self.textEdit_password.toPlainText()
            if current_text:
                new_text = f"{password}\n{current_text}"
            else:
                new_text = password
            self.textEdit_password.setPlainText(new_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

    def copy_password(self):
        text = self.textEdit_password.toPlainText()
        passwords = text.split('\n')
        if passwords:
            last_password = passwords[0]
            clipboard = QApplication.clipboard()
            clipboard.setText(last_password)
            QMessageBox.information(self, "Успех", "Пароль скопирован в буфер обмена!")
        else:
            QMessageBox.warning(self, "Ошибка", "Нет пароля для копирования!")

    def evaluate_password_strength(self):
        password = self.lineEdit_evaluate.text()
        if not password:
            QMessageBox.warning(self, "Ошибка", "Введите пароль для оценки!")
            return

        score = 0
        if len(password) >= 8:
            score += 1
        if any(char.isupper() for char in password):
            score += 1
        if any(char.islower() for char in password):
            score += 1
        if any(char.isdigit() for char in password):
            score += 1
        if any(char in "!@#$%^&*()-_=+<>?" for char in password):
            score += 1

        if score <= 1:
            strength = "Очень слабый"
        elif score == 2:
            strength = "Слабый"
        elif score == 3:
            strength = "Средний"
        elif score == 4:
            strength = "Сильный"
        else:
            strength = "Очень сильный"

        self.label_result.setText(f"Надёжность: {strength}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordApp()
    window.show()
    sys.exit(app.exec_())
