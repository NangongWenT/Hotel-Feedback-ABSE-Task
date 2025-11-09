# 快速重启后端脚本

Write-Host "正在停止可能运行的后端进程..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*backend*"} | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "正在启动后端服务..." -ForegroundColor Yellow
Write-Host ""

$backendPath = Join-Path $PSScriptRoot "backend"
if (-not (Test-Path $backendPath)) {
    Write-Host "[ERROR] 后端目录不存在: $backendPath" -ForegroundColor Red
    exit 1
}

Set-Location $backendPath

# 启动后端
Write-Host "后端将在新窗口中启动..." -ForegroundColor Cyan
Write-Host "请查看新窗口的输出信息" -ForegroundColor Gray
Write-Host ""

$script = @"
cd `"$backendPath`"
.\venv\Scripts\python.exe app.py
pause
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $script

Write-Host "[OK] 后端服务已在新窗口启动" -ForegroundColor Green
Write-Host "   后端地址: http://localhost:5000" -ForegroundColor Gray
Write-Host ""
Write-Host "等待 5 秒后测试连接..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -UseBasicParsing -TimeoutSec 3
    Write-Host "[OK] 后端服务运行正常！" -ForegroundColor Green
} catch {
    Write-Host "[WARNING] 后端可能还在启动中，请查看新窗口的输出" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

