from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout
from PyQt5 import QtGui
from Katana import KatanaFile, NodegraphAPI

class InitialSetting(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # set Labels,Buttons,Edits
        self.labelHeader = QLabel()
        self.labelHeader.setStyleSheet("border-image:url(D:/Katana/Inhouse/Icons/Initial_setting.png);")
        self.labelHeader.setMinimumHeight(60)

        self.labelShow = QLabel("Show")
        self.lineShow = QLineEdit()

        self.labelSeq = QLabel("Sequence")
        self.lineSeq = QLineEdit()

        self.btnImport = QPushButton("Import template")
        self.btnImport.clicked.connect(self.btnImport_pressed)

        self.labelInOut = QLabel("In/Out Time")
        self.lineIn = QLineEdit()
        self.lineOut = QLineEdit()

        self.labelRes = QLabel("Resolution")
        self.lineResX = QLineEdit()
        self.lineResY = QLineEdit()

        self.btnSet = QPushButton("Set project")
        self.btnSet.clicked.connect(self.btnSet_pressed)

        self.labelSaveAs = QLabel("Save As")
        self.lineSaveAs = QLineEdit()

        self.btnSave = QPushButton("Save file")
        self.btnSave.clicked.connect(self.btnSave_pressed)



        # set hbox
        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.labelHeader)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self.labelShow,30)
        hbox1.addWidget(self.lineShow,50)
        hbox1.addStretch(10)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(self.labelSeq,30)
        hbox2.addWidget(self.lineSeq,50)
        hbox2.addStretch(10)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(10)
        hbox3.addWidget(self.btnImport,80)
        hbox3.addStretch(10)

        hbox4 = QHBoxLayout()
        hbox4.addStretch(10)
        hbox4.addWidget(self.labelInOut,30)
        hbox4.addWidget(self.lineIn,25)
        hbox4.addWidget(self.lineOut,25)
        hbox4.addStretch(10)

        hbox5 = QHBoxLayout()
        hbox5.addStretch(10)
        hbox5.addWidget(self.labelRes,30)
        hbox5.addWidget(self.lineResX,25)
        hbox5.addWidget(self.lineResY,25)
        hbox5.addStretch(10)

        hbox6 = QHBoxLayout()
        hbox6.addStretch(10)
        hbox6.addWidget(self.btnSet,80)
        hbox6.addStretch(10)

        hbox7 = QHBoxLayout()
        hbox7.addStretch(10)
        hbox7.addWidget(self.labelSaveAs,30)
        hbox7.addWidget(self.lineSaveAs,50)
        hbox7.addStretch(10)

        hbox8 = QHBoxLayout()
        hbox8.addStretch(10)
        hbox8.addWidget(self.btnSave,80)
        hbox8.addStretch(10)


        # set vbox
        vbox = QVBoxLayout()
        vbox.addLayout(hbox0,1)
        vbox.addStretch(1)
        vbox.addLayout(hbox1,1)
        vbox.addLayout(hbox2,1)
        vbox.addLayout(hbox3,1)
        vbox.addStretch(2)
        vbox.addLayout(hbox4,1)
        vbox.addLayout(hbox5,1)
        vbox.addLayout(hbox6,1)
        vbox.addStretch(2)
        vbox.addLayout(hbox7,1)
        vbox.addLayout(hbox8,1)
        vbox.addStretch(2)

        # set layout
        self.setLayout(vbox)

        # set window
        self.setWindowTitle("Initial Setting")
        self.setWindowIcon(QtGui.QIcon("D:/Katana/Inhouse/Icons/QIcon.png"))
        self.resize(370, 450)

        # show
        self.show()

    # buttons clicked.connect
    def btnImport_pressed(self):
        show = self.lineShow.text()
        seq = self.lineSeq.text()
        FileName = "D:/Katana/Show/" + show + "/Seq/" + seq + "/Template/template.katana"
        KatanaFile.Import(FileName)
    def btnSet_pressed(self):
        # inTime/outTime
        inTime = self.lineIn.text()
        outTime = self.lineOut.text()
        NodegraphAPI.SetInTime(inTime, final=True)
        NodegraphAPI.SetOutTime(outTime, final=True)
        NodegraphAPI.SetCurrentTime(inTime, final=True)

        # resolution
        resX = self.lineResX.text()
        resY = self.lineResY.text()
        CreateResolution = [resX, 'x', resY]
        Resolution = ''.join(CreateResolution)
        NodegraphAPI.GetRootNode().getParameter('resolution').setValue(Resolution, 0)

        # shot variable setting
        get_variable = NodegraphAPI.GetRootNode().getParameter('variables').createChildGroup("Shot")
        get_variable.createChildNumber("enable", 1)
        get_variable.createChildString("value", "")
        get_variable.createChildStringArray("options", 1)

    def btnSave_pressed(self):
        showName = self.lineShow.text()
        seqName = self.lineSeq.text()
        FileName = self.lineSaveAs.text()
        pathList = ['D:/Katana/Show/', showName, '/Seq/', seqName, '/KatanaFiles/', FileName]
        filePath = ''.join(pathList)
        KatanaFile.Save(filePath, None)