import io
import os
import sys
import json
import glob
import time
import socket
import base64
import pyautogui
from des import *
from PyQt5 import QtCore, QtGui, QtWidgets


class MyThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(list)

    def __init__(self, ip, port, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.active_socket = None
        self.ip = ip
        self.port = port
        self.command = 'screen'

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(0)

    def run(self) -> None:
        self.data_connection, _ = self.server.accept()
        self.active_socket = self.data_connection

        while True:
            if self.command.split(' ')[0] != 'screen':
                self.send_json(self.command.split(' '))
                response = self.receive_json()
                self.mysignal.emit([response])
                self.command = 'screen'
            if self.command.split(' ')[0] == 'screen':
                self.send_json(self.command.split(' '))
                response = self.receive_json()
                self.mysignal.emit([response])

    def send_json(self, data):
        try:
            json_data = json.dumps(data.decode('utf-8'))
        except:
            json_data = json.dumps(data)

        try:
            self.active_socket.send(json_data.encode('utf-8'))
        except ConnectionResetError:
            self.active_socket = None

    def receive_json(self):
        json_data = ''
        while True:
            try:
                if self.active_socket is not None:
                    json_data += self.active_socket.recv(1024).decode('utf-8')
                    return json.loads(json_data)
                else:
                    return None
            except ValueError:
                pass


class VNCServer(QtWidgets.QMainWindow):
    def __init__(self, ip_address, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ip = ip_address
        self.port = 5454
        self.thread_handler = MyThread(self.ip, self.port)
        self.thread_handler.start()

        self.thread_handler.mysignal.connect(self.screen_handler)

    def screen_handler(self, screen_value):
        data = ['mouse_left_click', 'mouse_right_click', 'mouse_double_left_click', 'key_press']

        if screen_value[0] not in data:
            decrypt_image = base64.b64decode(screen_value[0])

            with io.BytesIO() as buffer_file:
                buffer_file.write(decrypt_image)
                img_data = buffer_file.getvalue()
                image = QtGui.QPixmap()
                image.loadFromData(img_data)
                self.ui.label.setPixmap(image)

    def closeEvent(self, event):
        pass

    def event(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            current_button = event.button()

            if current_button == 1:
                mouse_cord = f'mouse_left_click {event.x()} {event.y()}'
            elif current_button == 2:
                mouse_cord = f'mouse_right_click {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord

        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            mouse_cord = f'mouse_double_left_click {event.x()} {event.y()}'
            self.thread_handler.command = mouse_cord

        elif event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key.Key_Backspace:
                self.thread_handler.command = f'backspace'
            elif event.key() == QtCore.Qt.Key.Key_CapsLock:
                self.thread_handler.command = f'capslock'
            else:
                self.thread_handler.command = f'key {event.key()}'

        return QtWidgets.QWidget.event(self, event)


def run(ip):
    app = QtWidgets.QApplication(sys.argv)
    myapp = VNCServer(ip_address=ip)
    myapp.show()
    sys.exit(app.exec_())
