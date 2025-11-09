# NVIDIA GPU 配置指南

## ✅ 检测到的硬件
- **GPU**: NVIDIA GeForce RTX 5060
- **显存**: 8GB (8151MiB)
- **CUDA 版本**: 12.8
- **驱动版本**: 573.24

## ⚠️ 当前状态
你刚才安装的是 **CPU 版本的 PyTorch**，需要重新安装支持 CUDA 的版本才能使用 GPU 加速。

---

## 📦 安装支持 CUDA 的 PyTorch

### 步骤 1：卸载 CPU 版本的 PyTorch

在 PowerShell 中执行（**注意：不需要激活虚拟环境，直接执行**）：

```powershell
# 进入后端目录
cd backend

# 卸载 CPU 版本的 PyTorch
pip uninstall torch torchvision torchaudio -y
```

### 步骤 2：安装 CUDA 12.1 版本的 PyTorch

你的系统显示 CUDA 12.8，但 PyTorch 官方支持 CUDA 12.1 和 12.4。CUDA 12.8 向后兼容，可以使用 CUDA 12.1 版本的 PyTorch。

```powershell
# 安装支持 CUDA 12.1 的 PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**或者，如果你想使用 CUDA 12.4（如果可用）：**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
```

### 步骤 3：验证 CUDA 安装

安装完成后，验证 GPU 是否可用：

```powershell
python -c "import torch; print(f'CUDA 可用: {torch.cuda.is_available()}'); print(f'GPU 名称: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"无\"}')"
```

**期望输出：**
```
CUDA 可用: True
GPU 名称: NVIDIA GeForce RTX 5060
```

---

## 🔧 解决 PowerShell 执行策略问题

虽然依赖已经安装成功，但虚拟环境激活失败。有两种解决方案：

### 方案 1：修改执行策略（推荐）

**以管理员身份运行 PowerShell**，然后执行：

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

然后就可以正常激活虚拟环境了：
```powershell
cd backend
.\venv\Scripts\activate
```

### 方案 2：直接使用 Python（无需激活虚拟环境）

如果不想修改执行策略，可以直接使用虚拟环境中的 Python：

```powershell
# 进入后端目录
cd backend

# 直接使用虚拟环境中的 Python（不需要激活）
.\venv\Scripts\python.exe app.py
```

或者使用完整路径：
```powershell
.\venv\Scripts\python.exe -m pip install ...
```

---

## 🚀 完整安装流程（GPU 版本）

### 1. 卸载 CPU 版本的 PyTorch

```powershell
cd backend
pip uninstall torch torchvision torchaudio -y
```

### 2. 安装 CUDA 版本的 PyTorch

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 3. 验证安装

```powershell
python -c "import torch; print(f'CUDA 可用: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\"}')"
```

### 4. 启动后端服务

**方法 A：激活虚拟环境后启动**
```powershell
# 先修改执行策略（管理员 PowerShell）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后激活虚拟环境
cd backend
.\venv\Scripts\activate
python app.py
```

**方法 B：直接使用虚拟环境 Python（无需激活）**
```powershell
cd backend
.\venv\Scripts\python.exe app.py
```

---

## 📊 性能对比

使用 GPU 后，模型推理速度会显著提升：

- **CPU**: 每条反馈分析约 2-5 秒
- **GPU (RTX 5060)**: 每条反馈分析约 0.1-0.3 秒

**提升约 10-50 倍！**

---

## ⚠️ 常见问题

### Q1: 安装 PyTorch 时提示找不到 CUDA？

**A:** 确保 CUDA 驱动已正确安装。你已经有了 CUDA 12.8，应该没问题。如果遇到问题，可以尝试：
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Q2: 验证时显示 CUDA 不可用？

**A:** 检查以下几点：
1. 确保已卸载 CPU 版本的 PyTorch
2. 确保安装了 CUDA 版本的 PyTorch
3. 重启 PowerShell 窗口
4. 检查 NVIDIA 驱动是否最新

### Q3: 显存不足？

**A:** 你的 RTX 5060 有 8GB 显存，足够运行 Qwen2-1.5B-Instruct 模型（约需 3GB）。如果遇到显存不足：
- 关闭其他占用 GPU 的程序
- 使用量化模型（需要修改代码）

### Q4: 启动时仍然显示 "未检测到CUDA"？

**A:** 
1. 确认 PyTorch 已正确安装 CUDA 版本
2. 运行验证命令检查
3. 查看启动日志，确认设备检测信息

---

## ✅ 验证清单

完成以下步骤后，你应该能够：

- [x] 检测到 NVIDIA GPU
- [ ] 安装 CUDA 版本的 PyTorch
- [ ] 验证 CUDA 可用
- [ ] 启动后端时显示 "✅ 检测到CUDA，将使用GPU"
- [ ] 模型推理速度明显提升

---

## 📝 快速命令总结

```powershell
# 1. 卸载 CPU 版本
cd backend
pip uninstall torch torchvision torchaudio -y

# 2. 安装 CUDA 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 3. 验证
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# 4. 启动（方法1：激活虚拟环境）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\activate
python app.py

# 4. 启动（方法2：直接使用）
.\venv\Scripts\python.exe app.py
```

