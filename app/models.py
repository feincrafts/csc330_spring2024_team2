from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin, current_user
from app import db

def get_user(username):
    user = User.query.filter_by(username=username).first()
    return user


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    password = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    admin = db.Column(db.Boolean, index=True, default=False)
    games = db.relationship('Game', secondary='user_games', backref='users')
    #using werkzeug.security here to hash passwords
    def set_password(self, password):
        self.password = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '{} {}'.format(self.username, self.email)

class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer)
    name = db.Column(db.String(64), index=True, nullable=False, primary_key=True)
    tasks = db.relationship('Task', backref='game', lazy=True)
    image = db.Column(db.String(128), nullable=True)

    def get_game_name(self):
        game = Game.query.get(self.game_id)
        if game:
            return game.name  
        else: 
            None
    
    def __repr__(self):
        return '{}'.format(self.name)

#relationship table
class User_Games(db.Model):
    __tablename__ = "user_games"
    username = db.Column(db.String(32), db.ForeignKey('user.username'), primary_key=True)
    game_name = db.Column(db.Integer, db.ForeignKey('game.name'), primary_key=True)

    def __repr__(self):
        return '{} {}'.format(self.username, self.game_name)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(200),index=True, nullable=False)
    complete = db.Column(db.Boolean, index=True, default=False)
    game_name = db.Column(db.Integer, db.ForeignKey('game.name'), nullable=False)
    
    def get_game_name(self):
        game = Game.query.get(self.game_id)
        if game:
            return game.name  
        else: 
            None
    
    def mark_as_complete(self):
        self.complete = True
        db.session.commit()
    
    def __repr__(self):
        return '{} {}'.format(self.goal, self.complete)

#Seperated the custom tasks from prepopulated tasks to keep the DB neat rather than a "is_custom" boolean
class CustomTask(db.Model):
    __tablename__ = 'custom_task'
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Boolean, default=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_name = db.Column(db.Integer, db.ForeignKey('game.name'), nullable=False)
    task_creator = db.relationship('User', backref='user_tasks')
    game = db.relationship('Game', backref='custom_tasks')
    
    #Creates custom tasks, make sure to use current_user.id to insert into creator_id
    @staticmethod
    def create_custom_task(goal, creator_id, game_name):
        #Tries to find the game in the DB before it makes the goal
        game = Game.query.filter_by(name=game_name).first()
        if game:
            new_task = CustomTask(goal=goal, creator_id=creator_id, game_name=game.name)
            db.session.add(new_task)
            db.session.commit()
            return new_task
        else:
            # If the game does not exist, handle the error or return None
            return None

    def mark_as_complete(self):
        self.complete = True
        db.session.commit()

    def __repr__(self):
        return '{} {}'.format(self.goal, self.complete)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(64), db.ForeignKey('game.id'))
    title =  db.Column(db.String(64))
    date = db.Column(db.String(32))
    description = db.Column(db.String(256))
    participants = db.Column(db.Integer)
    #user = db.Column(db.String(32), db.ForeignKey('user.username'))

    #add_event can be called to store the event in the DB, maybe we let the user know what format we need
    def add_event(self, title, date, description, participants):
        create_event = Event(title=title, date=date, description=description, participants=participants)
        db.session.add(create_event)
        db.session.commit()

    def __repr__(self):
        return '{} {} {}'.format(self.title, self.date, self.description)
