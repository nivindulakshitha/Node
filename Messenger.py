from tkinter import  FLAT, LEFT, N, NW, RIGHT, WORD, Canvas,Frame, LabelFrame, StringVar, Text, ttk, BOTH
from ttkthemes import ThemedTk
from datetime import datetime
import json

COLORS = {
    'black-0': '#ffffff',
    'black-0.75': '#cccccc',
    'black-0.5': '#888888',
    'black-0.25': '#444444',
    'black-1.0': '#000000',
    'Node-blue': '#2D8CFF',
    'Node-blue-light': '#A9CCFB',
    'node-red': '#D72638'
}

FONTS = {
    'headding': 'arial 12',
    'normal': 'tahoma 12',
    'mini': 'tahoma 10',
    'smaller': 'tahoma 8'
}

LINE = 1
thisNode = ''
recievers = ['Everyone']
msgbox_widget = []

def TxMessages(Rxes, message):
    global thisNode
    if len(message.strip()) > 0:
        data = json.dumps({'head':str(Rxes),'body': message.strip(), 'from':thisNode.getpeername()[1]}).encode('utf-8')
        thisNode.send(str(len(data)).zfill(4).encode())
        thisNode.send(data)
        RxMessages(json.dumps({'message':message.strip(), 'from':'SELF', 'to':str(Rxes), 'timestamp':datetime.now().strftime("%H:%M:%S")}))
    textarea.delete('1.0', 'end')
    textarea.delete('1.0', 'end')

def createMsgboxEntry(content, tag=''):
    template = {
        'content': content+'\n',
        'tag': tag
    }
    return template

def RxMessages(data):
    global recievers, msgbox_widget
    data = json.loads(data)
    
    if data['from'] == 'SERVER':
        if data['pos'] == 1586:
            ip, port = thisNode.getsockname()
            try:
                del data['message'][str(port)]
                recievers = list(data['message'].values())
                recievers.insert(0, 'Everyone')
            except:
                recievers = list(data['message'].values())
                recievers.insert(0, 'Everyone')
        elif data['pos'] == 1000:
            msgbox_widget.append(createMsgboxEntry(f"[Server@{data['timestamp']}] to Everyone", 'server-message'))
            msgbox_widget.append(createMsgboxEntry(data['message'], 'server-message'))
            msgbox_widget.append(createMsgboxEntry('\n', ''))
    elif data['from'] == 'SELF':
        msgbox_widget.append(createMsgboxEntry(f"[Me@{data['timestamp']}] to {data['to'].title()}", 'timestamp-note'))
        msgbox_widget.append(createMsgboxEntry(data['message'], 'self-message'))
        msgbox_widget.append(createMsgboxEntry('\n', ''))
    else:
        msgbox_widget.append(createMsgboxEntry(f"[{data['from']}@{data['timestamp']}]", 'timestamp-note'))
        msgbox_widget.append(createMsgboxEntry(data['message'], 'client-message'))
        msgbox_widget.append(createMsgboxEntry('\n', ''))

def setTags(box):
    box.tag_configure('server-message', foreground=COLORS['node-red'], font=FONTS['smaller'])
    box.tag_configure('timestamp-note', foreground=COLORS['black-0.5'], font=FONTS['smaller'])
    box.tag_configure('client-message', foreground=COLORS['black-0.25'], font=FONTS['mini'])
    box.tag_configure('self-message', foreground=COLORS['Node-blue'])

def start(port='Err', name='', node=''):
    global msgbox_widget, thisNode, textarea, LINE
    thisNode = node
    root = ThemedTk(theme='breeze')
    STYLE = ttk.Style()
    root.resizable(False, False)
    root.iconbitmap('Media/Asset-1_0.5x.ico')
    root.title(f'Node For Professionals [{port}] [{name}]')
    root.geometry(f'400x450+{int((root.winfo_screenwidth()/2)-200)}+{int((root.winfo_screenheight()/2)-225)}')
    root.config(bg=COLORS['black-0'])
    root.focus()

    entryBox = LabelFrame(root, background=COLORS['black-0'], bd=0, border=0)
    wrapper = LabelFrame(root, background=COLORS['black-0'], bd=1, border=1, width=400, height=335, borderwidth=1, highlightthickness=1, highlightbackground='#3daee9', relief=FLAT)

    canvas = Canvas(wrapper, background=COLORS['black-0'], bd=0, highlightthickness=0, relief=FLAT, height=335)
    canvas.pack(side=LEFT, fill=BOTH)

    bbox = Frame(canvas, background=COLORS['black-0'])
    canvas.create_window((0, 0), window=bbox, anchor=NW)
    messageBox = Text(bbox, height=20, width=50, bd=0, relief=FLAT, background=COLORS['black-0'], font=FONTS['mini'], wrap=WORD, state='disabled', cursor='arrow')
    messageBox.pack(ipadx=5, padx=2, ipady=10)
    setTags(messageBox)

    STYLE.configure('TScrollbar', background=COLORS['black-0'])
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=messageBox.yview)
    scrollbar.place(x=380, y=2, height=352)
    messageBox.configure(yscrollcommand=scrollbar.set)

    wrapper.pack(padx=(10, 20), pady=5, ipadx=2, ipady=4)
    entryBox.pack(fill=BOTH, expand=True, padx=10, pady=(5, 10), ipadx=2, ipady=2)

    canvas2 = Canvas(entryBox, background=COLORS['black-0'], height=3, bd=0, highlightthickness=0, relief=FLAT)
    canvas2.pack(side=LEFT, fill=BOTH)

    bbox2 = Frame(canvas2, background=COLORS['black-0'], pady=2, padx=2)
    canvas2.create_window((0, 0), window=bbox2, anchor=NW)

    selected_endpoint = StringVar()
    Rxes = ttk.Combobox(bbox2, textvariable=selected_endpoint, height=5, width=12, background=COLORS['black-0'], font=FONTS['mini'], state='readonly')
    Rxes['values'] = recievers
    Rxes.set('Everyone')
    Rxes.pack(side=RIGHT, anchor=N, padx=(5, 0), expand=True)
    root.option_add("*TCombobox*Listbox*Background", COLORS['black-0'])
    root.option_add("*Vertical.TScrollbar*Background", COLORS['black-0'])
    root.option_add("*TCombobox*Listbox*Font", FONTS['mini'])

    textarea = Text(bbox2, font=FONTS['mini'], width=36, bd=1, height=4, highlightthickness=1, background=COLORS['black-0'], relief=FLAT)
    textarea.pack(side=LEFT, ipady=3)
    textarea.focus_force()
    textarea.bind('<Shift_R><Return>', lambda event: TxMessages(Rxes.get(), textarea.get('1.0', 'end-1c')[:5000]))
    textarea.bind('<Shift_L><Return>', lambda event: TxMessages(Rxes.get(), textarea.get('1.0', 'end-1c')[:5000]))

    ttk.Button(bbox2, text="Send", width=12, command=lambda: TxMessages(Rxes.get(), textarea.get("1.0","end-1c")[:5000])).place(x=263, y=45)

    while True:
        Rxes['values'] = recievers
        if len(msgbox_widget) > 0:
            messageBox.config(state='normal')
            messageBox.insert(str(float(LINE)), msgbox_widget[0]['content'])
            messageBox.see("end")
            tag = msgbox_widget[0]['tag']
            if len(tag) != 0:
                messageBox.tag_add(tag, str(float(LINE)), str(float(LINE)+1)+"-1c")
            LINE += len(msgbox_widget[0]['content'].split('\n'))-1
            messageBox.config(state='disabled')
            msgbox_widget.pop(0)

        root.update()