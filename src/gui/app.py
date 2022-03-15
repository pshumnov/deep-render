import sys
from PIL.ImageQt import QImage
from PyQt5 import QtCore, QtWidgets, QtGui
from data_process import *
from pix2pix import Generate


import os
path = os.path.dirname(__file__)


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

        self.albedo = None
        self.depth = None
        self.normals = None


    def initUI(self):
        background = '#035d63'
        self.setMinimumSize(1200, 500)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet('''
            background-color: {:s};
            font-family: Segoe;
        '''.format(background))

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)

        self.btn_albedo = self.create_load_button(' Load albedo image', self.btn_albedo_clicked)
        self.btn_depth = self.create_load_button(' Load depth image', self.btn_depth_clicked)
        self.btn_normals = self.create_load_button(' Load normals image', self.btn_normals_clicked)
        self.btn_generate = self.create_load_button('Generate result', self.btn_generate_clicked, False)
        self.btn_generate.setVisible(False)

        self.canvas_albedo = self.create_canvas()
        self.canvas_depth = self.create_canvas()
        self.canvas_normals = self.create_canvas()


        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)

        self.layout.addWidget(TaskBar(self, 'DeepRender'))
        self.layout.addStretch(-1)
        self.layout.addLayout(self.main_layout)
        self.layout.addWidget(self.btn_generate, alignment=QtCore.Qt.AlignCenter)
        self.layout.addStretch(1)
        
        self.layout_albedo = QtWidgets.QVBoxLayout()
        self.layout_albedo.setContentsMargins(0,0,0,0)
        self.layout_depth = QtWidgets.QVBoxLayout()
        self.layout_depth.setContentsMargins(0,0,0,0)
        self.layout_normals = QtWidgets.QVBoxLayout()
        self.layout_normals.setContentsMargins(0,0,0,0)

        self.main_layout.addLayout(self.layout_albedo)
        self.main_layout.addLayout(self.layout_depth)
        self.main_layout.addLayout(self.layout_normals)

        self.layout_albedo.addWidget(self.canvas_albedo, alignment=QtCore.Qt.AlignCenter)
        self.layout_albedo.addWidget(self.btn_albedo, alignment=QtCore.Qt.AlignCenter)
        self.layout_depth.addWidget(self.canvas_depth, alignment=QtCore.Qt.AlignCenter)
        self.layout_depth.addWidget(self.btn_depth, alignment=QtCore.Qt.AlignCenter)
        self.layout_normals.addWidget(self.canvas_normals, alignment=QtCore.Qt.AlignCenter)
        self.layout_normals.addWidget(self.btn_normals, alignment=QtCore.Qt.AlignCenter)

        
    def create_load_button(self, text, func, icon=True):
        btn_load = QtWidgets.QPushButton(text)
        btn_load.clicked.connect(func)
        if icon:
            btn_load.setIcon(QtGui.QIcon(path + '/img/add.png'))
            btn_load.setIconSize(QtCore.QSize(25, 25))
        btn_load.setStyleSheet('''
            QPushButton {
                color: #ffffff;
                font-size: 10pt;
                border-radius: 0px;
            }
            QPushButton::hover { 
                background-color: #7ea2aa;
            }
        ''')
        btn_load.setFixedSize(btn_load.sizeHint().width() + 30, 
                                        btn_load.sizeHint().height() + 10)
        
        return btn_load


    def create_canvas(self):
        canvas = QtWidgets.QLabel()
        canvas.setFixedSize(QtCore.QSize(370, 270))
        canvas.setVisible(False)

        return canvas
        
    
    def btn_albedo_clicked(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Load albedo image', None, "Image (*.hdf5)")
        
        if filename[0]:
            try:
                self.albedo = load_albedo(filename[0])
            except:
                QtWidgets.QMessageBox.about(self, "Error", "Invalid albedo image file")
                return 

            img = array_to_img(self.albedo)
            self.canvas_albedo.setVisible(True)
            self.canvas_albedo.setPixmap(QtGui.QPixmap.fromImage(img).scaled(370, 370, 
                transformMode = QtCore.Qt.SmoothTransformation))

        if self.albedo is not None and self.depth is not None and self.normals is not None:
            self.btn_generate.setVisible(True)
    
    def btn_depth_clicked(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Load depth image', None, "Image (*.hdf5)")

        if filename[0]:
            try:
                self.depth = load_depth(filename[0])
            except:
                QtWidgets.QMessageBox.about(self, "Error", "Invalid depth image file")
                return
                
            img = array_to_img(self.depth, True)
            self.canvas_depth.setVisible(True)
            self.canvas_depth.setPixmap(QtGui.QPixmap.fromImage(img).scaled(370, 370, 
                transformMode = QtCore.Qt.SmoothTransformation))
                
        if self.albedo is not None and self.depth is not None and self.normals is not None:
            self.btn_generate.setVisible(True)

    def btn_normals_clicked(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Load normals image', None, "Image (*.hdf5)")
        
        if filename[0]:
            try:
                self.normals = load_normals(filename[0])
            except:
                QtWidgets.QMessageBox.about(self, "Error", "Invalid normals image file")
                return

            img = array_to_img(self.normals)
            self.canvas_normals.setVisible(True)
            self.canvas_normals.setPixmap(QtGui.QPixmap.fromImage(img).scaled(370, 370, 
                transformMode = QtCore.Qt.SmoothTransformation))
                
        if self.albedo is not None and self.depth is not None and self.normals is not None:
            self.btn_generate.setVisible(True)

    def btn_generate_clicked(self):
        result = Generate(self.albedo, self.depth, self.normals)
        img = array_to_img(result)
        self.dialog = PaintPicture(img)


class PaintPicture(QtWidgets.QDialog):
    def __init__(self, img):
        super(PaintPicture, self).__init__()
        self.img = img

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.canvas = QtWidgets.QLabel()
        self.canvas.setFixedSize(QtCore.QSize(512, 374))
        self.canvas.setPixmap(QtGui.QPixmap.fromImage(img))

        self.btn_save = QtWidgets.QPushButton('Save')
        self.btn_save.clicked.connect(self.save)
        self.btn_save.setStyleSheet('''
            QPushButton {
                color: #ffffff;
                font-size: 10pt;
                border-radius: 0px;
            }
            QPushButton::hover { 
                background-color: #7ea2aa;
            }
        ''')
        self.btn_save.setFixedSize(self.btn_save.sizeHint().width() + 30, 
                                        self.btn_save.sizeHint().height() + 10)

        self.layout.addWidget(TaskBar(self, 'Result'))
        self.layout.addStretch(-1)
        self.layout.addWidget(self.canvas, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.btn_save, alignment=QtCore.Qt.AlignCenter)
        self.layout.addStretch(1)

        self.setFixedSize(self.canvas.width(), 480)
        self.setStyleSheet('''
            background-color: #023C40;
            font-family: Segoe;
        ''')

        self.show()

    def save(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save result', None, "Image (*.png)")
        if filename[0]:
            self.img.save(filename[0])


class TaskBar(QtWidgets.QWidget):

    def __init__(self, parent, title):
        super(TaskBar, self).__init__()
        self.parent = parent
        
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QtWidgets.QLabel(title)

        btn_size = 30
        background = '#023c40'

        self.btn_close = QtWidgets.QPushButton()
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setIcon(QtGui.QIcon(path + '/img/close.png'))
        self.btn_close.setIconSize(QtCore.QSize(25, 25))
        self.btn_close.setStyleSheet('''
            background-color: {:s};
            border-radius: 0px;
        '''.format(background))

        self.btn_min = QtWidgets.QPushButton()
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setIcon(QtGui.QIcon(path + '/img/minimize.png'))
        self.btn_min.setIconSize(QtCore.QSize(25, 25))
        self.btn_min.setStyleSheet('''
            background-color: {:s};
            border-radius: 0px;
        '''.format(background))

        self.btn_max = QtWidgets.QPushButton()
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)
        self.btn_max.setIcon(QtGui.QIcon(path + '/img/restore.png'))
        self.btn_max.setIconSize(QtCore.QSize(25, 25))
        self.btn_max.setStyleSheet('''
            background-color: {:s};
            border-radius: 0px;
        '''.format(background))

        self.title.setFixedHeight(35)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet('''
            background-color: {:s};
            color: #ffffff;
            font-size: 10pt;
        '''.format(background))
        self.setLayout(self.layout)

        self.start = QtCore.QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(TaskBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False


    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def btn_min_clicked(self):
        self.parent.showMinimized()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())