import socket 
import uuid
import json

ip = 'localhost'
porta = 3333

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, porta)) 

client_id = str(uuid.uuid4())
print(f'client_id: {client_id}')

def send_data(route, payload):
    # d = { "payload": { "oloko": 2 }, "route": "/game/join", 'player_id': None }
    print(f'[{route}] {payload}')
    request_body = { "route": route, "payload": payload, "client_id": client_id }
    sock.send(json.dumps(request_body).encode())
    
    response = json.loads(sock.recv(4096).decode())
    
    if response['status'] == 'ERROR':
        message = response['message']
        print(f'[ERROR - {route}] {message}')
        raise Exception(message)

    payload = response['payload']
    print(f'[{route}] {payload}')
    return payload


def close_socket():
    sock.close()