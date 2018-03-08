import requests
import json
import uuid

print('Test 1: Add 3 players in player table')
header = {'content-type':'application/json'}
player1_uuid = str(uuid.uuid1())
player1 = {'id': player1_uuid, 'nickname': 'Jason', 'email': 'Jason@gmail.com'}
player2 = {'id': str(uuid.uuid1()), 'nickname': 'Sushi', 'email': 'Random@outlook.com'}
player3 = {'id': str(uuid.uuid1()), 'nickname': 'Vincent', 'email': 'ABCDE@hotmail.com', 'skill_point': 50}
r = requests.post('http://0.0.0.0:5000/player', data=json.dumps(player1), headers=header)
print(r.text)
r = requests.put('http://0.0.0.0:5000/player', data=json.dumps(player2), headers=header)
print(r.text)
r = requests.put('http://0.0.0.0:5000/player', data=json.dumps(player3), headers=header)
print(r.text)

print('Test 2: Get 1 player info from player table')
r = requests.get('http://0.0.0.0:5000/player/%s' % player1_uuid, headers=header)
print(r.text)

