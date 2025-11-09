# 安装 PyTorch Nightly 版本以支持 RTX 5060 GPU

## 🎯 目标

安装 PyTorch Nightly 版本，可能支持 RTX 5060 的 sm_120 计算能力。

## ⚠️ 重要提示

1. **Nightly 版本是实验性的**，可能不稳定
2. **可能仍然不支持 sm_120**，需要测试
3. **如果失败，会自动回退到 CPU 模式**

## 📝 安装步骤

### 步骤 1：卸载当前 PyTorch

```powershell
cd "C:\Users\32353\Desktop\大四上\NLP\CW\Hotel-Feedback-ABSA-Task-main\backend"
.\venv\Scripts\python.exe -m pip uninstall torch torchvision torchaudio -y
```

### 步骤 2：安装 PyTorch Nightly 版本

```powershell
.\venv\Scripts\python.exe -m pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
```

### 步骤 3：验证安装

```powershell
.\venv\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
```

### 步骤 4：测试 GPU 兼容性

```powershell
.\venv\Scripts\python.exe -c "import torch; device = torch.cuda.get_device_capability(0); print(f'计算能力: sm_{device[0]}{device[1]}'); test = torch.zeros(1).cuda(); print('GPU 测试成功！'); del test"
```

**如果看到 "GPU 测试成功！"，说明 GPU 可以工作！** ✅

### 步骤 5：重启后端

```powershell
.\venv\Scripts\python.exe app.py
```

查看启动信息，应该会显示：
```
✅ 检测到CUDA，将使用GPU: NVIDIA GeForce RTX 5060 Laptop GPU
```

## 🔄 如果 Nightly 版本仍然不支持

如果 Nightly 版本仍然不支持 sm_120，可以：

1. **回退到稳定版本**：
   ```powershell
   .\venv\Scripts\python.exe -m pip uninstall torch torchvision torchaudio -y
   .\venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

2. **等待 PyTorch 正式更新**：定期检查 PyTorch 更新

3. **使用 CPU 模式**：虽然慢，但可以正常工作

## 📋 验证清单

- [ ] PyTorch Nightly 已安装
- [ ] CUDA 可用：True
- [ ] GPU 测试成功
- [ ] 后端启动时显示使用 GPU
- [ ] 分析速度明显提升

## ⚠️ 注意事项

1. **Nightly 版本可能不稳定**，如果遇到问题，可以回退
2. **定期更新**：Nightly 版本更新频繁，可以定期更新
3. **备份当前环境**：如果担心，可以先备份虚拟环境

## 🎉 完成！

如果安装成功，你应该能够使用 GPU 加速了，速度会快很多！

