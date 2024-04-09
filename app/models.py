from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  #use this to add time implementation


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    password = db.Column(db.String(32), index=True, unique=False, nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    planner = db.relationship('Planner', backref='users', lazy='dynamic')

    def __repr__(self):
        return '{} {}'.format(self.username, self.email)
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    tasks = db.relationship('Task', backref='game', lazy=True)
    
    def __repr__(self):
        return '{} {}'.format(self.name)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(200),index=True, nullable=False)
    complete = db.Column(db.Boolean, index=True, default=False)
    users = db.relationship('User', secondary='user_task', backref='tasks')
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    
    def __repr__(self):
        return '{} {}'.format(self.goal, self.complete)

class Planner(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    #note to self add html templates here i think

    def add_game(self, game_id):
        game = Game.query.get(game_id)
        if game:
            self.user.games.append(game)
            db.session.commit()
            return True
        return False
    
    def __repr__(self):
        return '{} {}'.format(self)