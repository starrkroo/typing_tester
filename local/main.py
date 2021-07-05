import sys

import helper
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from threading import Thread


class Teacher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.response = ''
        self.initUI()
        Thread(target=self.create_socket_listener).start()

    def create_socket_listener(self):
        self.created_nm = helper.NetworkM()
        # previous_value = len(self.created_nm.user_ids)
        while True:
            resp = self.created_nm.start()
            # if len(self.created_nm.user_ids) != previous_value:
            if resp:
                self.user_cons_info.setText(f'{len(self.created_nm.user_ids)}/{self.created_nm.DEFAULT_COMPUTER_NUMBER}')
                # previous_value = len(self.created_nm.user_ids)


            print("Computer size is", self.created_nm.DEFAULT_COMPUTER_NUMBER)

    def initUI(self):
        # configuration for start button
        self.button = QPushButton('', self)
        self.button.setGeometry(250, 200, 200, 200)
        self.button.setFlat(True)
        self.button.setIcon(QIcon("access.png"))
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
        self.user_cons_info.setGeometry(250, 20, 200, 200)


        self.setGeometry(200, 20, 700, 600)
        self.setWindowTitle('Добро пожаловать!')
        self.show()

    def change_computer_size(self):
        print(self.how_many_pcs.text().isdigit())
        if self.how_many_pcs.text().isdigit():
            self.created_nm.set_pc_count(int(self.how_many_pcs.text()))
            print("Updated value: ", self.created_nm.DEFAULT_COMPUTER_NUMBER)

    def begin_mailing(self):
        self.created_nm.begin_mailing()
            # print(self.created_nm.DEFAULT_COMPUTER_NUMBER)
                # begin_some_timer()




app = QApplication(sys.argv)
my_window = Teacher()
# my_window.showFullScreen()
sys.exit(app.exec_())
