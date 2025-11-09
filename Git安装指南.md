# Git 安装指南

## 📥 下载和安装

### 步骤 1：下载 Git

1. **访问 Git 官网**
   - 网址：https://git-scm.com/download/win
   - 会自动检测你的系统并下载对应版本

2. **或者直接下载**
   - 64位 Windows：https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe

### 步骤 2：安装 Git

1. **运行安装程序**
2. **使用默认设置**（一路 Next）
   - 推荐选项：
     - ✅ Use Visual Studio Code as Git's default editor
     - ✅ Git from the command line and also from 3rd-party software
     - ✅ Use bundled OpenSSH
     - ✅ Use the OpenSSL library
     - ✅ Checkout Windows-style, commit Unix-style line endings

3. **完成安装**

### 步骤 3：验证安装

打开 PowerShell，运行：

```powershell
git --version
```

应该显示类似：`git version 2.43.0.windows.1`

### 步骤 4：配置 Git（首次使用）

```powershell
# 设置用户名
git config --global user.name "你的名字"

# 设置邮箱
git config --global user.email "你的邮箱@example.com"

# 验证配置
git config --global --list
```

## ✅ 安装完成！

安装完成后，你可以：
1. 使用 `快速上传到GitHub.ps1` 脚本上传代码
2. 或者按照 `上传到GitHub指南.md` 手动操作

## 🔗 相关文档

- `上传到GitHub指南.md` - 详细的上传步骤
- `快速上传到GitHub.ps1` - 自动化上传脚本

