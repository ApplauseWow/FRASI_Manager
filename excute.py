# -*-coding:utf-8-*-

from PyQt5.QtWidgets import QApplication
from GUI import Index
import sys
import threading
from Util import Utility

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # create the instance of GUI to show it
    static_ui = Index()
    static_ui.show()
    camera_thread = threading.Thread(target=Utility.open_camera, args=(static_ui.frame, ), name="camera")
    camera_thread.daemon = True
    camera_thread.start()
    sys.exit(app.exec_())