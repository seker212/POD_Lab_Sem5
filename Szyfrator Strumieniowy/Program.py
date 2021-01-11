from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import tkinter
from tkinter import filedialog
import sys
from unidecode import unidecode
import pathlib
import os

root = tkinter.Tk()
root.withdraw()
ENCODING = 'utf-8'

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Okno, self).__init__(*args,*kwargs)
        # Class Variables START
        self.textFilePath = None
        self.keyFilePath = None
        self.outputFilePath = None
        # Class Variables END

        self.setWindowTitle("Szyfrator Strumieniowy XOR")
        
        # Text Fields START
        titleText = QLabel()
        titleText.setText("Szyfrator Strumieniowy XOR")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Impact',24))

        authorText = QLabel()
        authorText.setText("Sebastian Skrobich 140779")
        authorText.setAlignment(Qt.AlignCenter)
        authorText.setFont(QFont('Impact',16))
        authorText.setStyleSheet("QLabel {color : grey}")

        self.textFileTextField = QLineEdit()
        self.textFileTextField.setReadOnly(True)

        self.keyFileTextField = QLineEdit()
        self.keyFileTextField.setReadOnly(True)

        self.outputFileTextField = QLineEdit()
        self.outputFileTextField.setReadOnly(True)
        # Text Fields END


        # Buttons START
        encryptButton = QPushButton()
        encryptButton.setText("ENCRYPT/DECRYPT")
        encryptButton.clicked.connect(self.encryptClicked)

        textFileButton = QPushButton()
        textFileButton.setText("CHOOSE TEXT FILE")
        textFileButton.clicked.connect(lambda: self.selectClicked(0))

        keyFileButton = QPushButton()
        keyFileButton.setText("CHOOSE KEY FILE")
        keyFileButton.clicked.connect(lambda: self.selectClicked(1))

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
        
        # Encrypt/Decrypt Button Box
        encryptButtonsL = QHBoxLayout()
        encryptButtonsL.addWidget(encryptButton)
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
        setKeyFileL.addWidget(self.keyFileTextField)
        setKeyFileL.addWidget(keyFileButton)
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
        if (self.textFilePath is None or self.keyFilePath is None or self.outputFilePath is None):
            self.errorMessageBox("Some paths are empty.")
        else:
            if os.stat(self.textFilePath).st_size*8 <= os.stat(self.keyFilePath).st_size:
                self.errorMessageBox("Key file is too short")
            else:
                textFile = open(self.textFilePath,'rb')
                keyFile = open(self.keyFilePath,'r',encoding="utf-8")
                outputByteArray = []
                xorValue = 0
                while True:
                    character = textFile.read(1)
                    xorValue = 0
                    if not character:
                        break
                    for i in range(8):
                        xorValue += (2**(7-i)) * int(keyFile.read(1))
                    outputByteArray.append(int.from_bytes(character, byteorder='big', signed=False) ^ xorValue)
                with open(self.outputFilePath,'wb') as outputFile:
                    outputFile.write(bytes(outputByteArray))
                textFile.close()
                keyFile.close()

    
    def selectClicked(self, typeInt):
        filePath = filedialog.askopenfilename()
        if typeInt == 0:
            self.textFilePath = filePath
            self.textFileTextField.setText(filePath)
        elif typeInt == 1:
            self.keyFilePath = filePath
            self.keyFileTextField.setText(filePath)
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