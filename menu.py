from ManagingClient import run as run_managing
from ReceivingSignalClient import VNCClient
import PySimpleGUI as Psg
import socket


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if __name__ == '__main__':
    Psg.theme("Reddit")
    main_layout = [
        [
            Psg.Text(size=1)
        ],
        [
            Psg.Input(size=40, key='-IP_CONNECT-'),
            Psg.Text(size=(25, 1)),
            Psg.Text(f"Ваш ip-адрес:  {get_ip()}", size=(25, 1))
        ],
        [
            Psg.Text(size=1)
        ],
        [
            Psg.Button('Подключиться', size=(15, 1), key='-CONNECT-'),
            Psg.Text(size=(50, 1)),
            Psg.Button('Открыть соединение', size=(15, 1), key='-OPEN_CON-')
        ]
    ]
    main_window = Psg.Window("Ru Viewer", main_layout)

    while True:
        event, values = main_window.read()
        if event == Psg.WINDOW_CLOSED:
            main_window.close()
            break
        if event == "-OPEN_CON-":
            main_window.close()
            run_managing(str(get_ip()))
        if event == "-CONNECT-":
            main_window.close()
            in_ip = str(values['-IP_CONNECT-'])
            myclient = VNCClient(in_ip, 5454)
            myclient.execute_handler()

