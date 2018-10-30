# -*-coding:utf-8-*-

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem, QMessageBox
from GUI import Index
import sys
import threading
import time
from Util import Utility


class Interaction(Index):
    """
    add interaction on the static GUI as the front end
    """

    def __init__(self):
        super(Interaction, self).__init__()
        self.menu.itemClicked[QTreeWidgetItem, int].connect(self.onClicked)

    # def closeEvent(self, QCloseEvent):
    #     """
    #     closing window signal trigger this function
    #     :param QCloseEvent: event
    #     :return: none
    #     """
    #     reply = QMessageBox.question(self, u'FRASI Manager', u"是否要退出程序？",
    #                                            QMessageBox.Yes | QMessageBox.No,
    #                                            QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         exit_thread = threading.Thread(target=Utility.socket_transmission, args=("exit",))
    #         exit_thread.start()
    #         time.sleep(2)
    #         exit_thread.join()
    #         QCloseEvent.accept()
    #     else:
    #         QCloseEvent.ignore()

    def onClicked(self, item, colum):
        """
        when click the item in menu, trigger this function
        :param item: object of item
        :param colum: number of colum
        :return: none
        """

        task = item.text(0)
        print task
        # print type(task) # object of task is unicode
        if task == u'人脸检测':
            camera_thread = threading.Thread(target=Utility.open_camera, args=(self.frame, ))
            camera_thread.daemon = True
            camera_thread.start()
        elif task == u'人脸考勤':
            # will be done
            pass
        elif task == u'人脸识别':
            rec_thread = threading.Thread(target=Utility.save_cache_of_frame, args=("recognition", ))
            rec_thread.daemon = True
            rec_thread.start()
        elif task == u'人脸检索':
            pass
        elif task == u'单脸注册':
            # will be done
            pass
        elif task == u'多脸注册':
            # will be done
            pass
        elif task == u'身份证注册':
            pass
        elif task == u'语音识别':
            pass
        elif task == u'语音检索':
            pass
        elif task == u'语音考勤':
            pass
        elif task == u'语音注册':
            pass
        elif task == u'数据导出':
            pass
        elif task == u'数据导入':
            pass
        elif task == u'统计查看':
            pass
        elif task == u'参数配置':
            # will be done
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # create the instance of GUI to show it
    front_end = Interaction()
    front_end.show()
    camera_thread = threading.Thread(target=Utility.open_camera, args=(front_end.frame, ))
    # static_ui = Index()
    # static_ui.show()
    # camera_thread = threading.Thread(target=Utility.open_camera, args=(static_ui.frame, ), name="camera")
    camera_thread.daemon = True
    camera_thread.start()
    sys.exit(app.exec_())