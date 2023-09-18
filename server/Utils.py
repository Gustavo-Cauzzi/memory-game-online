import json

def ok_response (payload = {}):
	return json.dumps({ "status": "OK", "payload": payload }).encode()

def error_response (message = ''):
	return json.dumps({ "status": "ERROR", "message": message }).encode()