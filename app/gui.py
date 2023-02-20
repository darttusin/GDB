from PyQt5 import QtCore, QtGui, QtWidgets
import re


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(464, 454)
        self.dialog = Dialog

        self.set_start_button()
        self.set_titles()
        self.set_upload_path()
        self.set_upload_file()
        self.set_save_path()
        self.set_save_file()
        self.set_tag_input()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "GDB"))
        self.startButton.setText(_translate("Dialog", "Запустить"))
        self.uploadFile.setText(_translate("Dialog", "..."))
        self.uploadPath.setText(_translate("Dialog", "None"))
        self.uploadPathTitle.setText(_translate("Dialog", "Выберите word файл"))
        self.savePathTitle.setText(_translate("Dialog", "Выберите место сохранения "))
        self.savePath.setText(_translate("Dialog", "None"))
        self.saveFile.setText(_translate("Dialog", "..."))
        self.tagTitle.setText(_translate("Dialog", "Напишите тег версии если нужен"))

    def set_start_button(self):
        self.startButton = QtWidgets.QPushButton(Dialog)
        self.startButton.setGeometry(QtCore.QRect(130, 340, 221, 51))
        self.startButton.setObjectName("startButton")
        self.startButton.clicked.connect(self.button_accept_clicked)
    
    def button_accept_clicked(self):
        self.version = self.tagInput.text()
        if self.version == "":
            print("Нет версии")
            self.version = "No version"
        else:
            print("Версия - " + self.version)

    def set_titles(self):
        self.uploadPathTitle = QtWidgets.QLabel(Dialog)
        self.uploadPathTitle.setGeometry(QtCore.QRect(150, 20, 141, 17))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        self.uploadPathTitle.setFont(font)
        self.uploadPathTitle.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.uploadPathTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.uploadPathTitle.setObjectName("uploadPathTitle")
        self.savePathTitle = QtWidgets.QLabel(Dialog)
        self.savePathTitle.setGeometry(QtCore.QRect(110, 120, 241, 20))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        self.savePathTitle.setFont(font)
        self.savePathTitle.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.savePathTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.savePathTitle.setObjectName("savePathTitle")
        self.tagTitle = QtWidgets.QLabel(Dialog)
        self.tagTitle.setGeometry(QtCore.QRect(100, 230, 271, 20))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        self.tagTitle.setFont(font)
        self.tagTitle.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tagTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.tagTitle.setObjectName("tagTitle")

    def set_upload_path(self):
        self.uploadPath = QtWidgets.QLabel(Dialog)
        self.uploadPath.setGeometry(QtCore.QRect(20, 60, 381, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        self.uploadPath.setFont(font)
        self.uploadPath.setFrameShape(QtWidgets.QFrame.Box)
        self.uploadPath.setObjectName("uploadPath")

    def set_upload_file(self):
        self.uploadFile = QtWidgets.QToolButton(Dialog)
        self.uploadFile.setGeometry(QtCore.QRect(410, 60, 31, 31))
        self.uploadFile.setObjectName("uploadFile")
        self.uploadFile.clicked.connect(self.button_upload_file_clicked)

    def button_upload_file_clicked(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self.dialog, "Open file", "/", "Word docx (*.docx)")
        self.file_path = file[0]
        self.file_name = self.file_path[::-1][0:self.file_path[::-1].index("/")][::-1]
        self.uploadPath.setText(self.file_name)
        print("Upload file path - " + self.file_path)

    def set_save_path(self):
        self.savePath = QtWidgets.QLabel(Dialog)
        self.savePath.setGeometry(QtCore.QRect(20, 160, 381, 31))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        self.savePath.setFont(font)
        self.savePath.setFrameShape(QtWidgets.QFrame.Box)
        self.savePath.setObjectName("savePath")
    
    def set_save_file(self):
        self.saveFile = QtWidgets.QToolButton(Dialog)
        self.saveFile.setGeometry(QtCore.QRect(410, 160, 31, 31))
        self.saveFile.setObjectName("saveFile")
        self.saveFile.clicked.connect(self.button_save_file_clicked)

    def button_save_file_clicked(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self.dialog, "Select Directory")
        self.save_directory = directory
        self.savePath.setText(directory)
        print("Save directory - " + directory)

    def set_tag_input(self):
        self.tagInput = QtWidgets.QLineEdit(Dialog)
        self.tagInput.setGeometry(QtCore.QRect(100, 270, 281, 31))
        self.tagInput.setObjectName("tagInput")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())