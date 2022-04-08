import pyautogui
import socket
import base64
import json
import time
import os
import io


class VNCClient:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print('Соеденение октрыто.')

        while True:
            try:
                self.client.connect((ip, port))
                break
            except:
                time.sleep(5)

    def close(self):
        self.client.shutdown(socket.SHUT_RDWR)
        self.client.close()

    def mouse_active(self, mouse_flag, x, y):
        if mouse_flag == 'mouse_left_click':
            pyautogui.leftClick(int(x), int(y))
            return "mouse_left_click"

        elif mouse_flag == 'mouse_right_click':
            pyautogui.rightClick(int(x), int(y))
            return "mouse_right_click"

        elif mouse_flag == 'mouse_double_left_click':
            pyautogui.doubleClick(int(x), int(y))
            return "mouse_double_left_click"

    @staticmethod
    def button_key_press(key):
        pyautogui.press(chr(int(key)))
        return 'key_press'

    @staticmethod
    def backspace_press():
        pyautogui.press('backspace')
        return 'key_press'

    @staticmethod
    def caps_press():
        pyautogui.press('capslock')
        return 'key_press'

    @staticmethod
    def screen_handler():
        data_tmp = pyautogui.screenshot()
        io_bytes = io.BytesIO()
        data_tmp.save(io_bytes, format=data_tmp.format)
        data_bytes = io_bytes.getvalue()
        reader = base64.b64encode(data_bytes)
        return reader

    def execute_handler(self):
        while True:
            try:
                responce = self.receive_json()
                if responce[0] == 'screen':
                    result = self.screen_handler()
                elif 'mouse' in responce[0]:
                    result = self.mouse_active(responce[0], responce[1], responce[2])
                elif 'key' in responce[0]:
                    result = self.button_key_press(responce[1])
                elif 'backspace' in responce[0]:
                    result = self.backspace_press()
                elif 'capslock' in responce[0]:
                    result = self.caps_press()
                self.send_json(result)
            except:
                continue

    def send_json(self, data):
        try:
            json_data = json.dumps(data.decode('utf-8'))
        except:
            json_data = json.dumps(data)
        self.client.send(json_data.encode('utf-8'))

    def receive_json(self):
        json_data = ''
        while True:
            try:
                json_data += self.client.recv(1024).decode('utf-8')
                return json.loads(json_data)
            except ValueError:
                pass
