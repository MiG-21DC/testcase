from flask import Flask
import flask_sqlalchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://shawn:shawn@postgres:5432/gamehive'
db = flask_sqlalchemy.SQLAlchemy(app)

guild_stat = db.Table('guild_stat',
                      db.Column('player_id', db.String(32), db.ForeignKey('player.id')),
                      db.Column('guild_id', db.String(32), db.ForeignKey('guild.id'))
                      )

item_stat = db.Table('item_stat',
                     db.Column('player_id', db.String(32), db.ForeignKey('player.id')),
                     db.Column('item_id', db.String(32), db.ForeignKey('Item.id'))
                     )


class Player(db.Model):
    id = db.Column(db.String(32), primary_key=True)     #UUID
    nickname = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    guilds = db.relationship('Guild', secondary=guild_stat, back_populates='players')
    items = db.relationship('Item', secondary=item_stat, back_populates='owners')


class Guild(db.Model):
    id = db.Column(db.String(32), primary_key=True)        #UUID
    name = db.Column(db.String(64), unique=True)
    country_code = db.Column(db.String(16))
    players = db.relationship('Player', secondary=guild_stat, back_populates='guilds')


class Item(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    owners = db.relationship('Player', secondary=item_stat, back_populates='items')

db.create_all()