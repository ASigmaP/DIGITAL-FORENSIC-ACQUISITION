from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
import sys
import hashlib
import subprocess
import logging
import time
import datetime
import os


class Akusisi(QtCore.QThread):
    countChanged = pyqtSignal(int)
    selesai = pyqtSignal(int)
    
    def run(self):

        #direktori penyimpanan
        c = mainWindow_2.c
        #source cloning
        source = mainWindow_2.source

        val = 0
        #proses cloning
        with open(source,'rb') as f:
            with open(c, "wb") as i:
                 while True:
                       val += 1
                       self.countChanged.emit(val)
                       if i.write(f.read(512)) == 0:
                           print("Acquisition Finished")
                           break


        # else:
        #     with open(source,'rb') as f:
        #        with open(c, "wb") as i:
        #             while True:
        #                 val += 1
                        # tar = tarfile.open(self, mode="w:gz")
                        # progress = tqdm(exs)
                        # for exs in progress:
                        #     tar.add(exs)
                        #     progress.set_description("f.compressing{exs}")

                        # self.countChanged.zip(val)
                        # if i.write(f.read(512)) == 0:
                        # #     print("Acquisition Finished")
                        # # if i.write(f.zip.ZIP_DEFLATED) ==0:
                        #     print("Acquisition Finished")
                        #     # zout = zipfile.ZipFile(zfilename, "w", zipfile.ZIP_fikDEFLATED)
                        # while True:
                        #     val += 1
                        #     self.countChanged.emit(val)
                        #     if i.write(f.read(512)) == 0:
                        #         print("Acquisition Finished")
                        #         break
                        #

        # proses aff

        self.play = Checksum()
        self.play.finished.connect(self.acquisitionFinished)
        self.play.start()

    def acquisitionFinished(self):
        nil = 1
        self.selesai.emit(nil)
            
        
            
class Checksum2(QThread):
    
    def run(self):
        nilai = 1
        self.kirimNilai.emit(nilai)
        print("DONE")
        
        


class Checksum(QThread):
    
    def run(self):
        
        #membuat file logging
        sumberNama = mainWindow_2.sumberNama
        dir = mainWindow_2.dir
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(filemode='w',filename=dir,level=logging.INFO,
                            format='%(levelname)s:%(message)s')
        
        #source cloning /dev/...
        source = mainWindow_2.source
        #direktori penyimpanan
        c = mainWindow_2.c
        #note
        note = mainWindow_2.note
        #examiner
        penguji = mainWindow_2.examiner
        #waktu mulai akusisi
        waktuMulai = mainWindow_2.waktuMulai
        
        #file loging source
        namaUSB = mainWindow_2.labelUSB
        storage = mainWindow_2.size
        id = mainWindow_2.uuidUSB
        sektor = mainWindow_2.sector
        
        #file logging
        logging.info("Source\t:{}".format(source))
        logging.info("Label\t:{}".format(namaUSB))
        logging.info("Size\t:{}".format(storage))
        logging.info("Sector\t:{}".format(sektor))
        logging.info("UUID\t:{}".format(id))
        logging.info("File name\t:{}".format(sumberNama))
        logging.info("Directory\t:{}".format(c))
        logging.info("Note\t:{}".format(note))
        logging.info("Examiner\t:{}".format(penguji))
        
        #event log append
##      lineLog = mainWindow_2.lineLogGlobal

        block_size = 2**16
         
        #Hash sumber cloning
        md5a = hashlib.md5()
        sha512a = hashlib.sha512()
        with open(source,'rb') as fileSource:
            while True:
                readSource = fileSource.read(block_size)
                if not readSource:
                    break
                md5a.update(readSource)
                sha512a.update(readSource)
        hasilSource = md5a.hexdigest()
        hasilSourceSHA512 = sha512a.hexdigest()

        #Hash hasil cloning
        md5b = hashlib.md5()
        sha512b = hashlib.sha512()
        with open(c,'rb') as fileCloning:
            while True:
                readCloning = fileCloning.read(block_size)
                if not readCloning:
                    break
                md5b.update(readCloning)
                sha512b.update(readCloning)
        hasilCloning = md5b.hexdigest()
        hasilCloningSHA512 = sha512b.hexdigest()
        
        #waktu selesai akusisi
        waktuSelesai = datetime.datetime.today().strftime("%d %B %Y, %H:%M")
        mulai = "Acquisition start\t: "+waktuMulai
        selesai = "Acquisition finished\t: "+waktuSelesai

        
        #file logging 
        logging.info("Acqusition start\t:{}".format(waktuMulai))
        logging.info("Acqusition finished:{}".format(waktuSelesai))
        logging.info("Source MD5 Hash\t:{}".format(hasilSource))
        logging.info("Cloning MD5 Hash\t:{}".format(hasilCloning))
        logging.info("Source SHA512 Hash\t:{}".format(hasilSourceSHA512))
        logging.info("Cloning SHA512 Hash:{}".format(hasilCloningSHA512))
        
        if hasilSource == hasilCloning:
            logging.info("Verified\t\t:MD5 Hash Matched")
        else:
            logging.info("Verified\t:MD5 Hash not Matched")

                                
class mainWindow_2(QMainWindow):

    def __init__(self):
        super().__init__()
        self.window1 = None
        self.directBack = False
        self.interface()

    def interface(self):
        #pengaturan window
        self.setWindowTitle("DIGITAL FORENSIC ACQUISITION ")
        #self.resize(880, 630)
        self.resize(480, 250)
        self.setWindowIcon(QtGui.QIcon("/home/debian/Documents/DIGITAL FORENSIC ACQUISITION/imgakuisisi.png"))

        #pengaturan menu bar
        # menuFile = self.menuBar().addMenu("File")
        # actionExit = menuFile.addAction("Exit")
        # actionExit.triggered.connect(self.menuExit)


        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)


        self.lblDirektori = QLabel("Image Directory: ", self)
        #self.lblDirektori.setGeometry(QtCore.QRect(80, 75, 135, 21))
        self.lblDirektori.setGeometry(QtCore.QRect(3, 30, 130, 21))
        self.lblDirektori.setFont(font)
        self.lblDirektori.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblCase = QLabel("File Name: ", self)
        #self.lblCase.setGeometry(QtCore.QRect(80, 110, 135, 21))
        self.lblCase.setGeometry(QtCore.QRect(3, 57, 130, 21))
        self.lblCase.setFont(font)
        self.lblCase.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblNote = QLabel("Notes: ", self)
        #self.lblNote.setGeometry(QtCore.QRect(80, 145, 135, 21))
        self.lblNote.setGeometry(QtCore.QRect(3, 85, 130, 21))
        self.lblNote.setFont(font)
        self.lblNote.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblExaminer = QLabel("Examiner: ", self)
        #self.lblExaminer.setGeometry(QtCore.QRect(80,250, 135, 21))
        self.lblExaminer.setGeometry(QtCore.QRect(3,132, 130, 21))
        self.lblExaminer.setFont(font)
        self.lblExaminer.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblImage = QLabel("Image Type: ", self)
        #self.lblImage.setGeometry(QtCore.QRect(80, 285, 135, 21))
        self.lblImage.setGeometry(QtCore.QRect(3, 158, 130, 21))
        self.lblImage.setFont(font)
        self.lblImage.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        
        self.lineDirektori = QLineEdit(self)
        #self.lineDirektori.setGeometry(QtCore.QRect(220, 75, 301, 25))
        self.lineDirektori.setGeometry(QtCore.QRect(138, 30, 230, 22))
        self.lineCase = QLineEdit(self)
        #self.lineCase.setGeometry(QtCore.QRect(220, 110, 301, 25))
        self.lineCase.setGeometry(QtCore.QRect(138, 57, 230, 22))
        self.lineNote = QPlainTextEdit(self)
        #self.lineNote.setGeometry(QtCore.QRect(220, 145, 301, 95))
        self.lineNote.setGeometry(QtCore.QRect(138, 85, 230, 40))
        self.lineExaminer = QLineEdit(self)
        #self.lineExaminer.setGeometry(QtCore.QRect(220, 250, 301, 25))
        self.lineExaminer.setGeometry(QtCore.QRect(138, 132, 230, 22))
        self.radioDD = QRadioButton(".dd", self)
        #self.radioDD.setGeometry(QtCore.QRect(220, 285, 95, 20))
        self.radioDD.setGeometry(QtCore.QRect(138, 160, 90, 17))
        #self.radioDD.toggled.connect(self.fungsiDD)
        # self.radioAFF = QRadioButton(".aff", self)
        # #self.radioAFF.setGeometry(QtCore.QRect(280, 285, 95, 20))
        # self.radioAFF.setGeometry(QtCore.QRect(198, 160, 90, 17))
        #self.radioAFF.toggled.connect(self.fungsiAFF)
        # self.radioAFF.setDisabled(True)
        
        self.progresAcqusition = QLabel("Acquisition Progress ", self)
        #self.progresAcqusition.setGeometry(QtCore.QRect(70, 350, 170, 21))
        self.progresAcqusition.setGeometry(QtCore.QRect(0, 188, 130, 21))
        self.progresAcqusition.setFont(font)
        self.progresAcqusition.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.progresAcqusition = QProgressBar(self)
        #self.progresAcqusition.setGeometry(QtCore.QRect(250, 350, 500, 25))
        self.progresAcqusition.setGeometry(QtCore.QRect(135, 188, 323, 22))

        #pengaturan button
        self.btnDir = QPushButton(self)
        #self.btnDir.setGeometry(QtCore.QRect(530, 75, 31, 25))
        self.btnDir.setGeometry(QtCore.QRect(373, 30, 30, 23))
        self.btnDir.setIcon(QtGui.QIcon("/home/debian/Documents/DIGITAL FORENSIC ACQUISITION/folder.jpg"))
        self.btnDir.clicked.connect(self.pathDirektori)

        self.btnStart = QPushButton("Start", self)
        self.btnStart.setFont(font)
        #self.btnStart.setGeometry(QtCore.QRect(745, 583, 93, 35))
        self.btnStart.setGeometry(QtCore.QRect(382, 218, 75, 25))
        iconStart = QtGui.QIcon()
        iconStart.addPixmap(QtGui.QPixmap("/home/debian/Documents/DIGITAL FORENSIC ACQUISITION/start"),
                            QtGui.QIcon.Normal)
        self.btnStart.setIcon(iconStart)
        self.btnStart.clicked.connect(self.tombolStart)

        self.btnBack = QPushButton("Back", self)
        self.btnBack.setFont(font)
        #self.btnBack.setGeometry(QtCore.QRect(645, 583, 93, 35))
        self.btnBack.setGeometry(QtCore.QRect(300, 218, 75, 25))
        iconBack = QtGui.QIcon()
        iconBack.addPixmap(QtGui.QPixmap("/home/debian/Documents/DIGITAL FORENSIC ACQUISITION/back"),
                           QtGui.QIcon.Normal)
        self.btnBack.setIcon(iconBack)
        self.btnBack.clicked.connect(self.tombolBack)

        self.show()

    def menuExit(self):
        reply = QMessageBox.question(self, "Caution",
                                     "Are you sure want to exit?", QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            QApplication.quit()
        else:
            pass

    def pathDirektori(self):
        self.folderDir = QFileDialog.getExistingDirectory(self, "Select folder")
        #self.folderDir = QFileDialog.getSaveFileName(self, "save File")
        self.lineDirektori.setText(self.folderDir)
        
    def fungsiDD(self):
        if self.radioDD.isChecked() == True:
            a = self.lineCase.text()
            self.b = a+".dd"
            
    # def fungsiAFF(self):
    #     if self.radioAFF.isChecked() == True:
    #         a = self.lineCase.text()
    #         self.b = a+".aff"
    #
    def tombolBack(self):
        self.directBack = True
        self.window1.show()
        self.destroy()
        self.close()
        
    def closeEvent(self, eventQCloseEvent):
        if self.directBack == True:
            eventQCloseEvent.accept()
        else:
            reply = QMessageBox.question(self, "Caution",
                                         "All running processes will be canceled \nAre you sure want to exit?", QMessageBox.Yes | QMessageBox.No)

            if reply == QMessageBox.Yes:
                eventQCloseEvent.accept()
            else:
                eventQCloseEvent.ignore()
        
            
    def tombolStart(self):
        try:
            dirField = self.lineDirektori.text()
            filenameField = self.lineCase.text()
            cek = dirField + "/" + filenameField + ".dd"
            mainWindow_2.note = self.lineNote.toPlainText()
            mainWindow_2.examiner = self.lineExaminer.text()

            if os.path.exists(cek):
                reply = QMessageBox.warning(self, "Warning", "File Exist!")
            elif dirField == "" or filenameField == "" or  mainWindow_2.note == "" or mainWindow_2.examiner == "" or self.radioDD.isChecked() == False:
                reply = QMessageBox.warning(self, "Warning", "Complete the field!")

            else:
                
                try:
                    if self.radioDD.isChecked() == True:
                        dd = self.lineCase.text()+".dd"
                        check = self.folderDir+"/"+dd
            
                    #waktu mulai akusisi
                    mainWindow_2.waktuMulai = datetime.datetime.today().strftime("%d %B %Y, %H:%M")
                        
                    #membuat file logging
                    mainWindow_2.sumberNama = self.lineCase.text()
                    mainWindow_2.name = mainWindow_2.sumberNama+".log"
                    mainWindow_2.sumberDir = self.folderDir
                    mainWindow_2.dir = mainWindow_2.sumberDir+"/"+mainWindow_2.name
                    #logging.basicConfig(filename=dir,level=logging.INFO,
                                        #format='%(levelname)s:%(message)s')
                    
                    #direktori penyimpanan
##                  mainWindow_2.a = self.folderDir
##                  mainWindow_2.b = "/"+self.b
                    mainWindow_2.c = check
                    
                    #examiner
                    mainWindow_2.examiner = self.lineExaminer.text()   
                    #mengambil value note
                    mainWindow_2.note = self.lineNote.toPlainText()
                    #source cloning /dev/...
                    mainWindow_2.source = "/dev/"+mainWindow_2.hasil
                
                    #untuk event log
                    asal = "Source\t: "+mainWindow_2.source
                    ukuran = "Size\t: "+mainWindow_2.size
                    namaLog = "File name\t: "+mainWindow_2.sumberNama
                    dirLog = "Directory\t: "+mainWindow_2.c
                    noteLog = "Note\t: "+mainWindow_2.note
                    
                    #event log source
                    usbInfo1 = subprocess.getoutput("sudo blkid -s LABEL | grep "+ mainWindow_2.source)
                    time.sleep(1)
                    usbInfo2 = subprocess.getoutput("sudo blkid -s UUID | grep "+ mainWindow_2.source)
                    time.sleep(1)
                    usbInfo3 = subprocess.getoutput("sudo fdisk -l | grep "+ mainWindow_2.source +"| grep bytes")

                    mainWindow_2.labelUSB = usbInfo1[18:-1]
                    labelUSBx = "Label\t: "+mainWindow_2.labelUSB
                    mainWindow_2.uuidUSB = usbInfo2[17:-1]
                    uuidUSBx = "UUID\t: "+mainWindow_2.uuidUSB
                    mainWindow_2.sector = usbInfo3.split()[6]
                    sectorx = "Sector\t: "+mainWindow_2.sector
                    pembatas = "||---------------->>"


                    jumlahSek = int(mainWindow_2.sector)
                    self.progresAcqusition.setMaximum(jumlahSek)
                    
                    self.calc = Akusisi()
                    self.calc.countChanged.connect(self.onCountChanged)
                    self.calc.selesai.connect(self.akusisiSelesai)
                    self.calc.start() 
                    

            
                
                except Exception as e:
                    reply = QMessageBox.warning(self, "Warning", "Error occoured")
                    print("e")
                    print(e)
        except Exception as e:
            reply = QMessageBox.warning(self, "Warning", "Error occoured")
            print(e)
                    
                
    def onCountChanged(self, val):
        self.progresAcqusition.setValue(val)

    def akusisiSelesai(self, nil):
        a = nil
        if a == 1:
            reply = QMessageBox.about(self, "Message","Acquisition Finished")
            

if __name__ == '__main__':
    aplikasi = QApplication(sys.argv)
    ex = mainWindow_2()
    sys.exit(aplikasi.exec())
