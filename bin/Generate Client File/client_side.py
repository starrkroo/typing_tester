import socket
import sys
from PyQt5.QtWidgets import QLineEdit, QLabel, QApplication, QMainWindow, QPushButton, QWidget, QPlainTextEdit, QDesktopWidget
from PyQt5.QtGui import QFont
from threading import Thread
from time import sleep


MAIN_CONNECTION_SERVER = '192.168.1.49'

class User(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer_counter = 0
        self.initUI()
        Thread(target=self.get_started).start()

    def initUI(self):
        # shows line for editing, timer, and exit button
        self.current_window = QWidget()

        # client socket for connection to server
        self.socket__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket__.connect((MAIN_CONNECTION_SERVER, 5001))

        # configuration of screen -- width, height
        screen_config = QDesktopWidget().screenGeometry(-1)
        screen_width, screen_height = screen_config.width(), screen_config.height()

        # self.current_window objects:

        # main field, where user must enter text
        self.log = QPlainTextEdit(self.current_window)
        self.log.setEnabled(False)
        self.log.setGeometry(0,
                             screen_height // 6,
                             screen_width,
                             int(screen_height * 3/4)
            )
        self.log.setFont(QFont('Times', 20))

        # button to exit out of game
        self.exit_button = QPushButton('Exit', self.current_window)
        self.exit_button.setGeometry(screen_width - screen_width // 4 + 15 + 50, 30, 35, 25)
        self.exit_button.clicked.connect(self.exit_out)
        self.exit_button.setEnabled(False)

        # label to show how much time is left
        self.timer_info = QLabel('', self.current_window)
        self.timer_info.setFont(QFont('Times', 50))
        self.timer_info.setGeometry(screen_width // 2 - 300, 30, 350, 170)

        self.setGeometry(200, 20, 700, 600)
        self.setWindowTitle('Добро пожаловать!')
        self.setCentralWidget(self.current_window)
        self.show()

    def closeEvent(self, event):
        self.socket__.close()
        sys.exit()

    def change_button(self):
        self.exit_button.setEnabled(True)

    def exit_out(self):
        sys.exit()

    def show_data(self):
        # self.timer_info.setText(
        #     str(
        #         len(self.log.toPlainText().strip())
        #     ))
        self.timer_info.setFont(QFont('Times', 100))
        self.log.setReadOnly(True)

    def send_text_to_server(self):
        self.socket__.send(self.log.toPlainText().encode())
        if self.socket__.recv(1024).decode() == '1':
            self.timer_info.setText("+")
        else:
            self.timer_info.setText("-")

    def begin_timer(self):
        while self.timer_counter != 10:
            self.timer_counter += 1
            self.timer_info.setText(str(self.timer_counter))
            sleep(1)

        self.send_text_to_server()
        self.change_button()
        self.show_data()
        self.end_game()

    def get_started(self):
        print('reading')
        msg = self.socket__.recv(1024)
        if msg.decode() == '1':
            self.start_game()
            Thread(target=self.begin_timer).start()

    def start_game(self):
        self.log.setEnabled(True)

    def end_game(self):
        self.log.setEnabled(False)



app = QApplication(sys.argv)
my_window = User()
my_window.showFullScreen()
sys.exit(app.exec_())

# msg = s.recv(1024)




# if msg == '1':
