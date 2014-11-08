import socket
from threading import Thread

HOST = ''
PORT = 10015


class ConnectedUser:
    conn = None
    addr = None

    def __init__(self, name, conn, addr):
        self.name = name
        self.conn = conn
        self.addr = addr


connected_users = []


def notify_all(msg, exclude=None):
    for u in connected_users:
        if u != exclude:
            u.conn.send(msg.encode('utf-8'))
    print(msg)


def client_proc(conn, addr):
    try:
        print('Accepted connection, client addr: ', addr)

        conn.send('What is your name ?'.encode('utf-8'))
        name = conn.recv(1024).decode('utf-8')
        conn.send('Hi, {}!.'.format(name).encode('utf-8'))

        user = ConnectedUser(name, conn, addr)
        global connected_users
        connected_users.append(user)

        formatted = '>>>{} joined chat!'.format(name)
        notify_all(formatted, user)
        conn.send('Type /exit or /quit to disconnect chat'.encode('utf-8'))

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode('utf-8')
                if msg in ['/quit', '/exit']:
                    break
                formatted = "{} ({}): {}".format(name, addr[0], msg)
                notify_all(formatted, user)
            except socket.error as e:
                break

        connected_users = list(filter(lambda x: x.conn != conn, connected_users))
        conn.close()
        formatted = "<<<{} ({}) disconnected".format(name, addr[0])
        notify_all(formatted)
    except KeyboardInterrupt:
        exit()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print('Started listening on port ', PORT)

    while True:
        conn, addr = s.accept()

        client_thread = Thread(target=client_proc, kwargs={'conn': conn, 'addr': addr})
        client_thread.start()

if __name__ == '__main__':
    main()
