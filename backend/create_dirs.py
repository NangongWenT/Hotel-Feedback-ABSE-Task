"""创建必要的目录"""
from pathlib import Path

# 项目根目录（backend 的父目录）
BASE_DIR = Path(__file__).parent.parent

# 创建目录
dirs = [
    BASE_DIR / 'data',
    BASE_DIR / 'data' / 'uploads',
    BASE_DIR / 'model' / 'cache'
]

for dir_path in dirs:
    dir_path.mkdir(parents=True, exist_ok=True)
    print(f'Directory created: {dir_path}')

print('\nAll directories created successfully!')

