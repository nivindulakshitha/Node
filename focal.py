from tkinter import BOTTOM, END, ttk
from ttkthemes import ThemedTk
from tkinter import Label, Frame
from PIL import ImageTk, Image
import CLIENT_NODE
import socket_sys
END = False

COLORS = {
    'black-0': '#ffffff',
    'black-0.75': '#cccccc',
    'black-0.5': '#888888',
    'black-0.25': '#444444',
    'black-1.0': '#000000'
}

FONTS = {
    'headding': 'arial 12',
    'normal': 'tahoma 12',
    'mini': 'tahoma 10',
    'smaller': 'tahoma 8'
}

def joinAServer(port):
    global root, END
    try:
        root.withdraw()
        CLIENT_NODE.connectTo(port)
        END = True
    except:
        connectionErrorLabel.config(text='No connection could be made', foreground='#DA4167')
        clientNodeEntry.delete(0, END)
        root.deiconify()
        clientNodeEntry.focus()

def beAServer():
    global root
    root.withdraw()
    import SERVER_NODE

root = ThemedTk(theme='breeze')
LOGO = ImageTk.PhotoImage(Image.open("Media/Node logo.png"))
STYLE = ttk.Style()
root.resizable(False, False)
root.iconbitmap('Media/icon.ico')
root.title('Node For Professionals')
root.geometry(f'400x450+{int((root.winfo_screenwidth()/2)-200)}+{int((root.winfo_screenheight()/2)-225)}')
root.config(bg=COLORS['black-0'])

Label(root, image=LOGO, background=COLORS['black-0']).pack(pady=20)

clientNodeEntry = ttk.Entry(root, width=30, font=FONTS['mini'])
clientNodeEntry.pack(pady=(50, 0))
clientNodeEntry.focus()
connectionErrorLabel = Label(root, text='Insert target port and hit Enter (ex: 00000)', background=COLORS['black-0'], foreground='#2d8cff', font=FONTS['smaller'])
connectionErrorLabel.pack(pady=(0, 15))

STYLE.configure('TButton', font=FONTS['mini'])
ttk.Button(root, text="Join the node", command=lambda: joinAServer(port=clientNodeEntry.get())).pack()

separator = Frame(root, bg=COLORS['black-0.75'], height=1, bd=0)
separator.pack(fill="x", padx=20, pady=25)

STYLE.configure('TLabel', background=COLORS['black-0'])
serverNodeLabel = ttk.Label(root, text=f'Node name : {socket_sys.name}\nListening on: {socket_sys.host}:{socket_sys.port}', font=FONTS['mini'])
serverNodeLabel.pack()
ttk.Button(root, text="Be a server", command=beAServer).pack(pady=15)

Label(root, text='Version: 1.1.0 (2022)', foreground=COLORS['black-0.5'], background=COLORS['black-0'], font=(FONTS['mini'])).pack(side=BOTTOM , pady=10)

root.bind('<Return>', lambda event: joinAServer(port=clientNodeEntry.get()))

while not(END):
    root.update()
else:
    root.destroy()
