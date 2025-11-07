"""
分析路由
"""
from flask import Blueprint, request, jsonify, session
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from models import db, Feedback, AspectSentiment
from services.sentiment_analyzer import SentimentAnalyzer
from utils.language_detector import detect_language
from utils.file_parser import parse_uploaded_file
import traceback

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/analysis')

# 全局情感分析器实例
analyzer = None

def get_analyzer():
    """获取情感分析器实例（单例模式）"""
    global analyzer
    if analyzer is None:
        analyzer = SentimentAnalyzer()
    return analyzer

@analysis_bp.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    """分析文本情感"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': '文本不能为空'}), 400
        
        analyzer = get_analyzer()
        result = analyzer.analyze(text)
        
        return jsonify({
            'sentiment': result,
            'language': detect_language(text)
        }), 200
        
    except Exception as e:
        print(f"情感分析失败: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'分析失败: {str(e)}'}), 500

@analysis_bp.route('/aspect', methods=['POST'])
def analyze_aspect():
    """分析特定方面的情感"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        data = request.get_json()
        text = data.get('text', '').strip()
        aspect = data.get('aspect', '').strip()
        
        if not text:
            return jsonify({'error': '文本不能为空'}), 400
        if not aspect:
            return jsonify({'error': '方面不能为空'}), 400
        
        analyzer = get_analyzer()
        result = analyzer.analyze_aspect(text, aspect)
        
        return jsonify({
            'aspect': aspect,
            'sentiment': result
        }), 200
        
    except Exception as e:
        print(f"方面分析失败: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'分析失败: {str(e)}'}), 500

@analysis_bp.route('/aspects', methods=['POST'])
def analyze_aspects():
    """分析所有方面的情感"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': '文本不能为空'}), 400
        
        analyzer = get_analyzer()
        result = analyzer.analyze_with_aspects(text)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"方面分析失败: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'分析失败: {str(e)}'}), 500

@analysis_bp.route('/batch', methods=['POST'])
def batch_analyze():
    """批量分析评论文件"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        if 'file' not in request.files:
            return jsonify({'error': '请上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        # 解析文件
        try:
            feedbacks_data = parse_uploaded_file(file)
        except Exception as e:
            return jsonify({'error': f'文件解析失败: {str(e)}'}), 400
        
        if not feedbacks_data:
            return jsonify({'error': '文件中没有有效的评论数据'}), 400
        
        # 批量分析
        analyzer = get_analyzer()
        processed = 0
        errors = []
        
        for idx, feedback_data in enumerate(feedbacks_data):
            try:
                text = feedback_data.get('text', '').strip()
                if not text:
                    continue
                
                # 分析情感和方面
                result = analyzer.analyze_with_aspects(text)
                
                # 创建反馈记录
                language = detect_language(text)
                feedback = Feedback(
                    user_id=session['user_id'],
                    text=text,
                    original_language=language,
                    sentiment_label=result.get('sentiment', {}).get('label', 'neutral'),
                    sentiment_score=result.get('sentiment', {}).get('score', 0.5),
                    hotel_name=feedback_data.get('hotel_name'),
                    rating=feedback_data.get('rating')
                )
                db.session.add(feedback)
                db.session.flush()
                
                # 保存方面情感
                aspect_sentiments = result.get('aspect_sentiments', {})
                for aspect_name, sentiment_label in aspect_sentiments.items():
                    aspect_sentiment = AspectSentiment(
                        feedback_id=feedback.id,
                        aspect_name=aspect_name,
                        sentiment_label=sentiment_label
                    )
                    db.session.add(aspect_sentiment)
                
                processed += 1
                
            except Exception as e:
                errors.append(f"第{idx+1}条评论处理失败: {str(e)}")
                continue
        
        db.session.commit()
        
        return jsonify({
            'message': '批量分析完成',
            'processed': processed,
            'total': len(feedbacks_data),
            'errors': errors[:10]  # 只返回前10个错误
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"批量分析失败: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'批量分析失败: {str(e)}'}), 500

