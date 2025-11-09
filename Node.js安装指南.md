# Node.js 安装指南

## ⚠️ 当前问题

`npm` 命令找不到，说明系统中未安装 Node.js 或 Node.js 未添加到 PATH 环境变量。

## 📥 安装 Node.js

### 步骤 1：下载 Node.js

1. **访问 Node.js 官网**
   - 打开浏览器，访问：https://nodejs.org/zh-cn/download/
   - 或者直接访问：https://nodejs.org/zh-cn/ （会自动检测你的系统）

2. **选择版本**
   - **推荐：LTS 版本**（Long Term Support，长期支持版）
   - 这是最稳定的版本，适合生产环境
   - 当前 LTS 版本通常是 v20.x 或 v22.x

3. **下载安装程序**
   - 点击 "Windows Installer (.msi)" 下载
   - 文件大小约 30-40 MB

### 步骤 2：安装 Node.js

1. **运行安装程序**
   - 双击下载的 `.msi` 文件
   - 如果出现"用户账户控制"提示，点击"是"

2. **安装向导**
   - 点击 "Next"（下一步）
   - 接受许可协议，点击 "Next"
   - **重要：** 在 "Custom Setup" 页面，确保勾选：
     - ✅ **Add to PATH**（添加到 PATH 环境变量）
     - ✅ **npm package manager**（npm 包管理器）
   - 继续点击 "Next"，直到 "Install"（安装）
   - 点击 "Install" 开始安装
   - 安装完成后点击 "Finish"（完成）

### 步骤 3：验证安装

**重要：安装完成后，必须关闭并重新打开 PowerShell 窗口！**

1. **关闭当前的 PowerShell 窗口**

2. **重新打开 PowerShell**（以普通用户身份即可，不需要管理员）

3. **验证 Node.js 和 npm**
   ```powershell
   node --version
   npm --version
   ```

   **期望输出：**
   ```
   v20.x.x  （或类似版本号）
   10.x.x   （或类似版本号）
   ```

   如果显示版本号，说明安装成功！✅

   **如果仍然显示"找不到命令"：**
   - 检查是否重启了 PowerShell
   - 检查安装时是否勾选了 "Add to PATH"
   - 可能需要重启电脑

---

## 🚀 安装完成后启动前端

### 步骤 1：安装前端依赖

打开 PowerShell，执行：

```powershell
# 进入前端目录
cd "C:\Users\32353\Desktop\大四上\NLP\CW\Hotel-Feedback-ABSA-Task-main\frontend"

# 安装依赖（首次运行需要，可能需要几分钟）
npm install
```

**成功标志：** 看到类似以下输出：
```
added 1234 packages in 2m
```

### 步骤 2：启动前端开发服务器

```powershell
npm run dev
```

**成功标志：** 看到类似以下输出：
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## 📋 完整启动流程

### 终端 1：启动后端

```powershell
cd "C:\Users\32353\Desktop\大四上\NLP\CW\Hotel-Feedback-ABSA-Task-main\backend"
.\venv\Scripts\python.exe app.py
```

**保持这个窗口打开！**

### 终端 2：启动前端（安装 Node.js 后）

```powershell
cd "C:\Users\32353\Desktop\大四上\NLP\CW\Hotel-Feedback-ABSA-Task-main\frontend"
npm install  # 首次运行需要
npm run dev
```

**保持这个窗口打开！**

### 访问系统

1. 打开浏览器
2. 访问：`http://localhost:5173`
3. 使用默认管理员账户登录：
   - 用户名：`admin`
   - 密码：`admin123`

---

## ⚠️ 常见问题

### Q1: 安装后仍然找不到 npm？

**解决方案：**
1. 确保已关闭并重新打开 PowerShell
2. 检查安装时是否勾选了 "Add to PATH"
3. 尝试重启电脑
4. 手动检查环境变量：
   - 右键"此电脑" → "属性" → "高级系统设置" → "环境变量"
   - 在 "系统变量" 的 "Path" 中，应该包含 Node.js 的路径（如 `C:\Program Files\nodejs\`）

### Q2: npm install 很慢？

**解决方案：**
可以使用国内镜像源加速：
```powershell
npm install --registry=https://registry.npmmirror.com
```

或者永久设置镜像源：
```powershell
npm config set registry https://registry.npmmirror.com
```

### Q3: 端口 5173 被占用？

**解决方案：**
- 关闭占用端口的程序
- 或者修改 `frontend/vite.config.js` 中的端口配置

---

## ✅ 检查清单

完成以下步骤后，你应该能够：

- [ ] Node.js 已安装
- [ ] `node --version` 显示版本号
- [ ] `npm --version` 显示版本号
- [ ] 前端依赖已安装（`npm install` 成功）
- [ ] 前端开发服务器已启动（`npm run dev` 成功）
- [ ] 可以访问 http://localhost:5173

---

## 🎉 完成！

安装完 Node.js 后，你就可以：
- ✅ 启动前端开发服务器
- ✅ 访问完整的 Web 界面
- ✅ 使用所有功能

祝你使用愉快！🚀

