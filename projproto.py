import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg
from PyQt5.QtGui import QLinearGradient, QColor, QPen
import numpy as np
import sqlite3
from pyqtgraph import AxisItem, DateAxisItem
from datetime import datetime, timedelta
from login import Ui_MainWindow as login_class
from main_window2 import Ui_MainWindow

class user:
    def __init__(self, userid):
        self.userid = userid

class MainWindow(QMainWindow):
    windowStateChanged = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.conn = self.create_connection()
        self.init_table()
        #self.set_login()
        self.set_login()


    def set_login(self):
        self.login_window= QMainWindow()
        self.login_ui = login_class()
        self.login_ui.setupUi(self.login_window)
        self.login_ui.loginButton_2.clicked.connect(self.check_login)
        self.login_ui.Password_Entry_2.setEchoMode(QLineEdit.Password)
        self.login_window.show()
        

    def check_login(self):
        username = self.login_ui.NameEntry_2.text()
        password = self.login_ui.Password_Entry_2.text()
        if self.login(username, password):
            print('yes')
            self.login_window.close()
            self.show_main()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password. Please try again.")

    def show_main(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Expenzio')
        self.showMaximized()
        self.ui.Dashboard_Button.toggled.connect(self.on_Dashboard_Button_toggled)
        self.ui.Dashboard_Button.setChecked(True)
        # Initialize sidebar hidden state
        self.sidebar_hidden = False

        # Connect window state change event
        self.windowStateChanged.connect(self.handle_window_state_change)

        # Additional initialization code
        self.initialize_graph()
        self.sidebar_animation_apply()
        self.ui.MenuButton.clicked.connect(self.toggle_sidebar)
        self.create_overview()
        self.ui.comboBox_3.currentIndexChanged.connect(self.draw_graph)
        self.windowStateChanged.connect(self.handle_window_state_change)
        

    def login(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id FROM User WHERE username=? AND password=?;", (username, password))
        result = cursor.fetchone()
        print
        if result:
            self.current_user = user(result[0])
            return True
        else:
            return False

    def create_connection(self):
        try:
            conn = sqlite3.connect('Expenzio.db')
            return conn
        except sqlite3.Error as e:
            print(e)
            return None

    def init_table(self):
        cursor = self.conn.cursor()
        query1 = "CREATE TABLE IF NOT EXISTS User (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);"
        query2 = "CREATE TABLE IF NOT EXISTS Wallet (wallet_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, wallet_name TEXT NOT NULL, balance REAL NOT NULL DEFAULT 0, FOREIGN KEY (user_id) REFERENCES User(user_id));"
        query3 = "CREATE TABLE IF NOT EXISTS Transactions (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, wallet_id INTEGER NOT NULL, amount REAL NOT NULL, description TEXT, category TEXT, transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Income', 'Expense')), transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (wallet_id) REFERENCES Wallet(wallet_id));"
        
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
        
        # Check if admin user exists
        cursor.execute("SELECT * FROM User WHERE username = 'admin';")
        admin_exists = cursor.fetchone()
        print(admin_exists)
        if not admin_exists:
            cursor.execute("INSERT INTO User (username, password) VALUES (?, ?);", ('admin', '1234')) 
        self.conn.commit()
    
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

    def create_overview(self):
        layout_OUT=QHBoxLayout()
        outside_widget=self.ui.widget_7 
        heading_list=["Total spend","You owe","You get back","Settled up"]
        data_list=[205,3500,600,405]
        for i in range(4):
            layout_in=QVBoxLayout()
            inside_widget=QWidget()
            data=QLabel(f'{data_list[i]}$')
            heading=QLabel(f'{heading_list[i]}')
            data.setStyleSheet("*{color:rgb(255,255,255);\n"
 "font: 15pt 'MS Shell Dlg 2';}")
            heading.setStyleSheet("*{color: rgb(116, 131, 169);\n"
 "font: 10pt 'MS Shell Dlg 2';}")
            inside_widget.setLayout(layout_in)
            layout_in.addWidget(data)
            layout_in.addWidget(heading)
            layout_OUT.addWidget(inside_widget)
        outside_widget.setLayout(layout_OUT)

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

    def resizeEvent(self, event):
        print("Resize event triggered")
        self.findsize()

    def findsize(self):
        new_size = self.ui.mainwidget.geometry()
        stframe = self.ui.Statistics_frame
        stframe.give_size(new_size.width(), new_size.height())
    windowStateChanged = pyqtSignal()
    
    def event(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.windowStateChanged.emit()
        return super().event(event)

    def handle_window_state_change(self): 
        self.sidebar_hidden = False 
        self.findsize()

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
        self.months=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        self.plot_layout.addWidget(self.plot_widget)
        self.plot_layout.setContentsMargins(0, 0, 30,0)
        self.ui.widget_3.setLayout(self.plot_layout)

        # Set size policy for plot widget to Expanding
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.days = self.last_seven_days()
        self.plot_widget.setBackground(None)
        
        self.draw_graph()

    def draw_graph(self):
        # Set view range for x and y axes
        self.plot_widget.setXRange(0, 30)
        self.plot_widget.setYRange(0, 20)

        # Adjust view limits
        self.plot_widget.setLimits(xMin=0, xMax=12, yMin=0, yMax=100)

        # Disable x-axis zooming
        self.plot_widget.setMouseEnabled(x=False, y=True)

        # Get the selected heading from the combo box
        heading = self.ui.comboBox_3.currentText()
        self.plot_widget.setTitle(heading)

        # Create a gradient for the plot line
        gradient = QLinearGradient(0, 0, 0, 40)
        gradient.setColorAt(0.0, QColor('#0d00ff'))
        gradient.setColorAt(1.0, QColor('#f000bc'))
        pen = QPen(gradient, 1)
        pen.setWidth(0)

        # Clear the plot widget
        self.plot_widget.clear()

        # Set up date axis
        date_axis = DateAxisItem(orientation='bottom')
        self.plot_widget.setAxisItems({'bottom': date_axis})

        if heading == "Last 7 days":
            self.plot_widget.getAxis('bottom').setTicks([[(i, f'{self.days[i]}') for i in range(0, 7)]])
            x = np.array([0, 1, 2, 3, 4, 5, 6])
            y = np.array([2, 30, 5, 35, 25, 37, 20])
            self.plot = self.plot_widget.plot(x, y, pen=pen)
            self.plot_widget.setLabel('bottom', 'Day')
        elif heading == "This month":
            self.plot_widget.getAxis('bottom').setTicks([[(i, f'week{i+1}') for i in range(0, 5)]])
            x = np.array([0, 1, 2, 3])
            y = np.array([4, 5, 11, 40])
            self.plot = self.plot_widget.plot(x, y, pen=pen)
            self.plot_widget.setLabel('bottom', 'week')
        elif heading == "This year":
            self.plot_widget.getAxis('bottom').setTicks([[(i, f'{self.months[i]}') for i in range(0, 12)]])
            x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
            y = np.array([45, 5, 20, 80, 2, 35, 25, 4, 5, 11, 40, 4])
            self.plot = self.plot_widget.plot(x, y, pen=pen)
            self.plot_widget.setLabel('bottom', 'months')

        # Auto-range the plot
        self.plot_widget.autoRange()

        # Set y-axis to AxisItem
        text_axis = AxisItem(orientation='left')
        self.plot_widget.setAxisItems({'left': text_axis})
        self.plot_widget.setMinimumSize(100, 100)
        self.plot_widget.getAxis('left').setPen('#6f7da2')
        self.plot_widget.getAxis('bottom').setPen('#6f7da2')
        self.plot_widget.update()
        QApplication.processEvents() 
        # Explicitly set grid visibility
        self.plot_widget.getAxis('left').setGrid(255)  # Adjust opacity for left axis grid lines
        self.plot_widget.setLabel('left', 'Expenses($)')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
