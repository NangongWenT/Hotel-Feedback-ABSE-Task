"""
Admin/Dashboard routes
"""
from flask import Blueprint, request, jsonify, session
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from models import db, User, Feedback, AspectSentiment
from sqlalchemy import func, case
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def require_login():
    """
    Only check if logged in, no longer force admin privileges.
    This allows regular users to see Dashboard data after logging in.
    """
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    return None

@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics and trend data"""
    try:
        error = require_login()
        if error:
            return error
        
        # --- 1. 基础统计 ---
        total_feedbacks = Feedback.query.count()
        
        # Sentiment distribution
        sentiment_stats = db.session.query(
            Feedback.sentiment_label,
            func.count(Feedback.id)
        ).group_by(Feedback.sentiment_label).all()
        
        sentiment_distribution = {}
        for label, count in sentiment_stats:
            key = label if label is not None else 'neutral'
            sentiment_distribution[key] = count
        
        # Last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_feedbacks = Feedback.query.filter(
            Feedback.created_at >= seven_days_ago
        ).count()
        
        # Language distribution
        language_stats = db.session.query(
            Feedback.original_language,
            func.count(Feedback.id)
        ).group_by(Feedback.original_language).all()
        
        language_distribution = {}
        for lang, count in language_stats:
            key = lang if lang is not None else 'unknown'
            language_distribution[key] = count
        
        # Aspect statistics
        aspect_stats = db.session.query(
            AspectSentiment.aspect_name,
            AspectSentiment.sentiment_label,
            func.count(AspectSentiment.id)
        ).group_by(
            AspectSentiment.aspect_name,
            AspectSentiment.sentiment_label
        ).all()
        
        aspect_distribution = {}
        for aspect_name, sentiment_label, count in aspect_stats:
            if not aspect_name: continue
            if aspect_name not in aspect_distribution:
                aspect_distribution[aspect_name] = {}
            # Ensure default value
            safe_label = sentiment_label if sentiment_label else 'neutral'
            aspect_distribution[aspect_name][safe_label] = count

        # --- 2. New: Calculate trend data for the last 6 months (for frontend curve chart) ---
        trend_data = []
        end_date = datetime.utcnow()
        
        for i in range(5, -1, -1):
            # Simple month calculation: i*30 days before current time
            month_date = end_date - timedelta(days=i*30)
            month_str = month_date.strftime('%Y-%m') 
            month_name = month_date.strftime('%b')   
            
         
            # Use case statement to count negative and very_negative
            stats = db.session.query(
                func.count(Feedback.id),
                func.sum(case(
                    (Feedback.sentiment_label == 'negative', 1), 
                    (Feedback.sentiment_label == 'very_negative', 1), 
                    else_=0
                ))
            ).filter(func.strftime('%Y-%m', Feedback.created_at) == month_str).first()
            
            trend_data.append({
                "month": month_name,
                "volume": stats[0] or 0,     # Total volume
                "negative": stats[1] or 0    # Negative count
            })
        
        return jsonify({
            'total_feedbacks': total_feedbacks,
            'recent_feedbacks': recent_feedbacks,
            'sentiment_distribution': sentiment_distribution,
            'language_distribution': language_distribution,
            'aspect_distribution': aspect_distribution,
            'trend_data': trend_data  # New field returned to frontend
        }), 200
        
    except Exception as e:
        import traceback
        error_msg = f'获取统计失败: {str(e)}'
        print(error_msg)
        print(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

@admin_bp.route('/feedbacks', methods=['GET'])
def list_all_feedbacks():
    """Get all feedback list (including dynamic Aspects)"""
    try:
        error = require_login()
        if error:
            return error
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        pagination = Feedback.query.order_by(
            Feedback.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        # 🔥 Key modification: Build detailed list with aspects
        feedbacks_list = []
        for f in pagination.items:
            f_dict = f.to_dict()
            
            # Query the specific Aspect data associated with this comment
            # Frontend will use this data to render colored Key Aspects tags
            aspects = AspectSentiment.query.filter_by(feedback_id=f.id).all()
            f_dict['aspects'] = [{
                'name': a.aspect_name,
                'sentiment': a.sentiment_label
            } for a in aspects]
            
            feedbacks_list.append(f_dict)
        
        return jsonify({
            'feedbacks': feedbacks_list,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500

@admin_bp.route('/users', methods=['GET'])
def list_users():
    """Get all users"""
    try:
        error = require_login() # Loosen permissions
        if error:
            return error
        
        users = User.query.all()
        
        return jsonify({
            'users': [u.to_dict() for u in users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500

@admin_bp.route('/analyze/<int:feedback_id>', methods=['POST'])
def analyze_feedback(feedback_id):
    """Analyze a single feedback"""
    try:
        error = require_login() # Loosen permissions, allow regular users to re-analyze
        if error:
            return error
        
        feedback = Feedback.query.get_or_404(feedback_id)
        
        # Import analyzer (local import to avoid circular dependency)
        from services.sentiment_analyzer import SentimentAnalyzer
        
        analyzer = SentimentAnalyzer()
        
        # Analyze sentiment and aspects
        result = analyzer.analyze_with_aspects(feedback.text)
        
        # 更新反馈记录
        feedback.sentiment_label = result.get('sentiment', {}).get('label', 'neutral')
        feedback.sentiment_score = result.get('sentiment', {}).get('score', 0.5)
        
        # Delete old aspect sentiments
        AspectSentiment.query.filter_by(feedback_id=feedback.id).delete()
        
        # Save new aspect sentiments
        aspect_sentiments = result.get('aspect_sentiments', {})
        for aspect_name, sentiment_label in aspect_sentiments.items():
            aspect_sentiment = AspectSentiment(
                feedback_id=feedback.id,
                aspect_name=aspect_name,
                sentiment_label=sentiment_label
            )
            db.session.add(aspect_sentiment)
        
        db.session.commit()
        
        return jsonify({
            'message': '分析完成',
            'feedback': feedback.to_dict(),
            'analysis': result
        }), 200
        
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"分析失败: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'分析失败: {str(e)}'}), 500