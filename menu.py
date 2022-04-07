from ManagingClient import run as run_managing
from ReceivingSignalClient import VNCClient
import PySimpleGUI as Psg
import socket


if __name__ == '__main__':
    Psg.theme("DarkGrey1")
    main_layout = [
        [
            Psg.Input(size=40, key='-IP_CONNECT-'),
            Psg.Text(f"Ваш ip-адрес:  {socket.gethostbyname(socket.gethostname())}", size=(40, 1))
        ],
        [
            Psg.Button('Подключиться', size=(15, 1), key='-CONNECT-'),
            Psg.Text(size=(50, 1)),
            Psg.Button('Открыть соединение', size=(15, 1), key='-OPEN_CON-')
        ]
    ]
    main_window = Psg.Window("Ru Viewer", main_layout, button_color="#000")

    while True:
        event, values = main_window.read()
        if event == Psg.WINDOW_CLOSED:
            main_window.close()
            break
        if event == "-CONNECT-":
            main_window.close()
            in_ip = str(values['-IP_CONNECT-'])
            run_managing(in_ip)
        if event == "-OPEN_CON-":
            main_window.close()
            myclient = VNCClient(str(socket.gethostbyname(socket.gethostname())), 5454)
            myclient.execute_handler()

