from PyQt5 import QtWidgets,QtCore,QtGui
from colour import Color
class Button(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        #Timer for smooth transitions
        self.tm = QtCore.QBasicTimer()
        # Initialize mouse state
        self.mouse = ''
        self.grade = 0
        # Initialize shadow expansion properties
        self.expand = 0
        self.maxExpand = 4
        
    # Event handler for mouse enter
    def enterEvent(self, e) -> None:
        self.mouse = 'on'
        self.tm.start(20, self)

    # Event handler for mouse leave
    def leaveEvent(self, e) -> None:
        self.mouse = 'off'

    # Timer event for smooth transitions
    def timerEvent(self, e) -> None:
        if self.mouse == 'on' and self.expand < self.maxExpand:
            self.expand += 1
            #self.shadow.setColor(QtGui.QColor(self.garding_s_seq[self.expand-1]))
            self.setGeometry(self.x()-1, int(self.y()-1), self.width()+2, self.height()+2)
        elif self.mouse == 'off' and  self.expand > 0:
            self.expand -= 1
            self.setGeometry(self.x()+1, int(self.y()+1), self.width()-2, self.height()-2)
        elif self.mouse == 'off' and self.expand in [0, self.maxExpand]:
           # self.shadow.setColor(QtGui.QColor(self.init_s_color))
            self.tm.stop()
class custFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shadow = QtWidgets.QGraphicsDropShadowEffect()
        self.setGraphicsEffect(self.shadow)
        #Timer for smooth transitions
        self.tm = QtCore.QBasicTimer()
        self.shadow.setOffset(7,10)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QtGui.QColor("#0f0936"))
        self.repeatationtime=4
        

        # Initialize mouse state
        self.mouse = ''
        # Initialize color gradient for button background

        self.grade = 0
        
        self.timer=0
        # Initialize shadow expansion properties
        self.expand = 0
        self.maxExpand = 4
        self.init_s_color = "#0f0936"
        self.end_s_color = "#0098FF"
        self.garding_s_seq = self.gradeColor(c1=self.init_s_color, c2=self.end_s_color, steps=self.maxExpand)
    

    # Method to change button color
    def changeColor(self, color=(255,255,255)):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
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
        if self.mouse == 'on' and self.expand < self.maxExpand:
            self.expand += 1
            self.shadow.setOffset(1,2)
            self.shadow.setColor(QtGui.QColor(self.garding_s_seq[self.expand-1]))
            self.setGeometry(self.x()-1, int(self.y()-1), self.width()+2, self.height()+2)
        elif self.mouse == 'off' and  self.expand > 0:
            self.expand -= 1
            self.setGeometry(self.x()+1, int(self.y()+1), self.width()-2, self.height()-2)
        elif self.mouse == 'off' and self.expand in [0, self.maxExpand]:
            self.shadow.setOffset(7,10)
            self.shadow.setColor(QtGui.QColor(self.init_s_color))
            self.tm.stop()
        
class statframe(custFrame):
     def give_size(self,windoww,windowh):
         self.wcounter=int((windoww/8)/self.repeatationtime)
         self.hcounter=int((windowh)/5/self.repeatationtime)
         self.xcounter=int((windoww)/9/self.repeatationtime)
         self.ycounter=int((windowh)/9/self.repeatationtime)

     def timerEvent(self,e) -> None:
        delaytime=65
        
        maxtimer=delaytime+self.repeatationtime
        self.raise_()
        if self.mouse == 'on' and self.expand < self.maxExpand:
            self.expand += 1
            self.shadow.setColor(QtGui.QColor(self.garding_s_seq[self.expand-1]))
            self.shadow.setOffset(1,2)
            self.setGeometry(self.x()-1, int(self.y()-1), self.width()+2, self.height()+2)
        elif self.mouse == 'off' and self.timer > delaytime and self.expand==self.maxExpand:
            self.timer-=1
            self.setGeometry(self.x()-self.xcounter, int(self.y()+self.ycounter), self.width()-self.wcounter, self.height()-self.hcounter)

        elif self.mouse == 'off' and  self.expand > 0 :
            self.expand -= 1
            self.timer -= 1
            self.setGeometry(self.x()+1, int(self.y()+1), self.width()-2, self.height()-2)
        elif self.mouse == 'off' and self.expand in [0, self.maxExpand]:
            self.shadow.setOffset(7,10)
            self.shadow.setColor(QtGui.QColor(self.init_s_color))
            self.timer=0
            self.tm.stop()
        elif self.mouse == 'on' and self.expand==self.maxExpand and self.timer<maxtimer:
                self.timer+=1
                if self.timer>delaytime:
                    self.setGeometry(self.x()+self.xcounter, int(self.y()-self.ycounter), self.width()+self.wcounter, self.height()+self.hcounter)
                    
        
        
