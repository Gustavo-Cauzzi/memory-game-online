import json

def ok_response (route, payload = {}):
	return json.dumps({ "status": "OK", "route": route, "payload": payload }).encode()

def error_response (route, message = ''):
	return json.dumps({ "status": "ERROR", "route": route, "message": message }).encode()

def server_emit_event (route, payload = {}):
	return json.dumps({ "status": "OK", "route": route, "payload": payload, "server_event": True }).encode()

def find(fun, arr):
	return next(filter(fun, arr), None)

class AppException(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)

class AppResponse():
	def __init__(self, server_emit_route=None, server_emit_payload=None, payload={}, to=None):
		if server_emit_route and server_emit_payload:
			multiple_routes = isinstance(server_emit_route, list)
			self.server_emit_route = [server_emit_route] if not multiple_routes else server_emit_route
			self.server_emit_payload = [server_emit_payload] if not multiple_routes else server_emit_payload
		else:
			self.server_emit_route = None
			self.server_emit_payload = None
		self.payload = payload
		self.to = None if not to else to if isinstance(to, list) else [to]
	
	def __str__(self):
		return f'server_emit_route={self.server_emit_route}, server_emit_payload={self.server_emit_payload}, payload={self.payload}'
