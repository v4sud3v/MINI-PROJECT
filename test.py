from PyQt5 import QtWidgets, QtGui, QtCore
from colour import Color # pip install colour

# Main widget class
class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        # Set stylesheet to customize button appearance
        self.setStyleSheet("QPushButton{height: 30px;width: 200px;}")

        # Create horizontal layout
        layout = QtWidgets.QHBoxLayout()

        # Create custom button
        btn = Button("2020 is an interesting year.")
        
        # Add button to layout
        layout.addStretch()
        layout.addWidget(btn)
        layout.addStretch()
        self.setLayout(layout)

# Custom button class
class Button(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Add shadow effect to the button
        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.setGraphicsEffect(self.shadow)
       # Timer for smooth transitions
        self.tm = QtCore.QBasicTimer()
        
        # Set initial shadow properties
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QtGui.QColor("#3F3F3F"))
        
        # Initialize mouse state
        self.mouse = ''
        # Initialize color gradient for button background
        self.changeColor(color="lightgrey")
        self.grade = 0
        
        # Initialize shadow expansion properties
        self.expand = 0
        self.maxExpand = 4
        self.init_s_color = "#3F3F3F"
        self.end_s_color = "#FFFF33"
        self.garding_s_seq = self.gradeColor(c1=self.init_s_color, c2=self.end_s_color, steps=self.maxExpand)
        
        # Initialize background color gradient properties
        self.maxGrade = 15
        self.init_bg_color = "lightgrey"
        self.end_bg_color = "darkgrey"
        self.gradding_bg_seq = self.gradeColor(c1=self.init_bg_color, c2=self.end_bg_color, steps=self.maxGrade)

    # Method to change button color
    def changeColor(self, color=(255,255,255)):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(color))
        self.setPalette(palette)

    # Method to generate color gradient
    def gradeColor(self, c1, c2, steps):
        return list([str(i) for i in Color(c1).range_to(Color(c2), steps)])

    # Event handler for mouse enter
    def enterEvent(self, e) -> None:
        self.mouse = 'on'
        self.tm.start(15, self)

    # Event handler for mouse leave
    def leaveEvent(self, e) -> None:
        self.mouse = 'off'

    # Timer event for smooth transitions
    def timerEvent(self, e) -> None:
        if self.mouse == 'on' and self.grade < self.maxGrade:
            self.grade += 1
            self.changeColor(color=self.gradding_bg_seq[self.grade-1])
        elif self.mouse == 'off' and self.grade > 0:
            self.changeColor(color=self.gradding_bg_seq[self.grade-1])
            self.grade -= 1

        if self.mouse == 'on' and self.expand < self.maxExpand:
            self.expand += 1
            self.shadow.setColor(QtGui.QColor(self.garding_s_seq[self.expand-1]))
            self.setGeometry(self.x()-1, int(self.y()-1), self.width()+2, self.height()+2)
        elif self.mouse == 'off' and  self.expand > 0:
            self.expand -= 1
            self.setGeometry(self.x()+1, int(self.y()+1), self.width()-2, self.height()-2)
        elif self.mouse == 'off' and self.expand in [0, self.maxExpand] and self.grade in [0, self.maxGrade]:
            self.shadow.setColor(QtGui.QColor(self.init_s_color))
            self.tm.stop()

# Main program
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    main = Main()
    main.show()
    app.exec_()
