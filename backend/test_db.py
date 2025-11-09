"""测试数据库连接"""
from app import create_app
from models import db, User

app = create_app()
with app.app_context():
    try:
        users = User.query.all()
        print(f'Database OK: {len(users)} users found')
        for u in users:
            print(f'  - {u.username} ({u.role})')
    except Exception as e:
        print(f'Database Error: {str(e)}')
        import traceback
        traceback.print_exc()

