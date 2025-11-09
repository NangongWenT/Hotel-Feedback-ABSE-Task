# 酒店反馈分析系统 - 启动脚本
# 使用方法：在 PowerShell 中运行 .\启动脚本.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  酒店反馈分析系统 - 启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "⚠️  检测到 Node.js 未在 PATH 中，正在临时添加..." -ForegroundColor Yellow
    $env:PATH += ";C:\Program Files\nodejs"
}

# 检查 Node.js 和 npm
try {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
    Write-Host "✅ npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js 未安装或无法访问" -ForegroundColor Red
    Write-Host "请先安装 Node.js: https://nodejs.org/zh-cn/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "请选择要启动的服务：" -ForegroundColor Cyan
Write-Host "1. 启动后端服务（Flask）" -ForegroundColor White
Write-Host "2. 启动前端服务（Vite）" -ForegroundColor White
Write-Host "3. 同时启动后端和前端（需要两个终端）" -ForegroundColor White
Write-Host ""
$choice = Read-Host "请输入选项 (1/2/3)"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $projectRoot "backend"
$frontendPath = Join-Path $projectRoot "frontend"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "正在启动后端服务..." -ForegroundColor Cyan
        Write-Host "后端地址: http://localhost:5000" -ForegroundColor Green
        Write-Host ""
        Set-Location $backendPath
        & ".\venv\Scripts\python.exe" app.py
    }
    "2" {
        Write-Host ""
        Write-Host "正在启动前端服务..." -ForegroundColor Cyan
        Write-Host "前端地址: http://localhost:5173" -ForegroundColor Green
        Write-Host ""
        Set-Location $frontendPath
        npm run dev
    }
    "3" {
        Write-Host ""
        Write-Host "⚠️  需要打开两个终端窗口" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "终端 1 - 后端服务：" -ForegroundColor Cyan
        Write-Host "  cd `"$backendPath`"" -ForegroundColor White
        Write-Host "  .\venv\Scripts\python.exe app.py" -ForegroundColor White
        Write-Host ""
        Write-Host "终端 2 - 前端服务：" -ForegroundColor Cyan
        Write-Host "  cd `"$frontendPath`"" -ForegroundColor White
        Write-Host "  npm run dev" -ForegroundColor White
        Write-Host ""
        Write-Host "按任意键退出..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    }
    default {
        Write-Host "无效选项" -ForegroundColor Red
    }
}

