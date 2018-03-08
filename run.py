import requests
import json
import uuid

print('Test 1: Add 3 players in player table')
header = {'content-type':'application/json'}
player1 = {'id': str(uuid.uuid1()), 'nickname': 'Jason', 'email': 'Jason@gmail.com'}
player2 = {'id': str(uuid.uuid1()), 'nickname': 'Sushi', 'email': 'Random@outlook.com'}
player3 = {'id': str(uuid.uuid1()), 'nickname': 'Vincent', 'email': 'ABCDE@hotmail.com', 'skill_point': 50}
r = requests.post('http://0.0.0.0:5000/player', data=json.dumps(player1), headers=header)
print(r.text)
r = requests.put('http://0.0.0.0:5000/player', data=json.dumps(player2), headers=header)
print(r.text)
r = requests.put('http://0.0.0.0:5000/player', data=json.dumps(player3), headers=header)
print(r.text)