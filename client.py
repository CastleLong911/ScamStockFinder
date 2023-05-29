from os import name
import sys
from typing import DefaultDict
import finder
import priceRecorder
from threading import Thread
import progressManager as pm

from PyQt5.QtCore import QLine, Qt
from PyQt5.QtGui import QTextBlock, QTextLine
from PyQt5.QtWidgets import *

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(100,100,300,100)
        self.setWindowTitle("ScamStocksFinder")
        #첫번째 줄
        self.inputKeyLineEdit = QLineEdit(self)
        self.inputKeyLineEdit.setEchoMode(QLineEdit.Password)
        firstQLabel = QLabel("key : ")
        ##getRealtimePriceBtn = QPushButton("get",self)
        ##getRealtimePriceBtn.clicked.connect(self.getRealtimePriceBtnClicked)
        #두번째 줄
        secondQLabel = QLabel("search stocks with CB")
        searchCBBtn = QPushButton("search",self)
        searchCBBtn.clicked.connect(self.searchCBBtnClicked)

        #진행바
        self.pbar = QProgressBar()
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(100)
        
        
        #원산지
        nameLabel = QLabel("made by Jian")
        font = nameLabel.font()
        font.setPointSize(5)
        nameLabel.setFont(font)
        nameLabel.setAlignment(Qt.AlignRight)
        

        vLayout = QVBoxLayout()
        #group = QGroupBox()

        hLayout1 = QHBoxLayout()
        hLayout1.addWidget(firstQLabel)
        ##hLayout1.addWidget(getRealtimePriceBtn)
        hLayout1.addWidget(self.inputKeyLineEdit)

        hLayout2 = QHBoxLayout()
        hLayout2.addWidget(secondQLabel)
        hLayout2.addWidget(searchCBBtn)
        vLayout.addLayout(hLayout1)
        vLayout.addLayout(hLayout2)
        vLayout.addWidget(self.pbar)
        #vLayout.addWidget(group)
        vLayout.addWidget(nameLabel)

        self.setLayout(vLayout)

    def getPb(self,num):
        while(num<100):
            num = pm.progress.getProgressGage
            self.pbar.setValue(num)
        return

    def getRealtimePriceBtnClicked(self):
        self.pbar.setValue(0)
        
        
        def getProgress():
            num = 1
            while(num < 100):
                num = pm.progress.getProgressGage()

                self.pbar.setValue(num)
                print(num)
                
        def getRealtimePrice():
            priceRecorder.getRealtimePrice()

        t1 = Thread(target=getProgress,args=())   
        t1.start()

        t2 = Thread(target=getRealtimePrice,args=())
        t2.start() 


    def searchCBBtnClicked(self):
        def getCB():
            finder.pilgrim(self.inputKeyLineEdit.text())
        
        def getProgress():
            num = 0
            while(num < 100):
                num = pm.progress.getProgressGage()

                self.pbar.setValue(num)
                print(num)
        ##finder.pilgrim(self.inputKeyLineEdit.text())
        t1 = Thread(target=getProgress,args=())   
        t1.start()

        t2 = Thread(target=getCB,args=())
        t2.start() 
        ##getCB()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
