"""
Flask主应用
"""
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, User
from werkzeug.security import generate_password_hash
from routes.auth import auth_bp
from routes.feedback import feedback_bp
from routes.analysis import analysis_bp
from routes.admin import admin_bp
import os

def create_app():
    """创建Flask应用"""
    try:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = str(Config.UPLOAD_FOLDER)
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
    
    # 启用CORS
    CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'http://localhost:3000'])
    
    # 初始化数据库
    db.init_app(app)
    
    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(admin_bp)
    
    # 创建数据库表
    with app.app_context():
            try:
        db.create_all()
        
        # 创建默认管理员账户（如果不存在）
        admin = User.query.filter_by(username=Config.DEFAULT_ADMIN_USERNAME).first()
        if not admin:
            admin = User(
                username=Config.DEFAULT_ADMIN_USERNAME,
                password_hash=generate_password_hash(Config.DEFAULT_ADMIN_PASSWORD),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print(f"默认管理员账户已创建: {Config.DEFAULT_ADMIN_USERNAME} / {Config.DEFAULT_ADMIN_PASSWORD}")
            except Exception as e:
                print(f"[ERROR] 数据库初始化失败: {str(e)}")
                import traceback
                traceback.print_exc()
                raise
    except Exception as e:
        print(f"[ERROR] 应用创建失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """健康检查"""
        return {'status': 'ok', 'message': '服务运行正常'}, 200
    
    @app.route('/', methods=['GET'])
    def index():
        """根路由 - 用于测试"""
        return {
            'message': '酒店反馈分析系统 API',
            'status': 'running',
            'endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'feedback': '/api/feedback',
                'analysis': '/api/analysis',
                'admin': '/api/admin'
            }
        }, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)

