#import setting
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QFont


class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()

        #app settings
        self.setWindowTitle("Calculator")
        self.resize(250, 300)

        #all objects/widgets
        self.text_box = QLineEdit()
        self.text_box.setFont(QFont("Helvetica", 32))
        self.grid = QGridLayout()
        self.text_box.setStyleSheet("QLineEdit { background-color: black; color: white }")

        self.buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        ]

        row = 0
        col = 0

        for text in self.buttons:
            button = QPushButton(text)
            button.clicked.connect(self.button_click)
            button.setStyleSheet("QPushButton {background-color: #ff7f00; font: 25pt Comic Sans Ms; padding: 10px; color: white }")
            self.grid.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.clear = QPushButton("Clear")
        self.delete = QPushButton("<-")
        self.clear.setStyleSheet("QPushButton { background-color: #ff7f00; font: 25pt Comic Sans Ms; padding: 10px; color: white }")
        self.delete.setStyleSheet("QPushButton { background-color: #ff7f00; font: 25pt Comic Sans Ms; padding: 10px; color: white}")

        master_layout = QVBoxLayout()
        master_layout.addWidget(self.text_box)
        master_layout.addLayout(self.grid)

        button_row = QHBoxLayout()
        button_row.addWidget(self.clear)
        button_row.addWidget(self.delete)
        master_layout.addLayout(button_row)
        master_layout.setContentsMargins(25,25,25,25)

        self.setLayout(master_layout)

        self.clear.clicked.connect(self.button_click)
        self.delete.clicked.connect(self.button_click)

    #application function
    def button_click(self):
        button = calculator.sender()
        text =button.text()

        if text == "=":
            symbol = self.text_box.text()
            try:
                result = eval(symbol)
                self.text_box.setText(str(result))
            except Exception as e:
                print("Error: ", e)
        elif text == "Clear":
            self.text_box.clear()
        elif text == "<-":
            current_value = self.text_box.text()
            self.text_box.setText(current_value[:-1])
        else:
            current_value = self.text_box.text()
            self.text_box.setText(current_value + text)
        


#show/run
if __name__ in "__main__":
    calculator = QApplication([])
    main_window = CalculatorApp()
    main_window.setStyleSheet("QWidget { background-color: #f0f0f8 }")
    main_window.show()
    calculator.exec_()