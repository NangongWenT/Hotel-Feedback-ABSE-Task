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
    
    # 设备配置：优先使用GPU，即使计算能力不完全兼容也尝试使用
    # 检查CUDA是否可用
    if torch.cuda.is_available():
        try:
            device_capability = torch.cuda.get_device_capability(0)
            device_capability_str = f"sm_{device_capability[0]}{device_capability[1]}"
            
            # PyTorch 2.5.1 支持的计算能力
            supported_capabilities = ['sm_50', 'sm_60', 'sm_61', 'sm_70', 'sm_75', 'sm_80', 'sm_86', 'sm_90']
            
            # 尝试强制使用 GPU，即使计算能力不完全兼容
            # PyTorch 可能会使用兼容模式运行
            try:
                # 设置环境变量，尝试使用兼容模式
                import os
                # 尝试设置 CUDA 架构列表，强制使用兼容的 kernel
                os.environ.setdefault('TORCH_CUDA_ARCH_LIST', '9.0')  # 尝试使用 sm_90 的 kernel
                
                # 测试 GPU 是否真的可以工作
                test_tensor = torch.zeros(1).cuda()
                # 尝试一个简单的操作
                result = test_tensor + 1
                del test_tensor, result
                torch.cuda.empty_cache()
                
        DEVICE = 'cuda'
                if device_capability_str not in supported_capabilities:
                    print(f"[WARNING] GPU 计算能力 {device_capability_str} 不完全兼容，但尝试使用兼容模式")
                    print(f"   支持的计算能力: {', '.join(supported_capabilities)}")
                    print(f"   将尝试使用 GPU（兼容模式），如果失败会自动回退到 CPU")
                print(f"[OK] 检测到CUDA，将使用GPU: {torch.cuda.get_device_name(0)}")
        print(f"   CUDA版本: {torch.version.cuda}")
        print(f"   PyTorch版本: {torch.__version__}")
                print(f"   计算能力: {device_capability_str}")
            except Exception as e:
                print(f"[WARNING] GPU 测试失败: {str(e)}")
                print("   将自动回退到 CPU 模式")
                DEVICE = 'cpu'
        except Exception as e:
            print(f"[WARNING] GPU 检测失败: {str(e)}")
            print("   将自动回退到 CPU 模式")
            DEVICE = 'cpu'
    else:
        DEVICE = 'cpu'
        print("[WARNING] 未检测到CUDA，将使用CPU")
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

