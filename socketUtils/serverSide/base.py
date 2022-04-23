import socket

class Base:
    def __init__(self, ip = '10.0.0.187', port = 1234):
        self.ip = ip
        self.port = port
        #print(f'Hi, {self.ip}')

    def test(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('',self.port))
        s.listen(5)

        while True:
            clientsocket, address = s.accept()
            print(f"Connection from {self.ip} has been established!")
            clientsocket.send(bytes("Welcome to the server!", "utf-8"))


if __name__ == '__main__':
    b = Base()
    b.test()
