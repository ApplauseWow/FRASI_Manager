# -*-coding:utf-8-*-

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QTreeWidgetItem, QMessageBox, QDialog
from GUI import Index, Sys_Option_UI, Identify_Id_UI, Sign_In_UI
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
        self.id_num.setText("")
        self.name.setText("")
        self.date.setText("")
        self.status.setText("")
        self.sys_ui = System()
        # self.compare_ui = Compare()
        self.re_signal = True

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

    def onClicked(self, item, column):
        """
        when click the item in menu, trigger this function
        :param item: object of item
        :param column: number of colum
        :return: none
        """

        task = item.text(0)
        print task
        # print type(task) # object of task is unicode
        if task == u'人脸检测':
            camera_thread = threading.Thread(target=Utility.open_camera, args=(self.frame, ))
            camera_thread.daemon = True
            camera_thread.start()
        elif task == u'人脸识别' or task == u"人脸考勤":
            if self.re_signal:
                self.re_signal = False
                rec_thread = threading.Thread(target=Utility.save_cache_of_frame, args=("recognition",))
                rec_thread.daemon = True
                rec_thread.start()
                # use the queue between socket thread and main GUI thread to get the recognition result
                if task == u"人脸考勤":
                    self.status.setText(u"考勤中...")
                    get_thread = threading.Thread(target=self.get_q_data, args=(result_q, True))
                else:
                    self.status.setText(u'识别中...')
                    get_thread = threading.Thread(target=self.get_q_data, args=(result_q, ))
                get_thread.daemon = True
                get_thread.start()
            elif not self.re_signal:
                # back end is recognizing... wait...
                pass
        elif task == u'人脸检索':
            pass
        elif task == u'单脸注册':
            self.setDisabled(True)
            compare_ui = Compare(self)
            compare_ui.raise_()
            compare_ui.show()
        elif task == u'多脸注册':
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

    def get_q_data(self, queue, attendance=False):
        """
        to get the data in the queue
        :param queue: which queue
        :param attendance: attendance
        :return: none
        """

        while True:
            if queue.empty():
                pass
            elif not queue.empty():
                try:
                    data = queue.get(timeout=5)
                    self.id_num.setText(data['id'])
                    self.name.setText(data['name'])
                    self.date.setText(data['date'])
                    if data is not None:
                        if not attendance:
                            self.status.setText(u"识别成功")
                        elif attendance:
                            sql = "insert into attendance_record (userid, device_deployment_id, remarks, attendance_status, time) values(%s,%s,%s,%s,%s)"
                            arg_list = [data['id'], 1, '1', '1', data['date']]
                            op = ["insert", sql, arg_list]
                            feedback = Utility.sql_operation(op)
                            if feedback['result'] > 0:
                                self.status.setText(u"考勤成功")
                            else:
                                self.status.setText(u"考勤失败")
                    elif data is None:
                        self.status.setText(u"脸太多")  # 后面有人
                    self.re_signal = True
                    break
                except Queue.Empty as e:
                    print e
                    self.id_num.setText("")
                    self.name.setText("")
                    self.date.setText("")
                    self.status.setText(u"重新操作")
                    self.re_signal = True
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
        self.rejected.connect(self.init_params)
        self.accepted.connect(self.save_params)

    def closeEvent(self, QCloseEvent):
        """
        close the dialog, and initial parameters
        :param QCloseEvent: signal
        :return: none
        """

        self.recognition_count.setText(str(RECOGNITION_FRAME))
        self.sign_in_count.setText(str(REGISTER_FRAME))
        self.interval.setText(str(AUTO_SLEEP_INTERIM))
        self.detect_coint.setText(str(DETECT_FRAME))

    def init_params(self):
        """
        init the params if didn't accept
        :return: none
        """

        self.recognition_count.setText(str(RECOGNITION_FRAME))
        self.sign_in_count.setText(str(REGISTER_FRAME))
        self.interval.setText(str(AUTO_SLEEP_INTERIM))
        self.detect_coint.setText(str(DETECT_FRAME))

    def save_params(self):
        """
        save the params in the dialog
        :return: none
        """

        xml_path = os.path.join(os.getcwd(), "sys.xml")
        params = dict()
        params["recognition_frame"] = self.recognition_count.text()
        params["register_frame"] = self.sign_in_count.text()
        params["auto_sleep_interim"] = self.interval.text()
        params["detect_frame"] = self.detect_coint.text()
        Utility.write_xml(xml_path, params)


class Compare(Identify_Id_UI):
    """
    to make sure that there exist this identity
    """

    def __init__(self):
        super(Compare, self).__init__()
        self.id_input.setText("")


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