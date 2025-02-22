from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QHBoxLayout,QVBoxLayout,QMessageBox,QFileDialog
from PyQt5.QtGui import QPainter, QPen, QIcon
from PyQt5.QtCore import Qt
import os
from Katana import KatanaFile, NodegraphAPI

class ImportEnv(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # get show name
        show_name = self.get_show_info()['dict_show_name']
        # get Env liveGroup list
        env_str = self.get_env_info()['dict_env_str']


        # set Labels,Buttons,Edits
        self.labelHeader = QLabel()
        self.labelHeader.setStyleSheet("border-image:url(D:/Katana/Inhouse/Icons/Import_env.png);")
        self.labelHeader.setMinimumHeight(60)

        self.labelShow = QLabel("Info")

        self.labelShowName = QLabel(show_name)
        self.labelShowName.setStyleSheet('font-weight: bold;'
                                         'font-size: 16pt; ')

        self.labelEnvList = QLabel(env_str)


        self.btnImport = QPushButton("Import Env")
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
        self.setWindowTitle("Import Environment")
        self.setWindowIcon(QIcon("D:/Katana/Inhouse/Icons/QIcon.png"))
        self.resize(370, 370)



    def get_show_info(self):
        katana_name = NodegraphAPI.GetProjectDir()
        katana_name_list = katana_name.split('/')[0:4]
        show_dir = '/'.join(katana_name_list)
        show_name = katana_name_list[3]
        show_name_dict = {'dict_show_dir':show_dir,'dict_show_name':show_name}
        return show_name_dict

    def get_env_info(self):
        show_dir = self.get_show_info()['dict_show_dir']
        env_dir = show_dir + '/Env/liveGroup'
        env_list = os.listdir(env_dir)

        # get only file name without file format
        env_name_list = []
        for i,v in enumerate(env_list):
            fileName = env_list[i].split('.')[0]
            env_name_list.append(fileName)

        env_str = ',\n'.join(env_name_list)
        env_info_dict = {'dict_env_dir':env_dir,'dict_env_str':env_str}
        return env_info_dict


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
        env_dir = self.get_env_info()['dict_env_dir']

        env_file = QFileDialog.getOpenFileNames(self, "Import Env",
                                                env_dir,
                                                "LIVEGROUP Files (*.livegroup)")

        # create node
        root = NodegraphAPI.GetRootNode()
        new_env = NodegraphAPI.CreateNode('LiveGroup', root)
        # set source value
        new_env.getParameter('source').setValue(env_file[0][0], 0)
        # set node name
        env_file_name = env_file[0][0].split('/')[6]
        env_name = env_file_name.split('.')[0]
        new_env.setName('Env_'+ env_name)
