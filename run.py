import requests
import json
import uuid

print('Test 1: Add 3 players in player table')
header = {'content-type':'application/json'}
player1_uuid = str(uuid.uuid1())
player2_uuid = str(uuid.uuid1())
player3_uuid = str(uuid.uuid1())
player1 = {'id': player1_uuid, 'nickname': 'Jason', 'email': 'Jason@gmail.com'}
player2 = {'id': player2_uuid, 'nickname': 'Sushi', 'email': 'Random@outlook.com'}
player3 = {'id': player3_uuid, 'nickname': 'Vincent', 'email': 'ABCDE@hotmail.com', 'skill_point': 50}
r = requests.post('http://0.0.0.0:5000/player', data=json.dumps(player1), headers=header)
print(r.text)
r = requests.put('http://0.0.0.0:5000/player', data=json.dumps(player2), headers=header)
print(r.text)
r = requests.put('http://0.0.0.0:5000/player', data=json.dumps(player3), headers=header)
print(r.text)
input("Press Enter to continue...")

print('Test 2: Get 1 player info from player table')
r = requests.get('http://0.0.0.0:5000/player/%s' % player1_uuid, headers=header)
print(r.text)
input("Press Enter to continue...")

print('Test 3: Add 50 skill point to player 1')
update_info = {'id': player1_uuid, 'skill_point': 50}
r = requests.put('http://0.0.0.0:5000/player', data=json.dumps(update_info), headers=header)
print(r.text)
r = requests.get('http://0.0.0.0:5000/player/%s' % player1_uuid, headers=header)
print(r.text)
input("Press Enter to continue...")

print('Test 4: Delete 1 player info from player table')
r = requests.delete('http://0.0.0.0:5000/player/%s' % player1_uuid, headers=header)
print(r.text)
input("Press Enter to continue...")

print('Test 5: Add 2 guilds')
guild1_uuid = str(uuid.uuid1())
guild2_uuid = str(uuid.uuid1())
guild1 = {'id': guild1_uuid, 'name': 'Pink'}
guild2 = {'id': guild2_uuid, 'name': 'Floyd', 'country_code': '01'}
r = requests.post('http://0.0.0.0:5000/guild', data=json.dumps(guild1), headers=header)
print(r.text)
r = requests.put('http://0.0.0.0:5000/guild', data=json.dumps(guild2), headers=header)
print(r.text)
input("Press Enter to continue...")

print('Test 6: Get 1 guild info')
r = requests.get('http://0.0.0.0:5000/guild/%s' % guild1_uuid, headers=header)
print(r.text)
input("Press Enter to continue...")

print('Test 7: Add 99 country code to guild 1')
update_info = {'id': guild1_uuid, 'country_code': 99}
r = requests.put('http://0.0.0.0:5000/guild', data=json.dumps(update_info), headers=header)
print(r.text)
r = requests.get('http://0.0.0.0:5000/guild/%s' % guild1_uuid, headers=header)
print(r.text)
input("Press Enter to continue...")

print('Test 8: Delete 1 guild')
r = requests.delete('http://0.0.0.0:5000/guild/%s' % guild1_uuid, headers=header)
print(r.text)
input("Press Enter to continue...")

print('Test 9: Add two players to the guild')
player3_guild = {'player_id': player3_uuid, 'guild_id': guild2_uuid}
player2_guild = {'player_id': player2_uuid, 'guild_id': guild2_uuid}
r = requests.post('http://0.0.0.0:5000/playerguild', data=json.dumps(player3_guild), headers=header)
print(r.text)
r = requests.post('http://0.0.0.0:5000/playerguild', data=json.dumps(player2_guild), headers=header)
input("Press Enter to continue...")

print('Test 10: Delete 1 players from the guild')
player3_guild = {'player_id': player3_uuid, 'guild_id': guild2_uuid}
r = requests.delete('http://0.0.0.0:5000/playerguild', data=json.dumps(player3_guild), headers=header)
print(r.text)
input("Press Enter to continue...")

print('Test 11: Add 3 items in item table')
item1_uuid = str(uuid.uuid1())
item2_uuid = str(uuid.uuid1())
item3_uuid = str(uuid.uuid1())
item1 = {'id': item1_uuid, 'name': 'Sword', 'skill_point': '30'}
item2 = {'id': item2_uuid, 'name': 'Shield', 'skill_point': '20'}
item3 = {'id': item3_uuid, 'name': 'Axes'}
r = requests.post('http://0.0.0.0:5000/item', data=json.dumps(item1), headers=header)
print(r.text)
r = requests.put('http://0.0.0.0:5000/item', data=json.dumps(item2), headers=header)
print(r.text)
r = requests.put('http://0.0.0.0:5000/item', data=json.dumps(item3), headers=header)
print(r.text)
input("Press Enter to continue...")

print('Test 12: Add two items to the player')
item2_player = {'player_id': player2_uuid, 'item_id': item2_uuid}
item1_player = {'player_id': player2_uuid, 'item_id': item1_uuid}
r = requests.post('http://0.0.0.0:5000/itemplayer', data=json.dumps(item2_player), headers=header)
print(r.text)
r = requests.post('http://0.0.0.0:5000/playerguild', data=json.dumps(item1_player), headers=header)
input("Press Enter to continue...")