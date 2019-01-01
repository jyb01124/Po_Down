import sys, os, time, threading, subprocess
import search_address as sa_m 
import search_video_page as svp_m

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("po_down.ui")[0]

class Main_class(QMainWindow, form_class):

    svp = svp_m.search_video_page()
    sa = sa_m.search_address()
    page = 1
    vkey = []
    quality = 0

    def __init__(self):
        super(Main_class, self).__init__()
        self.setupUi(self)

        self.path_btn.clicked.connect(self.set_path)
        self.page_spin.valueChanged.connect(self.spin_changed)
        self.Search_btn.clicked.connect(self.search_clicked)
        self.rb_720.clicked.connect(self.set_radio_btn)
        self.rb_480.clicked.connect(self.set_radio_btn)
        self.rb_240.clicked.connect(self.set_radio_btn)
        
    def set_radio_btn(self):
        if self.rb_720.isChecked():
            self.quality = 720
        elif self.rb_480.isChecked():
            self.quality = 480
        else:
            self.quality = 240


    def set_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'Select directory') 
        self.path.setText(dir_path)
    
    def search_clicked(self):
        self.Search_result.clear()
        t = threading.Thread(target=self.thread_title_list)
        t.start()

    def thread_title_list(self):
        search_sentence = self.Search_bar.text()
        error = 0
        print(search_sentence)
        print(self.page)
        for i in range(1, self.page+1):
            try:
                self.vkey.append(self.svp.search(search_sentence,i))
            except:
                self.SB.showMessage("검색실패 : 다시 검색버튼을 눌려주세요.")
                error = 1
            for j in range(0,20):
                try:
                    self.Search_result.addItem(list(self.vkey[i].values())[j])
                except:
                    self.SB.showMessage("검색실패 : 다시 검색버튼을 눌려주세요.")
                    error = 1
        if error == 0:
            self.SB.showMessage("검색완료 : 다운로드 시작 버튼을 눌려주세요.")

    def spin_changed(self):
        self.page = self.page_spin.value()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MC = Main_class()
    MC.show()
    app.exec_()

#self.statusBar.showMessage(self.lineEdit.text())