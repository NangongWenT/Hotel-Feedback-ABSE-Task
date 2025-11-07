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
    
    # 设备配置：优先使用GPU
    # 检查CUDA是否可用
    if torch.cuda.is_available():
        DEVICE = 'cuda'
        print(f"✅ 检测到CUDA，将使用GPU: {torch.cuda.get_device_name(0)}")
        print(f"   CUDA版本: {torch.version.cuda}")
        print(f"   PyTorch版本: {torch.__version__}")
    else:
        DEVICE = 'cpu'
        print("⚠️  未检测到CUDA，将使用CPU")
        print("   提示：如需使用GPU，请确保：")
        print("   1. 已安装NVIDIA GPU驱动")
        print("   2. 已安装CUDA工具包")
        print("   3. 已安装支持CUDA的PyTorch版本")
        print("   安装命令: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    
    # Flask配置
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    DEBUG = True
    
    # 文件上传配置
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'uploads'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB（支持批量处理10000条评论）
    ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx', 'xls', 'json'}
    
    # 用户配置
    DEFAULT_ADMIN_USERNAME = 'admin'
    DEFAULT_ADMIN_PASSWORD = 'admin123'  # 生产环境请修改

