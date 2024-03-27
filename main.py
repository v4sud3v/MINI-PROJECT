import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton, QWidget
from PyQt5.QtCore import Qt, pyqtSlot,QFile,QTextStream
from main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
       # self.ui.Dashboard.setChecked(True)

if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())