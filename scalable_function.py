# -*-coding:utf-8-*-

from PyQt5.QtWidgets import QMainWindow, QDialog
from UI.index import Ui_Index_UI
from UI.identify_id import Ui_Identity_ID_UI
from UI.sign_in import Ui_Sign_In_UI
from UI.sys_option import Ui_sys_option


class Index(QMainWindow, Ui_Index_UI):
    """
    GUI 
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



"""
following functions are scalable and pluggable
"""



