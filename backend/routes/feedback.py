"""
反馈路由
"""
from flask import Blueprint, request, jsonify, session
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from models import db, User, Feedback, AspectSentiment
from services.sentiment_analyzer import SentimentAnalyzer
from utils.language_detector import detect_language
import traceback

feedback_bp = Blueprint('feedback', __name__, url_prefix='/api/feedback')

# 全局情感分析器实例
analyzer = None

def get_analyzer():
    """获取情感分析器实例（单例模式）"""
    global analyzer
    if analyzer is None:
        analyzer = SentimentAnalyzer()
    return analyzer

@feedback_bp.route('/submit', methods=['POST'])
def submit_feedback():
    """提交反馈"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': '反馈内容不能为空'}), 400
        
        # 检测语言
        language = detect_language(text)
        
        # 情感分析
        try:
            analyzer = get_analyzer()
            sentiment_result = analyzer.analyze(text)
            
            # 创建反馈记录
            feedback = Feedback(
                user_id=session['user_id'],
                text=text,
                original_language=language,
                sentiment_label=sentiment_result['label'],
                sentiment_score=sentiment_result['score']
            )
            db.session.add(feedback)
            db.session.flush()
            
            # 方面情感分析
            try:
                aspects_result = analyzer.analyze_with_aspects(text)
                for aspect_name, aspect_label in aspects_result.get('aspect_sentiments', {}).items():
                    aspect_sentiment = AspectSentiment(
                        feedback_id=feedback.id,
                        aspect_name=aspect_name,
                        sentiment_label=aspect_label
                    )
                    db.session.add(aspect_sentiment)
            except Exception as e:
                print(f"方面分析失败: {str(e)}")
                # 方面分析失败不影响主流程
            
            db.session.commit()
            
            return jsonify({
                'message': '反馈提交成功',
                'feedback': feedback.to_dict(),
                'sentiment': sentiment_result
            }), 201
            
        except Exception as e:
            db.session.rollback()
            print(f"情感分析失败: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': f'情感分析失败: {str(e)}'}), 500
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'提交失败: {str(e)}'}), 500

@feedback_bp.route('/list', methods=['GET'])
def list_feedbacks():
    """获取当前用户的反馈列表"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        user_id = session['user_id']
        feedbacks = Feedback.query.filter_by(user_id=user_id).order_by(Feedback.created_at.desc()).all()
        
        return jsonify({
            'feedbacks': [f.to_dict() for f in feedbacks]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500

@feedback_bp.route('/<int:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    """获取单个反馈详情"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        feedback = Feedback.query.get_or_404(feedback_id)
        
        # 检查权限
        if feedback.user_id != session['user_id'] and session.get('role') != 'admin':
            return jsonify({'error': '无权访问'}), 403
        
        return jsonify({'feedback': feedback.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500

