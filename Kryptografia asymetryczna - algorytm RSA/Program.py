from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import tkinter
from tkinter import filedialog
import sys
from unidecode import unidecode
import pathlib
import rsa

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

        self.setWindowTitle("Kryptografia asymetryczna RSA")
        
        # Text Fields START
        titleText = QLabel()
        titleText.setText("Kryptografia asymetryczna RSA")
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

        
        self.qTextField = QLineEdit()
        self.qTextField.setPlaceholderText('q')

        self.pTextField = QLineEdit()
        self.pTextField.setPlaceholderText('p')
        # Text Fields END


        # Buttons START
        encryptButton = QPushButton()
        encryptButton.setText("ENCRYPT")
        encryptButton.clicked.connect(self.encryptClicked)

        decryptButton = QPushButton()
        decryptButton.setText("DECRYPT")
        decryptButton.clicked.connect(self.decryptClicked)

        textFileButton = QPushButton()
        textFileButton.setText("CHOOSE TEXT FILE")
        textFileButton.clicked.connect(lambda: self.selectClicked(0))

        keyFileButton = QPushButton()
        keyFileButton.setText("CHOOSE KEY FILE")
        keyFileButton.clicked.connect(lambda: self.selectClicked(1))

        outputFileButton = QPushButton()
        outputFileButton.setText("CHOOSE OUTPUT FILE")
        outputFileButton.clicked.connect(lambda: self.selectClicked(2))

        generateButton = QPushButton()
        generateButton.setText("GENERATE KEY")
        generateButton.clicked.connect(self.generateClicked)

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

        # Generate Box
        generateFieldsL = QHBoxLayout()
        generateFieldsL.addWidget(self.pTextField)
        generateFieldsL.addWidget(self.qTextField)
        generateL = QVBoxLayout()
        generateL.addLayout(generateFieldsL)
        generateL.addWidget(generateButton)
        generateLW = QWidget()
        generateLW.setLayout(generateL)
        
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
        mainMenu.addWidget(generateLW)

        mainMenu.addWidget(infoLW)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)


    def encryptClicked(self):
        if (self.textFilePath is None or self.keyFilePath is None or self.outputFilePath is None):
            self.errorMessageBox("Input Error: Some paths are empty.")
        else:
            try:
                rsa.encrypt(self.textFilePath, self.keyFilePath, self.outputFilePath)
            except ValueError as err:
                self.errorMessageBox('Validation Error: '+str(err.args))

    def decryptClicked(self):
        if (self.textFilePath is None or self.keyFilePath is None or self.outputFilePath is None):
            self.errorMessageBox("Input Error: Some paths are empty.")
        else:
            rsa.decrypt(self.textFilePath, self.keyFilePath, self.outputFilePath)

    def generateClicked(self):
        if (self.pTextField.text().isnumeric() and self.qTextField.text().isnumeric()):
            p = int(self.pTextField.text())
            q = int(self.qTextField.text())
            if (rsa.isPrime(p) and rsa.isPrime(q)):
                e, d, n = rsa.genKeys(p, q)
                rsa.saveKey(e,n,'key_pub.txt')
                rsa.saveKey(d,n,'key_prv.txt')
            else:
                self.errorMessageBox("Input Error: p and q must be a prime number")
        else:
            self.errorMessageBox("Input Error: p and q must consist only of digits..")
    
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