# -*-coding:utf-8-*-

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem, QMessageBox, QDialog
from GUI import Index, Sys_Option_UI
import sys
import threading
import time
from Util import *


class Interaction(Index):
    """
    add interaction on the static GUI as the front end
    """

    def __init__(self):
        super(Interaction, self).__init__()
        self.menu.itemClicked[QTreeWidgetItem, int].connect(self.onClicked)
        self.sys_ui = System()

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
            self.status.setText(u'识别中...')
            rec_thread = threading.Thread(target=Utility.save_cache_of_frame, args=("recognition", ))
            rec_thread.daemon = True
            rec_thread.start()
            # use the queue between socket thread and main GUI thread to get the recognition result
            get_thread = threading.Thread(target=self.get_q_data, args=(result_q, ))
            get_thread.daemon = True
            get_thread.start()
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
            self.sys_ui.show()

    def get_q_data(self, queue):
        """
        to get the data in the queue
        :param queue: which queue
        :return: none
        """

        while True:
            if queue.empty():
                pass
            elif not queue.empty():
                data = queue.get(timeout=5)
                self.id_num.setText(data)
                if data is not None:
                    self.status.setText(u"识别成功")
                elif data is None:
                    self.status.setText(u"脸太多")# 后面有人
                break


class System(Sys_Option_UI):
    """
    override the system option UI
    """

    def __init__(self):
        super(System, self).__init__()
        self.recognition_count.setText(str(RECOGNITION_FRAME))
        self.sign_in_count.setText(str(REGISTER_FRAME))
        self.interval.setText(str(AUTO_SLEEP_INTERIM))
        self.detect_coint.setText(str(DETECT_FRAME))

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