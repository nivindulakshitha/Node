import socket, random

name = 'THISPC-40DK751'
host = socket.gethostbyname(socket.gethostname())
port = random.randint(10000, 65534)