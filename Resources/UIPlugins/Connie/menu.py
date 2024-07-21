import UI4
from PyQt5.QtWidgets import QAction, QMenu, QMessageBox
from PyQt5.QtGui import QIcon
from Katana import NodegraphAPI



#  menu
def studio_pipe_menu():
    main_window = UI4.App.Layouts._PrimaryWindow
    main_menu = main_window.findChild(UI4.App.MainMenu.MainMenu)
    studio_menu = QMenu(parent=main_menu)
    studio_menu.setTitle('Connie')
    main_menu.addMenu(studio_menu)


    tools = {Initial_Setting:'Initial Setting',
             Shot_Setting:'Shot Setting',
             Import_Env:'Import Env',
             Import_Light:'Import Light'}

    for k,v in tools.items():
        action = QAction(QIcon('D:/Katana/Inhouse/Icons/QIcon_grey.png'),v,studio_menu)
        action.triggered.connect(k)
        studio_menu.addAction(action)




#  global variable to float custom windows
#  I don't feel the need to float multiple windows, so I made only one global variable.
g_window = None




#  click event
def Initial_Setting():
    from Resources.UIPlugins.Connie.InitialSetting import InitialSetting
    global g_window
    g_window = InitialSetting()
    g_window.show()


def Shot_Setting():
    katana_name = NodegraphAPI.GetProjectDir()
    if katana_name == "":
        QMessageBox.warning(None, "warning", "Save Katana file first  ")
    else:
        from Resources.UIPlugins.Connie.ShotSetting import ShotSetting
        global g_window
        g_window = ShotSetting()
        g_window.show()


def Import_Env():
    katana_name = NodegraphAPI.GetProjectDir()
    if katana_name == "":
        QMessageBox.warning(None, "warning", "Save Katana file first  ")
    else:
        from Resources.UIPlugins.Connie.ImportEnv import ImportEnv
        global g_window
        g_window = ImportEnv()
        g_window.show()


def Import_Light():
    katana_name = NodegraphAPI.GetProjectDir()
    if katana_name == "":
        QMessageBox.warning(None, "warning", "Save Katana file first  ")
    else:
        from Resources.UIPlugins.Connie.ImportLight import ImportLight
        global g_window
        g_window = ImportLight()
        g_window.show()
