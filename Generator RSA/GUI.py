from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import tkinter
import threading
from tkinter import filedialog
import generator
import sys
from unidecode import unidecode
import pathlib

root = tkinter.Tk()
root.withdraw()
ENCODING = 'utf-8'

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Okno, self).__init__(*args,*kwargs)
        # Class Variables START
        self.filePath = None
        self.lock = False
        self.progressPrecent = [0]
        # Class Variables END

        self.setWindowTitle("POD Generator RSA")

        #Progress Bar
        # self.progressBar = QProgressBar()
        
        # Text Fields START
        titleText = QLabel()
        titleText.setText("Generator RSA")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Impact',24))

        authorText = QLabel()
        authorText.setText("Sebastian Skrobich 140779")
        authorText.setAlignment(Qt.AlignCenter)
        authorText.setFont(QFont('Impact',16))
        authorText.setStyleSheet("QLabel {color : grey}")

        self.progress = QLabel()
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setFont(QFont('Consolas',16))

        key_e_label = QLabel()
        key_e_label.setText("e:")

        key_n_label = QLabel()
        key_n_label.setText("n:")

        key_x0_label = QLabel()
        key_x0_label.setText("x_0:")

        self.key_e = QLineEdit()
        self.key_e.setPlaceholderText("e")

        self.key_n = QLineEdit()
        self.key_n.setPlaceholderText("n")

        self.key_x0 = QLineEdit()
        self.key_x0.setPlaceholderText("x_0")

        self.bits_number = QLineEdit()
        self.bits_number.setPlaceholderText("How many bits to generate")

        self.fileTextField = QLineEdit()
        self.fileTextField.setReadOnly(True)
        # Text Fields END

        # Check boxes START
        self.loop_lock_box = QCheckBox()
        self.loop_lock_box.setText('Lock Looping')

        self.reqiure_prime_box = QCheckBox()
        self.reqiure_prime_box.setText('Require Primal Numbers')
        self.reqiure_prime_box.setChecked(True)
        # Check boxes END

        # Buttons START
        generateButton = QPushButton()
        generateButton.setText("GENERATE")
        generateButton.clicked.connect(self.generateClicked)

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

        #Key Values Box
        #e
        key_eL = QVBoxLayout()
        key_eL.addWidget(key_e_label)
        key_eL.addWidget(self.key_e)
        #n
        key_nL = QVBoxLayout()
        key_nL.addWidget(key_n_label)
        key_nL.addWidget(self.key_n)
        #x0
        key_x0L = QVBoxLayout()
        key_x0L.addWidget(key_x0_label)
        key_x0L.addWidget(self.key_x0)
        #main box
        keysL = QHBoxLayout()
        keysL.addLayout(key_eL)
        keysL.addLayout(key_nL)
        keysL.addLayout(key_x0L)
        keysLW = QWidget()
        keysLW.setLayout(keysL)

        # Number to generate and generate button Box
        generateL = QHBoxLayout()
        generateL.addWidget(self.bits_number)
        generateL.addWidget(generateButton)
        generateLW = QWidget()
        generateLW.setLayout(generateL)

        #Check boxes Box
        checkboxesL = QHBoxLayout()
        checkboxesL.addWidget(self.loop_lock_box)
        checkboxesL.addWidget(self.reqiure_prime_box)
        checkboxesLW = QWidget()
        checkboxesLW.setLayout(checkboxesL)

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

        # Progress Box
        progressL = QHBoxLayout()
        # progressL.addWidget(self.progressBar)
        progressL.addWidget(self.progress)
        progressLW = QWidget()
        progressLW.setLayout(progressL)

        # Parts Layout END


        #Main Layout
        mainMenu = QVBoxLayout()
        mainMenu.setAlignment(Qt.AlignCenter)
        mainMenu.addWidget(titleLW)
        mainMenu.addWidget(setFileLW)
        mainMenu.addWidget(keysLW)
        mainMenu.addWidget(checkboxesLW)
        mainMenu.addWidget(generateLW)
        mainMenu.addWidget(progressLW)
        mainMenu.addWidget(infoLW)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        # self.progressBar.setValue(int(self.progressPrecent[0]))
        self.setCentralWidget(mainMenuW)


    
    def selectClicked(self):
        if not self.lock:
            self.filePath = filedialog.askopenfilename()
            self.fileTextField.setText(self.filePath)

    def generateClicked(self):
        if not self.lock:
            if self.filePath is not None:
                e = int(self.key_e.text())
                n = int(self.key_n.text())
                x0 = int(self.key_x0.text())
                bit_num = int(self.bits_number.text())
                if e < 2 or n < 2 or x0 < 2 or bit_num < 1:
                    self.errorMessageBox('Numbers Error. Make sure the numbers are 2 or more')
                else:
                    if self.reqiure_prime_box.isChecked():
                        if generator.isPrime(e) and generator.isPrime(n) and generator.isPrime(x0):
                            self.thread = threading.Thread(target=self.safeGeneration, args = (e,n,x0,bit_num,self.filePath, self.loop_lock_box.isChecked(), self.progressPrecent), daemon = True)
                            progressThread = threading.Thread(target=self.setProgress, daemon = True)
                            self.thread.start()
                            progressThread.start()
                        else:
                            self.errorMessageBox('Given numbers are not prime')
                    else:
                        self.thread = threading.Thread(target=self.safeGeneration, args = (e,n,x0,bit_num,self.filePath, self.loop_lock_box.isChecked(), self.progressPrecent), daemon = True)
                        progressThread = threading.Thread(target=self.setProgress, daemon = True)
                        self.thread.start()
                        progressThread.start()
            else:
                self.errorMessageBox('Please choose text file')

    
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
    
    def lockInput(self, test : bool):
        self.key_e.setReadOnly(test)
        self.key_n.setReadOnly(test)
        self.key_x0.setReadOnly(test)
        self.bits_number.setReadOnly(test)
        self.lock = test
    
    def safeGeneration(self, e, n, x0, number_to_generate, filename, loop_lock, progress):
        self.lockInput(True)
        generator.generate(e, n, x0, number_to_generate, filename, loop_lock, progress)
        self.lockInput(False)
    
    def setProgress(self):
        while self.thread.is_alive():
            self.progress.setText("{:.2f}%".format(self.progressPrecent[0]))


#MAIN
app = QApplication(sys.argv)
window = Okno()
window.setFixedSize(800,600)
window.setStyleSheet("background-color: rgb(245,245,220)")
window.show()

app.exec_()