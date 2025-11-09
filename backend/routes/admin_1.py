"""
管理员路由
"""
from flask import Blueprint, request, jsonify, session
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from models import db, User, Feedback, AspectSentiment
from sqlalchemy import func
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def require_admin():
    """检查管理员权限"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    if session.get('role') != 'admin':
        return jsonify({'error': '需要管理员权限'}), 403
    return None

@admin_bp.route('/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    try:
        error = require_admin()
        if error:
            return error
        
        # 总反馈数
        total_feedbacks = Feedback.query.count()
        
        # 情感分布（处理 None 值）
        sentiment_stats = db.session.query(
            Feedback.sentiment_label,
            func.count(Feedback.id)
        ).group_by(Feedback.sentiment_label).all()
        
        sentiment_distribution = {}
        for label, count in sentiment_stats:
            # 处理 None 值
            key = label if label is not None else '未分析'
            sentiment_distribution[key] = count
        
        # 最近7天的反馈数
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_feedbacks = Feedback.query.filter(
            Feedback.created_at >= seven_days_ago
        ).count()
        
        # 语言分布（处理 None 值）
        language_stats = db.session.query(
            Feedback.original_language,
            func.count(Feedback.id)
        ).group_by(Feedback.original_language).all()
        
        language_distribution = {}
        for lang, count in language_stats:
            # 处理 None 值
            key = lang if lang is not None else '未知'
            language_distribution[key] = count
        
        # 方面统计（处理 None 值）
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
            # 跳过 None 值
            if aspect_name is None or sentiment_label is None:
                continue
            if aspect_name not in aspect_distribution:
                aspect_distribution[aspect_name] = {}
            aspect_distribution[aspect_name][sentiment_label] = count
        
        return jsonify({
            'total_feedbacks': total_feedbacks,
            'recent_feedbacks': recent_feedbacks,
            'sentiment_distribution': sentiment_distribution,
            'language_distribution': language_distribution,
            'aspect_distribution': aspect_distribution
        }), 200
        
    except Exception as e:
        import traceback
        error_msg = f'获取统计失败: {str(e)}'
        print(error_msg)
        print(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

@admin_bp.route('/feedbacks', methods=['GET'])
def list_all_feedbacks():
    """获取所有反馈（管理员）"""
    try:
        error = require_admin()
        if error:
            return error
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        feedbacks = Feedback.query.order_by(
            Feedback.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'feedbacks': [f.to_dict() for f in feedbacks.items],
            'total': feedbacks.total,
            'page': page,
            'per_page': per_page,
            'pages': feedbacks.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500

@admin_bp.route('/users', methods=['GET'])
def list_users():
    """获取所有用户（管理员）"""
    try:
        error = require_admin()
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
    """分析单个反馈（管理员）"""
    try:
        error = require_admin()
        if error:
            return error
        
        feedback = Feedback.query.get_or_404(feedback_id)
        
        # 导入分析器
        from services.sentiment_analyzer import SentimentAnalyzer
        from utils.language_detector import detect_language
        
        analyzer = SentimentAnalyzer()
        
        # 分析情感和方面
        result = analyzer.analyze_with_aspects(feedback.text)
        
        # 更新反馈记录
        feedback.sentiment_label = result.get('sentiment', {}).get('label', 'neutral')
        feedback.sentiment_score = result.get('sentiment', {}).get('score', 0.5)
        
        # 删除旧的方面情感
        AspectSentiment.query.filter_by(feedback_id=feedback.id).delete()
        
        # 保存新的方面情感
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

