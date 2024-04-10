
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QVBoxLayout,QSizePolicy
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve,QRect,pyqtSlot,QParallelAnimationGroup,QEvent,pyqtSignal,Qt,QPointF
import pyqtgraph as pg
from PyQt5.QtGui import QLinearGradient,QColor,QPen
import numpy as np
from main_window import Ui_MainWindow
from pyqtgraph import AxisItem,DateAxisItem
from datetime import datetime, timedelta


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Dashboard_Button.setChecked(True)
        self.ui.changingwidget.setCurrentIndex(0)
        self.initialize_graph()
        self.sidebar_animation_apply()
        self.ui.MenuButton.clicked.connect(self.toggle_sidebar)

        # Connect window state change event
        self.windowStateChanged.connect(self.handle_window_state_change)

        # Initialize sidebar hidden state
        self.sidebar_hidden = False
        self.ui.comboBox_3.currentIndexChanged.connect(self.change_graph)
    def sidebar_animation_apply(self):
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
    def change_graph(self):
        heading=self.ui.comboBox_3.currentText()
        self.plot_widget.setTitle(heading)

    def last_seven_days(self):
        # Get the current system date
        current_date = datetime.now().date()
        
        # Initialize a list to store the days
        days = []

        # Define a list of day names
        day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Loop through the last 7 days and append their names to the list
        for i in range(7):
            date = current_date - timedelta(days=i)
            day_name = day_names[date.weekday()]
            days.append(day_name)

        return days[::-1]
   
    def initialize_graph(self):
        # Create a plot widget for the line graph
        self.plot_widget = pg.PlotWidget()
        self.plot_layout = QVBoxLayout(self.ui.widget_3)

        self.plot_layout.addWidget(self.plot_widget)
        self.plot_layout.setContentsMargins(0, 0, 30,0)
        self.ui.widget_3.setLayout(self.plot_layout)

        # Set size policy for plot widget to Expanding
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        days = self.last_seven_days()
        print(days)
        # Sample x values corresponding to Monday to Saturday
        x = np.array([0,1, 2, 3, 4, 5, 6])
        y = np.array([2, 30, 5, 35, 25, 37, 20])
        # Create a linear gradient for the pen
        gradient = QLinearGradient(0, 0, 0, 30)  # (xstart, ystart, xstop, ystop)
        gradient.setColorAt(0.0, QColor('#0d00ff'))
        gradient.setColorAt(1.0, QColor('#f000bc'))
        pen = QPen(gradient, 1)
        pen.setWidth(0) # QPen with this gradient

        # Plot data with custom GradientLinePlot
        self.plot = self.plot_widget.plot(x, y, pen=pen)

        # Set the size of the plot widget
        self.plot_widget.setMinimumSize(100, 100)  # Adjust the size as needed

        # Set background color to transparent
        self.plot_widget.setBackground(None)
        graph_title=self.ui.comboBox_3.currentText()
        self.plot_widget.setTitle(graph_title)
        self.plot_widget.setXRange(0, 20)  # Set view range for x-axis
        self.plot_widget.setYRange(0, 20)  # Set view range for y-axis
        self.plot_widget.setLimits(xMin=0, xMax=7, yMin=0, yMax=100)  # Adjust these values as needed
        self.plot_widget.setMouseEnabled(x=False, y=False)  # Disable both x and y zooming
  
        
        # Set x-axis to DateAxisItem
        date_axis =DateAxisItem(orientation='bottom')
        self.plot_widget.setAxisItems({'bottom': date_axis})
        self.plot_widget.getAxis('bottom').setTicks([[(i,f'{days[i]}') for i in range(0, 7)]])
        
        
        # Set y-axis to AxisItem
        text_axis = AxisItem(orientation='left')
        self.plot_widget.setAxisItems({'left': text_axis})
        self.plot_widget.getAxis('left').setTicks([[(i, f'${i}') for i in range(0, 100,10)]])
        
        self.plot_widget.getAxis('left').setPen('#6f7da2')
        self.plot_widget.getAxis('bottom').setPen('#6f7da2')                                                                             
        self.plot_widget.showGrid(y=True)
        self.plot_widget.setLabel('bottom', 'Day')
        self.plot_widget.setLabel('left', 'Expenses')
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
                                        mainwidget_start_geometry.width() - self.ui.widget_2.width(),
                                        mainwidget_start_geometry.height())
        self.mainwidget_animation.setStartValue(mainwidget_start_geometry)
        self.mainwidget_animation.setEndValue(mainwidget_end_geometry)

        self.group.start()
        self.sidebar_hidden = False

    def hide_sidebar(self):
        start_geometry = self.ui.widget_2.geometry()
        end_geometry = QRect(-self.ui.widget_2.width(), start_geometry.y(), start_geometry.width(),
                             start_geometry.height())
        self.sidebar_animation.setStartValue(start_geometry)
        self.sidebar_animation.setEndValue(end_geometry)

        # Calculate main widget's end position
        mainwidget_start_geometry = self.ui.mainwidget.geometry()
        mainwidget_end_geometry = QRect(0, mainwidget_start_geometry.y(),
                                        mainwidget_start_geometry.width() + self.ui.widget_2.width(),
                                        mainwidget_start_geometry.height())
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


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())