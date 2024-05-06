import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
import pyqtgraph as pg
import sqlite3
from datetime import datetime, timedelta

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Tracker Graphs")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        self.plot_button = QPushButton("Plot Last 7 Days")
        self.plot_button.clicked.connect(self.plot_last_7_days)
        self.layout.addWidget(self.plot_button)

        self.plot_button2 = QPushButton("Plot Weekly Sum")
        self.plot_button2.clicked.connect(self.plot_weekly_sum)
        self.layout.addWidget(self.plot_button2)

        self.plot_button3 = QPushButton("Plot Monthly Sum")
        self.plot_button3.clicked.connect(self.plot_monthly_sum)
        self.layout.addWidget(self.plot_button3)

        self.conn = sqlite3.connect('Expenzio.db')
        
    def query_database(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def plot_last_7_days(self):
        query = """
            SELECT strftime('%Y-%m-%d', transaction_date) as date, sum(amount) 
            FROM transactions 
            WHERE transaction_date >= date('now', '-7 days')
            GROUP BY strftime('%Y-%m-%d', transaction_date)
        """
        result = self.query_database(query)
        dates = [datetime.strptime(row[0], '%Y-%m-%d').strftime('%A') for row in result]
        amounts = [row[1] for row in result]
        self.plot_graph(dates, amounts, 'Day', 'Amount ($)')

    def plot_weekly_sum(self):
        query = """
            SELECT strftime('%W', transaction_date) as week, sum(amount) 
            FROM transactions 
            WHERE strftime('%Y', transaction_date) = strftime('%Y', 'now')
            GROUP BY strftime('%W', transaction_date)
        """
        result = self.query_database(query)
        weeks = [f'Week {row[0]}' for row in result]
        amounts = [row[1] for row in result]
        self.plot_graph(weeks, amounts, 'Week', 'Amount ($)')

    def plot_monthly_sum(self):
        query = """
            SELECT strftime('%m', transaction_date) as month, sum(amount) 
            FROM transactions 
            WHERE strftime('%Y', transaction_date) = strftime('%Y', 'now')
            GROUP BY strftime('%m', transaction_date)
        """
        result = self.query_database(query)
        months = [datetime.strptime(row[0], '%m').strftime('%B') for row in result]
        amounts = [row[1] for row in result]
        self.plot_graph(months, amounts, 'Month', 'Amount ($)')

    def plot_graph(self, x, y, x_label, y_label):
        self.plot_widget.clear()
        self.plot_widget.plot(x, y, pen='b')
        self.plot_widget.setLabel('bottom', x_label)
        self.plot_widget.setLabel('left', y_label)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
