import sys
import asyncio

# TODO: вернуть возможность задавать количество компов, по дефолту -- 1

from bin import helper
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont
from threading import Thread
from time import sleep
from fuzzywuzzy import fuzz


class Teacher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.response = ''
        self.initUI()
        Thread(target=self.create_socket_listener).start()
        self.DEFAULT_PERCENT_TOGO_CHECK = 15

    def create_socket_listener(self):
        self.created_nm = helper.NetworkM()
        # previous_value = len(self.created_nm.user_ids)
        while True:
            resp = self.created_nm.start()
            # if len(self.created_nm.user_ids) != previous_value:
            if resp:
                self.user_cons_info.setText(f'{len(self.created_nm.user_ids)}/{self.created_nm.DEFAULT_COMPUTER_NUMBER}')
                if len(self.created_nm.user_ids) == self.created_nm.DEFAULT_COMPUTER_NUMBER:
                    self.user_cons_info.setStyleSheet("color: green")
                else:
                    self.user_cons_info.setStyleSheet("color: red")
                # previous_value = len(self.created_nm.user_ids)

    def closeEvent(self, event):
        self.created_nm.end_connection()

    def initUI(self):
        # configuration for start button
        self.button = QPushButton('', self)
        self.button.setGeometry(250, 200, 200, 200)
        self.button.setFlat(True)
        self.button.setIcon(QIcon("bin/assets/access.png"))
        self.button.setIconSize(QSize(200, 200))
        self.button.clicked.connect(self.begin_mailing)

        # configuration for setting user number
        self.how_many_pcs = QLineEdit('', self)
        self.how_many_pcs.setGeometry(150, 150, 50, 30)
        # button for this config
        self.how_many_pcs__button = QPushButton('send', self)
        self.how_many_pcs__button.setGeometry(200, 150, 50, 30)
        self.how_many_pcs__button.clicked.connect(self.change_computer_size)

        # configuration for monitoring how many user are on the server
        self.user_cons_info = QLabel('', self)
        self.user_cons_info.setStyleSheet("color: red")
        self.user_cons_info.setFont(QFont('Times', 80))
        self.user_cons_info.setGeometry(280, 20, 200, 200)

        self.setGeometry(200, 20, 700, 600)
        self.setWindowTitle('Добро пожаловать!')
        self.show()
        
    def change_computer_size(self):
        if self.how_many_pcs.text().isdigit():
            self.created_nm.set_pc_count(int(self.how_many_pcs.text()))
            self.user_cons_info.setText(f'{len(self.created_nm.user_ids)}/{self.created_nm.DEFAULT_COMPUTER_NUMBER}')

            if len(self.created_nm.user_ids) == self.created_nm.DEFAULT_COMPUTER_NUMBER:
                self.user_cons_info.setStyleSheet("color: green")
            else:
                self.user_cons_info.setStyleSheet("color: red")

    async def wait_for_end(self):
        print('1')
        await asyncio.sleep(10)
        print('go on')
        readstream = open('bin/assets/default_text.txt', encoding='utf-8')
        default_read_text = readstream.read()
        readstream.close()

        for client_socket in self.created_nm.to_monitor:
            print(client_socket)
            recved = client_socket.recv(1024).decode().lower()
            if fuzz.ratio(recved,
                          default_read_text.lower()) > self.DEFAULT_PERCENT_TOGO_CHECK:
                client_socket.send("1".encode())
            else:
                client_socket.send("0".encode())


    def begin_mailing(self):
        self.created_nm.begin_mailing()
        loop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(self.wait_for_end())
            loop.run_until_complete()
        finally:
            loop.close()
        # Thread(target=self.wait_for_end).start()


app = QApplication(sys.argv)
my_window = Teacher()
# my_window.showFullScreen()
sys.exit(app.exec_())
