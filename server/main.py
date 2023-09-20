from inspect import signature
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
	"/game": Game.get_games_info,

	"/game/create": Game.game_create,
	"/game/join": Game.game_join,
}
# --------------------------------
			
inputs = [server_socket]

def handle_client(client_socket, address):
	global inputs
	raw_data = client_socket.recv(1024)
	
	if not raw_data:
		print("Socket closed ------------------------")
		inputs = list(filter(lambda s: not s is client_socket, inputs))
		return

	decoded_data = raw_data.decode()
	data = json.loads(decoded_data) # { "payload": { "test": 2 }, "route": "/game/join", 'client_id': "uuid" }
	data['socket'] = client_socket

	route = data['route']
	print(f'[{route}] {data}')

	if route == 'STOP_APPLICATION':
		client.close()
		server_socket.close()
		exit(0)

	if route in router:
		fun = router[data['route']]
		parameters_quantity = len(signature(fun).parameters)
		params = [data] if parameters_quantity == 1 else []
		print(params, route, fun)
		fun(*params)

print(server_socket)

while True:
	readable, writable, exceptional = select.select(inputs, [], [], 1)
	for sock in readable:
		if sock is server_socket:
			client_socket, client_address = sock.accept()
			client_socket.setblocking(1)
			inputs.append(client_socket)
			threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
		else:
			threading.Thread(target=handle_client, args=(sock, None)).start()
        


