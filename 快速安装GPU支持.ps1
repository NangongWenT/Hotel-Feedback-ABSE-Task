# 快速安装 PyTorch Nightly 版本以支持 RTX 5060 GPU

Write-Host "正在卸载当前 PyTorch..." -ForegroundColor Yellow
cd backend
.\venv\Scripts\python.exe -m pip uninstall torch torchvision torchaudio -y

Write-Host ""
Write-Host "正在安装 PyTorch Nightly 版本（CUDA 12.1）..." -ForegroundColor Yellow
Write-Host "这可能需要几分钟..." -ForegroundColor Gray
.\venv\Scripts\python.exe -m pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

Write-Host ""
Write-Host "验证安装..." -ForegroundColor Yellow
$result = .\venv\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"

Write-Host $result

Write-Host ""
Write-Host "测试 GPU 兼容性..." -ForegroundColor Yellow
try {
    $testResult = .\venv\Scripts\python.exe -c "import torch; device = torch.cuda.get_device_capability(0); print(f'计算能力: sm_{device[0]}{device[1]}'); test = torch.zeros(1).cuda(); print('GPU 测试成功！'); del test; torch.cuda.empty_cache()"
    Write-Host $testResult -ForegroundColor Green
    Write-Host ""
    Write-Host "✅ GPU 支持已安装并测试成功！" -ForegroundColor Green
    Write-Host "现在可以重启后端服务器使用 GPU 加速了！" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️  GPU 测试失败，可能需要使用 CPU 模式" -ForegroundColor Yellow
    Write-Host "系统会自动回退到 CPU 模式" -ForegroundColor Gray
}

Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

