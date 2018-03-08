from flask import Flask, request
import flask_sqlalchemy
# from flask_restful import Resource, Api
import json
# import requests
import ast
# import flask_restless

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shawn:shawn@localhost/gamehive'
db = flask_sqlalchemy.SQLAlchemy(app)


guild_player = db.Table('guild_stat',
                      db.Column('player_id', db.String(128), db.ForeignKey('player.id')),
                      db.Column('guild_id', db.String(128), db.ForeignKey('guild.id'))
                      )

item_player = db.Table('item_stat',
                     db.Column('player_id', db.String(128), db.ForeignKey('player.id')),
                     db.Column('item_id', db.String(128), db.ForeignKey('item.id'))
                     )


class Player(db.Model):
    id = db.Column(db.String(128), primary_key=True)     #UUID
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    skill_point = db.Column(db.Integer, default=0)
    guilds = db.relationship('Guild', secondary=guild_player,
                             backref=db.backref('guild_player', lazy='dynamic'))


class Guild(db.Model):
    id = db.Column(db.String(128), primary_key=True)        #UUID
    name = db.Column(db.String(64), unique=True)
    country_code = db.Column(db.String(16))


class Item(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    skill_point = db.Column(db.Integer, default=0)
    owners = db.relationship('Player', secondary=item_player,
                             backref=db.backref('owner', lazy='dynamic'))

db.create_all()


# class WorkOnPlayer(Resource):
#     def get(self, nickname):
#         print('here2')
#         res = db.session.query('Player').filter_by(nickname=nickname).first()
#         print('here')
#         print(res)
#         if res is None:
#             return 404
#         return json.dumps({'id': res.id, 'nickname': res.nickname, 'email': res.email})
# api = Api(app)
# api.add_resource(WorkOnPlayer, '/player')

# manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
# player_blueprint = manager.create_api(Player, methods=['GET', 'POST', 'PUT', 'DELETE'])
# guild_blueprint = manager.create_api(Guild, methods=['GET', 'POST', 'PUT', 'DELETE'])
# item_blueprint = manager.create_api(Item, methods=['GET', 'POST', 'PUT', 'DELETE'])


@app.route('/')
def root():
    return 'Game Hive Player API'


# Get one user info.
# Request method: GET /player/<player_id>
@app.route('/player/<player_id>', methods=['GET'])
def get_player(player_id):
    res = Player.query.filter_by(id=player_id).first()
    if res is None:
        return 404
    return json.dumps({'id': res.id, 'nickname': res.nickname,
                       'email': res.email, 'skill_point': res.skill_point})


# Add or update a player info
# Request method: POST /player or PUT /player
# Content style: {'id': <UUID> , 'nickname': <nickname>,
# 'email': <email>, 'skill_point': <skill_point>}
# Skill point is optional (Default 0)
@app.route('/player', methods=['POST', 'PUT'])
def add_player():
    data = request.get_data(as_text=True)
    data = ast.literal_eval(data)
    player_id = data['id']
    try:
        skill_point = data['skill_point']
    except:
        skill_point = 0
    if request.method == 'POST':
        newplayer = Player(id=data['id'], nickname=data['nickname'],
                           email=data['email'], skill_point=skill_point)
        db.session.add(newplayer)
        db.session.commit()
        return json.dumps({'success': 'true'})
    else:
        res = Player.query.filter_by(id=player_id).first()
        if res is None:
            newplayer = Player(id=data['id'], nickname=data['nickname'],
                               email=data['email'], skill_point=skill_point)
            db.session.add(newplayer)
            db.session.commit()
        else:
            try:
                new_nickname = data['nickname']
                res.nickname = new_nickname
            except:
                pass
            try:
                new_email = data['email']
                res.email = new_email
            except:
                pass
            try:
                new_skill_point = data['skill_point']
                res.skill_point = new_skill_point
            except:
                pass
            db.session.commit()
        return json.dumps({'success': 'true'})


# Delete a user
# Request method: DELETE /player/<player_id>
@app.route('/player/<player_id>', methods=['DELETE'])
def delete_player(player_id):
    res = Player.query.filter_by(id=player_id).delete()
    db.session.commit()
    if res is None:
        return 404
    return json.dumps({'success': 'true'})


# Get one guild info.
# Request method: GET /guild/<guild_id>
@app.route('/guild/<guild_id>', methods=['GET'])
def get_guild(guild_id):
    res = Guild.query.filter_by(id=guild_id).first()
    if res is None:
        return 404
    return json.dumps({'id': res.id, 'name': res.name, 'country_code': res.country_code})


# Add or update a guild info
# Request method: POST /guild or PUT /guild
# Content style: {'id': <UUID> , 'name': <name>, 'country_code': <country_code>}
# Country code is optional
@app.route('/guild', methods=['POST', 'PUT'])
def add_guild():
    data = request.get_data(as_text=True)
    data = ast.literal_eval(data)
    guild_id = data['id']
    try:
        country_code = data['country_code']
    except:
        country_code = None
    if request.method == 'POST':
        newguild = Guild(id=data['id'], name=data['name'], country_code=country_code)
        db.session.add(newguild)
        db.session.commit()
        return json.dumps({'success': 'true'})
    else:
        res = Guild.query.filter_by(id=guild_id).first()
        if res is None:
            newguild = Guild(id=data['id'], name=data['name'], country_code=country_code)
            db.session.add(newguild)
            db.session.commit()
        else:
            try:
                name = data['name']
                res.name = name
            except:
                pass
            try:
                country_code = data['country_code']
                res.country_code = country_code
            except:
                pass
            db.session.commit()
        return json.dumps({'success': 'true'})


# Delete a guild
# Request method: DELETE /guild/<guild_id>
@app.route('/guild/<guild_id>', methods=['DELETE'])
def delete_guild(guild_id):
    res = Guild.query.filter_by(id=guild_id).delete()
    db.session.commit()
    if res is None:
        return 404
    return json.dumps({'success': 'true'})


# Add a player to a guild
# Request method: POST /playerguild
# Content style: {'player_id': <UUID> , 'guild_id': <UUID>}
@app.route('/playerguild', methods=['POST'])
def add_player_to_guild():
    data = request.get_data(as_text=True)
    data = ast.literal_eval(data)
    guild_id = data['guild_id']
    player_id = data['player_id']
    res = Guild.query.filter_by(id=guild_id).first()
    if res is None:
        return 404
    player_res = Player.query.filter_by(id=player_id).first()
    if player_res is None:
        return 404
    res.guild_player.append(player_res)
    db.session.commit()
    return json.dumps({'success': 'true'})


# Delete a player to a guild
# Request method: DELETE /playerguild
# Content style: {'player_id': <UUID> , 'guild_id': <UUID>}
@app.route('/playerguild', methods=['DELETE'])
def delete_player_from_guild():
    data = request.get_data(as_text=True)
    data = ast.literal_eval(data)
    guild_id = data['guild_id']
    player_id = data['player_id']
    res = Guild.query.filter_by(id=guild_id).first()
    if res is None:
        return 404
    player_res = Player.query.filter_by(id=player_id).first()
    if player_res is None:
        return 404
    res.guild_player.remove(player_res)
    db.session.commit()
    return json.dumps({'success': 'true'})


# Get one item info.
# Request method: GET /item/<item_id>
@app.route('/item/<item_id>', methods=['GET'])
def get_item(item_id):
    res = Item.query.filter_by(id=item_id).first()
    if res is None:
        return 404
    return json.dumps({'id': res.id, 'name': res.name, 'skill_point': res.skill_point})


# Add or update an item info
# Request method: POST /item or PUT /item
# Content style: {'id': <UUID> , 'name': <name>, 'skill_point': <skill_point>}
# Skill point is optional (Default 0)
@app.route('/item', methods=['POST', 'PUT'])
def add_item():
    data = request.get_data(as_text=True)
    data = ast.literal_eval(data)
    item_id = data['id']
    try:
        skill_point = data['skill_point']
    except:
        skill_point = 0
    if request.method == 'POST':
        newitem = Item(id=data['id'], name=data['name'], skill_point=skill_point)
        db.session.add(newitem)
        db.session.commit()
        return json.dumps({'success': 'true'})
    else:
        res = Item.query.filter_by(id=item_id).first()
        if res is None:
            newitem = Item(id=data['id'], name=data['name'], skill_point=skill_point)
            db.session.add(newitem)
            db.session.commit()
        else:
            try:
                name = data['name']
                res.name = name
            except:
                pass
            try:
                skill_point = data['skill_point']
                res.skill_point = skill_point
            except:
                pass
            db.session.commit()
        return json.dumps({'success': 'true'})


# Delete an item
# Request method: DELETE /item/<item_id>
@app.route('/item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    res = Item.query.filter_by(id=item_id).delete()
    db.session.commit()
    if res is None:
        return 404
    return json.dumps({'success': 'true'})


# Add an item to a player
# Request method: POST /itemplayer
# Content style: {'item_id': <UUID> , 'player_id': <UUID>}
@app.route('/itemplayer', methods=['POST'])
def add_item_to_player():
    data = request.get_data(as_text=True)
    data = ast.literal_eval(data)
    item_id = data['item_id']
    player_id = data['player_id']
    item_res = Item.query.filter_by(id=item_id).first()
    if item_res is None:
        return 404
    player_res = Player.query.filter_by(id=player_id).first()
    if player_res is None:
        return 404
    player_res.owner.append(item_res)
    db.session.commit()
    return json.dumps({'success': 'true'})


# Delete an item from a player
# Request method: DELETE /itemplayer
# Content style: {'item_id': <UUID> , 'player_id': <UUID>}
@app.route('/itemplayer', methods=['DELETE'])
def delete_item_from_player():
    data = request.get_data(as_text=True)
    data = ast.literal_eval(data)
    item_id = data['item_id']
    player_id = data['player_id']
    item_res = Item.query.filter_by(id=item_id).first()
    if item_res is None:
        return 404
    player_res = Player.query.filter_by(id=player_id).first()
    if player_res is None:
        return 404
    player_res.owner.remove(item_res)
    db.session.commit()
    return json.dumps({'success': 'true'})


# Get total points of a player
@app.route('/player_point/<player_id>', methods=['GET'])
def player_point(player_id):
    res = Item.query.filter(Item.owners.any(id=player_id)).all()
    if res is None:
        return 404
    print(res)
    return json.dumps({'success': 'true'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
