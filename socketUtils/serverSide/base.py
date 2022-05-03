import socket

class Base:
    def __init__(self, ip = '10.0.0.187', port = 1234, function='test'):
        self.ip = ip
        self.port = port
        if function == 'test':
            self.test()
        #print(f'Hi, {self.ip}')

    def test(self):
        self.socketConnect()

        while True:
            print('Waiting for client to connect')
            clientsocket, address = self.s.accept()
            print(f"Connection from {self.ip} has been established!")
            clientsocket.send(bytes("Welcome to the server!", "utf-8"))
    
    # method to keep connecting method consistent 
    def socketConnect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('',self.port))
        self.s.listen(5)
        
if __name__ == '__main__':
    b = Base()

