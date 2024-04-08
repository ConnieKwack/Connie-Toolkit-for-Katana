from Katana import Callbacks

def execute(**kwargs):
    from Resources.UIPlugins.Connie import menu
    menu.studio_pipe_menu()

callback_type = Callbacks.Type.onStartupComplete
Callbacks.addCallback(callback_type, execute, callbackObjectHash=None)