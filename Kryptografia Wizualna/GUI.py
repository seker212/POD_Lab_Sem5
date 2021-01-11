from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import tkinter
from tkinter import filedialog
import sys
from unidecode import unidecode
import pathlib
import os
import crypt

root = tkinter.Tk()
root.withdraw()
ENCODING = 'utf-8'

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Okno, self).__init__(*args,*kwargs)
        # Class Variables START
        self.inputFilePath = None
        self.additionalImageFilePath = None
        self.outputFilePath = None
        # Class Variables END

        self.setWindowTitle("Kryptografia Wizualna")
        
        # Text Fields START
        titleText = QLabel()
        titleText.setText("Kryptografia Wizualna")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Impact',24))

        authorText = QLabel()
        authorText.setText("Sebastian Skrobich 140779")
        authorText.setAlignment(Qt.AlignCenter)
        authorText.setFont(QFont('Impact',16))
        authorText.setStyleSheet("QLabel {color : grey}")

        self.inputFileTextField = QLineEdit()
        self.inputFileTextField.setReadOnly(True)

        self.additionalImageFileTextField = QLineEdit()
        self.additionalImageFileTextField.setReadOnly(True)

        self.outputFileTextField = QLineEdit()
        self.outputFileTextField.setReadOnly(True)
        # Text Fields END


        # Buttons START
        encryptButton = QPushButton()
        encryptButton.setText("WRITE")
        encryptButton.clicked.connect(self.encryptClicked)

        self.wideButton = QRadioButton("1x2")
        self.squareButton = QRadioButton("2x2")
        self.squareButton.setChecked(True)

        decryptButton = QPushButton()
        decryptButton.setText("READ")
        decryptButton.clicked.connect(self.decryptClicked)

        inputFileButton = QPushButton()
        inputFileButton.setText("CHOOSE INPUT IMAGE FILE")
        inputFileButton.clicked.connect(lambda: self.selectClicked(0))

        additionalImageFileButton = QPushButton()
        additionalImageFileButton.setText("CHOOSE ADDITIONAL IMAGE FILE")
        additionalImageFileButton.clicked.connect(lambda: self.selectClicked(1))

        outputFileButton = QPushButton()
        outputFileButton.setText("CHOOSE OUTPUT IMAGE FILE")
        outputFileButton.clicked.connect(lambda: self.selectClicked(2))

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

        # Text File Box
        
        # Encrypt/Decrypt Button Box
        encryptButtonsL = QHBoxLayout()
        encryptButtonsL.addWidget(encryptButton)
        encryptButtonsL.addWidget(decryptButton)
        encryptButtonsLW = QWidget()
        encryptButtonsLW.setLayout(encryptButtonsL)

        modeButtonsL = QHBoxLayout()
        modeButtonsL.addWidget(self.wideButton)
        modeButtonsL.addWidget(self.squareButton)
        modeButtonsLW = QWidget()
        modeButtonsLW.setLayout(modeButtonsL)

        # Text File Select Box
        setTextFileL = QHBoxLayout()
        setTextFileL.addWidget(self.inputFileTextField)
        setTextFileL.addWidget(inputFileButton)
        setTextFileLW = QWidget()
        setTextFileLW.setLayout(setTextFileL)

        # Key File Select Box
        setKeyFileL = QHBoxLayout()
        setKeyFileL.addWidget(self.additionalImageFileTextField)
        setKeyFileL.addWidget(additionalImageFileButton)
        setKeyFileLW = QWidget()
        setKeyFileLW.setLayout(setKeyFileL)

        # Output File Select Box
        setOutputFileL = QHBoxLayout()
        setOutputFileL.addWidget(self.outputFileTextField)
        setOutputFileL.addWidget(outputFileButton)
        setOutputFileLW = QWidget()
        setOutputFileLW.setLayout(setOutputFileL)

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
        mainMenu.addWidget(setKeyFileLW)
        mainMenu.addWidget(setOutputFileLW)
        mainMenu.addWidget(encryptButtonsLW)
        mainMenu.addWidget(modeButtonsLW)

        mainMenu.addWidget(infoLW)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)


    def encryptClicked(self):
        if (self.inputFilePath is None or self.additionalImageFilePath is None or self.outputFilePath is None):
            self.errorMessageBox("Some paths are empty.")
        else:
            crypt.encrypt(self.inputFilePath, self.additionalImageFilePath, self.outputFilePath, self.squareButton.isChecked())
            
    
    def decryptClicked(self):
        if (self.inputFilePath is None or self.additionalImageFilePath is None or self.outputFilePath is None):
            self.errorMessageBox("Some paths are empty.")
        else:
            crypt.dectypt(self.inputFilePath, self.additionalImageFilePath, self.outputFilePath)
    
    def selectClicked(self, typeInt):
        filePath = filedialog.askopenfilename()
        if typeInt == 0:
            self.inputFilePath = filePath
            self.inputFileTextField.setText(filePath)
        elif typeInt == 1:
            self.additionalImageFilePath = filePath
            self.additionalImageFileTextField.setText(filePath)
        elif typeInt == 2:
            self.outputFilePath = filePath
            self.outputFileTextField.setText(filePath)
            
    
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