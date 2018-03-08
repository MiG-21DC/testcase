import requests
import json
import uuid

header = {'content-type':'application/json'}
player1 = {'id': str(uuid.uuid1), 'nickname': 'Jason', 'email': 'Jason@gmail.com'}
player2 = {'id': str(uuid.uuid1), 'nickname': 'Sushi', 'email': 'Random@outlook.com'}
r = requests.post('http://0.0.0.0:5000/player', data=json.dumps(player1), headers=header)
print(r.text)
r = requests.put('http://0.0.0.0:5000/player', data=json.dumps(player2), headers=header)
print(r.text)