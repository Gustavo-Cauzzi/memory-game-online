from queue import Queue
from time import sleep
import socket 
import xmlrpc.server
import json
import threading

routes = {}
def on(route, callback):
    routes[route] = callback

def server_event(payload):
    print(f"[SERVER EMITION] {payload} {type(payload)} {isinstance(payload, xmlrpc.client.Binary)}")
    if isinstance(payload, xmlrpc.client.Binary):
        payload = json.loads(payload.data.decode('ascii'))
    routes[payload['route']](payload['payload'])   

ip = 'localhost'
porta = 3333

print("Estabelecendo conexão...")
main_server = xmlrpc.client.ServerProxy(("http://localhost:" + str(porta)))
client_port = main_server.get_port()
client_server = xmlrpc.server.SimpleXMLRPCServer(("localhost", client_port), allow_none=True)

print('Iniciando servidor interno na porta ' + str(client_port))
client_server.register_function(server_event, 'server_event')
threading.Thread(target=client_server.serve_forever).start()

connection_response = json.loads(main_server.connect(str(client_port)).data.decode('ascii'))
client_id = connection_response['payload']['client_id']
print("ID do cliente definido como " + client_id)

'''
Exemplo de comunicação entre os sockets
{ 
    "payload": { "game_id": 2 }, 
    "route": "/game/join", 
    'player_id': 'uuid' 
}
'''
def send_data(route, payload = {}):
    print(f'[REQUEST {route}] {payload}')
    request_body = { "route": route, "payload": payload, "client_id": client_id }
    # client_socket.send(json.dumps(request_body).encode())
    func = None
    try:
        func = getattr(main_server, route)
    except:
        print(f"Chamada {route} não encontrada no servidor")

    raw_response = func(request_body)
    response = json.loads(raw_response.data.decode('ascii'))

    print(f'response: {response}')
    
    if response['status'] == 'ERROR':
        message = response['message']
        print(f'[ERROR - {route}] {message}')
        raise Exception(message)

    print(f'[RESPONSE {route}] {response["payload"]}')
    return response['payload']

def close_connection():
    main_server.disconnect(client_id)
