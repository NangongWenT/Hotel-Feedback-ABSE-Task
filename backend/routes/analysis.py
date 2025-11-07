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

def require_admin():
    """检查管理员权限"""
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    if session.get('role') != 'admin':
        return jsonify({'error': '需要管理员权限'}), 403
    return None

@analysis_bp.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    """分析文本情感（仅管理员）"""
    try:
        error = require_admin()
        if error:
            return error
        
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
    """分析特定方面的情感（仅管理员）"""
    try:
        error = require_admin()
        if error:
            return error
        
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
    """分析所有方面的情感（仅管理员）"""
    try:
        error = require_admin()
        if error:
            return error
        
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
    """批量分析评论文件（仅管理员）"""
    try:
        error = require_admin()
        if error:
            return error
        
        if 'file' not in request.files:
            return jsonify({'error': '请上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '文件名为空'}), 400
        
        print(f"开始处理批量上传文件: {file.filename}")
        
        # 解析文件
        try:
            feedbacks_data = parse_uploaded_file(file)
            print(f"文件解析成功，共 {len(feedbacks_data)} 条评论")
        except Exception as e:
            print(f"文件解析失败: {str(e)}")
            print(traceback.format_exc())
            return jsonify({'error': f'文件解析失败: {str(e)}'}), 400
        
        if not feedbacks_data:
            return jsonify({'error': '文件中没有有效的评论数据'}), 400
        
        # 限制批量处理数量，避免超时
        max_batch_size = 10000
        if len(feedbacks_data) > max_batch_size:
            return jsonify({
                'error': f'文件包含的评论数量过多（{len(feedbacks_data)}条），请分批上传，每次不超过{max_batch_size}条'
            }), 400
        
        # 批量分析
        analyzer = get_analyzer()
        processed = 0
        errors = []
        
        print(f"开始批量分析，共 {len(feedbacks_data)} 条评论")
        
        # 根据数据量调整提交频率
        commit_interval = 50 if len(feedbacks_data) > 1000 else 20
        
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
                
                # 定期提交，避免内存问题和事务超时
                if processed % commit_interval == 0:
                    try:
                        db.session.commit()
                        print(f"已处理 {processed}/{len(feedbacks_data)} 条评论")
                    except Exception as commit_error:
                        db.session.rollback()
                        error_msg = f"数据库提交失败（第{processed}条）: {str(commit_error)}"
                        errors.append(error_msg)
                        print(error_msg)
                        # 继续处理，不中断整个流程
                
            except Exception as e:
                error_msg = f"第{idx+1}条评论处理失败: {str(e)}"
                errors.append(error_msg)
                print(error_msg)
                # 只打印关键错误，避免日志过多
                if len(errors) <= 20:  # 只打印前20个错误的详细堆栈
                    print(traceback.format_exc())
                db.session.rollback()  # 回滚当前事务
                continue
            
        # 最终提交剩余的数据
        try:
            db.session.commit()
        except Exception as commit_error:
            db.session.rollback()
            error_msg = f"最终提交失败: {str(commit_error)}"
            errors.append(error_msg)
            print(error_msg)
        
        print(f"批量分析完成，成功处理 {processed}/{len(feedbacks_data)} 条评论")
        
        return jsonify({
            'message': '批量分析完成',
            'processed': processed,
            'total': len(feedbacks_data),
            'errors': errors[:10] if errors else []  # 只返回前10个错误
        }), 200
        
    except Exception as e:
        db.session.rollback()
        error_msg = f"批量分析失败: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

