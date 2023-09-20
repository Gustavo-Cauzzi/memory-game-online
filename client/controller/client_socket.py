from time import sleep
import socket 
import uuid
import json
from queue import Queue
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
    print("Routes aa: ", routes)

def listen():
    while True:
        raw_data = client_socket.recv(4096).decode()
        if not raw_data:
            print("Resposta vazia - Socket fechado")
            return

        data = json.loads(raw_data)
        
        if not 'server_event' in data:
            responses_queue.put(data)
            
        print('routes: ', routes)
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
    
    # response = json.loads(client_socket.recv(4096).decode())
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

    payload = response['payload']
    print(f'[RESPONSE {route}] {payload}')
    return payload

client_id = send_data('CONNECT')['client_id']
print(f'client_id: {client_id}')

def close_socket():
    client_socket.close()
