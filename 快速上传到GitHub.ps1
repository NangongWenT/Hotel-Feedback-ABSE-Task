# 快速上传代码到 GitHub 脚本

# 刷新环境变量（确保 Git 可用）
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  上传代码到 GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Git 是否安装
Write-Host "检查 Git 安装..." -ForegroundColor Yellow
try {
    $gitVersion = & git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Git 已安装: $gitVersion" -ForegroundColor Green
    } else {
        throw "Git 未找到"
    }
} catch {
    Write-Host "[ERROR] Git 未安装！" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装 Git:" -ForegroundColor Yellow
    Write-Host "  1. 访问: https://git-scm.com/download/win" -ForegroundColor White
    Write-Host "  2. 下载并安装 Git" -ForegroundColor White
    Write-Host "  3. 重新运行此脚本" -ForegroundColor White
    Write-Host ""
    Write-Host "按任意键退出..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""

# 进入项目目录
$projectPath = $PSScriptRoot
Set-Location $projectPath
Write-Host "项目目录: $projectPath" -ForegroundColor Gray
Write-Host ""

# 检查是否已初始化 Git 仓库
if (-not (Test-Path ".git")) {
    Write-Host "初始化 Git 仓库..." -ForegroundColor Yellow
    & git init
    Write-Host "[OK] Git 仓库已初始化" -ForegroundColor Green
    Write-Host ""
}

# 检查远程仓库
Write-Host "检查远程仓库..." -ForegroundColor Yellow
$remoteUrl = & git remote get-url origin 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARNING] 未设置远程仓库" -ForegroundColor Yellow
    Write-Host ""
    $repoUrl = Read-Host "请输入 GitHub 仓库地址 (例如: https://github.com/用户名/仓库名.git)"
    if ($repoUrl) {
        & git remote add origin $repoUrl
        Write-Host "[OK] 远程仓库已添加" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] 未提供仓库地址，退出" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[OK] 远程仓库: $remoteUrl" -ForegroundColor Green
}
Write-Host ""

# 询问版本号
Write-Host "选择版本管理方式:" -ForegroundColor Yellow
Write-Host "  1. 创建新分支 (例如: v2.0)" -ForegroundColor White
Write-Host "  2. 创建标签 (例如: v2.0)" -ForegroundColor White
Write-Host "  3. 直接推送到主分支" -ForegroundColor White
Write-Host ""
$choice = Read-Host "请选择 (1/2/3)"

$versionName = ""
if ($choice -eq "1" -or $choice -eq "2") {
    $versionName = Read-Host "请输入版本号 (例如: v2.0)"
    if (-not $versionName) {
        $versionName = "v2.0"
        Write-Host "使用默认版本号: $versionName" -ForegroundColor Gray
    }
}
Write-Host ""

# 添加文件
Write-Host "添加文件到暂存区..." -ForegroundColor Yellow
& git add .
Write-Host "[OK] 文件已添加" -ForegroundColor Green
Write-Host ""

# 提交
Write-Host "提交更改..." -ForegroundColor Yellow
$commitMessage = "版本更新: 修复编码问题和登录功能，优化情感分析"
if ($versionName) {
    $commitMessage = "版本 $versionName : 修复编码问题和登录功能，优化情感分析"
}
& git commit -m $commitMessage
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] 更改已提交" -ForegroundColor Green
} else {
    Write-Host "[WARNING] 没有需要提交的更改" -ForegroundColor Yellow
}
Write-Host ""

# 根据选择执行操作
if ($choice -eq "1") {
    # 创建新分支
    Write-Host "创建新分支: $versionName" -ForegroundColor Yellow
    & git checkout -b $versionName
    Write-Host "[OK] 分支已创建并切换" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "推送到 GitHub..." -ForegroundColor Yellow
    & git push -u origin $versionName
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] 代码已推送到分支: $versionName" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] 推送失败，请检查网络连接和权限" -ForegroundColor Red
    }
} elseif ($choice -eq "2") {
    # 创建标签
    Write-Host "创建标签: $versionName" -ForegroundColor Yellow
    & git tag -a $versionName -m "版本 $versionName : 修复编码问题和登录功能"
    Write-Host "[OK] 标签已创建" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "推送到 GitHub..." -ForegroundColor Yellow
    & git push origin main
    & git push origin $versionName
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] 代码和标签已推送" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] 推送失败，请检查网络连接和权限" -ForegroundColor Red
    }
} else {
    # 直接推送
    Write-Host "推送到 GitHub (主分支)..." -ForegroundColor Yellow
    & git push origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] 代码已推送" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] 推送失败，请检查网络连接和权限" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

