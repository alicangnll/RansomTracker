from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    locations = db.Column(db.Text)
    meta = db.Column(db.String)
    name = db.Column(db.String)
    profile = db.Column(db.Text)
    tools = db.Column(db.Text)
    ttps = db.Column(db.Text)
    url = db.Column(db.String)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    discovered = db.Column(db.String)
    published = db.Column(db.String)
    post_url = db.Column(db.String)
    country = db.Column(db.String)
    activity = db.Column(db.String)
    website = db.Column(db.String)
    duplicates = db.Column(db.Text)
    screenshot = db.Column(db.Text)