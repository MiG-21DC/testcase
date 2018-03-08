from flask import Flask
import flask_sqlalchemy
from flask_restful import Resource, Api
import json
# import flask_restless

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shawn:shawn@localhost/gamehive'
db = flask_sqlalchemy.SQLAlchemy(app)
api = Api(app)

guild_stat = db.Table('guild_stat',
                      db.Column('player_id', db.String(128), db.ForeignKey('player.id')),
                      db.Column('guild_id', db.String(128), db.ForeignKey('guild.id'))
                      )

item_stat = db.Table('item_stat',
                     db.Column('player_id', db.String(128), db.ForeignKey('player.id')),
                     db.Column('item_id', db.String(128), db.ForeignKey('item.id'))
                     )


class Player(db.Model):
    id = db.Column(db.String(128), primary_key=True)     #UUID
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    guilds = db.relationship('Guild', secondary=guild_stat, back_populates='players')
    items = db.relationship('Item', secondary=item_stat, back_populates='owners')


class Guild(db.Model):
    id = db.Column(db.String(128), primary_key=True)        #UUID
    name = db.Column(db.String(64), unique=True)
    country_code = db.Column(db.String(16))
    players = db.relationship('Player', secondary=guild_stat, back_populates='guilds')


class Item(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    owners = db.relationship('Player', secondary=item_stat, back_populates='items')

db.create_all()


class WorkOnPlayer(Resource):
    def get(self, nickname):
        res = Player.query.filter_by(username=nickname).first()
        if res is None:
            return 404
        return json.dumps({'id': res.id, 'nickname': res.nickname, 'email': res.email})

api.add_resource(WorkOnPlayer, '/player')

# manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
# player_blueprint = manager.create_api(Player, methods=['GET', 'POST', 'PUT', 'DELETE'])
# guild_blueprint = manager.create_api(Guild, methods=['GET', 'POST', 'PUT', 'DELETE'])
# item_blueprint = manager.create_api(Item, methods=['GET', 'POST', 'PUT', 'DELETE'])


@app.route('/')
def root():
    return 'Game Hive Player API'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
