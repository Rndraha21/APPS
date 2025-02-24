# All imports
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QFileDialog, QStackedWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate, Qt, QRegExp, QSize
from PyQt5.QtGui import QRegExpValidator, QColor, QPixmap, QIcon
import sys
import hashlib
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class PasswordLineEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #d0d4dc;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                padding-right: 30px;  /* Make space for the icon */
            }
        """)

        self.show_password_button = QPushButton()
        eye_icon = QIcon(QPixmap("eye.png"))  # Pastikan path gambar benar
        self.show_password_button.setIcon(eye_icon)
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        self.show_password_button.setStyleSheet("QPushButton { border: none; background: transparent; }")
        self.show_password_button.setIconSize(QSize(20, 20))
        self.show_password_button.move(self.password_edit.x() + self.password_edit.width() - 30, self.password_edit.y() + 8)
        self.show_password_button.raise_()

        layout = QHBoxLayout()
        layout.addWidget(self.password_edit)
        self.setLayout(layout)

    def toggle_password_visibility(self):
        if self.show_password_button.isChecked():
            self.password_edit.setEchoMode(QLineEdit.Normal)
            eye_slash_icon = QIcon(QPixmap("eye-slash.png"))  # Pastikan path gambar benar
            self.show_password_button.setIcon(eye_slash_icon)
        else:
            self.password_edit.setEchoMode(QLineEdit.Password)
            eye_icon = QIcon(QPixmap("eye.png"))  # Pastikan path gambar benar
            self.show_password_button.setIcon(eye_icon)

    def text(self):
        return self.password_edit.text()

    def setPlaceholderText(self, text):
        self.password_edit.setPlaceholderText(text)

    def setFixedWidth(self, width):
        self.password_edit.setFixedWidth(width)
        self.show_password_button.move(self.password_edit.x() + self.password_edit.width() - 30, self.show_password_button.y())

    def clear(self):
        self.password_edit.clear()
        
class LoginPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(550, 700)  # Ukuran yang lebih besar
        self.setStyleSheet("""
            font-family: Arial, sans-serif;
        """)

        # Logo
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("Logo.png").scaled(150, 150))  # Logo lebih besar
        self.logo.setAlignment(Qt.AlignCenter)

        # Title
        self.title = QLabel("Tekno 24\nExpense Tracker")
        self.title.setWordWrap(True)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            color: #333;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 20px;
        """)

        # Username and Password
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #d0d4dc;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
        """)

        # Password dengan Show/Hide Button dalam container
        self.password_container = QWidget()
        self.password_container.setFixedWidth(250)  # Sama dengan username
        self.password_container.setStyleSheet("background: transparent;")

        password_inner_layout = QHBoxLayout(self.password_container)
        password_inner_layout.setContentsMargins(0, 0, 0, 0)  # Hilangkan margin

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedWidth(250)
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #d0d4dc;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
        """)

        self.show_password_button = QPushButton()
        eye_icon = QIcon(QPixmap("eye-slash.png")) 
        self.show_password_button.setIcon(eye_icon)
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        self.show_password_button.setStyleSheet("""
            QPushButton { 
                border: none; 
                background: transparent; 
                width: 30px;
            }
        """)

        password_inner_layout.addWidget(self.password)
        password_inner_layout.addWidget(self.show_password_button)
        # Login Button
        self.login_button = QPushButton("Login")
        self.login_button.setFixedWidth(250)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        
        self.register_button = QPushButton("Register")
        self.register_button.setFixedWidth(250)
        
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;  /* Blue color for register */
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px; /* Add some margin */
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.register_button.clicked.connect(self.show_registration_form)

        # Main Layout (for login) - add password_layout using addLayout
        self.login_widgets = [self.logo, self.title, self.username, self.password_container, self.login_button, self.register_button]
        
        self.login_layout = QVBoxLayout()
        self.login_layout.addStretch(1)
        for widget in self.login_widgets:
            if isinstance(widget, QWidget):  # Check if it's a QWidget
                self.login_layout.addWidget(widget, alignment=Qt.AlignCenter)
            elif isinstance(widget, QHBoxLayout):  # Check if it's a QHBoxLayout
                self.login_layout.addLayout(widget)  # Use addLayout
            if widget in [self.username, self.password]:  # Still access self.password even if it's in a layout
                widget.setFixedWidth(250)
        self.login_layout.addStretch(1)

        # Registration Form and Layout
        self.registration_form = RegistrationForm(self)  # Pass self (LoginPage) as parent
        self.registration_layout = QVBoxLayout()
        self.registration_layout.addWidget(self.registration_form)

        # Main (stacked) Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.login_layout)
        self.main_layout.addLayout(self.registration_layout)
        self.registration_form.hide()

        self.setLayout(self.main_layout)
    def toggle_password_visibility(self):
        if self.show_password_button.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
            eye_slash_icon = QIcon()  # Create a QIcon for eye-slash
            eye_slash_icon.addPixmap(QPixmap("eye.png"))
            self.show_password_button.setIcon(eye_slash_icon)
        else:
            self.password.setEchoMode(QLineEdit.Password)
            eye_icon = QIcon()  # Create a QIcon for eye
            eye_icon.addPixmap(QPixmap("eye-slash.png"))
            self.show_password_button.setIcon(eye_icon)
    def handle_login(self):
        username = self.username.text()
        password = self.password.text()

        query = QSqlQuery()
        query.prepare("SELECT password FROM users WHERE username = ?")
        query.addBindValue(username)
        if query.exec_() and query.next():
            stored_password = query.value(0)
            hashed_password = hashlib.sha256(password.encode()).hexdigest() # Hash input password
            if hashed_password == stored_password:
                self.parent().setCurrentIndex(1)  # Switch to main page
            else:
                QMessageBox.warning(self, "Error", "Password salah!")
        else:
            QMessageBox.warning(self, "Error", "Username tidak ditemukan!")

    def show_registration_form(self):
        for widget in self.login_widgets:  # Hide login widgets
            widget.hide()
        self.registration_form.show()  # Show registration form

class RegistrationForm(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.title = QLabel("Registration")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            color: #333;
            font-size: 28px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
            margin-bottom: 20px;
        """)

        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("Logo.png").scaled(150, 150))  # Logo lebih besar
        self.logo.setAlignment(Qt.AlignCenter)

        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Username")
        self.reg_username.setFixedWidth(250)
        self.reg_username.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #d0d4dc;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
        """)

        self.password_container = QWidget()
        self.password_container.setFixedWidth(250)  # Sama dengan username
        self.password_container.setStyleSheet("background: transparent;")

        password_inner_layout = QHBoxLayout(self.password_container)
        password_inner_layout.setContentsMargins(0, 0, 0, 0)  # Hilangkan margin

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFixedWidth(250)
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #d0d4dc;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
        """)

        self.show_password_button = QPushButton()
        eye_icon = QIcon(QPixmap("eye-slash.png")) 
        self.show_password_button.setIcon(eye_icon)
        self.show_password_button.setCheckable(True)
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        self.show_password_button.setStyleSheet("""
            QPushButton { 
                border: none; 
                background: transparent; 
                width: 30px;
            }
        """)
        password_inner_layout.addWidget(self.password)
        password_inner_layout.addWidget(self.show_password_button)
        
        self.confirm_password_container = QWidget()  # Container for confirm password
        self.confirm_password_container.setFixedWidth(250)
        self.confirm_password_container.setStyleSheet("background: transparent;")

        confirm_password_inner_layout = QHBoxLayout(self.confirm_password_container)
        confirm_password_inner_layout.setContentsMargins(0, 0, 0, 0)

        self.confirm_password = QLineEdit()
        self.confirm_password.setPlaceholderText("Konfirmasi Password")
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setFixedWidth(250)
        self.confirm_password.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #d0d4dc;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
            }
        """)
        self.show_confirm_password_button = QPushButton()  # Button for confirm password
        eye_icon = QIcon(QPixmap("eye-slash.png"))
        self.show_confirm_password_button.setIcon(eye_icon)
        self.show_confirm_password_button.setCheckable(True)
        self.show_confirm_password_button.clicked.connect(self.toggle_confirm_password_visibility)  # Connect to a new function
        self.show_confirm_password_button.setStyleSheet("""
            QPushButton { 
                border: none; 
                background: transparent; 
                width: 30px;
            }
        """)
        confirm_password_inner_layout.addWidget(self.confirm_password)
        confirm_password_inner_layout.addWidget(self.show_confirm_password_button)
        
        self.register_button = QPushButton("Daftar")
        self.register_button.clicked.connect(self.register_user)
        self.register_button.setFixedWidth(250)
        # ... (styling for QPushButton)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  /* Blue color for register */
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px; /* Add some margin */
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.back_button = QPushButton("Kembali")
        self.back_button.clicked.connect(self.hide_registration_form)
        self.back_button.setFixedWidth(250)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;  /* Blue color for register */
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 80px; /* Add some margin */
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.logo)
        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.reg_username, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.password_container, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.confirm_password_container, alignment=Qt.AlignCenter)  # Add the container
        self.main_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)
        self.main_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        self.setLayout(self.main_layout)
    
    def toggle_confirm_password_visibility(self):  # New function for confirm password
        if self.show_confirm_password_button.isChecked():
            self.confirm_password.setEchoMode(QLineEdit.Normal)
            eye_slash_icon = QIcon()
            eye_slash_icon.addPixmap(QPixmap("eye.png"))
            self.show_confirm_password_button.setIcon(eye_slash_icon)
        else:
            self.confirm_password.setEchoMode(QLineEdit.Password)
            eye_icon = QIcon()
            eye_icon.addPixmap(QPixmap("eye-slash.png"))
            self.show_confirm_password_button.setIcon(eye_icon)
    
    def toggle_password_visibility(self):
        if self.show_password_button.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
            eye_slash_icon = QIcon()  # Create a QIcon for eye-slash
            eye_slash_icon.addPixmap(QPixmap("eye.png"))
            self.show_password_button.setIcon(eye_slash_icon)
        else:
            self.password.setEchoMode(QLineEdit.Password)
            eye_icon = QIcon()  # Create a QIcon for eye
            eye_icon.addPixmap(QPixmap("eye-slash.png"))
            self.show_password_button.setIcon(eye_icon)
    
    def hide_registration_form(self):
        self.hide()  # Hide registration form
        login_page = self.parent()  # Get the parent (LoginPage)
        for widget in login_page.login_widgets:  # Access login widgets
            widget.show()
        login_page.username.clear()  # Clear username field
        login_page.password.clear()  # Clear password field
        # self.table.setRowCount(0)  # Clear the table when logging out  (If needed)
        
    def register_user(self):
        username = self.reg_username.text()
        password = self.password.text()
        confirm_password = self.confirm_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username dan password harus diisi.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Password dan konfirmasi password tidak cocok.")
            return

        # Hash the password before storing it
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        query = QSqlQuery()
        query.prepare("INSERT INTO users (username, password) VALUES (?, ?)")
        query.addBindValue(username)
        query.addBindValue(hashed_password) #Store the hashed password

        if query.exec_():
            QMessageBox.information(self, "Sukses", "Registrasi berhasil.")
            self.reg_username.clear()
            self.password.clear()
            self.confirm_password.clear()
            self.hide_registration_form() # Hide the form after successful registration
        else:
            QMessageBox.critical(self, "Error", "Gagal mendaftar: " + query.lastError().text())


    

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikasi Catatan Pengeluaran")
        self.setFixedSize(570, 700)

        # Stacked Widget untuk mengelola beberapa halaman
        self.stacked_widget = QStackedWidget(self)

        # Halaman Login
        self.login_page = LoginPage(self)
        self.stacked_widget.addWidget(self.login_page)

        # Halaman Utama (Pengeluaran)
        self.expense_page = QWidget()  # Ganti dengan implementasi halaman pengeluaran Anda
        self.stacked_widget.addWidget(self.expense_page)

        # Layout Utama
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

        # Inisialisasi halaman pengeluaran
        self.init_expense_page()

    def init_expense_page(self):
        # Main app objects & settings
        self.setFixedSize(570, 700)
        self.setWindowTitle("Aplikasi Catatan Pengeluaran")
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                font-family: 'Segoe';
            }
            QLabel#title {
                color: #2d3e50;
                font-size: 24px;
                font-weight: bold;
                padding: 20px 0;
                font-family: 'Segoe UI';
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QComboBox, QDateEdit {
                background: white;
                border: 1px solid #d0d4dc;
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                opacity: 0.9;
            }
                        #addButton {
                background-color: #4CAF50;
                color: white;
            }
            #deleteButton {
                background-color: #f44336;
                color: white;
            }
            #exportButton {
                background-color: #2196F3;
                color: white;
                font-size: 12px;
                padding: 8px;
            }
            QTableWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #d0d4dc;
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        # Widgets
        self.title = QLabel("Lacak Pengeluaran Anda")
        self.title.setObjectName("title")
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.date_box.setFixedWidth(150)
        self.date_box.setCalendarPopup(True)

        self.dropdown = QComboBox()
        self.dropdown.setFixedWidth(150)

        self.dropdown_method = QComboBox()
        self.dropdown_method.setFixedWidth(150)
        
        self.amount = QLineEdit()
        self.amount.setFixedWidth(150)
        self.amount.setAlignment(Qt.AlignRight)
        self.amount.setPlaceholderText("Rp 0")
        self.amount.textChanged.connect(self.format_amount)
        self.amount.setValidator(QRegExpValidator(QRegExp(r'[0-9]*'), self.amount))
        
        self.description = QLineEdit()
        self.description.setFixedWidth(150)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Tambah")
        self.delete_button = QPushButton("Hapus")
        self.export_button = QPushButton("📄 PDF")
        
        self.add_button.setObjectName("addButton")
        self.delete_button.setObjectName("deleteButton")
        
        self.export_button.setObjectName("exportButton")
        self.export_button.setFixedWidth(100)

        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)
        self.export_button.clicked.connect(self.export_to_pdf)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        # Add Logout Button
        self.logout_button = QPushButton("Keluar")  # Logout button
        self.logout_button.clicked.connect(self.logout)  # Connect to logout function
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;  /* Red for logout */
                color: white;
                border-radius: 8px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px; /* Add some margin */
            }
            QPushButton:hover {
                background-color: #d32f2f; /* Darker red on hover */
            }
        """)

        # Add Logout Button to Layout (e.g., Row 4 or a new row)
        # Table setup
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["No.", "Jenis Transaksi", "Tanggal", "Kategori", "Jumlah", "Keterangan"])
        self.table.setColumnHidden(0, True)  # Sembunyikan kolom ID
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setWordWrap(True)
        self.table.setColumnWidth(0, 10)
        self.table.setFixedWidth(550)

        # Layouts
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()
        self.row4 = QHBoxLayout()

        # Row 1
        self.row1.addWidget(QLabel("Tanggal:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Pilih Kategori:"))
        self.dropdown.setEditable(True)
        self.dropdown.lineEdit().setPlaceholderText("Pilih Kategori")
        self.dropdown.lineEdit().setReadOnly(True)  # Agar tidak bisa diketik
        self.dropdown.addItems(["Makanan", "Transportasi", "Sewa", "Belanja", "Hiburan", "Tagihan", "Lainnya"])
        self.dropdown.setCurrentIndex(-1)  # Membuat tampilan kosong
        self.row1.addWidget(self.dropdown)

        # Row 2
        self.row2.addWidget(QLabel("Jumlah:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Keterangan:"))
        self.description.setPlaceholderText("Masukkan keterangan")
        self.row2.addWidget(self.description)

        # Row 3
        self.row3.addWidget(QLabel("Jenis Transaksi:"))
        self.dropdown_method.setEditable(True)
        self.dropdown_method.lineEdit().setPlaceholderText("Pilih Metode")
        self.dropdown_method.lineEdit().setReadOnly(True)
        self.dropdown_method.addItems(["Cash", "Transfer", "BRI", "Dana", "GoPay", "QRIS", "Lainnya"])
        self.dropdown_method.setCurrentIndex(-1)
        self.row3.addWidget(self.dropdown_method)

        # Row 4
        self.row4.addLayout(button_layout)
        self.row4.addWidget(self.logout_button, alignment=Qt.AlignRight)

                # Combine layouts
        self.master_layout.addWidget(self.title, alignment=Qt.AlignCenter)
        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)
        self.master_layout.addLayout(self.row4)
        self.master_layout.addWidget(self.table)
        self.master_layout.addWidget(self.export_button, alignment=Qt.AlignRight)

        self.expense_page.setLayout(self.master_layout)
        self.load_table()

    def format_amount(self):
        cursor_pos = self.amount.cursorPosition()
        original_length = len(self.amount.text())
        
        clean_text = self.amount.text().replace("Rp", "").replace(".", "").strip()
        
        if clean_text:
            try:
                num = int(clean_text)
                formatted = "Rp {:,}".format(num).replace(",", ".")
                
                self.amount.blockSignals(True)
                self.amount.setText(formatted)
                
                new_pos = cursor_pos + (len(formatted) - original_length)
                self.amount.setCursorPosition(max(3, new_pos))
            except ValueError:
                pass
            finally:
                self.amount.blockSignals(False)

    def load_table(self):
        self.table.setRowCount(0)
        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        total = 0.0

        while query.next():
            expense_id = query.value(0)
            transaction_type = query.value(1)
            date = query.value(2)
            category = query.value(3)
            amount = query.value(4)
            description = query.value(5)

            try:
                amount_float = float(amount)
                formatted_amount = "Rp {:,.0f}".format(amount_float).replace(",", ".")
                total += amount_float
            except:
                formatted_amount = "Invalid amount"
            
            self.table.insertRow(row)
            
            # ID (hidden)
            item_number = QTableWidgetItem(str(expense_id))
            item_number.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item_number)

            # Jenis Transaksi dengan wrapping
            item_transaction = QTableWidgetItem(transaction_type)
            item_transaction.setFlags(item_transaction.flags() | Qt.TextWordWrap)
            self.table.setItem(row, 1, item_transaction)
            
            # Tanggal
            item_date = QTableWidgetItem(date)
            item_date.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, item_date)

            # Kategori
            self.table.setItem(row, 3, QTableWidgetItem(category))
            
            # Jumlah
            self.table.setItem(row, 4, QTableWidgetItem(formatted_amount))
            
            # Keterangan dengan wrapping
            item_desc = QTableWidgetItem(description)
            item_desc.setFlags(item_desc.flags() | Qt.TextWordWrap)
            self.table.setItem(row, 5, item_desc)
            
            row += 1

        # Tambah baris total
        total_row = self.table.rowCount()
        self.table.insertRow(total_row)
        
        total_item = QTableWidgetItem("Total Pengeluaran")
        total_item.setFlags(Qt.ItemIsEnabled)
        total_item.setBackground(QColor(79, 175, 80))
        total_item.setForeground(QColor(255, 255, 255))
        
        self.table.setItem(total_row, 1, total_item)
        self.table.setSpan(total_row, 1, 1, 3)

        formatted_total = "Rp {:,.0f}".format(total).replace(",", ".")
        self.table.setItem(total_row, 4, QTableWidgetItem(formatted_total))

    def delete_expense(self):
        selected_row = self.table.currentRow()
        total_rows = self.table.rowCount()
        
        if selected_row == -1:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih data yang akan dihapus!")
            return
            
        if selected_row == total_rows - 1:
            QMessageBox.warning(self, "Peringatan", "Tidak bisa menghapus baris total!")
            return

        expense_id = self.table.item(selected_row, 0).text()
        
        confirm = QMessageBox.question(
            self, 
            "Konfirmasi", 
            "Apakah Anda yakin ingin menghapus data ini?", 
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM expenses WHERE id = ?")
            query.addBindValue(expense_id)
            
            if not query.exec_():
                QMessageBox.critical(self, "Error", "Gagal menghapus data: " + query.lastError().text())
            else:
                self.load_table()
    def add_expense(self):
        transaction_type = self.dropdown_method.currentText()
        date = self.date_box.date().toString("dd-MM-yyyy")
        category = self.dropdown.currentText()
        amount_text = self.amount.text().replace("Rp", "").replace(".", "").strip()
        description = self.description.text()

        if not amount_text:
            QMessageBox.warning(self, "Error", "Jumlah tidak boleh kosong!")
            return
        elif not category:
            QMessageBox.warning(self, "Error", "Jangan lupa pilih kategori")
            return
        elif not description:
            QMessageBox.warning(self, "Error", "Jangan lupa isi keterangan!")
            return
        elif not transaction_type:
            QMessageBox.warning(self, "Error", "Jangan lupa pilih jenis transaksi")
            return

        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Error", "Format jumlah tidak valid!")
            return

        query = QSqlQuery()
        query.prepare("""
            INSERT INTO expenses (
                transaction_type, 
                date, 
                category, 
                amount, 
                description
            ) VALUES (?, ?, ?, ?, ?)
        """)
        
        query.addBindValue(transaction_type)
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        
        if not query.exec_():
            error_msg = query.lastError().text()
            QMessageBox.critical(self, "Error", f"Gagal menyimpan data:\n{error_msg}")
            return

        self.amount.clear()
        self.description.clear()
        self.load_table()

    def export_to_pdf(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            "Simpan PDF", 
            "", 
            "PDF Files (*.pdf)"
        )
        if not filename:
            return

        # Ambil data dari database
        query = QSqlQuery("SELECT transaction_type, date, category, amount, description FROM expenses")
        data = []
        headers = ["Jenis Transaksi", "Tanggal", "Kategori", "Jumlah", "Keterangan"]
        data.append(headers)
        total = 0.0

        while query.next():
            transaction_type = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)
            
            formatted_amount = "Rp {:,.0f}".format(amount).replace(",", ".")
            data.append([transaction_type, date, category, formatted_amount, description])
            total += amount

        # Tambah baris total
        data.append(["Total Pengeluaran", "", "", "Rp {:,.0f}".format(total).replace(",", "."), ""])

        # Buat PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title = Paragraph("<b>Laporan Pengeluaran</b>", styles["Title"])
        elements.append(title)
        
        # Buat tabel
        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-2), colors.HexColor('#f8f9fa')),
            ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#d0d4dc')),
            ('SPAN', (0,-1), (2,-1)),
            ('ALIGN', (-2,-1), (-1,-1), 'RIGHT'),
        ])
        table.setStyle(style)
        elements.append(table)
        
        doc.build(elements)
        QMessageBox.information(self, "Sukses", "PDF berhasil disimpan di:\n" + filename)
        
    def logout(self):
        confirm = QMessageBox.question(
                self,
                "Konfirmasi",
                "Apakah Anda yakin ingin keluar?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            self.stacked_widget.setCurrentIndex(0)  # Switch to login page
            self.login_page.username.clear()  # Clear username field (optional)
            self.login_page.password.clear()  # Clear password field (optional)
            self.table.setRowCount(0) # Clear the table when logging out
            # Optionally close the database connection here if you want to ensure it's closed
            # database.close()

# Database setup
def initialize_database():
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName("data.db")
    
    if not database.open():
        QMessageBox.critical(None, "Error", "Tidak bisa membuka database!")
        return False

    # Buat tabel  jika belum ada
    query = QSqlQuery()
    if not query.exec_("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """):
        print("Error membuat tabel :", query.lastError().text())
        return False

    # Buat tabel expenses jika belum ada
    if not query.exec_("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """):
        print("Error membuat tabel expenses:", query.lastError().text())
        return False
    
    return True

# Panggil fungsi inisialisasi sebelum menjalankan aplikasi
if not initialize_database():
    sys.exit(1)


# Run app (no changes needed)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec_())