import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QListWidget, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Expense Tracker')
        self.setWindowIcon(QIcon('icon.png'))
        
        self.expenses = []

        self.init_ui()
        
        self.load_expenses()

    def init_ui(self):
        # Widgets
        self.expense_label = QLabel('Expense:')
        self.expense_input = QLineEdit()
        
        self.category_label = QLabel('Category:')
        self.category_input = QLineEdit()
        
        self.add_button = QPushButton('Add Expense')
        self.add_button.clicked.connect(self.add_expense)

        self.expense_list = QListWidget()
        self.expense_list.itemDoubleClicked.connect(self.edit_expense)

        self.delete_button = QPushButton('Delete Expense')
        self.delete_button.clicked.connect(self.delete_expense)
        
        self.save_button = QPushButton('Save Expenses')
        self.save_button.clicked.connect(self.save_expenses)
        
        self.load_button = QPushButton('Load Expenses')
        self.load_button.clicked.connect(self.load_expenses)

        # Layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.expense_label)
        input_layout.addWidget(self.expense_input)
        input_layout.addWidget(self.category_label)
        input_layout.addWidget(self.category_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)

        file_button_layout = QHBoxLayout()
        file_button_layout.addWidget(self.save_button)
        file_button_layout.addWidget(self.load_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.expense_list)
        main_layout.addLayout(file_button_layout)

        self.setLayout(main_layout)

    def add_expense(self):
        expense = self.expense_input.text()
        category = self.category_input.text()
        
        if expense and category:
            self.expenses.append({'expense': expense, 'category': category})
            self.update_expense_list()
            self.expense_input.clear()
            self.category_input.clear()

    def edit_expense(self, item):
        new_expense, ok_pressed = QInputDialog.getText(self, "Edit Expense", 
                                                        "Expense:", QLineEdit.Normal, item.text())
        if ok_pressed and new_expense:
            index = self.expense_list.row(item)
            self.expenses[index]['expense'] = new_expense
            self.update_expense_list()

    def delete_expense(self):
        selected_items = self.expense_list.selectedItems()
        if not selected_items:
            return
        
        confirm = QMessageBox.question(self, 'Delete Expense', 'Are you sure you want to delete the selected expense(s)?',
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            for item in selected_items:
                index = self.expense_list.row(item)
                del self.expenses[index]
            self.update_expense_list()

    def update_expense_list(self):
        self.expense_list.clear()
        for item in self.expenses:
            self.expense_list.addItem(f"{item['expense']} - {item['category']}")

    def save_expenses(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Expenses', '', 'JSON Files (*.json)')
        if filename:
            with open(filename, 'w') as f:
                json.dump(self.expenses, f)
    
    def load_expenses(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Load Expenses', '', 'JSON Files (*.json)')
        if filename:
            with open(filename, 'r') as f:
                self.expenses = json.load(f)
            self.update_expense_list()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tracker = ExpenseTracker()
    tracker.show()
    sys.exit(app.exec_())
