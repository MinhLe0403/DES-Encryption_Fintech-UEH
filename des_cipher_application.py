import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QFrame, QTableWidget, QTableWidgetItem, QRadioButton, QSizePolicy)
from PyQt6.QtCore import Qt
from des_algorithmn import DES

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.des = DES()
        self.last_encrypted_text = "" #Dùng để lưu lại bản mã khi bấm giải mã
        
        self.setWindowTitle("DES cung Le Cong")
        self.setMinimumSize(800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 80, 30, 30)
        central_widget.setLayout(main_layout)
        
        title = QLabel("ỨNG DỤNG MÃ HÓA DES LÊ CÔNG")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; font-family: 'Montserrat'; color: #ffffff; margin-bottom: 50px;")
        main_layout.addWidget(title)
        
        input_frame = QFrame()
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10)
        input_frame.setLayout(input_layout)
        
        plaintext_layout = QHBoxLayout()
        plaintext_label = QLabel("Nhập bản tin M:")
        plaintext_label.setStyleSheet("font-size: 16px; font-family: 'Montserrat'; font-weight: bold;")
        self.plaintext_input = QLineEdit()
        self.plaintext_input.setStyleSheet("font-size: 16px; font-family: 'Montserrat'; font-weight: bold; padding: 8px;")
        plaintext_layout.addWidget(plaintext_label, 1)
        plaintext_layout.addWidget(self.plaintext_input, 2)
        input_layout.addLayout(plaintext_layout)
        
        key_layout = QHBoxLayout()
        key_label = QLabel("Nhập khóa K:")
        key_label.setStyleSheet("font-size: 16px; font-family: 'Montserrat'; font-weight: bold;")
        self.key_input = QLineEdit()
        self.key_input.setStyleSheet("font-size: 16px; font-family: 'Montserrat'; font-weight: bold; padding: 8px;")
        key_layout.addWidget(key_label, 1)
        key_layout.addWidget(self.key_input, 2)
        input_layout.addLayout(key_layout)
        
        main_layout.addWidget(input_frame)
        
        buttons_container = QHBoxLayout()
        self.encrypt_radio = QRadioButton("Mã hóa")
        self.decrypt_radio = QRadioButton("Giải mã")
        self.encrypt_radio.setChecked(True)
        self.encrypt_radio.setStyleSheet("font-size: 16px; font-family: 'Montserrat'; font-weight: bold;")
        self.decrypt_radio.setStyleSheet("font-size: 16px; font-family: 'Montserrat'; font-weight: bold;")
        
        buttons_container.addWidget(self.encrypt_radio)
        buttons_container.addWidget(self.decrypt_radio)
        
        button_style = """
            QPushButton {
                font-size: 16px; font-family: 'Montserrat'; font-weight: bold; padding: 10px;
                background-color: #ff529f; color: white; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ff72b0;
            }
            QPushButton:pressed {
                background-color: #ff318f;
            }
        """
        
        self.submit_btn = QPushButton("Thực hiện")
        self.submit_btn.setStyleSheet(button_style)
        self.submit_btn.clicked.connect(self.process_des)
        buttons_container.addWidget(self.submit_btn)
        
        self.genkey_btn = QPushButton("Sinh Khóa")
        self.genkey_btn.setStyleSheet(button_style)
        self.genkey_btn.clicked.connect(self.generate_key)
        buttons_container.addWidget(self.genkey_btn)
        
        main_layout.addLayout(buttons_container)
        
        result_layout = QHBoxLayout() 
        result_label = QLabel("Kết quả:")
        result_label.setStyleSheet("font-size: 16px; font-family: 'Montserrat'; font-weight: bold;")
        self.result_input = QLineEdit()
        self.result_input.setReadOnly(True)
        self.result_input.setStyleSheet("font-size: 16px; font-family: 'Montserrat'; font-weight: bold; padding: 8px;")
        result_layout.addWidget(result_label, 1)
        result_layout.addWidget(self.result_input, 2)
        
        main_layout.addLayout(result_layout)
        
        self.ki_table = QTableWidget(16, 2)
        self.ki_table.setHorizontalHeaderLabels(['Vòng', 'Khóa vòng'])
        self.ki_table.setStyleSheet("font-size: 14px; font-family: 'Montserrat';")
        main_layout.addWidget(self.ki_table)

    def process_des(self):
        key = self.key_input.text().upper()
        if self.encrypt_radio.isChecked():
            plaintext = self.plaintext_input.text().upper()
            if not plaintext or not key:
                self.result_input.setText("Nhập đầy đủ bản rõ và khóa.")
                return
            result = self.des.encrypt(plaintext, key)
            self.last_encrypted_text = result  # Lưu lại bản mã cuối cùng
            self.result_input.setText(result)
        else:
            if self.last_encrypted_text:
                result = self.des.decrypt(self.last_encrypted_text, key)
                self.result_input.setText(result)
                self.plaintext_input.setText(result)  # Tự động điền lại bản rõ
            else:
                self.result_input.setText("Không có dữ liệu để giải mã.")
        
        # Hiển thị khóa vòng lên bảng
        subkeys = self.des.generate_subkeys(key)
        for i in range(16):
            self.ki_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.ki_table.setItem(i, 1, QTableWidgetItem(self.des.binary_to_hex(subkeys[i])))

    def generate_key(self):
        key = ''.join(random.choices('0123456789ABCDEF', k=16))
        self.key_input.setText(key)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())