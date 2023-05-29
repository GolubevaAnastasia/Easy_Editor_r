#создай тут фоторедактор Easy Editor!
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QRadioButton, QTextEdit, QLineEdit, QInputDialog, QFileDialog
from PyQt5.QtCore import Qt
import os
from PIL import Image,ImageFilter
from PIL.ImageFilter import SHARPEN
from PyQt5.QtGui import QPixmap

app=QApplication([]) 
main_win=QWidget()#mw
main_win.setWindowTitle('Easy Editor')

b1=QPushButton('Папка')#p
lists=QListWidget()#sp, lw
picture=QLabel('Картинка')#car
b2=QPushButton('Лево')#but_1
b3=QPushButton('Право')#...
b4=QPushButton('Зеркало')
b5=QPushButton('Резкость')
b6=QPushButton('ЧБ')

line=QHBoxLayout()#row
lin_1=QVBoxLayout()
lin_2=QVBoxLayout()
g_lin=QHBoxLayout()#dop_lin

lin_1.addWidget(b1)
lin_1.addWidget(lists)

g_lin.addWidget(b1)
g_lin.addWidget(b2)
g_lin.addWidget(b3)
g_lin.addWidget(b4)
g_lin.addWidget(b5)
g_lin.addWidget(b6)

lin_2.addWidget(picture)
lin_2.addLayout(g_lin)

line.addLayout(lin_1,10)
line.addLayout(lin_2,90)

workdir=''

def filter(files, extensions):
    '''просматриваем все файлы и отбираем в список, только графические файлы'''
    result=[]
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    '''получаем путь к папке'''
    global workdir #обращаемся к глобальной переменной
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions=['.jpg', '.png', '.jpeg']
    chooseWorkdir()
    files=os.listdir(workdir) #список имён файлов из указанной папки
    filenames=filter(files, extensions)
    lists.clear()
    for filename in filenames:
        lists.addItem(filename)
b1.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):   
        self.image=None
        self.filename=None
        self.save_dir='Processor'
    
    def loadImage(self, filename):
        '''при загрузке запоминаем путь и имя файла'''
        self.filename=filename
        fullname=os.path.join(workdir, filename)
        self.image=Image.open(fullname)
    
    def saveImage(self):
        '''сохраняет копию файла в подпапке'''
        path=os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path)or os.path.isdir(path)):
            os.mkdir(path)
        fullname=os.path.join(path, self.filename)
        self.image.save(fullname)

    def showImage(self, path):
        picture.hide()
        pixmapimage=QPixmap(path)
        w, h=picture.width(), picture.height()
        pixmapimage=pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        picture.setPixmap(pixmapimage)
        picture.show()

    def make_nc(self):
        self.image=self.image.convert('L')
        self.saveImage()
        image_path=os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image=self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path=os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image=self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path=os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
        self.showImage(image_path)

    def do_mirrow(self):
        self.image=self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path=os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_contrast(self):
        self.image=self.image.filter(SHARPEN)
        self.saveImage()
        image_path=os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

def showChosenImage():
    if lists.currentRow()>=0:
        filename=lists.currentItem().text()
        workimage.loadImage(filename)
        workimage.showImage(os.path.join(workdir, workimage.filename))

workimage=ImageProcessor()
lists.currentRowChanged.connect(showChosenImage)

b6.clicked.connect(workimage.make_nc)
b2.clicked.connect(workimage.do_left)
b3.clicked.connect(workimage.do_right)
b5.clicked.connect(workimage.do_contrast)
b4.clicked.connect(workimage.do_mirrow)
 
main_win.setLayout(line)
main_win.show()
app.exec_()