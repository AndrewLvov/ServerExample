import socket
from threading import Thread

HOST = ''
PORT = 10015


def client_proc(conn, addr):
    try:
        print('Accepted connection, client addr: ', addr)

        conn.send('What is your name ?'.encode('utf-8'))
        name = conn.recv(1024).decode('utf-8')
        while True:
            data = conn.recv(1024)
            if not data:
                break
            msg = data.decode('utf-8')
            if msg == '<quit>':
                break
            print("{} ({}): ".format(name, addr[0]), msg)

        print("{} ({}) disconnected".format(name, addr[0]))
        conn.close()
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
