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
        self.set_login()
       


    def set_login(self):
        self.login_window= QMainWindow()
        self.login_ui = login_class()
        self.login_ui.setupUi(self.login_window)
        self.login_ui.loginButton_2.clicked.connect(self.check_login)
        self.login_ui.Password_Entry_2.setEchoMode(QLineEdit.Password)
        self.login_window.show()

    def add_transaction(self):
        try:
            cursor=self.conn.cursor()
            wallet_name=self.ui.group_.currentText()
            amount=self.ui.amount.text()
            description=self.ui.description.text()
            category=self.ui.comboBox_2.currentText()
            trans_type=self.ui.group_1.currentText()
            trans_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            cursor.execute("select wallet_id from Wallet where user_id=? and wallet_name=?",(self.current_user.userid,wallet_name))
            res=cursor.fetchone()
            wallet_id=res[0]
            print("wallet id:",wallet_id)
            cursor.execute("select balance from wallet where wallet_id=?",(wallet_id,))
            res1=cursor.fetchone()
            if trans_type=="Income":
                walletbalance=res1[0]+int(amount)
            else:
                walletbalance=res1[0]-int(amount)
            cursor.execute("update wallet set balance=? where wallet_id=? ;",(walletbalance,wallet_id))
            self.conn.commit()
            cursor.execute("insert into Transactions(wallet_id,amount,description,category,transaction_type,transaction_date) values(?,?,?,?,?,?);",(wallet_id,amount,description,category,trans_type,trans_date))
            self.conn.commit()
            self.ui.amount.clear()
            self.ui.description.clear()
            self.update_categories_progressbar()
            self.clear_layout(self.ui.scrollArea.layout())
            self.create_history()
            self.create_overview()
            
        except:
            self.conn.commit()
            self.ui.amount.clear()
            QMessageBox.warning(self, "error occorred","Invalid data!")

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
        self.animations = []
        # Initialize sidebar hidden state
        self.sidebar_hidden = False

        # Connect window state change event
        self.windowStateChanged.connect(self.handle_window_state_change)

        # Additional initialization code
        self.expense_cat_list = ['Dining Out', 'Travel & Transportation', 'Groceries', 'Clothing & Accessories', 'Health & Fitness', 'Entertainment','Other']
        self.income_cat_list = ['Salary', 'Investments', 'Gifts & Donations', 'Rental Income', 'Freelance Work', 'Savings & Interests', 'Other']
        self.initialize_graph()
        self.sidebar_animation_apply()
        self.ui.MenuButton.clicked.connect(self.toggle_sidebar)
        self.create_overview()
        self.ui.comboBox_3.currentIndexChanged.connect(self.draw_graph)
        self.windowStateChanged.connect(self.handle_window_state_change)
        self.ui.pushButton.clicked.connect(self.add_transaction)
        self.ui.group_1.currentIndexChanged.connect(self.update_category)
        self.update_category()
        self.update_categories_progressbar()
        self.create_history()
        self.ui.scrollArea_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrollArea_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)    



    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()

    def create_history(self):
        print("create history")
        
        # Create a scroll area
        scroll_area = self.ui.scrollArea_3

        # Create a main widget for the scroll area
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        cursor = self.conn.cursor()
        cursor.execute("SELECT amount, transaction_date, transaction_type, description FROM transactions where wallet_id in(select wallet_id from wallet where user_id=?)ORDER BY transaction_date desc;",(self.current_user.userid,
        ))
        values = cursor.fetchall()
        print(values)
        if not values:
            print("No transactions yet")
            label = QLabel("No transactions yet")
            label.setStyleSheet("font-size: 16px; color:white;") 
            label.setAlignment(Qt.AlignCenter) 
            main_layout.addWidget(label)
            main_widget.setLayout(main_layout)
        else:
            for row in range(len(values)):
                if row <=5:            
                    amount, date, trans_type,description = values[row]
                    date = datetime.strptime(date, "%d-%m-%Y %H:%M:%S").strftime("%b %d, %Y, %H:%M:%S")


                    trans_widget = QWidget()
                    
                    trans_layout = QVBoxLayout(trans_widget)

                    label1 = QLabel(str(amount))
                    label1.setStyleSheet("font-size: 16px;")  # Increase the font size
                    label1.setMinimumHeight(20)  # Increase the minimum height of the label
                    trans_layout.addWidget(label1)
                    label2 = QLabel(date)
                    label2.setStyleSheet("font-size: 16px;")  # Increase the font size
                    label2.setMinimumHeight(20)  # Increase the minimum height of the label
                    trans_layout.addWidget(label2)
                    label3 = QLabel(description)
                    label3.setStyleSheet("font-size: 16px;")  # Increase the font size
                    label3.setMinimumHeight(20)  # Increase the minimum height of the label
                    trans_layout.addWidget(label3)

                    if trans_type == "Expense":
                        trans_widget.setStyleSheet(
            "    background-color: rgba(255, 255, 255, 10);\n"
            "    border: 1px solid rgba(255, 0, 0, 50);\n"
            "    border-radius: 10px;\n"
            "    font-size: 18px;\n"  # Increase the font size
            "    color:white;\n")
                    else:
                        trans_widget.setStyleSheet("background-color: rgba(255, 255, 255, 10);\n"
            "    border: 1px solid rgba(0, 255, 0, 50);\n"
            "    border-radius: 10px;\n"
            "    font-size: 18px;\n"  # Increase the font size
            "    color:white;\n")

                    main_layout.addWidget(trans_widget)

            # Set the main layout as the layout of the main widget
                main_widget.setLayout(main_layout)

            # Set the main widget as the widget for the scroll area
        scroll_area.setWidget(main_widget)

    def update_category(self):    
        trans_type=self.ui.group_1.currentText()
        if trans_type=="Expense":
             self.ui.comboBox_2.clear()
             self.ui.comboBox_2.addItems(self.expense_cat_list)
        else:
            self.ui.comboBox_2.clear()
            self.ui.comboBox_2.addItems(self.income_cat_list)
        
    def login(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id FROM User WHERE username=? AND password=?;", (username, password))
        result = cursor.fetchone()
        if result:
            self.current_user = user(result[0])
            cursor.execute("SELECT * from Wallet WHERE user_id=?;", (self.current_user.userid,))
            wallet_exist=cursor.fetchone()
            if wallet_exist==None:
                cursor.execute("insert into Wallet (user_id,wallet_name,balance)values(?,?,?)",(self.current_user.userid,"Wallet1",0))
                cursor.execute("insert into budget_table (user_id,budget_amount)values(?,?)",(self.current_user.userid,0))
                self.conn.commit()
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
    def update_categories_progressbar(self):
        cursor=self.conn.cursor()
        expenselis=[]
        for category in self.expense_cat_list:
            cursor.execute("select sum(amount) from transactions where category=?",(category,))
            value=cursor.fetchone()
            if value[0]==None:
                value=(0,)
            expenselis.append(value[0])
        cursor.execute("select sum(amount) from transactions where transaction_type='Expense' and wallet_id in (select wallet_id from wallet where user_id =?)",(self.current_user.userid,))
        total=cursor.fetchone()
        print("total spend:",total)
        total=total[0]
        print(expenselis)
        for amount in expenselis:
            if total != 0 and total != None:
                amountpercent = int((amount / total) * 100)
            else:
                amountpercent = 0
            expenselis[expenselis.index(amount)]=amountpercent
        bar_list=[self.ui.food_bar,self.ui.travel,self.ui.groceries_bar,self.ui.clothes,self.ui.health_bar,self.ui.other_4,self.ui.other]
        for i in range(len(expenselis)):
            animation = QPropertyAnimation(bar_list[i], b"value")
            animation.setDuration(400)  # Set animation duration in milliseconds
            animation.setStartValue(0)  # Start value
            animation.setEndValue(expenselis[i])  # End value
            animation.start()
            self.animations.append(animation)  # Store the animation
            bar_list[i].setValue(expenselis[i])

        
    def init_table(self):
        cursor = self.conn.cursor()
        query1 = "CREATE TABLE IF NOT EXISTS User (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL);"
        query2 = "CREATE TABLE IF NOT EXISTS Wallet (wallet_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, wallet_name TEXT NOT NULL, balance REAL NOT NULL DEFAULT 0, FOREIGN KEY (user_id) REFERENCES User(user_id));"
        query3 = "CREATE TABLE IF NOT EXISTS Transactions (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,wallet_id INTEGER NOT NULL,amount REAL NOT NULL,description TEXT,category TEXT,transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Income', 'Expense')),transaction_date TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now')),FOREIGN KEY (wallet_id) REFERENCES Wallet(wallet_id));"
        query4 = "CREATE TABLE budget_table (user_id INT,budget_amount DECIMAL(10, 2) DEFAULT 0.00);"
        
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
        cursor.execute(query4)
        
        # Check if admin user exists
        cursor.execute("SELECT * FROM User WHERE username = 'admin';")
        admin_exists = cursor.fetchone()
        print(admin_exists)
        if not admin_exists:
            cursor.execute("INSERT INTO User (username, password) VALUES (?, ?);", ('admin', '1234')) 
        self.conn.commit()
        #####################################################################################################################
    #UI stuff 
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
        cursor=self.conn.cursor()
        cursor.execute("select sum(amount) from transactions where transaction_type='Expense' and wallet_id in(select wallet_id from wallet where user_id=?);",(self.current_user.userid,))
        total_spend=cursor.fetchone()
        cursor.execute("select sum(amount) from transactions where transaction_type='Income' and wallet_id in(select wallet_id from wallet where user_id=?);",(self.current_user.userid,))
        total_income=cursor.fetchone()
        cursor.execute("select sum(balance) from wallet where user_id=?;",(self.current_user.userid,))
        total_balance=cursor.fetchone()

        if total_balance[0]==None:
            self.ui.getbackamount.setText(f'<center><span style="font-size: 15pt;">0$</span></center>')
        else:
            self.ui.getbackamount.setText(f'<center><span style="font-size: 15pt;">{total_balance[0]}$</span></center>')
        self.ui.getbackamount.setAlignment(Qt.AlignCenter)
    
        if total_income[0]==None:
            self.ui.owe_amount.setText(f'<center><span style="font-size: 15pt;">0$</span></center>')
        else:
            self.ui.owe_amount.setText(f'<center><span style="font-size: 15pt;">{total_income[0]}$</span></center>')
        self.ui.owe_amount.setAlignment(Qt.AlignCenter)
        if total_spend[0]==None:
            self.ui.spend_amount.setText(f'<center><span style="font-size: 15pt;">0$</span></center>')
        else:
            self.ui.spend_amount.setText(f'<center><span style="font-size: 15pt;">{total_spend[0]}$</span></center>')
        self.ui.spend_amount.setAlignment(Qt.AlignCenter)
       
        self.ui.label_34.setText('<center><span style="font-size: 15pt;">405$</span></center>')
        self.ui.label_34.setAlignment(Qt.AlignCenter)

       

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
