from time import sleep
import socket 
import json

def ok_response (route, payload = {}):
	return json.dumps({ "status": "OK", "route": route, "payload": payload }).encode()

def error_response (route, message = ''):
	return json.dumps({ "status": "ERROR", "route": route, "message": message }).encode()

def server_emit_event (route, payload = {}):
	return json.dumps({ "status": "OK", "route": route, "payload": payload, "server_event": True }).encode()

def find(fun, arr):
	return next(filter(fun, arr), None)

def check_if_os_port_is_open(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex(('127.0.0.1', port))
	sock.close()
	return result == 0

class AppException(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

class AppResponse():
	def __init__(self, connection_data=None, server_emit_route=None, server_emit_payload=None, payload={}, to=None):
		print("1")
		if server_emit_route and server_emit_payload:
			multiple_routes = isinstance(server_emit_route, list)
			self.server_emit_route = [server_emit_route] if not multiple_routes else server_emit_route
			self.server_emit_payload = [server_emit_payload] if not multiple_routes else server_emit_payload
		else:
			self.server_emit_route = None
			self.server_emit_payload = None
		self.payload = payload
		self.to = None if not to else to if isinstance(to, list) else [to]

		self.client_id = None if not connection_data else connection_data['client_id']

		self.response = ok_response('UNKNOWN' if not connection_data else connection_data['route'], payload)
		print(f'connection_data: {connection_data}')
		print(f'123')

		self.emit_if_necessary()
		print(f'1234')
	
	def emit_if_necessary(self):
		print(f'self.server_emit_route: {self.server_emit_route}')
		if self.server_emit_route:
			for idx, route in enumerate(self.server_emit_route):
				print(f'route: {route}')
				server_emit(self.client_id, route, self.server_emit_payload[idx], self.to)

	def __str__(self):
		return f'server_emit_route={self.server_emit_route}, server_emit_payload={self.server_emit_payload}, payload={self.payload}'


user_servers = {}
def server_emit(origin_client_id, route, payload, specific_targets_ids=None):
	print(f'[SERVER EMIT {route}](from: {origin_client_id}) {payload}')
	clients_to_remove = []

	print(f'user_servers: {user_servers}')

	# Send everybody but the one who's sending if not specified to whom
	targets_ids = [(c_id, user_servers[c_id]) for c_id in specific_targets_ids] if specific_targets_ids else user_servers.items() 
	print(f'targets_ids: {targets_ids}')

	for client_id, client_server in targets_ids:
		print(f'client_id: {client_id}')
		if client_id == origin_client_id:
			continue

		sleep(0.2)
		def try_communication(tries = 0):
			try:
				if tries < 5:
					client_server.server_event(server_emit_event(route, payload))
				else:
					clients_to_remove.append(client_id)
			except Exception as e:
				print(e)
				try_communication(tries + 1)
		try_communication()

		try:
			client_server.server_event(server_emit_event(route, payload))
		except Exception as e:
			print(e)
			clients_to_remove.append(client_id)

	for client_id_to_remove in clients_to_remove:
		print(f'{client_id_to_remove} parece ter desconectado (número de tentativas de comunicação máxima excedida)')
		user_servers.pop(client_id_to_remove)
