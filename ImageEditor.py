from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QListWidget, QWidget, QComboBox, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
import os
from PyQt5.QtGui import QPixmap,QIcon
from PIL import Image, ImageFilter, ImageEnhance


App = QApplication([])
App.setWindowIcon(QIcon("image-editing.png"))
main_window = QWidget()
main_window.setWindowTitle("Image Editor")
main_window.resize(900,700)

btn_folder = QPushButton("Folder")
file_list = QListWidget()

btn_left = QPushButton("Rotate Left")
btn_right = QPushButton("Rotate Right")
mirror = QPushButton("Mirror")
sharpness = QPushButton("Sharpness")
gray = QPushButton("B/W")
saturation = QPushButton("Saturation")
contrast = QPushButton("Contrast")
blur = QPushButton("Blur")

filter_box = QComboBox()
filter_box.addItem("Original")
filter_box.addItem("Rotate Left")
filter_box.addItem("Rotate Right")
filter_box.addItem("Mirror")
filter_box.addItem("Sharpness")
filter_box.addItem("B/W")
filter_box.addItem("Saturation")
filter_box.addItem("Contrast")
filter_box.addItem("Blur")

picture_box = QLabel("Image will appear here!")


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

working_directory = ''

def filter(files, exetensions):
    results = []
    for file in files:
        for ext in exetensions:
            if file.endswith(ext):
                results.append(file)
    return results

def getWorkDirectory():
    global working_directory
    working_directory = QFileDialog.getExistingDirectory()
    exetensions = ['.jpg','.jpeg','.png','.svg']
    filenames = filter(os.listdir(working_directory), exetensions)
    file_list.clear()
    for filename in filenames:
        file_list.addItem(filename)

class Editor:
    def __init__(self):
        self.image = None
        self.original = None
        self.filename = None
        self.save_folder = 'Edits/'
    
    def load_image(self, filename):
        self.filename = filename
        fullname = os.path.join(working_directory, self.filename)
        self.image = Image.open(fullname)
        self.original = self.image.copy()

    def save_image(self):
        path = os.path.join(working_directory, self.save_folder)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.makedirs(path)
        fullname = os.path.join(path, self.filename)
        self.image.save(fullname)
    
    def show_image(self, path):
        picture_box.hide()
        image = QPixmap(path)
        w, h = picture_box.width(), picture_box.height()
        image  = image.scaled(w, h, Qt.KeepAspectRatio)
        picture_box.setPixmap(image)
        picture_box.show()
    
    def transformImage(self, transformation):
        transformations = {
                'B/W': lambda image : image.convert('L'),
                'Saturation': lambda image : ImageEnhance.Color(image).enhance(1.2),
                'Rotate Left': lambda image : image.transpose(Image.ROTATE_90),
                'Rotate Right': lambda image : image.transpose(Image.ROTATE_270),
                'Sharpness': lambda image : image.filter(ImageFilter.SHARPEN),
                'Blur': lambda image : image.filter(ImageFilter.BLUR),
                'Mirror': lambda image : image.transpose(Image.FLIP_LEFT_RIGHT),
                'Contrast': lambda image : ImageEnhance.Contrast(image).enhance(1.2),
            }
        transform_function = transformations.get(transformation)
        if transform_function:
            self.image = transform_function(self.image)
            self.save_image()
        self.save_image()
        image_path = os.path.join(working_directory, self.save_folder, self.filename)
        self.show_image(image_path)

    # def gray(self):
    #     self.image = self.image.convert("L")
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)

    # def left(self):
    #     self.image = self.image.transpose(Image.ROTATE_90)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)

    # def right(self):
    #     self.image = self.image.transpose(Image.ROTATE_270)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)

    # def mirror(self):
    #     self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)

    # def sharpness(self):
    #     self.image = self.image.filter(ImageFilter.SHARPEN)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)

    # def blur(self):
    #     self.image = self.image.filter(ImageFilter.BLUR)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)

    # def color(self):
    #     self.image = ImageEnhance.Color(self.image).enhance(1.2)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)

    # def contrast(self):
    #     self.image = ImageEnhance.Contrast(self.image).enhance(1.2)
    #     self.save_image()
    #     image_path = os.path.join(working_directory, self.save_folder, self.filename)
    #     self.show_image(image_path)
    
    def apply_filter(self, filter_name):
        if filter_name == "Original":
            self.image = self.original.copy()
        else:
            mapping = {
                'B/W': lambda image : image.convert('L'),
                'Saturation': lambda image : ImageEnhance.Color(image).enhance(1.2),
                'Rotate Left': lambda image : image.transpose(Image.ROTATE_90),
                'Rotate Right': lambda image : image.transpose(Image.ROTATE_270),
                'Sharpness': lambda image : image.filter(ImageFilter.SHARPEN),
                'Blur': lambda image : image.filter(ImageFilter.BLUR),
                'Mirror': lambda image : image.transpose(Image.FLIP_LEFT_RIGHT),
                'Contrast': lambda image : ImageEnhance.Contrast(image).enhance(1.2),
            }
            filter_function = mapping.get(filter_name)
            if filter_function:
                self.image = filter_function(self.image)
                self.save_image()
                image_path = os.path.join(working_directory, main.save_folder, self.filename)
                self.show_image(image_path)
            pass
        self.save_image()
        image_path = os.path.join(working_directory, main.save_folder, self.filename)
        self.show_image(image_path)

def handle_filter():
    if file_list.currentRow() >= 0:
        select_file = filter_box.currentText()
        main.apply_filter(select_file)

def displayImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        main.load_image(filename)
        main.show_image(os.path.join(working_directory, main.filename))


main = Editor()
btn_folder.clicked.connect(getWorkDirectory)
file_list.currentRowChanged.connect(displayImage)
filter_box.currentTextChanged.connect(handle_filter)

gray.clicked.connect(lambda: main.transformImage('B/W'))
btn_left.clicked.connect(lambda: main.transformImage('Rotate Left'))
btn_right.clicked.connect(lambda: main.transformImage('Rotate Right'))
sharpness.clicked.connect(lambda: main.transformImage('Sharpness'))
contrast.clicked.connect(lambda:main.transformImage('Contrast'))
blur.clicked.connect(lambda: main.transformImage('Blur'))
mirror.clicked.connect(lambda: main.transformImage('Mirror'))
saturation.clicked.connect(lambda: main.transformImage('Saturation'))

main_window.show()
App.exec_()