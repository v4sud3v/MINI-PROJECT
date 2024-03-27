# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1102, 658)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("*{ \n"
"    font: 9pt \"Century Gothic\";\n"
"\n"
"background-color: rgb(255, 255, 255);}\n"
"QLineEdit{\n"
"border-bottom: 1px solid;\n"
"border-color:rgba(255, 255, 255,100);\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(-20, -90, 1261, 871))
        self.widget.setStyleSheet("QPushButton{background-color:rgba(0,0,0,100);\n"
"border-radius:5px;\n"
"color:#fff;}\n"
"QPushButton:hover{\n"
"background-color:rgba(0,0,0,130);\n"
"color:rgb(60, 223, 255);\n"
"}")
        self.widget.setObjectName("widget")
        self.loginHeading = QtWidgets.QLabel(self.widget)
        self.loginHeading.setGeometry(QtCore.QRect(265, 200, 71, 41))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.loginHeading.setFont(font)
        self.loginHeading.setStyleSheet("color:rgb(255, 255, 255);\n"
"background-color:transparent;")
        self.loginHeading.setObjectName("loginHeading")
        self.passwordLabel = QtWidgets.QLabel(self.widget)
        self.passwordLabel.setGeometry(QtCore.QRect(100, 300, 81, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.passwordLabel.setFont(font)
        self.passwordLabel.setStyleSheet("color:#fff;\n"
"background-color:transparent;")
        self.passwordLabel.setObjectName("passwordLabel")
        self.Password_Entry = QtWidgets.QLineEdit(self.widget)
        self.Password_Entry.setGeometry(QtCore.QRect(190, 300, 220, 22))
        self.Password_Entry.setStyleSheet("background-color:transparent;\n"
"border-radius:3px;\n"
"padding-left: 10px;\n"
"color:#fff;\n"
"")
        self.Password_Entry.setCursorPosition(0)
        self.Password_Entry.setObjectName("Password_Entry")
        self.createButton = QtWidgets.QPushButton(self.widget)
        self.createButton.setGeometry(QtCore.QRect(190, 470, 220, 28))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.createButton.setFont(font)
        self.createButton.setStyleSheet("#createButton:hover{color:rgb(60, 223, 255);}")
        self.createButton.setObjectName("createButton")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(80, 150, 411, 521))
        self.label_3.setStyleSheet("*{border-radius:30px;\n"
"\n"
"    background-color: rgb(48, 71, 125);\n"
"}")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.forgotButton = QtWidgets.QPushButton(self.widget)
        self.forgotButton.setGeometry(QtCore.QRect(190, 410, 220, 28))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.forgotButton.setFont(font)
        self.forgotButton.setStyleSheet("#forgotButton{background-color:transparent;\n"
"}")
        self.forgotButton.setObjectName("forgotButton")
        self.NameEntry = QtWidgets.QLineEdit(self.widget)
        self.NameEntry.setGeometry(QtCore.QRect(190, 260, 220, 22))
        self.NameEntry.setStyleSheet("background-color:transparent;\n"
"border-radius:3px;\n"
"padding-left: 10px;\n"
"color:#fff;\n"
"")
        self.NameEntry.setCursorPosition(0)
        self.NameEntry.setObjectName("NameEntry")
        self.Usernamelabel = QtWidgets.QLabel(self.widget)
        self.Usernamelabel.setGeometry(QtCore.QRect(100, 260, 91, 20))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Usernamelabel.setFont(font)
        self.Usernamelabel.setStyleSheet("color:#fff;\n"
"background-color:transparent;")
        self.Usernamelabel.setObjectName("Usernamelabel")
        self.loginButton = QtWidgets.QPushButton(self.widget)
        self.loginButton.setGeometry(QtCore.QRect(190, 360, 220, 28))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.loginButton.setFont(font)
        self.loginButton.setStyleSheet("")
        self.loginButton.setObjectName("loginButton")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 1101, 751))
        self.label_2.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(23, 34, 63, 255), stop:0.531579 rgba(40, 57, 98, 255));\n"
"border-radius:25px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(550, 90, 671, 661))
        self.label.setStyleSheet("\n"
"border-image: url(:/images/images/imgman.jpg);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2.raise_()
        self.label_3.raise_()
        self.forgotButton.raise_()
        self.loginHeading.raise_()
        self.NameEntry.raise_()
        self.loginButton.raise_()
        self.Usernamelabel.raise_()
        self.Password_Entry.raise_()
        self.createButton.raise_()
        self.passwordLabel.raise_()
        self.label.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.loginHeading.setText(_translate("MainWindow", "Log In"))
        self.passwordLabel.setText(_translate("MainWindow", "Password"))
        self.createButton.setText(_translate("MainWindow", "Create new "))
        self.forgotButton.setText(_translate("MainWindow", "Forgot Password"))
        self.Usernamelabel.setText(_translate("MainWindow", "User name"))
        self.loginButton.setText(_translate("MainWindow", "Log In"))
import imageresources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
