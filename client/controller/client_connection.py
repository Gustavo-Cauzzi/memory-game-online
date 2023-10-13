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
    print("Ha", payload, type(payload))
    print(f"Routessss {routes}, {payload['route']}")
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

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect((ip, porta)) 

# client_id = None

# responses_queue = Queue() 

# def listen():
#     while True:
#         raw_data = client_socket.recv(16384).decode()
#         if not raw_data:
#             print("Resposta vazia - Socket fechado")
#             exit(0)

#         data = json.loads(raw_data)
        
#         if not 'server_event' in data:
#             responses_queue.put(data)
            
#         print(f'[SERVER {data["route"]}] {data["payload"]}')
#         if data['route'] in routes:
#             routes[data['route']](data['payload'])

# threading.Thread(target=listen).start()

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

    # response = None
    # while not response:
    #     sleep(0.2)
    #     pending_response = responses_queue.get()
    #     if pending_response:
    #         response = pending_response
    
    if response['status'] == 'ERROR':
        message = response['message']
        print(f'[ERROR - {route}] {message}')
        raise Exception(message)

    print(f'[RESPONSE {route}] {response["payload"]}')
    return response['payload']

# client_id = send_data('CONNECT')['client_id']
# print(f'client_id: {client_id}')

def close_connection():
    main_server.disconnect(client_id)
