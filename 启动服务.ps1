# 启动前后端服务脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  酒店反馈分析系统 - 服务启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 刷新环境变量
Write-Host "刷新环境变量..." -ForegroundColor Yellow
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 检查 Node.js
Write-Host "检查 Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js 未找到，请先安装 Node.js" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动后端服务..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$backendPath = Join-Path $PSScriptRoot "backend"
if (-not (Test-Path $backendPath)) {
    Write-Host "❌ 后端目录不存在: $backendPath" -ForegroundColor Red
    exit 1
}

# 启动后端（新窗口）
Write-Host "正在启动后端服务（新窗口）..." -ForegroundColor Yellow
$backendScript = @"
cd `"$backendPath`"
.\venv\Scripts\python.exe app.py
pause
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript

Write-Host "✅ 后端服务已在新窗口启动" -ForegroundColor Green
Write-Host "   后端地址: http://localhost:5000" -ForegroundColor Gray
Write-Host ""

Start-Sleep -Seconds 3

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动前端服务..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$frontendPath = Join-Path $PSScriptRoot "frontend"
if (-not (Test-Path $frontendPath)) {
    Write-Host "❌ 前端目录不存在: $frontendPath" -ForegroundColor Red
    exit 1
}

# 检查前端依赖
if (-not (Test-Path (Join-Path $frontendPath "node_modules"))) {
    Write-Host "⚠️  前端依赖未安装，正在安装..." -ForegroundColor Yellow
    Set-Location $frontendPath
    npm.cmd install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 前端依赖安装失败" -ForegroundColor Red
        exit 1
    }
}

# 启动前端（新窗口）
Write-Host "正在启动前端服务（新窗口）..." -ForegroundColor Yellow
$frontendScript = @"
`$env:Path = [System.Environment]::GetEnvironmentVariable(`"Path`",`"Machine`") + `";`" + [System.Environment]::GetEnvironmentVariable(`"Path`",`"User`")
cd `"$frontendPath`"
npm.cmd run dev
pause
"@

Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript

Write-Host "✅ 前端服务已在新窗口启动" -ForegroundColor Green
Write-Host "   前端地址: http://localhost:5173" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "服务信息：" -ForegroundColor Yellow
Write-Host "  - 后端: http://localhost:5000" -ForegroundColor White
Write-Host "  - 前端: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "访问系统：" -ForegroundColor Yellow
Write-Host "  打开浏览器访问: http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "默认账户：" -ForegroundColor Yellow
Write-Host "  用户名: admin" -ForegroundColor White
Write-Host "  密码: admin123" -ForegroundColor White
Write-Host ""
Write-Host "提示：两个服务窗口已打开，关闭窗口会停止对应的服务" -ForegroundColor Gray
Write-Host ""

