# 启动前端服务器 - 解决执行策略问题

Write-Host "正在刷新环境变量..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "验证 Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    $npmVersion = npm.cmd --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
    Write-Host "✅ npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js 未找到" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "进入前端目录..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
Set-Location $frontendPath

Write-Host "检查依赖..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules")) {
    Write-Host "⚠️  正在安装依赖..." -ForegroundColor Yellow
    npm.cmd install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 依赖安装失败" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "正在启动前端开发服务器..." -ForegroundColor Yellow
Write-Host "前端将在 http://localhost:5173 运行" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Gray
Write-Host ""

# 使用 npm.cmd 而不是 npm，避免执行策略问题
npm.cmd run dev

