import select
import socket 
import threading
import json
import Game

PORT = 3333
IP = 'localhost'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT)) 
server_socket.listen(10)

# --------------------------------
router = {
	"/game/create": Game.game_create,
	"/game/join": Game.game_join,
}
# --------------------------------
			
inputs = [server_socket]

def handle_client(client_socket, address):
	raw_data = client_socket.recv(1024).decode()
	data = json.loads(raw_data) # { "payload": { "test": 2 }, "route": "/game/join", 'client_id': "uuid" }
	data['socket'] = client_socket

	route = data['route']
	print(f'[{route}] {data}')

	if route == 'STOP_APPLICATION':
		client.close()
		server_socket.close()
		exit(0)

	if route in router:
		router[data['route']](data)

while True:
	readable, writable, exceptional = select.select(inputs, [], inputs, 1)
	for s in readable:
		if s is server_socket:
			connection, client_address = s.accept()
			connection.setblocking(1)
			print(f'{client_address} conectado')
			inputs.append(connection)
			threading.Thread(target=handle_client, args=(connection, client_address)).start()


