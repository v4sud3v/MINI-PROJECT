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
from calendar import monthrange
from main_window2 import Ui_MainWindow
from create_account import Ui_Dialog as create_account_class
from userinfo import  Ui_Dialog as userinfo_class
class user:
    def __init__(self, userid):
        self.userid = userid
        self.budget = 0

class MainWindow(QMainWindow):
    windowStateChanged = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.conn = self.create_connection()
        self.init_table()
        self.set_login()
       
       
    def set_login(self):
        self.login_window= QMainWindow()
        self.login_window.setWindowTitle('login')
        self.login_ui = login_class()
        self.login_ui.setupUi(self.login_window)
        self.login_ui.loginButton_2.clicked.connect(self.check_login)
        self.login_ui.Password_Entry_2.setEchoMode(QLineEdit.Password)
        self.login_ui.createButton_2.clicked.connect(self.show_create_account)
        self.login_ui.forgotButton_2.clicked.connect(self.forgot_password)  
        self.login_window.show()
    
    def add_wallet(self):
        # Create a QDialog
        dialog = QDialog(self)

        # Set the dialog's window color and border radius
        dialog.setStyleSheet("""
            QWidget {
                background-color: #1c2948;
                border-radius: 20px;
            }
            QLabel, QLineEdit, QPushButton {
                color: white;
            }
        """)

        layout = QVBoxLayout(dialog)

        # Add a QLabel
        label = QLabel("Enter wallet name:", dialog)
        layout.addWidget(label)

        lineEdit = QLineEdit(dialog)
        layout.addWidget(lineEdit)

        button = QPushButton("OK", dialog)
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)

        # Show the dialog and get the entered wallet name
        if dialog.exec_():
            wallet_name = lineEdit.text()

            # Get the ID of the current user
            cursor = self.conn.cursor()
            cursor.execute("SELECT user_id FROM User WHERE user_id = ?", (self.current_user.userid,))
            use_id = cursor.fetchone()[0]

            # Add the wallet to the database
            cursor.execute("INSERT INTO Wallet (user_id, wallet_name) VALUES (?, ?)", (use_id, wallet_name))

            # Commit the changes and close the cursor
            self.conn.commit()
            cursor.close()

            # Update the combo boxes
            self.ui.group_.addItem(wallet_name)
            self.ui.group_3.addItem(wallet_name)
    
    def update_wallets(self):
        # Fetch all the wallets from the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT wallet_name FROM Wallet where user_id=?;", (self.current_user.userid,))
    
        # Get all the wallet names
        wallet_names = [row[0] for row in cursor.fetchall()]
    
        # Close the cursor
        cursor.close()
    
        
        self.ui.group_.clear()
        self.ui.group_3.clear()
        # Add the wallet names to the combo boxes if they're not already there
       
        self.ui.group_.addItems(wallet_names)
            
        self.ui.group_3.addItems(wallet_names)


    def rename_wallet(self):
        # Create a QDialog
        dialog = QDialog(self)

        # Set the dialog's window color and border radius
        dialog.setStyleSheet("""
            QWidget {
                background-color: #1c2948;
                border-radius: 20px;
            }
            QLabel, QLineEdit, QPushButton {
                color: white;
            }
        """)

        layout = QVBoxLayout(dialog)

        # Add a QLabel and QLineEdit for the old wallet name
        old_label = QLabel("Enter old wallet name:", dialog)
        layout.addWidget(old_label)

        old_lineEdit = QLineEdit(dialog)
        layout.addWidget(old_lineEdit)

        # Add a QLabel and QLineEdit for the new wallet name
        new_label = QLabel("Enter new wallet name:", dialog)
        layout.addWidget(new_label)

        new_lineEdit = QLineEdit(dialog)
        layout.addWidget(new_lineEdit)

        # Add a QLabel for the error message
        error_label = QLabel("", dialog)
        error_label.setStyleSheet("color: red;")
        layout.addWidget(error_label)

        button = QPushButton("OK", dialog)
        button.clicked.connect(lambda: self.rename_wallet_action(old_lineEdit.text(), new_lineEdit.text(), error_label, dialog))
        layout.addWidget(button)
        dialog.exec_()

    def rename_wallet_action(self, old_wallet_name, new_wallet_name, error_label, dialog):
        # Check if the old wallet name exists in the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT 1 FROM Wallet WHERE wallet_name = ?", (old_wallet_name,))
        if cursor.fetchone() is None:
            # If the old wallet name does not exist, show an error message
            error_label.setText("The old wallet name does not exist.")
            return

        # Update the wallet in the database
        cursor.execute("UPDATE Wallet SET wallet_name = ? WHERE wallet_name = ?", (new_wallet_name, old_wallet_name))

        # Commit the changes and close the cursor
        self.conn.commit()
        cursor.close()

        # Update the combo boxes
        index = self.ui.group_.findText(old_wallet_name)
        if index != -1:
            self.ui.group_.setItemText(index, new_wallet_name)

        index = self.ui.group_3.findText(old_wallet_name)
        if index != -1:
            self.ui.group_3.setItemText(index, new_wallet_name)

        # Close the dialog
        dialog.accept()

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

            cursor.execute("select balance from wallet where wallet_id=?",(wallet_id,))
            res1=cursor.fetchone()
            if trans_type=="Income":
                walletbalance = format(res1[0] + float(amount), '.2f')
            else:
                walletbalance = format(res1[0] - float(amount), '.2f')
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

    def display_widget(self):
        # Simulated database query (replace with actual query)
        cursor = self.conn.cursor()
        wallname=self.ui.group_3.currentText()
        cursor.execute("SELECT wallet_id from Wallet where wallet_name=? and user_id=?",(wallname,self.current_user.userid))
        wallet_id=cursor.fetchone()
        if wallet_id is None:
            return
        cursor.execute("SELECT wallet_id, amount, description, category, transaction_type, transaction_date FROM Transactions where wallet_id=?", (wallet_id[0],))
        wallet_data = cursor.fetchall()

        # Find the Monthly_frame_6 inside changingwidget
        monthly_frame = self.ui.changingwidget.widget(1)  # Assuming Monthly_frame_6 is at index 1

        if monthly_frame is not None:
            # Find the scroll area inside Monthly_frame_6
            scroll_area = monthly_frame.findChild(QScrollArea, "scrollArea")

            if scroll_area is not None:
                # Set scroll area to vertical scrolling
                scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

                # Make the scroll bar invisible but still functional
                scroll_area.verticalScrollBar().setStyleSheet("QScrollBar {width:0px;}")

                # Clear previous content
                content_widget = scroll_area.takeWidget()
                if content_widget:
                    content_widget.deleteLater()

                # Create a widget to hold the data entries
                data_widget = QWidget()
                data_layout = QVBoxLayout(data_widget)
                data_widget.setLayout(data_layout)

                # Create widgets for each data entry
                for entry in wallet_data:
                    # Format the date
                    formatted_date = datetime.strptime(entry[5], "%d-%m-%Y %H:%M:%S").strftime("%b %d, %Y")

                    # Create a QLabel for the date and add it to the data_layout
                    date_label = QLabel(f"{formatted_date}")
                    date_label.setStyleSheet("QLabel { color: white; font-family: 'Century Gothic'; font-size: 16px; }")
                    data_layout.addWidget(date_label)

                    entry_widget = QWidget()
                    entry_layout = QVBoxLayout(entry_widget)

                    # Set widget border radius and background color
                    entry_widget.setStyleSheet("QWidget { border-radius: 20px; background-color: rgb(45, 63, 109); }")
                    entry_widget.setFixedHeight(100)
                    entry_label = QLabel(f"Wallet ID: {entry[0]}, Amount: {entry[1]:.2f}, Description: {entry[2]}, Category: {entry[3]}, Type: {entry[4]}", entry_widget)
                    entry_layout.addWidget(entry_label)

                    # Set label color, font, and size
                    entry_label.setStyleSheet("QLabel { color: white; font-family: 'Century Gothic'; font-size: 16px; }")

                    entry_widget.setLayout(entry_layout)
                    data_layout.addWidget(entry_widget)

                    # Add padding between the widgets
                    data_layout.addSpacing(10)  # Set your desired spacing here

                # Set the layout for the scroll area's content
                scroll_area.setWidget(data_widget)
    
    def wallet_balance(self):
        # Get the current wallet name
        wall_name = self.ui.group_3.currentText()
    
        # Fetch the balance from the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT balance FROM Wallet WHERE wallet_name = ?", (wall_name,))
        balance = cursor.fetchone()
    
        # Close the cursor
        cursor.close()
    
        # Update the QLabel with the balance
        if balance is not None:
            self.ui.getbackamount_5.setText(f'<center><span style="font-size: 15pt;">{balance[0]}$</span></center>')
        else:
            self.ui.getbackamount_5.setText("0")

    def update_salary_day(self, date=None):
        # If no date is provided, use the date from the dateEdit widget
        if date is None:
            date = self.ui.dateEdit.date()

        # Update the salary day in the database
        cursor = self.conn.cursor()
        cursor.execute("UPDATE budget_table SET sal_day = ? WHERE user_id = ?", (date.day(), self.current_user.userid))
        self.conn.commit()
        cursor.close()

        # Update the days before salary
        self.days_b_sal()
    def remove_wallet(self):
        # Create a QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Remove Wallet")
        msg.setText("Are you sure you want to remove this wallet?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        # Connect the buttonClicked signal to a slot that closes the message box
        msg.buttonClicked.connect(lambda: msg.done(0))

        if msg.exec_() == QMessageBox.Yes:
            # User clicked 'Yes', so remove the wallet
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Wallet WHERE wallet_name = ?", (self.ui.group_3.currentText(),))
            self.conn.commit()
            cursor.close()

            # Update the combo boxes
            self.update_wallets()
            self.ui.group_3.setCurrentIndex(0)
            self.wallet_balance()
            self.display_widget()
            self.update_Wallets_progressbar()
            self.update_categories_progressbar()
    
    def days_b_sal(self):
        # Get the current date
        current_date = QDate.currentDate()
    
        # Fetch the salary day from the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT sal_day FROM budget_table WHERE user_id = ?", (self.current_user.userid,))
        salary_day = cursor.fetchone()[0]
        cursor.close()
    
        # If salary_day is None, set it to the current day
        if salary_day is None:
            salary_day = current_date.day()
    
        # If the salary day is less than or equal to the current day, add a month to the current date
        if salary_day <= current_date.day():
            current_date = current_date.addMonths(1)
    
        # Set the day of the current date to the salary day
        salary_date = QDate(current_date.year(), current_date.month(), salary_day)
    
        # Set the date of the QDateEdit widget to the salary day
        self.ui.dateEdit.setDate(salary_date)
    
        # Calculate the days before salary
        days_before_salary = QDate.currentDate().daysTo(salary_date)
    
        # Update the QLabel with the days before salary
        self.ui.getbackamount_6.setText(f'<center><span style="font-size: 15pt;">{days_before_salary} days</span></center>')
        self.ui.overview_frame_5.update()
        
    def sign_out(self):
        self.close()
        self.set_login()

    def display_wallet(self):
        # Simulated database query (replace with actual query)
        cursor = self.conn.cursor()
        cursor.execute("SELECT wallet_name, balance FROM Wallet WHERE user_id=?", (self.current_user.userid,))
        wallet_data = cursor.fetchall()
    
        # Find the widget
        widget = self.ui.widget  # Replace with the actual QWidget
        widget_30 = widget.findChild(QWidget, "widget_30")  # Replace with the actual QWidget
    
        # Clear previous content
        if widget_30.layout() is not None:
            # Remove and delete the existing layout's children
            old_layout = widget_30.layout()
            while old_layout.count():
                child = old_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
        else:
            # If widget_30 does not have a layout, create one
            old_layout = QVBoxLayout(widget_30)
            widget_30.setLayout(old_layout)
    
        # Create widgets for each data entry
        for entry in wallet_data:
            # Create a QWidget for each wallet entry
            entry_widget = QWidget()
            entry_layout = QVBoxLayout(entry_widget)
    
            # Set widget border radius and background color
            entry_widget.setStyleSheet("QWidget { border-radius: 20px; background-color: rgb(45, 63, 109); }")
            entry_widget.setFixedHeight(100)
            entry_label = QLabel(f"Wallet Name: {entry[0]}, Balance: {entry[1]:.2f}", entry_widget)
            entry_layout.addWidget(entry_label)
    
            # Set label color, font, and size
            entry_label.setStyleSheet("QLabel { color: white; font-family: 'Century Gothic'; font-size: 16px; }")
    
            entry_widget.setLayout(entry_layout)
            old_layout.addWidget(entry_widget)
    
            # Add padding between the widgets
            old_layout.addSpacing(10)  # Set your desired spacing here
    def remove_account(self):
        # Create a QMessageBox
        msg = QMessageBox()
        msg.setWindowTitle("Remove Account")
        msg.setText("Are you sure you want to remove your account?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        # Connect the buttonClicked signal to a slot that closes the message box
        msg.buttonClicked.connect(lambda: msg.done(0))

        if msg.exec_() == QMessageBox.Yes:
            # User clicked 'Yes', so remove their details from all tables
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM wallet WHERE user_id=?", (self.current_user.userid,))
            cursor.execute("DELETE FROM User WHERE user_id=?", (self.current_user.userid,))
            cursor.execute("DELETE FROM Transactions WHERE wallet_id in (select wallet_id from user where user_id=?)", (self.current_user.userid,))
            cursor.execute("DELETE FROM budget_table WHERE user_id=?", (self.current_user.userid,))
            
            # Commit the changes and close the connection
            self.conn.commit()
            self.conn.close()

            # Close the main window and open the login window
            self.close()
            self.set_login()
            
        

        # Show the QMessageBox and get the result
        result = msg.exec_()

        # If the user clicked Yes, remove the account
        if result == QMessageBox.Yes:
            # Remove the account from the database
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM User WHERE user_id = ?", (self.current_user.userid,))
            self.conn.commit()
            cursor.close()

            # Close the application
            self.close()
    def check_login(self):
        username = self.login_ui.NameEntry_2.text()
        password = self.login_ui.Password_Entry_2.text()
        if self.login(username, password):
   
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
        self.ui.pushButton.clicked.connect(self.display_widget)
        self.ui.group_1.currentIndexChanged.connect(self.update_category)
        self.update_category()
        self.update_categories_progressbar()
        self.update_Wallets_progressbar()
        self.ui.group_3.currentIndexChanged.connect(self.update_Wallets_progressbar)
        self.create_history()
        self.ui.scrollArea_3.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.scrollArea_3.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)    
        self.display_widget()
        self.ui.group_3.currentIndexChanged.connect(self.display_widget)
        self.ui.pushButton_12.clicked.connect(self.add_wallet)
        self.update_wallets()
        self.ui.pushButton_5.clicked.connect(self.rename_wallet)
        self.ui.Wallets_Button.toggled.connect(self.update_Wallets_progressbar)
        self.ui.Wallets_Button.toggled.connect(self.update_categories_progressbar) 
        self.ui.Wallets_Button.toggled.connect(self.wallet_balance)
        self.ui.group_3.currentIndexChanged.connect(self.wallet_balance)
        self.ui.signout_2.clicked.connect(self.set_salary)
        self.ui.signout_3.clicked.connect(self.set_budget)
        self.days_b_sal()
        self.ui.dateEdit.dateChanged.connect(self.update_salary_day)
        self.ui.dateEdit.dateChanged.connect(self.days_b_sal)
        self.ui.accountButton.clicked.connect(self.user_info)
        self.ui.pushButton_2.clicked.connect(self.help1)
        self.ui.pushButton_3.clicked.connect(self.help2)
        self.ui.pushButton_4.clicked.connect(self.help3)
        self.ui.pushButton_6.clicked.connect(self.help4)
        self.ui.pushButton_7.clicked.connect(self.help5)
        self.ui.pushButton_8.clicked.connect(self.help6)
        self.ui.pushButton_9.clicked.connect(self.help7)
        self.ui.pushButton_10.clicked.connect(self.help8)
        self.ui.pushButton_11.clicked.connect(self.help9)
        self.ui.stackedWidget.setCurrentIndex(7)
        self.ui.Settings_Button.toggled.connect(self.display_wallet)
        self.ui.removeaccount.clicked.connect(self.remove_account)
        self.ui.signout.clicked.connect(self.sign_out)
    
    def forgot_password(self):
        msg = QMessageBox()
        msg.setWindowTitle("Forgot Password")
        msg.setText("Did you forget your lunch??")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
    def user_info(self):
        if hasattr(self, 'user_info_window') and self.user_info_window.isVisible():
            self.user_info_window.close()
            return
    
        self.user_info_window = QDialog()
        self.user_info_window.setWindowFlags(Qt.FramelessWindowHint)  # Remove window decorations
        self.user_info_ui = userinfo_class()
        self.user_info_ui.setupUi(self.user_info_window)
        
        # Set up the animation
        self.animation = QPropertyAnimation(self.user_info_window, b"geometry")
        self.animation.setDuration(200)  # Set animation duration in milliseconds
    
        # Get the current geometry of the window
        start_rect = QRect(QApplication.desktop().width(), 95, self.user_info_window.width(), self.user_info_window.height())
    
        # Calculate the end geometry of the window
        end_rect = QRect(QApplication.desktop().width() - self.user_info_window.width(), 95, self.user_info_window.width(), self.user_info_window.height())
    
        # Set the start and end values of the animation
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
    
        cursor=self.conn.cursor()
        cursor.execute("select username from user where user_id=?", (self.current_user.userid,))
        username=cursor.fetchone()
        self.user_info_ui.Name_.setText(f'Name:{username[0]}')
        self.user_info_ui.Name_.setStyleSheet("QLabel { color : white; font-size: 14px; font-family: Century Gothic; }")
        self.user_info_ui.Name_.setAlignment(Qt.AlignCenter)
    
        cursor.execute("select salary from budget_table where user_id=?", (self.current_user.userid,))
        salary=cursor.fetchone()
        self.user_info_ui.Salary.setText(f'Salary:{str(salary[0])}')
        self.user_info_ui.Salary.setStyleSheet("QLabel { color : white; font-size: 14px; font-family: Century Gothic; }")
        self.user_info_ui.Salary.setAlignment(Qt.AlignCenter)
    
        cursor.execute("select budget_amount from budget_table where user_id=?", (self.current_user.userid,))
        budget=cursor.fetchone()
        self.user_info_ui.label_3.setText(f'Budget:{str(budget[0])}')
        self.user_info_ui.label_3.setStyleSheet("QLabel { color : white; font-size: 14px; font-family: Century Gothic; }")
        self.user_info_ui.label_3.setAlignment(Qt.AlignCenter)
    
        # Start the animation
        self.animation.start()
    
        self.user_info_window.show()

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()

    def help1(self):
        self.ui.stackedWidget.setCurrentIndex(7)
    def help2(self):
        self.ui.stackedWidget.setCurrentIndex(8)
    def help3(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def help4(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def help5(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def help6(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    def help7(self):
        self.ui.stackedWidget.setCurrentIndex(5)
    def help8(self):
        self.ui.stackedWidget.setCurrentIndex(6)
    def help9(self):
        self.ui.stackedWidget.setCurrentIndex(4)
#####################################################################################################################################################################################################################################
#################SETTİNGS########################################################################################################################################################
    
    def set_budget(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Set Budget")
        dialog.setStyleSheet("""
            QWidget {
                background-color: #1c2948;
                border-radius: 20px;
            }
            QLabel, QLineEdit, QPushButton {
                color: white;
            }
        """)
    
        layout = QVBoxLayout(dialog)
    
        label = QLabel("Enter your budget:")
        layout.addWidget(label)
    
        lineEdit = QLineEdit()
        layout.addWidget(lineEdit)
    
        button = QPushButton("OK")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)
    
        if dialog.exec_():
            budget = float(lineEdit.text())
    
            # Update the budget in the database
            cursor = self.conn.cursor()
            cursor.execute("UPDATE budget_table SET budget_amount = ? WHERE user_id = ?", (budget, self.current_user.userid))
            self.conn.commit()
            cursor.close()
    
            # Update the current user's budget
            self.current_user.budget = budget
    
            # Update the overview
            self.create_overview()
    
    def set_salary(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Set Salary")
        dialog.setStyleSheet("""
            QWidget {
                background-color: #1c2948;
                border-radius: 20px;
            }
            QLabel, QLineEdit, QPushButton {
                color: white;
            }
        """)
    
        layout = QVBoxLayout(dialog)
    
        label = QLabel("Enter your salary:")
        layout.addWidget(label)
    
        lineEdit = QLineEdit()
        layout.addWidget(lineEdit)
    
        button = QPushButton("OK")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)
    
        if dialog.exec_():
            salary = int(lineEdit.text())
    
            # Update the salary in the database
            cursor = self.conn.cursor()
            cursor.execute("UPDATE budget_table SET salary = ? WHERE user_id = ?", (salary, self.current_user.userid))
            self.conn.commit()
            cursor.close()

    def show_create_account(self):
        self.create_account_window = QDialog()
        self.create_account_window.setWindowTitle('Create Account')
        self.create_account_ui = create_account_class()        
        self.create_account_ui.setupUi(self.create_account_window)
        self.create_account_ui.pushButton.clicked.connect(self.create_account)
        self.create_account_ui.amount_2.setEchoMode(QLineEdit.Password)
        self.create_account_ui.amount_3.setEchoMode(QLineEdit.Password)
        self.create_account_window.show()
    def create_account(self):
        user_name=self.create_account_ui.Name.text()
        password=self.create_account_ui.amount_2.text()
        password2=self.create_account_ui.amount_3.text()
        if password==password2:
            cursor=self.conn.cursor()
            cursor.execute("insert into User(username,password) values(?,?)",(user_name,password))
            self.conn.commit()
            self.create_account_window.close()
        else:
            QMessageBox.warning(self, "error occorred","Passwords do not match!")

#######################################################################################################################################################################################################################################
    
    def create_history(self):
        # Create a scroll area
        scroll_area = self.ui.scrollArea_3

        # Create a main widget for the scroll area
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        cursor = self.conn.cursor()
        cursor.execute("SELECT amount, transaction_date, transaction_type,category,description FROM transactions where wallet_id in(select wallet_id from wallet where user_id=?)ORDER BY transaction_date desc;",(self.current_user.userid,
        ))
        values = cursor.fetchall()

        if not values:
            
            label = QLabel("No transactions yet")
            label.setStyleSheet("font-size: 16px; color:white;") 
            label.setAlignment(Qt.AlignCenter) 
            main_layout.addWidget(label)
            main_widget.setLayout(main_layout)
        else:
            for row in range(len(values)):
                if row <=5:            
                    amount, date, trans_type,category,description = values[row]
                    date = datetime.strptime(date, "%d-%m-%Y %H:%M:%S").strftime("%b %d, %Y, %H:%M:%S")


                    trans_widget = QWidget()
                    
                    trans_layout = QVBoxLayout(trans_widget)

                    label1 = QLabel(str(amount))
                    label1.setStyleSheet("font-size: 16px;border:none;background-color:transparent;")  # Increase the font size
                    label1.setMinimumHeight(20)
                    label1.setMaximumHeight(20)  # Increase the minimum height of the label
                    trans_layout.addWidget(label1)
                    label2 = QLabel(date)
                    label2.setStyleSheet("font-size: 16px;border:none;background-color:transparent;")  # Increase the font size
                    label2.setMinimumHeight(20) 
                    label2.setMaximumHeight(20) # Increase the minimum height of the label
                    trans_layout.addWidget(label2)
                    label3 = QLabel(description)
                    label3.setStyleSheet("font-size: 16px;border:none;background-color:transparent;")  # Increase the font size
                    label3.setMinimumHeight(20)
                    label3.setMaximumHeight(20)  # Increase the minimum height of the label
                    trans_layout.addWidget(label3)
                    label4 = QLabel(category)
                    label4.setStyleSheet("font-size: 16px;border:none;background-color:transparent;")  # Increase the font size
                    label4.setMinimumHeight(20)
                    label4.setMaximumHeight(20)  # Increase the minimum height of the label
                    trans_layout.addWidget(label4)

                    if trans_type == "Expense":
                        trans_widget.setStyleSheet(
            "    background-color: rgba(255, 255, 255, 10);\n"
            "    border: 2px solid rgba(255, 3, 162, 50);\n"
            "    border-radius: 10px;\n"
            "    font-size: 18px;\n"  # Increase the font size
            "    color:white;\n")
                    else:
                        trans_widget.setStyleSheet("background-color: rgba(255, 255, 255, 10);\n"
            "    border: 2px solid rgba(4, 0, 240, 50);\n"
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
                self.conn.commit()
            cursor.execute("select budget_amount from budget_table where user_id=?",(self.current_user.userid,))
            budget=cursor.fetchone()
            if budget!=None:
                self.current_user.budget=budget[0]
            else:
                cursor.execute("insert into budget_table (user_id,budget_amount)values(?,?)",(self.current_user.userid,10000))
                self.conn.commit()
                self.current_user.budget=10000
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
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE category=? AND wallet_id IN (SELECT wallet_id FROM Wallet WHERE user_id = ?)", (category, self.current_user.userid))
            value=cursor.fetchone()
            if value[0]==None:
                value=(0,)
            expenselis.append(value[0])
        cursor.execute("SELECT SUM(amount) FROM Transactions WHERE transaction_type='Expense' AND wallet_id IN (SELECT wallet_id FROM Wallet WHERE user_id = ?)", (self.current_user.userid,))
        total=cursor.fetchone()
      
        total=total[0]

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

    def update_Wallets_progressbar(self):
        cursor=self.conn.cursor()
        expenselis=[]
        selected_wallet = self.ui.group_3.currentText()  # Fetch the current text from the combobox

        for category in self.expense_cat_list:
            cursor.execute("select sum(amount) from transactions t join Wallet w on t.wallet_id = w.wallet_id where t.category=? and w.wallet_name=? and w.user_id=?", (category, selected_wallet, self.current_user.userid))
            value=cursor.fetchone()
            if value[0]==None:
                value=(0,)
            expenselis.append(value[0])

        cursor.execute("select sum(amount) from transactions t join Wallet w on t.wallet_id = w.wallet_id where t.transaction_type='Expense' and w.wallet_name=? and w.user_id=?", (selected_wallet, self.current_user.userid))
        total=cursor.fetchone()
        total=total[0]

        for amount in expenselis:
            if total != 0 and total != None:
                amountpercent = int((amount / total) * 100)
            else:
                amountpercent = 0
            expenselis[expenselis.index(amount)]=amountpercent

        bar_list=[self.ui.food_bar_2,self.ui.travel_2,self.ui.groceries_bar_2,self.ui.clothes_2,self.ui.health_bar_2,self.ui.other_5,self.ui.other_2]
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
        query2 = "CREATE TABLE IF NOT EXISTS Wallet (wallet_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, wallet_name TEXT NOT NULL, balance DECIMAL(10, 2) NOT NULL DEFAULT 0, FOREIGN KEY (user_id) REFERENCES User(user_id));"
        query3 = "CREATE TABLE IF NOT EXISTS Transactions (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, wallet_id INTEGER NOT NULL, amount DECIMAL(10, 2) NOT NULL, description TEXT, category TEXT, transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Income', 'Expense')), transaction_date TEXT DEFAULT (strftime('%d-%m-%Y %H:%M', 'now')), FOREIGN KEY (wallet_id) REFERENCES Wallet(wallet_id));"
        query4 = "CREATE TABLE IF NOT EXISTS budget_table (user_id INT,budget_amount DECIMAL(10, 2) DEFAULT 0.00,salary INTEGER DEFAULT 0,sal_day DATE);"
        
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
        cursor.execute(query4)
        
        # Check if admin user exists
        cursor.execute("SELECT * FROM User WHERE username = 'admin';")
        admin_exists = cursor.fetchone()
    
        if not admin_exists:
            cursor.execute("INSERT INTO User (username, password) VALUES (?, ?);", ('admin', '1234')) 
        self.conn.commit()
        #####################################################################################################################################################################################################################################
    #UI stuff 
    def on_Dashboard_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(0)

    def on_Wallets_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(1)

    def on_Settings_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(2)

    def on_Help_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(3)

    def on_Info_Button_toggled(self):
        self.ui.changingwidget.setCurrentIndex(4)

    def create_overview(self):
        cursor=self.conn.cursor()
        cursor.execute("select sum(amount) from transactions where transaction_type='Expense' and wallet_id in(select wallet_id from wallet where user_id=?);",(self.current_user.userid,))
        total_spend=cursor.fetchone()
        cursor.execute("select sum(amount) from transactions where transaction_type='Income' and wallet_id in(select wallet_id from wallet where user_id=?);",(self.current_user.userid,))
        total_income=cursor.fetchone()
        cursor.execute("select sum(balance) from wallet where user_id=?;",(self.current_user.userid,))
        total_balance=cursor.fetchone()
        if total_balance[0]==None:
            self.ui.getbackamount_4.setText(f'<center><span style="font-size: 15pt;">0$</span></center>')
        else:
            self.ui.getbackamount_4.setText(f'<center><span style="font-size: 15pt;">{format(total_balance[0],'.2f')}$</span></center>')
        self.ui.getbackamount_4.setAlignment(Qt.AlignCenter)
    
        if total_income[0]==None:
            self.ui.owe_amount_4.setText(f'<center><span style="font-size: 15pt;">0$</span></center>')
        else:
            self.ui.owe_amount_4.setText(f'<center><span style="font-size: 15pt;">{total_income[0]}$</span></center>')
        self.ui.owe_amount_4.setAlignment(Qt.AlignCenter)
        if total_spend[0]==None:
            self.ui.spend_amount_4.setText(f'<center><span style="font-size: 15pt;">0$</span></center>')
        else:
            self.ui.spend_amount_4.setText(f'<center><span style="font-size: 15pt;">{total_spend[0]}$</span></center>')
        self.ui.spend_amount_4.setAlignment(Qt.AlignCenter)
       
        self.ui.label_43.setText(f'<center><span style="font-size: 15pt;">{self.current_user.budget}$</span></center>')
        self.ui.label_43.setAlignment(Qt.AlignCenter)
        self.draw_graph()

       

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
    def last_7_days():
        # Get today's date
        today = datetime.now().date()
        
        # Create a list to store the dates
        dates = []

        # Loop through the last 7 days
        for i in range(6, -1, -1):
            # Subtract days from today to get previous dates
            date = today - timedelta(days=i)
            dates.append(date)
        
        return dates

    # Test the function
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

        self.plot_widget.setBackground(None)
        
        self.draw_graph()
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
    def draw_graph(self):
        # Set view range for x and y axes
        self.plot_widget.setXRange(0, 30)
        self.plot_widget.setYRange(0, 20)

        # Adjust view limits
        self.plot_widget.setLimits(xMin=0, xMax=31, yMin=0, yMax=1000000000)

        # Disable x-axis zooming
        self.plot_widget.setMouseEnabled(x=False, y=True)

        # Get the selected heading from the combo box
        heading = self.ui.comboBox_3.currentText()
        self.plot_widget.setTitle(heading)

        # Create a gradient for the plot line
        gradient = QLinearGradient(0, 0, 0, self.current_user.budget)
        gradient.setColorAt(0.0, QColor('#0d00ff'))
        gradient.setColorAt(1.0, QColor('#f000bc'))
        pen = QPen(gradient, 1)
        pen.setWidth(0)

        # Clear the plot widget
        self.plot_widget.clear()

        # Set up date axis
        date_axis = DateAxisItem(orientation='bottom')
        self.plot_widget.setAxisItems({'bottom': date_axis})
        cursor=self.conn.cursor()


      
        # Initialize days7 as an empty list
        days7 = []
        
        # Get the dates for the last 7 days
        dates = [(datetime.now() - timedelta(days=i)).strftime('%d-%m-%Y') for i in range(7)]
        
        # Execute the query for each date
        cursor = self.conn.cursor()
        for date in dates:
            cursor.execute("SELECT SUM(amount) FROM Transactions WHERE transaction_type='Expense' and transaction_date LIKE ? AND wallet_id IN (SELECT wallet_id FROM Wallet WHERE user_id = ?);", (f'%{date}%', self.current_user.userid))
            result = cursor.fetchone()
            days7.append(result)
        
        now = datetime.now()
        year = now.year
        month = now.month
        _, num_days = monthrange(year, month)

        months_data=[]
        months_dates= [(datetime(year, month, day)).strftime('%d-%m-%Y') for day in range(1, num_days+1)]
        for date in months_dates:
            cursor.execute("SELECT SUM(amount) FROM Transactions WHERE transaction_type='Expense' and transaction_date LIKE ? AND wallet_id IN (SELECT wallet_id FROM Wallet WHERE user_id = ?);", (f'%{date}%', self.current_user.userid))
            result = cursor.fetchone()
            months_data.append(result)
        year_data=[]
        for i in range(1,13):
            if i<10:
                i=f'0{i}'
            cursor.execute("SELECT SUM(amount) FROM Transactions WHERE transaction_type='Expense' and transaction_date LIKE ? AND wallet_id IN (SELECT wallet_id FROM Wallet WHERE user_id = ?);", (f'%-{i}-%', self.current_user.userid))
            result = cursor.fetchone()
            year_data.append(result)
        if heading == "Last 7 days":
            # Use actual day names for x-axis labels
            x_labels = self.last_seven_days()
            for i in range(len(days7)):
                days7[i] = days7[i][0] if days7[i][0] is not None else 0
                days7=days7[::-1]   
            x = np.arange(7)  # Use the actual day of the week as x-values
            y = np.array(days7)
            self.plot = self.plot_widget.plot(x, y, pen=pen)
            self.plot_widget.getAxis('bottom').setTicks([[(i, label) for i, label in enumerate(x_labels)]])
            self.plot_widget.setLabel('bottom', 'Day')

        elif heading == "This month":
            # Extract day of the week from transaction date
            x_labels = [date.split('-')[0] for date in months_dates]
            for i in range(len(months_data)):
                months_data[i] = months_data[i][0] if months_data[i][0] is not None else 0
            x=np.arange(len(months_dates))
            y = np.array(months_data)
            self.plot = self.plot_widget.plot(x, y, pen=pen)
            self.plot_widget.getAxis('bottom').setTicks([[(i, label) for i, label in enumerate(x_labels)]])
            self.plot_widget.setLabel('bottom', 'Day')

        elif heading == "This year":
            # Use month names for x-axis labels
            x_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            x = np.arange(12)  # Use the month index as x-values
            for i in range(len(year_data)):
                year_data[i] = year_data[i][0] if year_data[i][0] is not None else 0
            
            y = np.array(year_data)
            self.plot = self.plot_widget.plot(x, y, pen=pen)
            self.plot_widget.getAxis('bottom').setTicks([[(i, label) for i, label in enumerate(x_labels)]])
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
