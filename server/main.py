from Utils import user_servers, AppResponse
from uuid import uuid4
import xmlrpc.server
import Game as Game

PORT = 3333
IP = 'localhost'

client_ports_incremental = PORT + 1 

def get_next_port():
	global client_ports_incremental
	next_port = client_ports_incremental
	client_ports_incremental += 1
	return next_port

def register_connection(port):
	uuid = str(uuid4())
	servidor = xmlrpc.client.ServerProxy(("http://localhost:" + port), allow_none=True)
	user_servers[uuid] = servidor
	response = AppResponse(payload={ "client_id": uuid }).response
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

servidor = xmlrpc.server.SimpleXMLRPCServer(("localhost", PORT), allow_none=True)
for route, handler in router.items():
	servidor.register_function(handler, route)
servidor.serve_forever()	