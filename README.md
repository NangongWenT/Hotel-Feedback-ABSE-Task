# 酒店反馈分析系统

基于 Qwen2-1.5B-Instruct 大语言模型的酒店反馈情感分析系统。

## 功能特性

- ✅ 用户登录/注册
- ✅ 反馈提交与情感分析
- ✅ 五档情感分类（非常积极、积极、中性、负面、非常负面）
- ✅ 方面情感分析（房间、服务、位置、价格等）
- ✅ 中英文支持
- ✅ 反馈列表查看
- ✅ 管理员统计功能
- ✅ 批量上传与分析
- ✅ 数据可视化Dashboard

## 技术栈

### 后端
- Flask 3.0
- SQLAlchemy
- Transformers (Qwen2-1.5B-Instruct)
- PyTorch
- Accelerate (GPU加速)

### 前端
- React 18
- Vite
- Ant Design 5
- React Router
- Recharts (数据可视化)

## 系统要求

### 基础要求
- **Python**: 3.8 或更高版本
- **Node.js**: 16.0 或更高版本
- **npm**: 8.0 或更高版本

### GPU要求（推荐）
- **NVIDIA GPU**: 8GB+ 显存（推荐）
- **CUDA**: 11.8 或 12.1（Windows/Linux）
- **macOS**: 支持 Metal Performance Shaders (MPS) 的 Apple Silicon (M1/M2/M3)

### CPU运行
- 系统可以在CPU上运行，但速度较慢
- 推荐至少 8GB RAM

## 安装与运行

### Windows 安装指南

#### 1. 安装 Python

1. 从 [Python官网](https://www.python.org/downloads/) 下载 Python 3.8+
2. 安装时勾选 "Add Python to PATH"
3. 验证安装：
```powershell
python --version
```

#### 2. 安装 CUDA（如需使用GPU）

**检查是否有NVIDIA GPU：**
```powershell
nvidia-smi
```

**如果有GPU，安装支持CUDA的PyTorch：**

1. 卸载CPU版本的PyTorch（如果已安装）：
```powershell
pip uninstall torch torchvision torchaudio -y
```

2. 根据CUDA版本安装PyTorch：

**CUDA 11.8（推荐）：**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**CUDA 12.1：**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

3. 验证CUDA安装：
```powershell
python -c "import torch; print(f'CUDA可用: {torch.cuda.is_available()}')"
```

#### 3. 后端设置

```powershell
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 升级pip
python -m pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

**注意：** 如果使用GPU，确保已安装支持CUDA的PyTorch后再安装其他依赖。

#### 4. 前端设置

```powershell
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

#### 5. 启动服务

**后端（新开一个终端）：**
```powershell
cd backend
venv\Scripts\activate
python app.py
```

后端将在 `http://localhost:5000` 运行

**前端（新开一个终端）：**
```powershell
cd frontend
npm run dev
```

前端将在 `http://localhost:5173` 运行

---

### macOS 安装指南

#### 1. 安装 Python

**使用 Homebrew（推荐）：**
```bash
# 安装 Homebrew（如果未安装）
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装 Python
brew install python@3.11
```

**或从官网下载：**
从 [Python官网](https://www.python.org/downloads/) 下载 macOS 安装包

验证安装：
```bash
python3 --version
```

#### 2. GPU支持（Apple Silicon）

**Apple Silicon (M1/M2/M3) 自动支持 Metal Performance Shaders (MPS)：**

PyTorch 会自动检测并使用 MPS（如果可用）。安装时使用标准命令即可：

```bash
pip install torch torchvision torchaudio
```

验证MPS：
```bash
python3 -c "import torch; print(f'MPS可用: {torch.backends.mps.is_available()}')"
```

**Intel Mac：**
只能使用CPU运行，速度较慢。

#### 3. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 升级pip
python3 -m pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

#### 4. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

#### 5. 启动服务

**后端（新开一个终端）：**
```bash
cd backend
source venv/bin/activate
python3 app.py
```

后端将在 `http://localhost:5000` 运行

**前端（新开一个终端）：**
```bash
cd frontend
npm run dev
```

前端将在 `http://localhost:5173` 运行

---

## 依赖说明

### 后端依赖 (`backend/requirements.txt`)

| 包名 | 版本 | 说明 |
|------|------|------|
| flask | 3.0.0 | Web框架 |
| flask-sqlalchemy | 3.1.1 | ORM |
| flask-cors | 4.0.0 | 跨域支持 |
| transformers | 4.57.1 | HuggingFace模型库 |
| torch | >=2.0.0 | 深度学习框架 |
| accelerate | >=0.20.0 | GPU加速库 |
| pandas | >=2.0.0 | 数据处理 |
| openpyxl | >=3.1.0 | Excel文件支持 |
| huggingface-hub | >=0.20.0 | 模型下载 |

**重要提示：**
- **Windows + GPU**: 需要安装支持CUDA的PyTorch（见上方Windows安装指南）
- **macOS + Apple Silicon**: PyTorch会自动使用MPS，无需额外配置
- **CPU运行**: 使用标准 `pip install torch` 即可

### 前端依赖 (`frontend/package.json`)

| 包名 | 版本 | 说明 |
|------|------|------|
| react | ^18.2.0 | UI框架 |
| react-router-dom | ^6.20.0 | 路由 |
| antd | ^5.11.0 | UI组件库 |
| recharts | ^2.10.3 | 图表库 |
| axios | ^1.6.2 | HTTP客户端 |
| vite | ^5.0.8 | 构建工具 |

---

## 项目结构

```
hotel_feedback/
├── backend/                 # 后端代码
│   ├── app.py              # Flask主应用
│   ├── config.py            # 配置文件
│   ├── models.py            # 数据库模型
│   ├── requirements.txt     # Python依赖
│   ├── routes/              # 路由
│   │   ├── auth.py          # 认证路由
│   │   ├── feedback.py      # 反馈路由
│   │   ├── analysis.py      # 分析路由
│   │   └── admin.py         # 管理员路由
│   ├── services/            # 服务
│   │   └── sentiment_analyzer.py  # 情感分析服务
│   └── utils/               # 工具
│       ├── language_detector.py    # 语言检测
│       └── file_parser.py          # 文件解析
├── frontend/                # 前端代码
│   ├── package.json         # Node.js依赖
│   ├── src/
│   │   ├── components/      # 组件
│   │   ├── pages/           # 页面
│   │   ├── contexts/        # 上下文
│   │   └── services/        # API服务
├── data/                    # 数据目录
│   └── hotel_feedback.db    # SQLite数据库
└── model/                   # 模型缓存
    └── cache/
        └── Qwen--Qwen2-1.5B-Instruct/
```

---

## 默认账户

- **管理员**: `admin` / `admin123`

**⚠️ 安全提示**: 生产环境请务必修改默认密码！

---

## 模型配置

系统使用 `Qwen/Qwen2-1.5B-Instruct` 模型，适合 8GB GPU。

### 模型要求
- **GPU显存**: 约 3GB（FP16）
- **CPU内存**: 约 4GB
- **模型大小**: 约 3GB

### 模型文件位置

模型会自动从本地缓存加载（`model/cache/Qwen--Qwen2-1.5B-Instruct/`）。

如果模型未下载，请确保：
1. 模型文件已下载到 `model/cache/Qwen--Qwen2-1.5B-Instruct/` 目录
2. 包含以下文件：
   - `model.safetensors` 或 `pytorch_model.bin`
   - `tokenizer.json`
   - `tokenizer_config.json`
   - `config.json`

### 设备选择

系统会自动检测并使用最佳设备：
- **Windows/Linux**: 优先使用 CUDA (GPU)，否则使用 CPU
- **macOS (Apple Silicon)**: 优先使用 MPS (GPU)，否则使用 CPU
- **macOS (Intel)**: 使用 CPU

启动时会显示检测到的设备信息。

---

## API 端点

### 认证
- `POST /api/auth/login` - 登录
- `POST /api/auth/logout` - 登出
- `GET /api/auth/me` - 获取当前用户

### 反馈
- `POST /api/feedback/submit` - 提交反馈
- `POST /api/feedback/batch-upload` - 批量上传反馈
- `GET /api/feedback/list` - 获取反馈列表
- `GET /api/feedback/<id>` - 获取反馈详情

### 分析（仅管理员）
- `POST /api/analysis/sentiment` - 分析情感
- `POST /api/analysis/aspect` - 分析特定方面
- `POST /api/analysis/aspects` - 分析所有方面
- `POST /api/analysis/batch` - 批量分析

### 管理员
- `GET /api/admin/stats` - 获取统计信息
- `GET /api/admin/feedbacks` - 获取所有反馈
- `GET /api/admin/users` - 获取所有用户
- `POST /api/admin/analyze/<feedback_id>` - 分析单个反馈

---

## 情感分类

系统使用五档情感分类：
- **very_positive** (非常积极): 0.9
- **positive** (积极): 0.7
- **neutral** (中性): 0.5
- **negative** (负面): 0.3
- **very_negative** (非常负面): 0.1

---

## 常见问题

### Windows 相关问题

**Q: 提示 "CUDA不可用" 但我的电脑有NVIDIA GPU？**

A: 需要安装支持CUDA的PyTorch：
```powershell
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Q: 安装PyTorch时提示找不到CUDA版本？**

A: 检查CUDA版本：
```powershell
nvidia-smi
```
然后根据显示的CUDA版本选择对应的PyTorch安装命令。

**Q: 模型加载失败，提示需要 `accelerate`？**

A: 安装accelerate库：
```powershell
pip install accelerate
```

### macOS 相关问题

**Q: Apple Silicon (M1/M2/M3) 如何使用GPU？**

A: PyTorch会自动使用MPS，无需额外配置。确保安装最新版本的PyTorch：
```bash
pip install torch torchvision torchaudio
```

**Q: Intel Mac 可以运行吗？**

A: 可以，但只能使用CPU，速度较慢。建议使用Apple Silicon Mac。

**Q: 提示 "zsh: command not found: python"？**

A: macOS默认使用 `python3`，请使用：
```bash
python3 --version
python3 -m venv venv
```

### 通用问题

**Q: 模型下载很慢？**

A: 可以手动下载模型文件到 `model/cache/Qwen--Qwen2-1.5B-Instruct/` 目录。

**Q: 内存不足？**

A: 
- GPU: 确保至少有8GB显存
- CPU: 确保至少有8GB RAM
- 可以尝试使用更小的模型或量化模型

**Q: 前端无法连接后端？**

A: 
1. 确保后端已启动（`http://localhost:5000`）
2. 检查 `frontend/src/services/api.js` 中的API地址
3. 检查CORS配置

**Q: 数据库错误？**

A: 删除 `data/hotel_feedback.db` 文件，重新启动后端会自动创建新数据库。

---

## 开发说明

### 环境变量

可以在 `backend/config.py` 中修改配置：
- `MODEL_NAME`: 模型名称
- `DEVICE`: 设备类型（自动检测）
- `DATABASE_URL`: 数据库路径

### 调试模式

后端默认开启调试模式，前端使用Vite热重载。

---

## 许可证

MIT License

---

## 更新日志

### v1.0.0
- ✅ 基础功能实现
- ✅ GPU/CPU自动检测
- ✅ Windows/macOS支持
- ✅ 批量上传与分析
- ✅ 数据可视化Dashboard
