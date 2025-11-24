"""
Project Configuration File
"""
import torch
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).parent.parent

class Config:
    """Configuration Class"""
    # Database Configuration
    DATABASE_URL = f'sqlite:///{BASE_DIR / "data" / "hotel_feedback.db"}'
    
    # Model Configuration
    # Recommended models (8GB GPU, good Chinese/English support):
    # - Qwen/Qwen2-1.5B-Instruct (1.5B parameters, ~3GB VRAM usage, recommended)
    # - Qwen/Qwen2-3B-Instruct (3B parameters, ~6GB VRAM usage)
    # - Qwen/Qwen2-7B-Instruct (7B parameters, ~14GB VRAM usage, requires quantization)
    MODEL_NAME = 'Qwen/Qwen2-1.5B-Instruct'  # Suitable for 8GB GPU, excellent performance in Chinese/English
    MODEL_CACHE_DIR = BASE_DIR / 'model' / 'cache'
    
    # Device Configuration: Prioritize GPU
    # Check if CUDA is available
    if torch.cuda.is_available():
        DEVICE = 'cuda'
        print(f"✅ CUDA detected, will use GPU: {torch.cuda.get_device_name(0)}")
        print(f"   CUDA version: {torch.version.cuda}")
        print(f"   PyTorch version: {torch.__version__}")
    else:
        DEVICE = 'cpu'
        print("⚠️  CUDA not detected, will use CPU")
        print("   Note: To use GPU, please ensure:")
        print("   1. NVIDIA GPU drivers are installed")
        print("   2. CUDA toolkit is installed")
        print("   3. CUDA-enabled PyTorch version is installed")
        print("   Installation command: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
    
    # Flask Configuration
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    DEBUG = True
    
    # File Upload Configuration
    UPLOAD_FOLDER = BASE_DIR / 'data' / 'uploads'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB (supports batch processing of 10,000 reviews)
    ALLOWED_EXTENSIONS = {'txt', 'csv', 'xlsx', 'xls', 'json'}
    
    # User Configuration
    DEFAULT_ADMIN_USERNAME = 'admin'
    DEFAULT_ADMIN_PASSWORD = 'admin123'  # Change in production environment

