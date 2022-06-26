import socket, socket_sys, json
from datetime import datetime
from tkinter import messagebox
from _thread import start_new_thread

def sendMessage(message, target, from_='server', position=0):
    if target == None or target == False or len(target) == 0:
        return
    if len(from_) == 0:
        from_ = 'Unknown'
    for port in target:
        try:
            if from_.lower() == 'server':
                temp_from_ = 'SERVER'
            else:
                temp_from_ = NAMES[str(from_)]
            sendData = json.dumps({'message':message, 'to':target, 'from':temp_from_, 'pos':position, 'timestamp':datetime.now().strftime("%H:%M:%S")}).encode()
            CONNECTIONS[str(port)].send(str(len(sendData)).zfill(4).encode())
            CONNECTIONS[str(port)].send(sendData)          
        except Exception as error:
            print(f"|> Message sending error to nd:{port} cause of {error}.")
            messagebox.showerror('Node for professionals', f'Message sending faliure;\nfrom: {from_.title()}\ntarget: {NAMES[str(port)]}\nmore: {error}')

def recievers(data, port):
    head = json.loads(data)['head']
    if head.lower() == 'Everyone'.lower():
        try:
            temp = list(NAMES.keys())
            temp.remove(str(port))
            return temp
        except:
            return list(NAMES.keys())
    if head.title() in list(NAMES.values()):
        return [list(NAMES.keys())[list(NAMES.values()).index(head.title())]]
    else:
        return False

def scrapBody(data):
    body = json.loads(data)['body']
    return body

def threading_connection(connection, port):
    print(f'?> {NAMES[str(port)]} (nd:{port}) is threading now on the server.')
    while True:
        try:
            buf_size = int(connection.recv(4).decode())
            data = connection.recv(buf_size)
        except ConnectionResetError as err:
            break
        if not data:
            break
        sendMessage(scrapBody(data.decode('utf-8')), recievers(data.decode('utf-8'), port), from_=str(port))
    sendMessage(f'{NAMES[str(port)]} is just disconnected.', recievers(json.dumps({'head':'Everyone'}), port), position=1000)
    print(f"|> {NAMES[str(port)]} (nd:{port}) is disconnected by itself.")
    del NAMES[str(port)]
    sendMessage(NAMES, recievers(json.dumps({'head':'Everyone'}), None), position=1586)
    connection.close()

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((socket_sys.host, socket_sys.port))
SERVER.listen()
print(f'|> Server is actively listening on {socket_sys.host}:{socket_sys.port}')

CONNECTIONS = {}
NAMES = {}

while True:
    SERVER.listen()
    connection, addr = SERVER.accept()
    ip, port = connection.getpeername()
    CONNECTIONS[str(port)] = connection
    tempdata = str(list(NAMES.values())).encode()
    connection.send(tempdata)
    NAMES[str(port)] = connection.recv(1024).decode().title()
    connection.send(str(port).encode())
    sendMessage(NAMES, recievers(json.dumps({'head':'Everyone'}), None), position=1586)
    sendMessage(f'{NAMES[str(port)]} is just connected.', recievers(json.dumps({'head':'Everyone'}), None), position=1000)
    start_new_thread(threading_connection, (connection, port))