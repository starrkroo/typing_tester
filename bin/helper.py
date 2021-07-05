
import socket


class NetworkM:
    """
        Class, that sends to each client of network message '1' which notifies user he is able for enter text
    """
    def __init__(self):
        """
        :param how_many_pc: how many pc in your computer club
        """
        self.to_monitor = []
        self.user_ids = []
        self.DEFAULT_COMPUTER_NUMBER = 2
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set up server socket
        hostname = socket.gethostname()
        local_ipv4 = socket.gethostbyname(hostname)
        print(local_ipv4)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((local_ipv4, 5001))
        self.server_socket.listen()

    def __accept_connection(self, data):
        """
        Function, which makes registration for user in network
        :param data: gets client socket and address from user
        :return: nothing, making registration for user
        """
        client_socket, address = data
        print("Connection from ", address)
        self.user_ids.append(address)
        self.to_monitor.append(client_socket)

    def __send_messages(self):
        """
            Send message for each user
        :return: nothing, simply sends messages
        """
        for index, client_socket in enumerate(self.to_monitor):
            print(index)
            client_socket.sendto('1'.encode(), self.user_ids[index])

    def set_pc_count(self, value):
        self.DEFAULT_COMPUTER_NUMBER = value

    def begin_mailing(self):
        if len(self.user_ids) == self.DEFAULT_COMPUTER_NUMBER:
            self.__send_messages()

    def end_connection(self):
        self.server_socket.close()

    def start(self):
        """
            Main loop for waiting user's connection
        :return:
            1 - if user is connected
        """

        try:
            generate_data = self.server_socket.accept()
        except OSError:
            exit()

        self.__accept_connection(generate_data)
        return 1


if __name__ == '__main__':
    trying = NetworkM()
    trying.set_pc_count(1)
    trying.start()
