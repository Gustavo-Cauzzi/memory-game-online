from inspect import signature
from Utils import user_servers, check_if_os_port_is_open, ok_response, server_emit_event, error_response, AppException, AppResponse
from time import sleep
from uuid import uuid4
import select
import socket 
import threading
import xmlrpc.server
import json
import Game as Game

PORT = 3333
IP = 'localhost'

client_ports_incremental = PORT + 1 

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind((IP, PORT)) 
# server_socket.listen(10)

# inputs = [server_socket]

def get_next_port():
	global client_ports_incremental
	print('sahuidashuiasdhbuidashui buias biuasbu dsaubi asbub u')
	next_port = client_ports_incremental
	client_ports_incremental += 1
	return next_port

def register_connection(port):
	print("odiaijosadjioadsoijasdoijadsijoiajdsjiadsjoi")
	uuid = str(uuid4())
	print("register_connection", uuid, str(port))
	servidor = xmlrpc.client.ServerProxy(("http://localhost:" + port), allow_none=True)
	print("connected")
	user_servers[uuid] = servidor
	print('user_servers: ', user_servers)
	print("a")
	response = AppResponse(payload={ "client_id": uuid }).response
	print("b")
	print(f'response: {response}')
	return response

def disconnect_client(client_id):
	user_servers.pop(client_id)

# --------------------------------
router = {
	"get_port": get_next_port,
	"connect": register_connection,
	"disconnect": disconnect_client,

	"game": Game.get_games_info,

	"game_create": Game.game_create,
	"game_join": Game.game_join,

	"game_card_turn": Game.game_card_turned,
}
# --------------------------------

# def handle_client(client_socket, address):
# 	def remove_socket():
# 		global inputs 
# 		print("-=-=-=- Socket closed -=-=-=-")
# 		inputs = list(filter(lambda s: not s is client_socket, inputs))

# 	try:
# 		raw_data = client_socket.recv(1024)
# 		if not raw_data:
# 			remove_socket()
# 			return
# 	except ConnectionResetError:
# 		remove_socket()
# 		return
        
# 	decoded_data = raw_data.decode()
# 	data = json.loads(decoded_data) # EX: { "payload": { "test": 2 }, "route": "/game/join", 'client_id': "uuid" }
# 	data['socket'] = client_socket

# 	route = data['route']
# 	print(f'[REQUEST {route}] {data["payload"] if "payload" in data else {}}')

# 	if route == 'STOP_APPLICATION':
# 		client_socket.close()
# 		server_socket.close()
# 		exit(0)

# 	if route in router:
# 		fun = router[data['route']]
# 		parameters_quantity = len(signature(fun).parameters)
# 		params = [data] if parameters_quantity == 1 else []
# 		try:
# 			appResponse = fun(*params)

# 			if not appResponse:
# 				return

# 			data['socket'].send(ok_response(data['route'], appResponse.payload))

# 			if appResponse.server_emit_route:
# 				for idx, route in enumerate(appResponse.server_emit_route):
# 					server_emit(data['client_id'], route, appResponse.server_emit_payload[idx], appResponse.to)
# 		except AppException as error:
# 			print(f'[ERROR {data["route"]}] {error}')
# 			data['socket'].send(error_response(data['route'], str(error)))

		# sleep(0.2)
		# def try_communication(tries = 0):
		# 	try:
		# 		if tries < 5:
		# 			client_server.send(server_emit_event(route, payload))
		# 		else:
		# 			clients_to_remove.append(client_id)
		# 	except:
		# 		try_communication(tries + 1)
		# try_communication()

# 	for client_id_to_remove in clients_to_remove:
# 		print(f'{client_id_to_remove} parece ter desconectado (número de tentativas de comunicação máxima excedida)')
# 		user_servers.pop(client_id_to_remove)



# while True:
# 	readable, writable, exceptional = select.select(inputs, [], [], 1)
# 	for sock in readable:
# 		if sock is server_socket:
# 			client_socket, client_address = sock.accept()
# 			client_socket.setblocking(1)
# 			inputs.append(client_socket)
# 			threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
# 		else:
# 			threading.Thread(target=handle_client, args=(sock, None)).start()

# def server_emmiter_middleware(handler, *payload):
# 	response = handler(*payload)
# 	if not isinstance(response, AppResponse) or not response.server_emit_route:
# 		return response

# 	if response.server_emit_route:
# 		for idx, route in enumerate(response.server_emit_route):
# 			server_emit(payload['client_id'], route, response.server_emit_payload[idx], response.to)
# 	return response

# def a(handler):
	# return lambda *payload: server_emmiter_middleware(handler, *payload)

servidor = xmlrpc.server.SimpleXMLRPCServer(("localhost", PORT), allow_none=True)
for route, handler in router.items():
	servidor.register_function(handler, route)
servidor.serve_forever()	