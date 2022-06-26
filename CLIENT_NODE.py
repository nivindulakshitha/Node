import socket, socket_sys
from tkinter import Label, ttk
from _thread import start_new_thread
from ttkthemes import ThemedTk
from tkinter import messagebox
client_socket = CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVERNODE = ''

def receiveMessages():
    while True:
        try:
            buf_size = CLIENT.recv(4).decode()
            data = CLIENT.recv(int(buf_size)).decode()
            from Messenger import RxMessages
            RxMessages(data)
        except ConnectionResetError as error:
            print(f'Server did not respond more:{error}')
            messagebox.showerror('Node for professionals', f'Server respond faliure (302);\nbuffer: {buf_size}\nmore: {error}')
            break
        except Exception as error:
            print(f'Something cause happened more:{error}')
            messagebox.showerror('Node for professionals', f'Server respond faliure (294);\nbuffer: {buf_size}\nmore: {error}')
            break

def filterPort(port):
    if ':' in port:
        return port.replace(':', '').strip()
    return port.strip()

def connectTo(port):
    global client_socket
    global SERVERNODE
    SERVERNODE = filterPort(port)
    try:
        CLIENT.connect((f'{socket.gethostbyname(socket_sys.host)}', int(SERVERNODE)))
        inUsing = CLIENT.recv(1024).decode()
        name = askNickName(inUsing)
        CLIENT.send(str(name).encode())
        port = CLIENT.recv(5).decode()
        start_new_thread(receiveMessages, ())
        from Messenger import start
        start(port, name, client_socket)
    except Exception as Error:
        print(Error)
        return
    

def askNickName(inUsing):
    global name
    name = ''
    popup = ThemedTk(theme='breeze')
    popup.title('')
    popup.iconbitmap('Media/Asset-1_0.5x.ico')
    popup.resizable(False, False)
    popup.configure(background='#FFFFFF')
    popup.focus()
    Label(popup, text='Pick up a nick name for you', background='#FFFFFF').pack(padx=5, pady=(10, 5))
    nameEntry = ttk.Entry(popup, width=20)
    nameEntry.pack(padx=5)
    nameEntry.focus_force()
    ttk.Button(popup, text='Proceed', command=lambda: proceed(nick=nameEntry.get())).pack(padx=5, pady=(5, 10))
    popup.bind('<Return>', lambda event: proceed(nick=nameEntry.get()))
    def proceed(nick):
        global name
        nick = nick.strip()
        if (checkAvailability(nick.strip()) and len(nick.split(' '))):
            if (len(nick) > 15):
                name = nick[:15].title()+'...'
            else:
                name = nick.title()
        else:
            return
    
    def checkAvailability(nick):
        if len(nick.strip()) == 0:
            messagebox.showerror("Node for professionals", "Place your nickname in the input box to proceed forward.")
            return False
        else:
            if len(nick) > 15:
                messagebox.showwarning("Node for professionals", "Your nickname must be organized in less than or equal to 15 characters.")
                return False
            elif len(nick) <= 3:
                messagebox.showwarning("Node for professionals", "Suggest nickname too short than required, use a different one.")
                return False
            elif not(nick.isalnum()):
                messagebox.showwarning("Node for professionals", "It seems like your name has a specific character (s). Only allowed A-Z and 0-9.")
                return False
            elif nick.strip().isnumeric():
                messagebox.showwarning("Node for professionals", "Only numbers can't be accepted. Use A-Z and 0-9 together.")
                return False
            elif nick.strip().title() in inUsing:
                messagebox.showwarning("Node for professionals", "This nickname is already in use. The nicknames should be unique to identify each other.")
                return False
            else:
                return True

    while True:
        if (name != ''):
            popup.destroy()
            break
        popup.update()
    return name