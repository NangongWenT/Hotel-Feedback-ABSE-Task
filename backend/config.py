"""
项目配置文件
"""
import torch
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent.parent

class Config:
    """配置类"""
    # 数据库配置
    DATABASE_URL = f'sqlite:///{BASE_DIR / "data" / "hotel_feedback.db"}'
    
    # 模型配置
    # 推荐模型（8GB GPU，中英文支持好）：
    # - Qwen/Qwen2-1.5B-Instruct (1.5B参数，显存占用约3GB，推荐)
    # - Qwen/Qwen2-3B-Instruct (3B参数，显存占用约6GB)
    # - Qwen/Qwen2-7B-Instruct (7B参数，显存占用约14GB，需要量化)
    MODEL_NAME = 'Qwen/Qwen2-1.5B-Instruct'  # 适合8GB GPU，中英文表现优秀
    MODEL_CACHE_DIR = BASE_DIR / 'model' / 'cache'
    # 自动检测CUDA，如果有GPU则使用cuda
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Flask配置
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    DEBUG = True
    
    # 文件上传配置
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx', 'xls'}
    
    # 用户配置
    DEFAULT_ADMIN_USERNAME = 'admin'
    DEFAULT_ADMIN_PASSWORD = 'admin123'  # 生产环境请修改

