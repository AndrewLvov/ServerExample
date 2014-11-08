from socketserver import BaseRequestHandler, TCPServer


class MySimpleChat(BaseRequestHandler):
    HOST = ''
    PORT = 10015

    def __init__(self, request, client_address, server):
        super(MySimpleChat, self).__init__(request, client_address, server)
        self.msg = ''

    def handle(self):
        self.request.send("What's your name ?".encode('utf-8'))
        self.msg = self.request.recv(1024).decode('utf-8')
        print("{}: {}".format(self.client_address[0], self.msg))


def main():
    server = TCPServer((MySimpleChat.HOST, MySimpleChat.PORT), MySimpleChat)
    server.serve_forever()

if __name__ == '__main__':
    main()
