import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QPushButton, QWidget
from PyQt5.QtCore import Qt, pyqtSlot,QFile,QTextStream
from main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Dashboard_Button.setChecked(True)
        self.ui.widget_2.hide()
        self.ui.changingwidget.setCurrentIndex(0)
        self.ui.Dashboard_Button_minimized.setChecked(True)

    def on_Dashboard_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(0)
    
    def on_Dashboard_Button_minimized_toggled(self):
        self.ui.changingwidget.setCurrentIndex(0)

    def on_Wallets_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(1)

    def on_Wallets_Button_minimized_toggled(self):
        self.ui.changingwidget.setCurrentIndex(1)

    def on_CategoriesButton_toggled(self):
        self.ui.changingwidget.setCurrentIndex(2)

    def on_CategoriesButton_minimized_toggled(self):
        self.ui.changingwidget.setCurrentIndex(2)

    def on_Settings_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(3)

    def on_Settings_Button_minimized_toggled(self):
        self.ui.changingwidget.setCurrentIndex(3)

    def on_Help_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(4)

    def on_HelpButton_minimized_toggled(self):
        self.ui.changingwidget.setCurrentIndex(4)

    def on_InfoButton_minimized_toggled(self):
        self.ui.changingwidget.setCurrentIndex(5)

if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())