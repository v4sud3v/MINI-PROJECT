import sys
from PyQt5.QtWidgets import QMainWindow,QApplication
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve,QRect,pyqtSlot,QParallelAnimationGroup,QEvent,pyqtSignal,Qt
from main_window import Ui_MainWindow

class MainWindow(QMainWindow):
    

    def __init__(self):
        super(MainWindow,self).__init__()

        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Dashboard_Button.setChecked(True)
        self.ui.changingwidget.setCurrentIndex(0)
        
        self.ui.MenuButton.clicked.connect(self.toggle_sidebar)

        # Connect window state change event
        self.windowStateChanged.connect(self.handle_window_state_change)

     # Initialize sidebar hidden state
        self.sidebar_hidden = False

        # Define sidebar animation
        self.sidebar_animation = QPropertyAnimation(self.ui.widget_2, b'geometry')
        self.sidebar_animation.setDuration(300)  # Animation duration (milliseconds)
        self.sidebar_animation.setEasingCurve(QEasingCurve.InOutQuad)  # Animation easing curve

        self.mainwidget_animation = QPropertyAnimation(self.ui.mainwidget, b'geometry')
        self.mainwidget_animation.setDuration(300)  # Animation duration (milliseconds)
        self.mainwidget_animation.setEasingCurve(QEasingCurve.InOutQuad)  # Animation easing curve

        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.sidebar_animation)
        self.group.addAnimation(self.mainwidget_animation)

    windowStateChanged = pyqtSignal()
    def event(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.windowStateChanged.emit()
        return super().event(event)

    def handle_window_state_change(self):
        if self.windowState() == Qt.WindowMaximized or self.windowState() == Qt.WindowFullScreen:
            self.sidebar_hidden = False
        elif self.windowState() == Qt.WindowMinimized:
            # Depending on your application's behavior, you may choose to set sidebar_hidden to True here.
            pass
        else:
            # For other states (e.g., Normal), maintain the current sidebar state.
            self.sidebar_hidden = False
    def toggle_sidebar(self):
        # Toggle sidebar visibility and trigger animation
        if self.sidebar_hidden:
            self.show_sidebar()
        else:
            self.hide_sidebar()

    def show_sidebar(self):
        start_geometry = self.ui.widget_2.geometry()
        end_geometry = QRect(0, start_geometry.y(), start_geometry.width(), start_geometry.height())
        self.sidebar_animation.setStartValue(start_geometry)
        self.sidebar_animation.setEndValue(end_geometry)

        # Calculate main widget's end position
        mainwidget_start_geometry = self.ui.mainwidget.geometry()
        mainwidget_end_geometry = QRect(self.ui.widget_2.width(), mainwidget_start_geometry.y(),
                                        mainwidget_start_geometry.width()-self.ui.widget_2.width(), mainwidget_start_geometry.height())
        self.mainwidget_animation.setStartValue(mainwidget_start_geometry)
        self.mainwidget_animation.setEndValue(mainwidget_end_geometry)

        self.group.start()
        self.sidebar_hidden = False

    def hide_sidebar(self):
        start_geometry = self.ui.widget_2.geometry()
        end_geometry = QRect(-self.ui.widget_2.width(), start_geometry.y(), start_geometry.width(), start_geometry.height())
        self.sidebar_animation.setStartValue(start_geometry)
        self.sidebar_animation.setEndValue(end_geometry)

        # Calculate main widget's end position
        mainwidget_start_geometry = self.ui.mainwidget.geometry()
        mainwidget_end_geometry = QRect(0, mainwidget_start_geometry.y(),
                                        mainwidget_start_geometry.width() + self.ui.widget_2.width(), mainwidget_start_geometry.height())
        self.mainwidget_animation.setStartValue(mainwidget_start_geometry)
        self.mainwidget_animation.setEndValue(mainwidget_end_geometry)

        self.group.start()
        self.sidebar_hidden = True

    @pyqtSlot()
    def sidebar_animation_finished(self):
        if self.sidebar_hidden:
            self.ui.widget_2.hide()
        else:
            self.ui.widget_2.show()

            # Adjust the geometry of the main widget to stretch horizontally
            mainwidget_geometry = self.ui.mainwidget.geometry()
            mainwidget_geometry.setWidth(mainwidget_geometry.width() + self.ui.widget_2.width())
            self.ui.mainwidget.setGeometry(mainwidget_geometry)

    def on_Dashboard_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(0)

    def on_Wallets_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(1)

    def on_CategoriesButton_toggled(self):
        self.ui.changingwidget.setCurrentIndex(2)

    def on_Settings_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(3)


    def on_Help_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(4)
    
    def on_Info_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(5)
    
if __name__=="__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())