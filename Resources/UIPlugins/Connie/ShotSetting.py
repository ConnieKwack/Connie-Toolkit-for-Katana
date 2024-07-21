from PyQt5.QtWidgets import QWidget,QLabel,QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,QMessageBox
from PyQt5 import QtGui
from Katana import KatanaFile, NodegraphAPI

class ShotSetting(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # set Labels,Buttons,Edits
        self.labelHeader = QLabel()
        self.labelHeader.setStyleSheet("border-image:url(D:/Katana/Inhouse/Icons/Shot_setting.png);")
        self.labelHeader.setMinimumHeight(60)

        self.labelShot = QLabel("Shot Name")
        self.lineShot = QLineEdit()

        self.btnSetVariable = QPushButton("Set variable")
        self.btnSetVariable.clicked.connect(self.btnSetVariable_pressed)

        self.btnCheck = QPushButton("Check list of caches")
        self.btnCheck.clicked.connect(self.btnCheck_pressed)

        self.btnImport = QPushButton("Import caches")
        self.btnImport.clicked.connect(self.btnImport_pressed)



        # set hbox
        hbox0 = QHBoxLayout()
        hbox0.addWidget(self.labelHeader)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(10)
        hbox1.addWidget(self.labelShot,30)
        hbox1.addWidget(self.lineShot,50)
        hbox1.addStretch(10)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(10)
        hbox2.addWidget(self.btnSetVariable,80)
        hbox2.addStretch(10)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(10)
        hbox3.addWidget(self.btnCheck,80)
        hbox3.addStretch(10)

        hbox4 = QHBoxLayout()
        hbox4.addStretch(10)
        hbox4.addWidget(self.btnImport,80)
        hbox4.addStretch(10)


        # set vbox
        vbox = QVBoxLayout()
        vbox.addLayout(hbox0)
        vbox.addStretch(20)
        vbox.addLayout(hbox1)
        vbox.addStretch(2)
        vbox.addLayout(hbox2)
        vbox.addStretch(2)
        vbox.addLayout(hbox3)
        vbox.addStretch(2)
        vbox.addLayout(hbox4)
        vbox.addStretch(20)

        # set layout
        self.setLayout(vbox)

        # set window
        self.setWindowTitle("Shot Setting")
        self.setWindowIcon(QtGui.QIcon("D:/Katana/Inhouse/Icons/QIcon.png"))
        self.resize(370, 300)




    def AddVariableSwitchPattern(self,shot):
        varSwitch = NodegraphAPI.GetNode('VariableSwitch')
        varSwitch_pattern = NodegraphAPI.GetNode('VariableSwitch').getParameter('patterns')
        varSwitch_patternNum = varSwitch_pattern.getNumChildren()
        # add port
        port_i = 'i' + str(varSwitch_patternNum)
        varSwitch.addInputPort(port_i)
        # set pattern
        pattern_i = 'patterns.i' + str(varSwitch_patternNum)
        varSwitch.getParameter(pattern_i).setValue(shot, 0)




    # buttons clicked.connect
    def btnSetVariable_pressed(self):
        root = NodegraphAPI.GetRootNode()
        shotName = self.lineShot.text()
        # insert new shot into variable array
        options_child = root.getParameter('variables.Shot.options').getNumChildren()
        new_i = options_child - 1
        new_str_i = str(new_i)
        options_param = "variables.Shot.options.i" + new_str_i
        root.getParameter('variables.Shot.options').insertArrayElement(1)
        root.getParameter(options_param).setValue(shotName, 0)
        # add pattern for variable switch node
        self.AddVariableSwitchPattern(shotName)

    def btnCheck_pressed(self):
        shotName = self.lineShot.text()
        scene_name = NodegraphAPI.GetProjectDir()
        pub_dir = scene_name.split('KatanaFiles')[0] + shotName + '/pub'

        import os
        asset_list = os.listdir(pub_dir)
        asset_str = ',\n'.join(asset_list)
        QMessageBox.about(None, "list of caches", shotName + ":\n\n" + asset_str)

    def btnImport_pressed(self):
        shotName = self.lineShot.text()
        scene_name = NodegraphAPI.GetProjectDir()
        pub_dir = scene_name.split('KatanaFiles')[0] + shotName + '/pub'
        count_asset = []

        # create Group node
        asset_group = NodegraphAPI.CreateNode("Group", NodegraphAPI.GetRootNode())
        asset_group.setName(shotName + "Grp")

        # create Merge node
        mergeN = NodegraphAPI.CreateNode("Merge", asset_group)
        NodegraphAPI.SetNodePosition(mergeN, (0, -90))
        # port issue...
        dot = NodegraphAPI.CreateNode("Dot", NodegraphAPI.GetRootNode())
        mergeN.getOutputPort('out').connect(dot.getInputPort('input'))
        dot.delete()

        # create UsdIn node--------------
        import os
        asset_list = os.listdir(pub_dir)

        for i, v in enumerate(asset_list):
            mergeN.addInputPort(f"i{i}")
            asset_file_name = pub_dir + '/' + v
            new_node = NodegraphAPI.CreateNode("UsdIn", asset_group)
            new_node.setName(v)
            new_node.getParameter('fileName').setValue(asset_file_name, 0)
            new_node.getParameter('location').setValue('/root/world/geo/asset', 0)
            new_node.getOutputPort('out').connect(mergeN.getInputPort(f"i{i}"))

            # set node position
            count_asset.append(v)
            position = (-150 + 150 * len(count_asset), 0)
            NodegraphAPI.SetNodePosition(new_node, (position))
