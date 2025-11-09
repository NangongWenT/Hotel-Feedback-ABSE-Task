# 修复 Node.js 路径问题

## ✅ 好消息

Node.js 已经成功安装在：`C:\Program Files\nodejs\`

但是 PATH 环境变量中没有包含这个路径，所以 PowerShell 找不到 `node` 和 `npm` 命令。

## 🔧 解决方案

### 方案 1：刷新环境变量（最简单）

**关闭当前的 PowerShell 窗口，然后重新打开一个新的 PowerShell 窗口。**

环境变量通常在安装时已经添加，但需要重启 PowerShell 才能生效。

### 方案 2：手动添加到 PATH（如果方案 1 不行）

1. **打开环境变量设置**
   - 按 `Win + R`，输入 `sysdm.cpl`，按回车
   - 或者：右键"此电脑" → "属性" → "高级系统设置" → "环境变量"

2. **编辑 PATH 变量**
   - 在"系统变量"部分，找到 `Path` 变量
   - 点击"编辑"
   - 点击"新建"
   - 输入：`C:\Program Files\nodejs`
   - 点击"确定"保存所有窗口

3. **重启 PowerShell**
   - 关闭所有 PowerShell 窗口
   - 重新打开 PowerShell
   - 运行 `node --version` 验证

### 方案 3：临时添加到当前会话（快速测试）

在当前的 PowerShell 窗口中运行：

```powershell
$env:PATH += ";C:\Program Files\nodejs"
node --version
npm --version
```

**注意：** 这只是临时添加，关闭 PowerShell 后就会失效。如果要永久生效，请使用方案 1 或 2。

### 方案 4：直接使用完整路径（临时方案）

如果不想修改环境变量，可以直接使用完整路径：

```powershell
# 使用 node
& "C:\Program Files\nodejs\node.exe" --version

# 使用 npm
& "C:\Program Files\nodejs\npm.cmd" install
& "C:\Program Files\nodejs\npm.cmd" run dev
```

或者创建一个别名：

```powershell
# 在当前 PowerShell 会话中创建别名
Set-Alias -Name node -Value "C:\Program Files\nodejs\node.exe"
Set-Alias -Name npm -Value "C:\Program Files\nodejs\npm.cmd"

# 然后就可以正常使用了
node --version
npm --version
```

---

## 🚀 推荐操作步骤

### 第一步：尝试刷新环境变量

1. **完全关闭当前的 PowerShell 窗口**
2. **重新打开一个新的 PowerShell 窗口**
3. **运行验证命令：**
   ```powershell
   node --version
   npm --version
   ```

如果显示版本号，说明问题已解决！✅

### 第二步：如果还是不行

使用方案 3 临时添加到当前会话：

```powershell
$env:PATH += ";C:\Program Files\nodejs"
node --version
npm --version
```

如果这样可以工作，说明需要永久添加到 PATH（使用方案 2）。

---

## 📝 验证安装

运行以下命令验证：

```powershell
node --version
npm --version
```

**期望输出：**
```
v20.x.x  （或类似版本号）
10.x.x   （或类似版本号）
```

---

## 🎯 安装前端依赖

一旦 `npm` 命令可用，就可以安装前端依赖：

```powershell
# 进入前端目录
cd "C:\Users\32353\Desktop\大四上\NLP\CW\Hotel-Feedback-ABSA-Task-main\frontend"

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

---

## 💡 提示

- **最简单的方法**：关闭并重新打开 PowerShell 窗口（方案 1）
- **如果还是不行**：检查安装时是否勾选了 "Add to PATH"
- **临时方案**：使用完整路径或创建别名（方案 4）
