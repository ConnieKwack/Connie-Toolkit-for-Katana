from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QHBoxLayout,QVBoxLayout,QFileDialog
from PyQt5.QtGui import QPainter, QPen, QIcon
from PyQt5.QtCore import Qt
import os
from Katana import KatanaFile, NodegraphAPI

class ImportLight(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # get show name
        show_name = self.get_show_info()['dict_show_name']
        # get lgt list
        lgt_str = self.get_light_info()['dict_lgt_str']


        # set Labels,Buttons,Edits
        self.labelHeader = QLabel()
        self.labelHeader.setStyleSheet("border-image:url(D:/Katana/Inhouse/Icons/Import_light.png);")
        self.labelHeader.setMinimumHeight(60)

        self.labelShow = QLabel("Info")

        self.labelShowName = QLabel(show_name)
        self.labelShowName.setStyleSheet('font-weight: bold;'
                                         'font-size: 16pt; ')

        self.labelEnvList = QLabel(lgt_str)


        self.btnImport = QPushButton("Import Light")
        self.btnImport.clicked.connect(self.btnImport_pressed)



        # set hbox
        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.labelHeader)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(10)
        vbox0 = QVBoxLayout()
        vbox0.addWidget(self.labelShow)
        vbox0.addStretch()
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.labelShowName)
        vbox1.addWidget(self.labelEnvList)
        vbox1.addStretch()

        hbox1.addLayout(vbox0,25)
        hbox1.addStretch()
        hbox1.addLayout(vbox1,55)
        hbox1.addStretch(10)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(self.btnImport, 80)
        hbox2.addStretch(10)


        # set vbox
        vbox = QVBoxLayout()
        vbox.addLayout(hbox0)
        vbox.addStretch(10)
        vbox.addLayout(hbox1,65)
        vbox.addStretch(10)
        vbox.addLayout(hbox2)
        vbox.addStretch(15)

        # set layout
        self.setLayout(vbox)

        # set window
        self.setWindowTitle("Import Light")
        self.setWindowIcon(QIcon("D:/Katana/Inhouse/Icons/QIcon.png"))
        self.resize(370, 370)



    def get_show_info(self):
        # for get show name
        katana_name = NodegraphAPI.GetProjectDir()
        katana_name_list = katana_name.split('/')[0:4]
        show_dir = '/'.join(katana_name_list)
        show_name = katana_name_list[3]

        # for get sequence directory
        for_seq_list = katana_name.split('/')[0:6]
        seq_dir = '/'.join(for_seq_list)

        show_name_dict = {'dict_show_dir':show_dir,'dict_show_name':show_name,'dict_seq_dir':seq_dir}
        return show_name_dict

    def get_light_info(self):
        seq_dir = self.get_show_info()['dict_seq_dir']
        lgt_dir = seq_dir + '/Macros/lights'
        lgt_list = os.listdir(lgt_dir)

        # get only file name without file format
        lgt_name_list = []
        for i,v in enumerate(lgt_list):
            fileName = lgt_list[i].split('.')[0]
            lgt_name_list.append(fileName)

        lgt_str = ',\n'.join(lgt_name_list)
        lgt_info_dict = {'dict_lgt_dir':lgt_dir,'dict_lgt_str':lgt_str}
        return lgt_info_dict


    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_line(qp)
        qp.end()

    def draw_line(self, qp):
        qp.setPen(QPen(Qt.gray, 1))
        qp.drawLine(100,100,100,260)



    # buttons clicked.connect
    def btnImport_pressed(self):
        lgt_dir = self.get_light_info()['dict_lgt_dir']
        lgt_file = QFileDialog.getOpenFileNames(self, "Import Light",
                                                lgt_dir,
                                                "MACRO Files (*.macro)")

        KatanaFile.Import(lgt_file[0][0])
