# 快速修复 Node.js PATH 问题
# 如果 node 或 npm 命令找不到，运行此脚本刷新环境变量

Write-Host "正在刷新环境变量..." -ForegroundColor Yellow

# 刷新 PATH 环境变量
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "环境变量已刷新！" -ForegroundColor Green
Write-Host ""

# 验证 Node.js 和 npm
Write-Host "验证安装..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
    Write-Host "✅ npm: $npmVersion" -ForegroundColor Green
    Write-Host ""
    Write-Host "现在可以使用 node 和 npm 命令了！" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js 未安装或未添加到 PATH" -ForegroundColor Red
    Write-Host "请确保："
    Write-Host "1. 已安装 Node.js"
    Write-Host "2. 安装时勾选了 'Add to PATH'"
    Write-Host "3. 重启 PowerShell 或运行此脚本"
}
