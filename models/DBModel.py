from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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

class Wallet(db.Model):
    __tablename__ = 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), unique=True, nullable=False)
    balance = db.Column(db.BigInteger, nullable=False)
    balance_usd = db.Column(db.Float, nullable=False)
    blockchain = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    family = db.Column(db.String(100), nullable=True)
    transactions = db.relationship('Transaction', backref='wallet', lazy=True, cascade="all, delete-orphan")

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    hash = db.Column(db.String(100), nullable=False)
    time = db.Column(db.BigInteger, nullable=False)  # Unix timestamp
    amount = db.Column(db.BigInteger, nullable=False)
    amount_usd = db.Column(db.Float, nullable=False)

class KriptoDegisim(db.Model):
    __tablename__ = 'kripto_degisim'
    id = db.Column(db.Integer, primary_key=True)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    cuzdanno = db.Column(db.String(100), nullable=False)
    degismeden_once = db.Column(db.BigInteger, nullable=False)
    degisimden_sonra = db.Column(db.BigInteger, nullable=False)