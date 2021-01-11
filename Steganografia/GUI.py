from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import tkinter
from tkinter import filedialog
import sys
from unidecode import unidecode
import pathlib
import os
import steganografia

root = tkinter.Tk()
root.withdraw()
ENCODING = 'utf-8'

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Okno, self).__init__(*args,*kwargs)
        # Class Variables START
        self.textFilePath = None
        self.bitmapFilePath = None
        self.outputFilePath = None
        # Class Variables END

        self.setWindowTitle("Steganografia")
        
        # Text Fields START
        titleText = QLabel()
        titleText.setText("Steganografia")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Impact',24))

        authorText = QLabel()
        authorText.setText("Sebastian Skrobich 140779")
        authorText.setAlignment(Qt.AlignCenter)
        authorText.setFont(QFont('Impact',16))
        authorText.setStyleSheet("QLabel {color : grey}")

        self.textFileTextField = QLineEdit()
        self.textFileTextField.setReadOnly(True)

        self.bitmapFileTextField = QLineEdit()
        self.bitmapFileTextField.setReadOnly(True)

        self.outputFileTextField = QLineEdit()
        self.outputFileTextField.setReadOnly(True)
        # Text Fields END


        # Buttons START
        encryptButton = QPushButton()
        encryptButton.setText("WRITE")
        encryptButton.clicked.connect(self.encryptClicked)

        decryptButton = QPushButton()
        decryptButton.setText("READ")
        decryptButton.clicked.connect(self.decryptClicked)

        textFileButton = QPushButton()
        textFileButton.setText("CHOOSE TEXT FILE")
        textFileButton.clicked.connect(lambda: self.selectClicked(0))

        bitmapFileButton = QPushButton()
        bitmapFileButton.setText("CHOOSE BITMAP FILE")
        bitmapFileButton.clicked.connect(lambda: self.selectClicked(1))

        outputFileButton = QPushButton()
        outputFileButton.setText("CHOOSE OUTPUT FILE")
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

        # Text File Select Box
        setTextFileL = QHBoxLayout()
        setTextFileL.addWidget(self.textFileTextField)
        setTextFileL.addWidget(textFileButton)
        setTextFileLW = QWidget()
        setTextFileLW.setLayout(setTextFileL)

        # Key File Select Box
        setKeyFileL = QHBoxLayout()
        setKeyFileL.addWidget(self.bitmapFileTextField)
        setKeyFileL.addWidget(bitmapFileButton)
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

        mainMenu.addWidget(infoLW)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)


    def encryptClicked(self):
        if (self.textFilePath is None or self.bitmapFilePath is None or self.outputFilePath is None):
            self.errorMessageBox("Some paths are empty.")
        else:
            if os.stat(self.textFilePath).st_size*8 > os.stat(self.bitmapFilePath).st_size:
                self.errorMessageBox("Text file is too long for chosen bitmap")
            else:
                steganografia.writeToBitmap(self.bitmapFilePath, self.textFilePath, self.outputFilePath)
    
    def decryptClicked(self):
        if (self.bitmapFilePath is None or self.outputFilePath is None):
            self.errorMessageBox("Some paths are empty.")
        else:
            steganografia.readFromBitmap(self.bitmapFilePath, self.outputFilePath)
    
    def selectClicked(self, typeInt):
        filePath = filedialog.askopenfilename()
        if typeInt == 0:
            self.textFilePath = filePath
            self.textFileTextField.setText(filePath)
        elif typeInt == 1:
            self.bitmapFilePath = filePath
            self.bitmapFileTextField.setText(filePath)
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