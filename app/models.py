from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  #use this to add time implementation
from flask_login import UserMixin

def get_user(username):
    user = User.query.filter_by(username=username).first()
    return user


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    password = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    games = db.relationship('Game', secondary='planner', backref='user')
    planner = db.relationship('Planner', backref='user', lazy=True, uselist=False)
    
    #using werkzeug.security here to hash passwords
    def set_password(self, password):
        self.password = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '{} {}'.format(self.username, self.email)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    users = db.relationship("User", secondary='planner', backref='game')
    tasks = db.relationship('Task', backref='game', lazy=True)
    planner_id = db.Column(db.Integer, db.ForeignKey('planner.id'), nullable=False)
    
    def __repr__(self):
        return '{}'.format(self.name)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(200),index=True, nullable=False)
    complete = db.Column(db.Boolean, index=True, default=False)
    #users = db.relationship('User', secondary='user_task', backref='tasks')
    #users = db.relationship('User', backref='tasks')
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    
    def mark_as_complete(self):
        self.complete = True
        db.session.commit()
    
    def __repr__(self):
        return '{} {}'.format(self.goal, self.complete)

class Planner(db.Model):
    __tablename__ = 'planner'
    id = db.Column(db.Integer, primary_key=True)
    games = db.relationship('Game', backref='planner', lazy=True)
    #tasks = db.relationship('Task', backref='planner', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #note to self add html templates here i think

    def add_game(self, game_id):
        game = Game.query.get(game_id)
        if game:
            self.user.games.append(game)
            db.session.commit()
            return True
        return False
    
    def __repr__(self):
        return '{}'.format(self)