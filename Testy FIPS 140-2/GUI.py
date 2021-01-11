from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import tkinter
from tkinter import filedialog
import sys
from unidecode import unidecode
import pathlib
import tests
import os

root = tkinter.Tk()
root.withdraw()
ENCODING = 'utf-8'

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Okno, self).__init__(*args,*kwargs)
        # Class Variables START
        self.filePath = None
        # Class Variables END

        self.setWindowTitle("Tests")
        
        # Text Fields START
        titleText = QLabel()
        titleText.setText("Tests")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Impact',24))

        authorText = QLabel()
        authorText.setText("Sebastian Skrobich 140779")
        authorText.setAlignment(Qt.AlignCenter)
        authorText.setFont(QFont('Impact',16))
        authorText.setStyleSheet("QLabel {color : grey}")

        singleBitsText = QLabel()
        singleBitsText.setText("Single Bits Test:")
        singleBitsText.setFont(QFont('Impact',14))

        seriesText = QLabel()
        seriesText.setText("Series Test:")
        seriesText.setFont(QFont('Impact',14))

        longSeriesText = QLabel()
        longSeriesText.setText("Long Series Test:")
        longSeriesText.setFont(QFont('Impact',14))

        pokerText = QLabel()
        pokerText.setText("Poker Test:")
        pokerText.setFont(QFont('Impact',14))


        self.singleBitsResult = QLabel()
        self.singleBitsResult.setFont(QFont('Impact',14))
        self.seriesResult = QLabel()
        self.seriesResult.setFont(QFont('Impact',14))
        self.longSeriesResult = QLabel()
        self.longSeriesResult.setFont(QFont('Impact',14))
        self.pokerResult = QLabel()
        self.pokerResult.setFont(QFont('Impact',14))

        self.fileTextField = QLineEdit()
        self.fileTextField.setReadOnly(True)
        # Text Fields END


        # Buttons START
        runButton = QPushButton()
        runButton.setText("RUN TESTS")
        runButton.clicked.connect(self.runClicked)

        textFileButton = QPushButton()
        textFileButton.setText("CHOOSE FILE")
        textFileButton.clicked.connect(lambda: self.selectClicked())

        infoButton = QPushButton()
        infoButton.setText("INFO")
        infoButton.clicked.connect(self.infoClicked)
        # Buttons END


        # Parts Layout START
        # Title Box
        titleL = QVBoxLayout()
        titleL.addWidget(titleText)
        titleL.addWidget(authorText)
        titleLW = QWidget()
        titleLW.setLayout(titleL)

        # Result Box
        resiltLabelsL = QVBoxLayout()
        resiltLabelsL.addWidget(singleBitsText)
        resiltLabelsL.addWidget(seriesText)
        resiltLabelsL.addWidget(longSeriesText)
        resiltLabelsL.addWidget(pokerText)
        resultL = QVBoxLayout()
        resultL.addWidget(self.singleBitsResult)
        resultL.addWidget(self.seriesResult)
        resultL.addWidget(self.longSeriesResult)
        resultL.addWidget(self.pokerResult)
        fullResultL = QHBoxLayout()
        fullResultL.addLayout(resiltLabelsL)
        fullResultL.addLayout(resultL)
        fullResultLW = QWidget()
        fullResultLW.setLayout(fullResultL)


        # Run Button Box
        runButtonsL = QHBoxLayout()
        runButtonsL.addWidget(runButton)
        runButtonsLW = QWidget()
        runButtonsLW.setLayout(runButtonsL)

        # Text File Select Box
        setTextFileL = QHBoxLayout()
        setTextFileL.addWidget(self.fileTextField)
        setTextFileL.addWidget(textFileButton)
        setTextFileLW = QWidget()
        setTextFileLW.setLayout(setTextFileL)

        # Info Button Box
        infoL = QVBoxLayout()
        infoL.addWidget(infoButton)
        infoLW = QWidget()
        infoLW.setLayout(infoL)
        # Parts Layout END


        #Main Layout
        mainMenu = QVBoxLayout()
        mainMenu.setAlignment(Qt.AlignCenter)
        mainMenu.addWidget(titleLW)
        
        mainMenu.addWidget(setTextFileLW)
        mainMenu.addWidget(fullResultLW)
        mainMenu.addWidget(runButtonsLW)

        mainMenu.addWidget(infoLW)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)


    def runClicked(self):
        if self.filePath is None:
            self.errorMessageBox("File path is empty.")
        elif os.stat(self.filePath).st_size < 20000:
            self.errorMessageBox("File is too short.")
        else:
            try:
                self.fillResult(tests.single_bits_test(self.filePath), self.singleBitsResult) 
                self.fillResult(tests.series_test(self.filePath), self.seriesResult) 
                self.fillResult(tests.long_series_test(self.filePath), self.longSeriesResult) 
                self.fillResult(tests.poker_test(self.filePath), self.pokerResult) 
            except Exception as error:
                self.errorMessageBox(str(error))

    def fillResult(self, test, field):
        if test == True:
            field.setStyleSheet("QLabel {color : green}")
            field.setText("POSITIVE")
        elif test == False:
            field.setStyleSheet("QLabel {color : red}")
            field.setText("NEGATIVE") 
    
    def selectClicked(self):
        filePath = filedialog.askopenfilename()
        self.filePath = filePath
        self.fileTextField.setText(filePath)
            
    
    def infoClicked(self):
        infoBox = QMessageBox()
        infoBox.setWindowTitle("INFO")
        with open('info.txt', 'rb') as infoFile:
            data = infoFile.read().decode('utf-8')
        infoBox.setText(data)
        infoBox.exec_()

    def errorMessageBox(self,text):
        errorBox = QMessageBox()
        errorBox.setWindowTitle("Error")
        errorBox.setText(text)
        errorBox.exec_()


#MAIN
app = QApplication(sys.argv)
window = Okno()
window.setFixedSize(500,400)
window.setStyleSheet("background-color: rgb(245,245,220)")
window.show()

app.exec_()