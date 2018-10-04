# -*-coding:utf-8-*-

from PyQt5.QtWidgets import QApplication
from scalable_function import Index
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # create the instance of GUI to show it
    static_ui = Index()
    static_ui.show()
    sys.exit(app.exec_())