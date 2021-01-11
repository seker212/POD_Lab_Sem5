from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import tkinter
from tkinter import filedialog
import sys
import decryption
import encryption
from unidecode import unidecode
import pathlib

root = tkinter.Tk()
root.withdraw()
ENCODING = 'utf-8'

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Okno, self).__init__(*args,*kwargs)
        # Class Variables START
        self.encryptor = encryption.Encryption()
        self.decryptor = decryption.Decryption()
        self.filePath = None
        # Class Variables END

        self.setWindowTitle("POD Lab 3")
        
        # Text Fields START
        titleText = QLabel()
        titleText.setText("Szyfr podstawieniowy prosty\r\nz wybranym kluczem")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Impact',24))

        authorText = QLabel()
        authorText.setText("Sebastian Skrobich 140779")
        authorText.setAlignment(Qt.AlignCenter)
        authorText.setFont(QFont('Impact',16))
        authorText.setStyleSheet("QLabel {color : grey}")

        inputTitle = QLabel()
        inputTitle.setText("Input:")

        outputTitle = QLabel()
        outputTitle.setText("Output:")

        self.inputField = QPlainTextEdit()
        self.inputField.setPlaceholderText("Set input here...")

        self.outputField = QPlainTextEdit()
        self.outputField.setReadOnly(True)
        self.outputField.setPlaceholderText("Output")

        self.keyField = QLineEdit()
        self.keyField.setPlaceholderText("Set key here...")

        self.fileTextField = QLineEdit()
        self.fileTextField.setReadOnly(True)
        # Text Fields END


        # Buttons START
        encryptButton = QPushButton()
        encryptButton.setText("ENCRYPT")
        encryptButton.clicked.connect(self.encryptClicked)

        decryptButton = QPushButton()
        decryptButton.setText("DECRYPT")
        decryptButton.clicked.connect(self.decryptClicked)

        generateButton = QPushButton()
        generateButton.setText("GENERATE")
        generateButton.clicked.connect(self.generateClicked)

        importKeyButton = QPushButton()
        importKeyButton.setText("IMPORT KEY")
        importKeyButton.clicked.connect(self.importKeyClicked)

        exportKeyButton = QPushButton()
        exportKeyButton.setText("EXPORT KEY")
        exportKeyButton.clicked.connect(self.exportKeyClicked)

        importInputButton = QPushButton()
        importInputButton.setText("IMPORT INPUT FROM FILE")
        importInputButton.clicked.connect(self.importInputClicked)

        exportOutputButton = QPushButton()
        exportOutputButton.setText("EXPORT OUTPUT TO FILE")
        exportOutputButton.clicked.connect(self.exportOutputClicked)

        swapButton = QPushButton()
        swapButton.setText("OUTPUT -> INPUT")
        swapButton.clicked.connect(self.swapClicked)

        fileButton = QPushButton()
        fileButton.setText("CHOOSE FILE")
        fileButton.clicked.connect(self.selectClicked)

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

        # Input Box
        inputTextL = QVBoxLayout()
        inputTextL.addWidget(inputTitle)
        inputTextL.addWidget(self.inputField)

        inputButtonL = QVBoxLayout()
        inputButtonL.addWidget(importInputButton)

        inputL = QHBoxLayout()
        inputL.addLayout(inputTextL)
        inputL.addLayout(inputButtonL)

        inputLW = QWidget()
        inputLW.setLayout(inputL)

        # Output Box
        outputTextL = QVBoxLayout()
        outputTextL.addWidget(outputTitle)
        outputTextL.addWidget(self.outputField)

        outputButtonL = QVBoxLayout()
        outputButtonL.addWidget(exportOutputButton)
        outputButtonL.addWidget(swapButton)

        outputL = QHBoxLayout()
        outputL.addLayout(outputTextL)
        outputL.addLayout(outputButtonL)

        outputLW = QWidget()
        outputLW.setLayout(outputL)

        # Key Box
        keyInputL = QHBoxLayout()
        keyInputL.addWidget(self.keyField)
        keyInputL.addWidget(generateButton)

        keyImportExportL = QHBoxLayout()
        keyImportExportL.addWidget(importKeyButton)
        keyImportExportL.addWidget(exportKeyButton)

        keyL = QVBoxLayout()
        keyL.addLayout(keyInputL)
        keyL.addLayout(keyImportExportL)

        keyLW = QWidget()
        keyLW.setLayout(keyL)
        
        # Encrypt/Decrypt Buttons Box
        encryptDecryptButtonsL = QHBoxLayout()
        encryptDecryptButtonsL.addWidget(encryptButton)
        encryptDecryptButtonsL.addWidget(decryptButton)
        encryptDecryptButtonsLW = QWidget()
        encryptDecryptButtonsLW.setLayout(encryptDecryptButtonsL)

        # File Select Box
        setFileL = QHBoxLayout()
        setFileL.addWidget(self.fileTextField)
        setFileL.addWidget(fileButton)
        setFileLW = QWidget()
        setFileLW.setLayout(setFileL)

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
        mainMenu.addWidget(setFileLW)
        mainMenu.addWidget(inputLW)
        mainMenu.addWidget(outputLW)
        mainMenu.addWidget(keyLW)
        mainMenu.addWidget(encryptDecryptButtonsLW)
        mainMenu.addWidget(infoLW)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)


    def encryptClicked(self):
        try:
            self.encryptor.setKey(self.keyField.text())
        except ValueError as e:
            self.errorMessageBox(str(e))
        result = self.encryptor.encrypt(self.inputField.toPlainText())
        self.outputField.setPlainText(result)
    
    def decryptClicked(self):
        try:
            self.decryptor.setKey(self.keyField.text())
        except ValueError as e:
            self.errorMessageBox(str(e))
        result = self.decryptor.decrypt(self.inputField.toPlainText())
        self.outputField.setPlainText(result)
    
    def selectClicked(self):
        self.filePath = filedialog.askopenfilename()
        self.fileTextField.setText(self.filePath)

    def generateClicked(self):
        self.keyField.setText(self.encryptor.generateKey())
    
    def importInputClicked(self):
        try:
            with open(self.filePath, 'rb') as importFile:
                self.inputField.setPlainText(importFile.read().decode(ENCODING, 'ignore'))
        except TypeError:
            self.errorMessageBox("No file defined")

    def exportOutputClicked(self):
        try:
            with open(self.filePath, 'wb') as exportFile:
                exportFile.write(self.outputField.toPlainText().encode(ENCODING, 'ignore'))
        except TypeError:
            self.errorMessageBox("No file defined")

    def importKeyClicked(self):
        try:
            with open(self.filePath, 'rb') as importFile:
                self.keyField.setText(importFile.read().decode(ENCODING, 'ignore'))
        except TypeError:
            self.errorMessageBox("No file defined")

    def exportKeyClicked(self):
        try:
            with open(self.filePath, 'wb') as exportFile:
                exportFile.write(self.keyField.text().encode(ENCODING, 'ignore'))
        except TypeError:
            self.errorMessageBox("No file defined")

    def swapClicked(self):
        self.inputField.setPlainText(self.outputField.toPlainText())
        self.outputField.clear()
    
    def infoClicked(self):
        # print(pathlib.Path(__file__).parent.absolute()) #FIXME: Check if file exist
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
window.setFixedSize(800,600)
window.setStyleSheet("background-color: rgb(245,245,220)")
window.show()

app.exec_()