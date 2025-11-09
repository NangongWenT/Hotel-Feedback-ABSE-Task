"""
认证路由
"""
from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from models import db, User
from config import Config

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return jsonify({
                'message': '登录成功',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({'error': '用户名或密码错误'}), 401
            
    except Exception as e:
        return jsonify({'error': f'登录失败: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """用户登出"""
    session.clear()
    return jsonify({'message': '登出成功'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """获取当前用户信息"""
    if 'user_id' not in session:
        return jsonify({'error': '未登录'}), 401
    
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册（仅用于创建普通用户）"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': '用户名已存在'}), 400
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role='user'
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': '注册成功',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'注册失败: {str(e)}'}), 500

