
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
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = str(Config.UPLOAD_FOLDER)
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
    
   
    CORS(app, supports_credentials=True, origins=['http://localhost:5173', 'http://localhost:3000'])
    
   
    db.init_app(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(admin_bp)
    
    
    with app.app_context():
        db.create_all()
        
       
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
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
       
        return {'status': 'ok', 'message': '服务运行正常'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=Config.DEBUG)

