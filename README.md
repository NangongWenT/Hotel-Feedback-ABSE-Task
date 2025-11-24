# Hotel Feedback Analysis System

A hotel feedback sentiment analysis system based on the Qwen2-1.5B-Instruct large language model.

## Features

- ✅ User login/registration
- ✅ Feedback submission and sentiment analysis
- ✅ Five-level sentiment classification (very positive, positive, neutral, negative, very negative)
- ✅ Aspect-based sentiment analysis (room, service, location, value, etc.)
- ✅ Bilingual support (English and Chinese)
- ✅ Feedback list viewing
- ✅ Admin statistics functionality
- ✅ Batch upload and analysis
- ✅ Data visualization dashboard
 

## Technology Stack

### Backend
- Flask 3.0
- SQLAlchemy
- Transformers (Qwen2-1.5B-Instruct)
- PyTorch
- Accelerate (GPU acceleration)

### Frontend
- React 18
- Vite
- Ant Design 5
- React Router
- Recharts (data visualization)
- CSS-in-JS (styling with glassmorphism effects)

## System Requirements

### Basic Requirements
- **Python**: 3.8 or higher
- **Node.js**: 16.0 or higher
- **npm**: 8.0 or higher

### GPU Requirements (Recommended)
- **NVIDIA GPU**: 8GB+ VRAM (recommended)
- **CUDA**: 11.8 or 12.1 (Windows/Linux)
- **macOS**: Apple Silicon (M1/M2/M3) with Metal Performance Shaders (MPS) support

### CPU Operation
- The system can run on CPU, but with slower performance
- Minimum 8GB RAM recommended

## Installation and Setup

### Windows Installation Guide

#### 1. Install Python

1. Download Python 3.8+ from [Python官网](https://www.python.org/downloads/)
2. Check "Add Python to PATH" during installation
3. Verify installation:
```powershell
python --version
```

#### 2. Install CUDA (for GPU usage)

**Check for NVIDIA GPU:**
```powershell
nvidia-smi
```

**If GPU is available, install CUDA-supported PyTorch:**

1. Uninstall CPU version of PyTorch (if installed):
```powershell
pip uninstall torch torchvision torchaudio -y
```

2. Install PyTorch according to CUDA version:

**CUDA 11.8 (Recommended):**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**CUDA 12.1:**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

3. Verify CUDA installation:
```powershell
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

#### 3. Backend Setup

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Note:** If using GPU, ensure CUDA-supported PyTorch is installed before installing other dependencies.

#### 4. Frontend Setup

```powershell
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

#### 5. Start Services

**Backend (in a new terminal):**
```powershell
cd backend
venv\Scripts\activate
python app.py
```

Backend will run on `http://localhost:5000`

**Frontend (in a new terminal):**
```powershell
cd frontend
npm run dev
```

Frontend will run on `http://localhost:5173`

---

### macOS Installation Guide

#### 1. Install Python

**Using Homebrew (Recommended):**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.11
```

**Or download from官网:**
Download macOS installer from [Python官网](https://www.python.org/downloads/)

Verify installation:
```bash
python3 --version
```

#### 2. GPU Support (Apple Silicon)

**Apple Silicon (M1/M2/M3) automatically supports Metal Performance Shaders (MPS):**

PyTorch will automatically detect and use MPS if available. Use standard command for installation:

```bash
pip install torch torchvision torchaudio
```

Verify MPS:
```bash
python3 -c "import torch; print(f'MPS available: {torch.backends.mps.is_available()}')"
```

**Intel Mac:**
Can only run on CPU, with slower performance.

#### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python3 -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### 4. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

#### 5. Start Services

**Backend (in a new terminal):**
```bash
cd backend
source venv/bin/activate
python3 app.py
```

Backend will run on `http://localhost:5000`

**Frontend (in a new terminal):**
```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:5173`

---

## Dependency Notes

### Backend Dependencies (`backend/requirements.txt`)

| Package | Version | Description |
|---------|---------|-------------|
| flask | 3.0.0 | Web framework |
| flask-sqlalchemy | 3.1.1 | ORM |
| flask-cors | 4.0.0 | CORS support |
| transformers | 4.57.1 | HuggingFace model library |
| torch | >=2.0.0 | Deep learning framework |
| accelerate | >=0.20.0 | GPU acceleration library |
| pandas | >=2.0.0 | Data processing |
| openpyxl | >=3.1.0 | Excel file support |
| huggingface-hub | >=0.20.0 | Model download |

**Important Notes:**
- **Windows + GPU**: Requires CUDA-supported PyTorch (see Windows installation guide above)
- **macOS + Apple Silicon**: PyTorch automatically uses MPS, no additional configuration needed
- **CPU operation**: Use standard `pip install torch`

### Frontend Dependencies (`frontend/package.json`)

| Package | Version | Description |
|---------|---------|-------------|
| react | ^18.2.0 | UI framework |
| react-router-dom | ^6.20.0 | Routing |
| antd | ^5.11.0 | UI component library |
| recharts | ^2.10.3 | Charting library |
| axios | ^1.6.2 | HTTP client |
| vite | ^5.0.8 | Build tool |

---

## Project Structure

```
hotel_feedback/
├── backend/                 # Backend code
│   ├── app.py              # Flask main application
│   ├── config.py            # Configuration file
│   ├── models.py            # Database models
│   ├── requirements.txt     # Python dependencies
│   ├── routes/              # Routes
│   │   ├── auth.py          # Authentication routes
│   │   ├── feedback.py      # Feedback routes
│   │   ├── analysis.py      # Analysis routes
│   │   └── admin.py         # Admin routes
│   ├── services/            # Services
│   │   └── sentiment_analyzer.py  # Sentiment analysis service
│   └── utils/               # Utilities
│       ├── language_detector.py    # Language detection
│       └── file_parser.py          # File parsing
├── frontend/                # Frontend code
│   ├── package.json         # Node.js dependencies
│   ├── src/
│   │   ├── components/      # Components
│   │   ├── pages/           # Pages
│   │   ├── contexts/        # Contexts
│   │   └── services/        # API services
├── data/                    # Data directory
│   └── hotel_feedback.db    # SQLite database
└── model/                   # Model cache
    └── cache/
        └── Qwen--Qwen2-1.5B-Instruct/
```

---

## Default Accounts

- **Admin**: `admin` / `admin123`

**⚠️ Security Note**: Always change default passwords in production environments!

---

## Model Configuration

The system uses the `Qwen/Qwen2-1.5B-Instruct` model, suitable for 8GB GPUs.

### Model Requirements
- **GPU VRAM**: Approximately 3GB (FP16)
- **CPU Memory**: Approximately 4GB
- **Model Size**: Approximately 3GB

### Model File Location

Models are automatically loaded from local cache (`model/cache/Qwen--Qwen2-1.5B-Instruct/`).

If the model is not downloaded, ensure:
1. Model files are downloaded to `model/cache/Qwen--Qwen2-1.5B-Instruct/` directory
2. Contains the following files:
   - `model.safetensors` or `pytorch_model.bin`
   - `tokenizer.json`
   - `tokenizer_config.json`
   - `config.json`

### Device Selection

The system automatically detects and uses the best available device:
- **Windows/Linux**: Prefers CUDA (GPU), falls back to CPU
- **macOS (Apple Silicon)**: Prefers MPS (GPU), falls back to CPU
- **macOS (Intel)**: Uses CPU

Device information is displayed on startup.

---

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

### Feedback
- `POST /api/feedback/submit` - Submit feedback
- `POST /api/feedback/batch-upload` - Batch upload feedback
- `GET /api/feedback/list` - Get feedback list
- `GET /api/feedback/<id>` - Get feedback details

### Analysis (Admin Only)
- `POST /api/analysis/sentiment` - Analyze sentiment
- `POST /api/analysis/aspect` - Analyze specific aspect
- `POST /api/analysis/aspects` - Analyze all aspects
- `POST /api/analysis/batch` - Batch analysis

### Admin
- `GET /api/admin/stats` - Get statistics
- `GET /api/admin/feedbacks` - Get all feedbacks
- `GET /api/admin/users` - Get all users
- `POST /api/admin/analyze/<feedback_id>` - Analyze single feedback

---

## Sentiment Classification

The system uses five-level sentiment classification:
- **very_positive**: 0.9
- **positive**: 0.7
- **neutral**: 0.5
- **negative**: 0.3
- **very_negative**: 0.1

---

## UI Enhancements

### Apple-style Glassmorphism Design
- Review cards feature rounded corners (30px) with glassmorphism effect
- Background blur (16px) for translucent elements
- Subtle drop shadows for depth perception
- Clean typography with good contrast

### Smooth Animations
- Natural floating animations for review cards with 6-second cycle
- Reduced animation amplitude (8px) for elegant feel
- Transition effects for state changes

### Enhanced Aspect Matrix
- Polygon-fill style aspect visualization
- Color-coded sentiment indicators
- Clear labeling of six key hotel aspects

### Layout Improvements
- Right-side area expanded to 65% of page width for better content visibility
- Improved visual hierarchy and spacing
- Optimized for both desktop and mobile views

---

## Frequently Asked Questions

### Windows-related Issues

**Q: "CUDA not available" error but I have an NVIDIA GPU?**

A: Install CUDA-supported PyTorch:
```powershell
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Q: Can't find CUDA version during PyTorch installation?**

A: Check CUDA version:
```powershell
nvidia-smi
```
Then select the corresponding PyTorch installation command based on the displayed CUDA version.

**Q: Model loading fails with "accelerate required" error?**

A: Install the accelerate library:
```powershell
pip install accelerate
```

### macOS-related Issues

**Q: How to use GPU on Apple Silicon (M1/M2/M3)?**

A: PyTorch automatically uses MPS, no additional configuration needed. Ensure you have the latest PyTorch version:
```bash
pip install torch torchvision torchaudio
```

**Q: Can Intel Macs run the system?**

A: Yes, but only on CPU with slower performance. Apple Silicon Macs are recommended.

**Q: "zsh: command not found: python" error?**

A: macOS uses `python3` by default, use:
```bash
python3 --version
python3 -m venv venv
```

### General Issues

**Q: Slow model download?**

A: You can manually download model files to the `model/cache/Qwen--Qwen2-1.5B-Instruct/` directory.

**Q: Out of memory errors?**

A: 
- GPU: Ensure at least 8GB VRAM
- CPU: Ensure at least 8GB RAM
- Consider using smaller models or quantized versions

**Q: Frontend cannot connect to backend?**

A: 
1. Ensure backend is running (`http://localhost:5000`)
2. Check API address in `frontend/src/services/api.js`
3. Verify CORS configuration

**Q: Database errors?**

A: Delete the `data/hotel_feedback.db` file and restart the backend to create a new database automatically.

---

## Development Notes

### Environment Variables

Configuration can be modified in `backend/config.py`:
- `MODEL_NAME`: Model name
- `DEVICE`: Device type (auto-detected)
- `DATABASE_URL`: Database path

### Debug Mode

Backend runs in debug mode by default, frontend uses Vite hot reload.

---

## License

MIT License

---

## Changelog

### v1.0.0
- ✅ Basic functionality implementation
- ✅ GPU/CPU auto-detection
- ✅ Windows/macOS support
- ✅ Batch upload and analysis
- ✅ Data visualization dashboard


