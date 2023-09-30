from inspect import signature
from Utils import ok_response, server_emit_event, error_response, AppException, AppResponse
from time import sleep
from uuid import uuid4
import select
import socket 
import threading
import json
import Game as Game

PORT = 3333
IP = 'localhost'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT)) 
server_socket.listen(10)

inputs = [server_socket]
user_sockets = {}

def register_connection(socket_data):
	uuid = str(uuid4())
	user_sockets[uuid] = socket_data['socket']
	print('user_sockets: ', user_sockets)
	return AppResponse(payload={ "client_id": uuid })

# --------------------------------
router = {
	"CONNECT": register_connection,

	"/game": Game.get_games_info,

	"/game/create": Game.game_create,
	"/game/join": Game.game_join,

	"/game/card/turn": Game.game_card_turned,
}
# --------------------------------

def handle_client(client_socket, address):
	def remove_socket():
		global inputs 
		print("-=-=-=- Socket closed -=-=-=-")
		inputs = list(filter(lambda s: not s is client_socket, inputs))

	try:
		raw_data = client_socket.recv(1024)
		if not raw_data:
			remove_socket()
			return
	except ConnectionResetError:
		remove_socket()
		return
        
	decoded_data = raw_data.decode()
	data = json.loads(decoded_data) # EX: { "payload": { "test": 2 }, "route": "/game/join", 'client_id': "uuid" }
	data['socket'] = client_socket

	route = data['route']
	print(f'[REQUEST {route}] {data["payload"] if "payload" in data else {}}')

	if route == 'STOP_APPLICATION':
		client_socket.close()
		server_socket.close()
		exit(0)

	if route in router:
		fun = router[data['route']]
		parameters_quantity = len(signature(fun).parameters)
		params = [data] if parameters_quantity == 1 else []
		try:
			appResponse = fun(*params)

			if not appResponse:
				return

			data['socket'].send(ok_response(data['route'], appResponse.payload))

			if appResponse.server_emit_route:
				for idx, route in enumerate(appResponse.server_emit_route):
					server_emit(data['client_id'], route, appResponse.server_emit_payload[idx], appResponse.to)
		except AppException as error:
			print(f'[ERROR {data["route"]}] {error}')
			data['socket'].send(error_response(data['route'], str(error)))

def server_emit(origin_client_id, route, payload, specific_targets_ids=None):
	print(f'[SERVER EMIT {route}](from: {origin_client_id}) {payload}')
	clients_to_remove = []

	# Send everybody but the one who's sending if not specified to whom
	targets_ids = [(c_id, user_sockets[c_id]) for c_id in specific_targets_ids] if specific_targets_ids else user_sockets.items() 
	
	for client_id, socket in targets_ids:
		if client_id == origin_client_id:
			continue

		sleep(0.2)
		def try_communication(tries = 0):
			try:
				if tries < 5:
					socket.send(server_emit_event(route, payload))
				else:
					clients_to_remove.append(client_id)
			except:
				try_communication(tries + 1)
		try_communication()

	for client_id_to_remove in clients_to_remove:
		print(f'{client_id_to_remove} parece ter desconectado (número de tentativas de comunicação máxima excedida)')
		user_sockets.pop(client_id_to_remove)



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
        


