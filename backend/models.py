"""
Database Models
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """User Model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Feedback(db.Model):
    """Feedback Model"""
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    original_language = db.Column(db.String(10), default='zh')  # 'zh' or 'en'
    sentiment_label = db.Column(db.String(20))  # very_positive, positive, neutral, negative, very_negative
    sentiment_score = db.Column(db.Float)
    hotel_name = db.Column(db.String(200))  # Hotel name
    rating = db.Column(db.Float)  # Rating (1-5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    aspects = db.relationship('AspectSentiment', backref='feedback', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'text': self.text,
            'language': self.original_language,  # 保持API兼容性，返回language字段
            'original_language': self.original_language,
            'sentiment_label': self.sentiment_label,
            'sentiment_score': self.sentiment_score,
            'hotel_name': self.hotel_name,
            'rating': self.rating,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'aspects': [aspect.to_dict() for aspect in self.aspects]
        }

class AspectSentiment(db.Model):
    """Aspect Sentiment Model"""
    __tablename__ = 'aspect_sentiments'
    
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedbacks.id'), nullable=False)
    aspect_name = db.Column(db.String(100), nullable=False)
    sentiment_label = db.Column(db.String(20))  # very_positive, positive, neutral, negative, very_negative
    sentiment_score = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'feedback_id': self.feedback_id,
            'aspect_name': self.aspect_name,
            'sentiment_label': self.sentiment_label,
            'sentiment_score': self.sentiment_score
        }

