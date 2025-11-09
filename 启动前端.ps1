# 启动前端服务器脚本

Write-Host "正在刷新环境变量..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "验证 Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
    Write-Host "✅ npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js 未找到，请先安装 Node.js" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "检查前端目录..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
if (-not (Test-Path $frontendPath)) {
    Write-Host "❌ 前端目录不存在: $frontendPath" -ForegroundColor Red
    exit 1
}

Write-Host "✅ 前端目录存在" -ForegroundColor Green
Write-Host ""

Write-Host "进入前端目录..." -ForegroundColor Yellow
Set-Location $frontendPath

Write-Host "检查 node_modules..." -ForegroundColor Yellow
if (-not (Test-Path "node_modules")) {
    Write-Host "⚠️  node_modules 不存在，正在安装依赖..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 依赖安装失败" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✅ node_modules 存在" -ForegroundColor Green
}

Write-Host ""
Write-Host "正在启动前端开发服务器..." -ForegroundColor Yellow
Write-Host "前端将在 http://localhost:5173 运行" -ForegroundColor Cyan
Write-Host "按 Ctrl+C 停止服务器" -ForegroundColor Gray
Write-Host ""

# 启动前端服务器
npm run dev

