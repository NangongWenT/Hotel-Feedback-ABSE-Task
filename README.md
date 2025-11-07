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

## 技术栈

### 后端
- Flask 3.0
- SQLAlchemy
- Transformers (Qwen2-1.5B-Instruct)
- PyTorch

### 前端
- React 18
- Vite
- Ant Design 5
- React Router

## 项目结构

```
hotel_feedback/
├── backend/                 # 后端代码
│   ├── app.py              # Flask主应用
│   ├── config.py            # 配置文件
│   ├── models.py            # 数据库模型
│   ├── routes/              # 路由
│   │   ├── auth.py          # 认证路由
│   │   ├── feedback.py      # 反馈路由
│   │   ├── analysis.py      # 分析路由
│   │   └── admin.py         # 管理员路由
│   ├── services/            # 服务
│   │   ├── sentiment_analyzer.py  # 情感分析服务
│   │   └── aspect_extractor.py     # 方面提取服务
│   └── utils/               # 工具
│       ├── language_detector.py    # 语言检测
│       ├── file_parser.py          # 文件解析
│       └── export.py               # 导出工具
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── components/      # 组件
│   │   ├── pages/           # 页面
│   │   ├── contexts/        # 上下文
│   │   └── services/        # API服务
│   └── package.json
├── data/                    # 数据目录
│   └── hotel_feedback.db    # SQLite数据库
└── model/                   # 模型缓存
    └── cache/
        └── Qwen--Qwen2-1.5B-Instruct/
```

## 安装与运行

### 1. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（Windows）
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

### 3. 启动服务

**后端：**
```bash
cd backend
venv\Scripts\activate
python app.py
```

后端将在 `http://localhost:5000` 运行

**前端：**
```bash
cd frontend
npm run dev
```

前端将在 `http://localhost:5173` 运行

## 默认账户

- **管理员**: `admin` / `admin123`

## 模型配置

系统使用 `Qwen/Qwen2-1.5B-Instruct` 模型，适合 8GB GPU。

模型会自动从本地缓存加载（`model/cache/Qwen--Qwen2-1.5B-Instruct/`）。

如果模型未下载，请确保：
1. 模型文件已下载到 `model/cache/Qwen--Qwen2-1.5B-Instruct/` 目录
2. 包含以下文件：
   - `model.safetensors`
   - `tokenizer.json`
   - `tokenizer_config.json`
   - `config.json`

## API 端点

### 认证
- `POST /api/auth/login` - 登录
- `POST /api/auth/logout` - 登出
- `GET /api/auth/me` - 获取当前用户

### 反馈
- `POST /api/feedback/submit` - 提交反馈
- `GET /api/feedback/list` - 获取反馈列表
- `GET /api/feedback/<id>` - 获取反馈详情

### 分析
- `POST /api/analysis/sentiment` - 分析情感
- `POST /api/analysis/aspect` - 分析特定方面
- `POST /api/analysis/aspects` - 分析所有方面

### 管理员
- `GET /api/admin/stats` - 获取统计信息
- `GET /api/admin/feedbacks` - 获取所有反馈
- `GET /api/admin/users` - 获取所有用户

## 情感分类

系统使用五档情感分类：
- **very_positive** (非常积极): 0.9
- **positive** (积极): 0.7
- **neutral** (中性): 0.5
- **negative** (负面): 0.3
- **very_negative** (非常负面): 0.1

## 注意事项

1. **首次运行**: 确保模型文件已下载到本地
2. **GPU要求**: 推荐使用 NVIDIA GPU（8GB+ 显存）
3. **数据库**: 首次运行会自动创建 SQLite 数据库
4. **生产环境**: 请修改 `config.py` 中的 `SECRET_KEY` 和默认密码

## 许可证

MIT License

