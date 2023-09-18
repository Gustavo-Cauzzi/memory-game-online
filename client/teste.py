import socket 
import json
import sys

ip = 'localhost'
porta = 3333

soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soquete.connect((ip, porta)) 

d = { "payload": { "oloko": 2 }, "route": "/game/join", 'player_id': None }
j = json.dumps(d)

soquete.send(j.encode())
dados = soquete.recv(1024).decode()
soquete.close()

print('Recebi: %s' % dados)

