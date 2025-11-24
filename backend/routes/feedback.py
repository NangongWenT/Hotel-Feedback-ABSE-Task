
from flask import Blueprint, request, jsonify, session, Response, stream_with_context
import sys
from pathlib import Path
import io
import csv
import json
import time
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
from models import db, Feedback, AspectSentiment
from services.sentiment_analyzer import SentimentAnalyzer
from utils.language_detector import detect_language
import traceback

feedback_bp = Blueprint('feedback', __name__, url_prefix='/api/feedback')


analyzer = None
def get_analyzer():
    global analyzer
    if analyzer is None:
        analyzer = SentimentAnalyzer()
    return analyzer

@feedback_bp.route('/submit', methods=['POST'])
def submit_feedback():

    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
            
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': '反馈内容不能为空'}), 400
            
        feedback = Feedback(
            user_id=session['user_id'],
            text=text,
            original_language=detect_language(text),
            created_at=datetime.utcnow()
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'message': '提交成功',
            'feedback': feedback.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '提交失败'}), 500


@feedback_bp.route('/batch-upload', methods=['POST'])
def batch_upload_stream():
    # 1. 基础验证 (非流式)
    if 'user_id' not in session:
        return jsonify({'error': '请先登录'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': '请上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400

  
    try:
        stream = file.read()
        content = None
        try:
            content = stream.decode('utf-8-sig')
        except:
            try:
                content = stream.decode('gbk')
            except:
                content = stream.decode('latin-1', errors='ignore')

        if not content:
            return jsonify({'error': '文件内容无法解码'}), 400

    
        f = io.StringIO(content)
        reader = csv.reader(f, delimiter=',')
        headers = next(reader, [])
        f.seek(0)
        
        delimiter = ','
        if len(headers) <= 1 and ';' in headers[0]:
            delimiter = ';'
        
        reader = csv.DictReader(f, delimiter=delimiter)
        

        target_key = None
        possible_keys = ['review', 'text', 'content', 'comment', 'body', '评论']
        
        fieldnames = [h.lower().strip() for h in reader.fieldnames] if reader.fieldnames else []
        real_field_map = {k.lower().strip(): k for k in reader.fieldnames}
        
        for key in possible_keys:
            if key in fieldnames:
                target_key = real_field_map[key]
                break
        
        if not target_key:
            return jsonify({'error': f'无法识别评论列，请确保包含: {", ".join(possible_keys)}'}), 400

        rows_to_process = []
        for row in reader:
            text_val = row.get(target_key, '').strip()
            if text_val:
                rows_to_process.append(text_val)
                
        total_count = len(rows_to_process)
        if total_count == 0:
            return jsonify({'error': '文件中没有有效数据'}), 400

    except Exception as e:
        return jsonify({'error': f'文件解析错误: {str(e)}'}), 400

   
    def generate():
        analyzer = get_analyzer()
        user_id = session['user_id'] # 获取当前用户ID
        
        processed_count = 0
        
      
        for text_val in rows_to_process:
            try:
             
                result = analyzer.analyze_with_aspects(text_val)
                
              
                feedback = Feedback(
                    user_id=user_id,
                    text=text_val,
                    original_language=detect_language(text_val),
                    sentiment_label=result.get('sentiment', {}).get('label', 'neutral'),
                    sentiment_score=result.get('sentiment', {}).get('score', 0.5),
                    created_at=datetime.utcnow()
                )
                db.session.add(feedback)
                db.session.flush()
                
             
                aspect_sentiments = result.get('aspect_sentiments', {})
                for aspect_name, sentiment_label in aspect_sentiments.items():
                    if aspect_name:
                        db.session.add(AspectSentiment(
                            feedback_id=feedback.id,
                            aspect_name=aspect_name,
                            sentiment_label=sentiment_label
                        ))
                
                db.session.commit()
                processed_count += 1
                
              
                yield f"data: {json.dumps({'current': processed_count, 'total': total_count, 'status': 'processing'})}\n\n"
                
            except Exception as e:
                print(f"处理出错: {str(e)}")
                db.session.rollback()
             
        
    
        yield f"data: {json.dumps({'current': processed_count, 'total': total_count, 'status': 'completed'})}\n\n"

    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')


@feedback_bp.route('/analyze/<int:feedback_id>', methods=['POST'])
def analyze_my_feedback(feedback_id):
    try:
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        
        feedback = Feedback.query.get_or_404(feedback_id)
        
        if session.get('role') != 'admin' and feedback.user_id != session['user_id']:
            return jsonify({'error': '无权操作'}), 403
            
        analyzer = get_analyzer()
        result = analyzer.analyze_with_aspects(feedback.text)
        
        feedback.sentiment_label = result.get('sentiment', {}).get('label', 'neutral')
        feedback.sentiment_score = result.get('sentiment', {}).get('score', 0.5)
        
        AspectSentiment.query.filter_by(feedback_id=feedback.id).delete()
        
        aspect_sentiments = result.get('aspect_sentiments', {})
        for aspect_name, sentiment_label in aspect_sentiments.items():
            db.session.add(AspectSentiment(
                feedback_id=feedback.id,
                aspect_name=aspect_name,
                sentiment_label=sentiment_label
            ))
        
        db.session.commit()
        
        return jsonify({
            'message': '分析完成',
            'feedback': feedback.to_dict(),
            'analysis': result
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500