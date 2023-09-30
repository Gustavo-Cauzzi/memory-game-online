from queue import Queue
from time import sleep
import socket 
import json
import threading

ip = 'localhost'
porta = 3333

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip, porta)) 

client_id = None

responses_queue = Queue()

routes = {}
def on(route, callback):
    routes[route] = callback

def listen():
    while True:
        raw_data = client_socket.recv(16384).decode()
        if not raw_data:
            print("Resposta vazia - Socket fechado")
            exit(0)

        data = json.loads(raw_data)
        
        if not 'server_event' in data:
            responses_queue.put(data)
            
        print(f'[SERVER {data["route"]}] {data["payload"]}')
        if data['route'] in routes:
            routes[data['route']](data['payload'])

threading.Thread(target=listen).start()

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
    client_socket.send(json.dumps(request_body).encode())
    
    response = None
    while True:
        sleep(0.2)
        pending_response = responses_queue.get()
        if pending_response:
            response = pending_response
            break
    
    if response['status'] == 'ERROR':
        message = response['message']
        print(f'[ERROR - {route}] {message}')
        raise Exception(message)

    print(f'[RESPONSE {route}] {response["payload"]}')
    return response['payload']

client_id = send_data('CONNECT')['client_id']
print(f'client_id: {client_id}')

def close_socket():
    client_socket.close()
