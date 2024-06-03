from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "customer_data"
    customer_id = db.Column(db.String(), nullable=False, primary_key=True)
    customer_name = db.Column(db.String(), nullable=False)
    interest_movie = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String(), nullable=True)
    interest_movie_choose = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f'<User {self.customer_name}>'
