# All import
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPalette, QColor
import random
import string

# Fungsi untuk menghasilkan password acak
def generate_password():
    panjang_text = panjang_input.text()

    if not panjang_text:  # Check if the input field is empty
        QMessageBox.warning(main_window, "Input Required", "Silahkan masukkan panjang password terlebih dahulu.")
        return  # Stop execution of the function if input is empty

    try:
        panjang = int(panjang_text)
        if panjang < 4 or panjang > 32:
            QMessageBox.warning(main_window, "Error", "Panjang password harus antara 4 dan 32!")
        else:
            characters = string.ascii_letters + string.digits + "!@#$%^&*"
            password = ''.join(random.choices(characters, k=panjang))
            long_pass.setText(password)

    except ValueError:
        QMessageBox.warning(main_window, "Error", "Masukkan angka yang valid!")

# Fungsi untuk menghapus password
def clear_password():
    long_pass.clear()
    panjang_input.clear()
    placeholder_label.show()  # Tampilkan kembali placeholder

# Fungsi untuk menyalin password ke clipboard
def copy_password():
    password_text = long_pass.text()  # Get the password text

    if password_text:  # Check if the password field is not empty
        clipboard = QApplication.clipboard()
        clipboard.setText(password_text)
        QMessageBox.information(main_window, "Copied", "Password telah disalin ke clipboard!")
    else:
        QMessageBox.warning(main_window, "No Password", "Tidak ada password untuk disalin.  Generate password terlebih dahulu.")

# Fungsi untuk mengupdate placeholder
def update_placeholder():
    if panjang_input.text():
        placeholder_label.hide()
    else:
        placeholder_label.show()

# Main app objects and settings
app = QApplication([])
app.setStyle("Fusion")

# Custom color palette
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.Highlight, QColor(255, 127, 0))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)

main_window = QWidget()
main_window.setWindowTitle("Password Creator")
main_window.setFont(QFont("Segoe UI", 10))
main_window.resize(QSize(350, 600))
main_window.setStyleSheet("""
    QWidget {
        background-color: #353535;
    }
    QLabel#title {
        font: bold 20pt 'Segoe UI';
        color: #ff7f00;
        padding: 15px;
    }
""")

# Create all app objects
title = QLabel("PASSWORD GENERATOR")
title.setObjectName("title")

panjang_input = QLineEdit()
panjang_input.setFont(QFont("Segoe UI", 12))
panjang_input.setAlignment(Qt.AlignCenter)
panjang_input.setStyleSheet("""
    QLineEdit {
        background-color: #252525;
        border: 2px solid #555;
        border-radius: 5px;
        color: white;
        padding: 10px;
        margin: 10px 50px;
    }
    QLineEdit:focus {
        border: 2px solid #ff7f00;
    }
""")
panjang_input.textChanged.connect(update_placeholder)  # Update placeholder on text change

# Placeholder label
placeholder_label = QLabel("Masukkan panjang password (4-32)")
placeholder_label.setFont(QFont("Segoe UI", 12))
placeholder_label.setStyleSheet("""
    QLabel {
        color: #888888; /* Warna placeholder */
        padding: 10px;  /* Keep padding for text inside the label */
    }
""")
placeholder_label.setAlignment(Qt.AlignCenter)


long_pass = QLineEdit()
long_pass.setFont(QFont("Consolas", 14))
long_pass.setAlignment(Qt.AlignCenter)
long_pass.setReadOnly(True)  # Make the QLineEdit read-only
long_pass.setStyleSheet("""
    QLineEdit {
        background-color: #252525;
        border: 2px solid #555;
        border-radius: 5px;
        color: #ff7f00;
        padding: 12px;
        margin: 10px 50px;
        letter-spacing: 2px;
    }
""")

# Tombol Create, Clear, dan Copy
create = QPushButton("Generate")
create.setFont(QFont("Segoe UI", 12))
create.setStyleSheet("""
    QPushButton {
        background-color: #ff7f00;
        color: black;
        border: none;
        border-radius: 5px;
        padding: 12px 25px;
        margin: 10px;
    }
    QPushButton:hover {
        background-color: #ff9933;
    }
    QPushButton:pressed {
        background-color: #cc6600;
    }
""")

clear = QPushButton("Clear")
clear.setFont(QFont("Segoe UI", 12))
clear.setStyleSheet("""
    QPushButton {
        background-color: #555555;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 12px 25px;
        margin: 10px;
    }
    QPushButton:hover {
        background-color: #777777;
    }
    QPushButton:pressed {
        background-color: #333333;
    }
""")

copy = QPushButton("Copy")
copy.setFont(QFont("Segoe UI", 12))
copy.setStyleSheet("""
    QPushButton {
        background-color: #007acc;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 12px 25px;
        margin: 10px;
    }
    QPushButton:hover {
        background-color: #0099ff;
    }
    QPushButton:pressed {
        background-color: #005f99;
    }
""")

# Menghubungkan tombol dengan fungsi
create.clicked.connect(generate_password)
clear.clicked.connect(clear_password)
copy.clicked.connect(copy_password)

# Layout
main_layout = QVBoxLayout()
main_layout.addWidget(title, alignment=Qt.AlignCenter)

input_layout = QVBoxLayout()
input_layout.setSpacing(0)  # Remove spacing between widgets in this layout
input_layout.addWidget(placeholder_label)  # Add placeholder
input_layout.addWidget(panjang_input)  # Add input field
input_layout.addWidget(long_pass)        # Add password display

button_layout = QHBoxLayout()
button_layout.addWidget(create)
button_layout.addWidget(clear)
button_layout.addWidget(copy)  # Menambahkan tombol Copy

main_layout.addLayout(input_layout)
main_layout.addLayout(button_layout)
main_layout.setSpacing(20)
main_layout.setContentsMargins(30, 20, 30, 30)

main_window.setLayout(main_layout)

# Run and show
main_window.show()
app.exec_()