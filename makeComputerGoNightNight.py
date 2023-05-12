import os
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDateTimeEdit, QLabel
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtGui import QFont, QPalette
import sys

app = QApplication(sys.argv)
class setTimeScreen(QWidget):
    def __init__(self, parent=None):
        super(setTimeScreen, self).__init__(parent)

        # self.resize(400,400)
        self.timeBox = QDateTimeEdit(QTime.currentTime().addSecs(7199))
        self.timeBox.setFont(QFont('Arial', 24, QFont.Bold))
        self.timeBox.setWrapping(True)
        executeButton = QPushButton("Sleep!")
        executeButton.setFont(QFont('Arial', 24, QFont.Bold))
        executeButton.clicked.connect(self.executeTimeStart)
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.timeBox)
        buttonLayout.addWidget(executeButton)
        self.timeUntilLabel = QLabel("2 hours until sleep.")
        self.timeUntilLabel.setFont(QFont('Arial', 24, QFont.Bold))

        layout = QVBoxLayout()
        layout.addWidget(QLabel("When would you like to go to sleep?"))
        layout.addLayout(buttonLayout)
        layout.addWidget(self.timeUntilLabel)
        self.setLayout(layout)

        timer = QTimer(self)
        timer.timeout.connect(self.setTimeUntil)
        timer.start(1000)


    def executeTimeStart(self, _):
        swapBetweenScreens(True, self.timeBox.time())

    def setTimeUntil(self):
        timeUntilSeconds = QTime.currentTime().secsTo(self.timeBox.time())
        if timeUntilSeconds < 0:
            timeUntilSeconds = timeUntilSeconds + 86400
        self.timeUntilLabel.setText(str(round(timeUntilSeconds/60/60, 1)) + " hours until sleep.")

class clockTimeScreen(QWidget):
    def __init__(self, time):
        super().__init__()
        self.time = time
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setGeometry(100, 100, 800, 400)
        self.showFullScreen()
        self.setStyleSheet("background-color:black;")
        
        layout = QVBoxLayout()
        font = QFont('Arial', 120, QFont.Bold)
        self.label = QLabel()
        self.label.setStyleSheet("color:#121212;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font)
        layout.addWidget(self.label)

        buttonLayout = QHBoxLayout()
        decreaseTimeButton = QPushButton("<<")
        decreaseTimeButton.setStyleSheet("color: white;")
        decreaseTimeButton.clicked.connect(self.decreaseTimeButtonPressed)
        buttonLayout.addWidget(decreaseTimeButton)

        cancelButton = QPushButton("Cancel")
        cancelButton.setStyleSheet("color: white;")
        cancelButton.clicked.connect(self.cancelButtonPressed)
        buttonLayout.addWidget(cancelButton)

        increaseTimeButton = QPushButton(">>")
        increaseTimeButton.setStyleSheet("color: white;")
        increaseTimeButton.clicked.connect(self.increaseTimeButtonPressed)
        buttonLayout.addWidget(increaseTimeButton)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

        loopTimer = QTimer(self)
        loopTimer.timeout.connect(self.showTime)
        loopTimer.start(1000)

        current_time = QTime.currentTime()
        distanceToTimeInSeconds = current_time.secsTo(self.time)
        if distanceToTimeInSeconds < 0:
            distanceToTimeInSeconds = distanceToTimeInSeconds + 86400
        self.shutOffTimer = QTimer(self)
        self.shutOffTimer.timeout.connect(self.goNightNight)
        self.shutOffTimer.start(distanceToTimeInSeconds*1000)

    def showTime(self):
        current_time = QTime.currentTime()
        distanceToTimeInSeconds = current_time.secsTo(self.time)
        if distanceToTimeInSeconds < 0:
            distanceToTimeInSeconds = distanceToTimeInSeconds + 86400
        hours = int(distanceToTimeInSeconds / 60 / 60)
        minutes = int((distanceToTimeInSeconds / 60 ) - (60 * hours))
        seconds = distanceToTimeInSeconds % 60
        if distanceToTimeInSeconds < 5:
            self.label.setStyleSheet("color:#121212;")
            label_time = "Goodnight :)"
        elif distanceToTimeInSeconds < 60:
            label_time = str(seconds)
            self.label.setStyleSheet("color:#540000;")
        elif distanceToTimeInSeconds < 3600:
            label_time = str(minutes) + ":" + str(seconds)
        else:
            label_time = str(hours) + ":" + str(minutes) + ":" + str(seconds)
        self.label.setText(label_time)

    
    def goNightNight(self):
        os.system("shutdown.exe /h")
        QApplication.quit()


    def cancelButtonPressed(self):
        swapBetweenScreens(False, None)
    
    def decreaseTimeButtonPressed(self):
        self.time = self.time.addSecs(-1800)
        self.updateTimerInterval()


    def increaseTimeButtonPressed(self):
        self.time = self.time.addSecs(3600)
        self.updateTimerInterval()

    def updateTimerInterval(self):
        distanceToTimeInSeconds = QTime.currentTime().secsTo(self.time)
        if distanceToTimeInSeconds < 0:
            distanceToTimeInSeconds = distanceToTimeInSeconds + 86400
        self.shutOffTimer.setInterval(distanceToTimeInSeconds * 1000)

mainWindow = setTimeScreen()
mainWindow.show()

secondScreen = QWidget()



def swapBetweenScreens(isMainScreen, time):
    global mainWindow
    global secondScreen 
    if isMainScreen:
        mainWindow.hide()
        secondScreen = clockTimeScreen(time)
        secondScreen.show()
    else:
        secondScreen.hide()
        mainWindow.show()

sys.exit(app.exec_())
