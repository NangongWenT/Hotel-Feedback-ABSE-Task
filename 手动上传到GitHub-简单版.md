# 手动上传到 GitHub - 简单版

## ✅ Git 已安装

Git 版本：2.51.2.windows.1

## 🚀 快速上传步骤

### 方法 1：使用脚本（推荐）

**重要：需要先刷新环境变量**

```powershell
# 刷新环境变量
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 运行脚本
cd "C:\Users\32353\Desktop\大四上\NLP\CW\Hotel-Feedback-ABSA-Task-main"
.\快速上传到GitHub.ps1
```

### 方法 2：手动操作

**步骤 1：刷新环境变量并进入项目目录**

```powershell
# 刷新环境变量（重要！）
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 进入项目目录
cd "C:\Users\32353\Desktop\大四上\NLP\CW\Hotel-Feedback-ABSA-Task-main"
```

**步骤 2：配置 Git（首次使用）**

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

**步骤 3：初始化仓库（如果还没有）**

```powershell
git init
```

**步骤 4：添加远程仓库**

```powershell
# 替换为你的 GitHub 仓库地址
git remote add origin https://github.com/你的用户名/你的仓库名.git
```

**步骤 5：添加文件并提交**

```powershell
git add .
git commit -m "版本 2.0: 修复编码问题和登录功能，优化情感分析"
```

**步骤 6：创建新分支（保留原版本）**

```powershell
git checkout -b v2.0
```

**步骤 7：推送到 GitHub**

```powershell
git push -u origin v2.0
```

## 📝 完整命令（复制粘贴）

```powershell
# 刷新环境变量
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 进入项目目录
cd "C:\Users\32353\Desktop\大四上\NLP\CW\Hotel-Feedback-ABSA-Task-main"

# 配置 Git（首次使用，替换为你的信息）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 初始化仓库
git init

# 添加远程仓库（替换为你的地址）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 添加文件
git add .

# 提交
git commit -m "版本 2.0: 修复编码问题和登录功能，优化情感分析"

# 创建新分支
git checkout -b v2.0

# 推送
git push -u origin v2.0
```

## ⚠️ 注意事项

1. **每次打开新的 PowerShell 窗口时，需要刷新环境变量**
2. **首次推送可能需要登录 GitHub（浏览器会弹出登录窗口）
3. **确保 GitHub 仓库已创建

## 🎯 如果遇到问题

### 问题 1：找不到 git 命令

**解决：** 刷新环境变量或重启 PowerShell

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

### 问题 2：需要登录 GitHub

**解决：** 浏览器会自动弹出登录窗口，或者使用 Personal Access Token

### 问题 3：仓库不存在

**解决：** 先在 GitHub 上创建仓库，然后使用仓库地址

## 🎉 完成！

上传成功后，你可以在 GitHub 上看到新分支 `v2.0`！

