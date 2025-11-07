"""
数据库模型
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' 或 'admin'
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
    """反馈模型"""
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    original_language = db.Column(db.String(10), default='zh')  # 'zh' 或 'en'
    sentiment_label = db.Column(db.String(20))  # very_positive, positive, neutral, negative, very_negative
    sentiment_score = db.Column(db.Float)
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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'aspects': [aspect.to_dict() for aspect in self.aspects]
        }

class AspectSentiment(db.Model):
    """方面情感模型"""
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

