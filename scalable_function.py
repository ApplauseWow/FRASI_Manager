# -*-coding:utf-8-*-

from PyQt5.QtWidgets import QMainWindow, QDialog
from UI.index import Ui_Index_UI
from UI.identify_id import Ui_Identity_ID_UI
from UI.sign_in import Ui_Sign_In_UI
from UI.sys_option import Ui_sys_option

# GUI classes

class Index(QMainWindow, Ui_Index_UI):
    """
    GUI -- main window
    """

    def __init__(self):
        super(Index, self).__init__()
        self.setupUi(self)
        self.menu.expandAll()
        self.id_ui = Ui_Identity_ID_UI()

        # creating child window demo
        # self.id_window = QDialog()
        # self.id_ui.setupUi(self.id_window)
        # self.id_window.show()


class Identify_Id_UI(QDialog, Ui_Identity_ID_UI):
    """
    GUI -- identify-id window
    """

    def __init__(self):
        super(Identify_Id_UI, self).__init__()
        self.setupUi(self)


class Sign_In_UI(QDialog, Ui_Sign_In_UI):
    """
    GUI -- sign-in window
    """

    def __init__(self):
        super(Sign_In_UI, self).__init__()
        self.setupUi(self)


class Sys_Option_UI(QDialog, Ui_sys_option):
    """
    GUI -- sys-option window
    """

    def __init__(self):
        super(Sys_Option_UI, self).__init__()
        self.setupUi(self)


# following functions in utilities class are scalable and pluggable

class Utility(object):
    """
    utilities
    """

