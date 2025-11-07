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
from utils.file_parser import parse_uploaded_file
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
    """提交反馈（用户只能提交，不进行分析）"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': '反馈内容不能为空'}), 400
        
        # 检测语言
        language = detect_language(text)
        
        # 创建反馈记录（不进行分析，等待管理员分析）
        feedback = Feedback(
            user_id=session['user_id'],
            text=text,
            original_language=language,
            sentiment_label=None,  # 未分析
            sentiment_score=None
        )
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'message': '反馈提交成功，等待管理员分析',
            'feedback': feedback.to_dict()
        }), 201
            
    except Exception as e:
        db.session.rollback()
        print(f"提交失败: {str(e)}")
        print(traceback.format_exc())
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

@feedback_bp.route('/batch-upload', methods=['POST'])
def batch_upload():
    """批量上传评论（用户只能上传，不进行分析）"""
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
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
        
        # 限制批量处理数量
        max_batch_size = 10000
        if len(feedbacks_data) > max_batch_size:
            return jsonify({
                'error': f'文件包含的评论数量过多（{len(feedbacks_data)}条），请分批上传，每次不超过{max_batch_size}条'
            }), 400
        
        # 批量上传（不进行分析）
        processed = 0
        errors = []
        
        print(f"开始批量上传，共 {len(feedbacks_data)} 条评论")
        
        for idx, feedback_data in enumerate(feedbacks_data):
            try:
                text = feedback_data.get('text', '').strip()
                if not text:
                    continue
                
                # 检测语言
                language = detect_language(text)
                
                # 创建反馈记录（不进行分析）
                feedback = Feedback(
                    user_id=session['user_id'],
                    text=text,
                    original_language=language,
                    sentiment_label=None,  # 未分析
                    sentiment_score=None,
                    hotel_name=feedback_data.get('hotel_name'),
                    rating=feedback_data.get('rating')
                )
                db.session.add(feedback)
                processed += 1
                
                # 每100条提交一次
                if processed % 100 == 0:
                    db.session.commit()
                    print(f"已上传 {processed}/{len(feedbacks_data)} 条评论")
                
            except Exception as e:
                error_msg = f"第{idx+1}条评论处理失败: {str(e)}"
                errors.append(error_msg)
                print(error_msg)
                db.session.rollback()
                continue
        
        # 最终提交
        try:
            db.session.commit()
        except Exception as commit_error:
            db.session.rollback()
            error_msg = f"最终提交失败: {str(commit_error)}"
            errors.append(error_msg)
            print(error_msg)
        
        print(f"批量上传完成，成功上传 {processed}/{len(feedbacks_data)} 条评论")
        
        return jsonify({
            'message': '批量上传完成，等待管理员分析',
            'processed': processed,
            'total': len(feedbacks_data),
            'errors': errors[:10] if errors else []
        }), 200
        
    except Exception as e:
        db.session.rollback()
        error_msg = f"批量上传失败: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

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

