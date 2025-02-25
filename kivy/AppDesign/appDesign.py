# Import Modules
import os
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QPushButton, QListWidget, QComboBox, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance

# App Settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("PhotoQt")
main_window.resize(900, 700)

# All app widgets/objects
btn_folder = QPushButton("Folder")
file_list =QListWidget()

btn_left = QPushButton("Left")
btn_right = QPushButton("Right")
mirror  = QPushButton("Mirror")
sharpness = QPushButton("Sharpen")
gray = QPushButton("B/W")
saturation = QPushButton("Color")
contrast = QPushButton("Contrast")
blur = QPushButton("Blur")


# Dropdown Box
filter_box = QComboBox()
filter_box.addItem("Original")
filter_box.addItem("Left")
filter_box.addItem("Right")
filter_box.addItem("Sharpen")
filter_box.addItem("B/W")
filter_box.addItem("Color")
filter_box.addItem("Contrast")
filter_box.addItem("Blur")

picture_box = QLabel("Image will appear here")

# App Design
master_layout = QHBoxLayout()

col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_folder)
col1.addWidget(file_list)
col1.addWidget(filter_box)
col1.addWidget(btn_left)
col1.addWidget(btn_right)
col1.addWidget(mirror)
col1.addWidget(sharpness)
col1.addWidget(gray)
col1.addWidget(saturation)
col1.addWidget(contrast)
col1.addWidget(blur)

col2.addWidget(picture_box)

master_layout.addLayout(col1, 20)
master_layout.addLayout(col2, 80)

main_window.setLayout(master_layout)



# All app funcitonality
working_directory = ""


# Filters files and extension
def filter (files, extensions):
    results = [] 
    for file in files:
        for ext in extensions:
            if file.endswith(ext):
                results.append(file)
    return results

# Choose current work directory
def getWorkDirectory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()
    extensions = ['.jpg', '.jpeg', '.png', '.svg']
    filenames = filter(os.listdir(working_directory), extensions)
    file_list.clear()
    for filename in filenames:
        file_list.addItem(filename)


class Editor():
    def __init__(self):
        self.image = None
        self.original = None
        self.filename = None
        self.save_folder = "edits/"

    def load_image(self, filename):
        self.filename = filename
        fullname = os.path.join(working_directory, self.filename)
        self.image = Image.open(fullname)
        self.original = self.image.copy()

    def save_image(self):
        path = os.path.join(working_directory, self.save_folder)
        if not(os.path.exsits(path) or os.path.isdir(path)):
            os.mkdir(path)

        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)

    def show_image(self, path):
        picture_box.hide()
        image = QPixmap(path)
        w, h = picture_box.width(), picture_box.height()
        image = image.scaled(w,h, Qt.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()



def display_image():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.load_image(filename)
        main.show_image(os.path.join(working_directory, main.filename))

main = Editor()
btn_folder.clicked.connect(getWorkDirectory)
file_list.currentRowChanged.connect(display_image)
# Show/Run
main_window.show()
app.exec_()