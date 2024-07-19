from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
from Katana import UI4, NodegraphAPI
from Resources.UIPlugins.Connie.ImportEnv import ImportEnv
from Resources.UIPlugins.Connie.ImportLight import ImportLight
from Resources.UIPlugins.Connie.InitialSetting import InitialSetting
from Resources.UIPlugins.Connie.ShotSetting import ShotSetting
from Resources.UIPlugins.Connie.menu import studio_pipe_menu

class Toolkit(UI4.Tabs.BaseTab):
    def __init__(self, parent):
        super(Toolkit, self).__init__(parent=parent)
        self.initUI()
        studio_pipe_menu()
        # Store window references
        self.windows = {}

    def initUI(self):
        self.Box = QLabel()
        self.Box.setMinimumHeight(30)

        self.Img = QLabel()
        self.Img.setStyleSheet("border-image:url(D:/Katana/Inhouse/Icons/Toolkit.png);")
        self.Img.setMinimumSize(109, 126)

        self.InitialSetting = QPushButton("Initial Setting")
        self.InitialSetting.clicked.connect(self.InitialSetting_pressed)
        self.InitialSetting.setStyleSheet(
            "background-color:#212121;"
            "border-radius: 5px;"
        )
        self.InitialSetting.setMinimumHeight(26)

        self.ShotSetting = QPushButton("Shot Setting")
        self.ShotSetting.clicked.connect(self.ShotSetting_pressed)
        self.ShotSetting.setStyleSheet(
            "background-color:#212121;"
            "border-radius: 5px;"
        )
        self.ShotSetting.setMinimumHeight(26)

        self.Env = QPushButton("Import Env")
        self.Env.clicked.connect(self.Env_pressed)
        self.Env.setStyleSheet(
            "background-color:#212121;"
            "border-radius: 5px;"
        )
        self.Env.setMinimumHeight(26)

        self.Lgt = QPushButton("Import Light")
        self.Lgt.clicked.connect(self.Lgt_pressed)
        self.Lgt.setStyleSheet(
            "background-color:#212121;"
            "border-radius: 5px;"
        )
        self.Lgt.setMinimumHeight(26)

        hBox1 = QHBoxLayout()
        hBox1.addWidget(self.InitialSetting)
        hBox2 = QHBoxLayout()
        hBox2.addWidget(self.ShotSetting)
        hBox3 = QHBoxLayout()
        hBox3.addWidget(self.Env)
        hBox4 = QHBoxLayout()
        hBox4.addWidget(self.Lgt)

        vBox0 = QVBoxLayout()
        vBox0.addWidget(self.Box)
        vBox0.addWidget(self.Img)
        vBox0.addStretch()

        vBox1 = QVBoxLayout()
        vBox1.addWidget(self.Box)
        vBox1.addLayout(hBox1)
        vBox1.addLayout(hBox2)
        vBox1.addLayout(hBox3)
        vBox1.addLayout(hBox4)
        vBox1.addStretch()

        canvas = QHBoxLayout()
        canvas.addStretch(10)
        canvas.addLayout(vBox0, 10)
        canvas.addLayout(vBox1, 40)
        canvas.addStretch(20)

        self.setLayout(canvas)
        self.show()

    def InitialSetting_pressed(self):
        self.windows['InitialSetting'] = InitialSetting()
        self.windows['InitialSetting'].show()

    def ShotSetting_pressed(self):
        katana_name = NodegraphAPI.GetProjectDir()
        if katana_name == "":
            QMessageBox.warning(None, "warning", "Save Katana file first")
        else:
            self.windows['ShotSetting'] = ShotSetting()
            self.windows['ShotSetting'].show()

    def Env_pressed(self):
        katana_name = NodegraphAPI.GetProjectDir()
        if katana_name == "":
            QMessageBox.warning(None, "warning", "Save Katana file first")
        else:
            self.windows['ImportEnv'] = ImportEnv()
            self.windows['ImportEnv'].show()

    def Lgt_pressed(self):
        katana_name = NodegraphAPI.GetProjectDir()
        if katana_name == "":
            QMessageBox.warning(None, "warning", "Save Katana file first")
        else:
            self.windows['ImportLight'] = ImportLight()
            self.windows['ImportLight'].show()

if __name__ == "__main__":
    ex = Toolkit()

PluginRegistry = [
    ('KatanaPanel', 2.0, 'Connie/Toolkit', Toolkit),
]
