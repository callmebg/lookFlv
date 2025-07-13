# 🚀 lookFlv 快速开始指南

## 📋 目录

- [环境准备](#环境准备)
- [安装步骤](#安装步骤)
- [启动程序](#启动程序)
- [功能使用](#功能使用)
- [故障排除](#故障排除)

## 🔧 环境准备

### 最低系统要求

- **操作系统**: Windows 7+ / Linux / macOS
- **Python版本**: 3.7 或更高版本
- **内存**: 512MB 可用内存
- **存储**: 100MB 可用磁盘空间

### 推荐环境

- **操作系统**: Windows 10/11 （获得最佳体验）
- **Python版本**: 3.8+ 
- **内存**: 2GB+ 可用内存

## 📦 安装步骤

### 方法一：直接安装（推荐）

1. **检查Python环境**
   ```bash
   python --version
   # 应显示 Python 3.7.x 或更高版本
   ```

2. **克隆项目**
   ```bash
   git clone https://github.com/username/lookFlv.git
   cd lookFlv
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

### 方法二：虚拟环境安装（开发推荐）

1. **创建虚拟环境**
   ```bash
   python -m venv lookflv_env
   
   # Windows
   lookflv_env\Scripts\activate
   
   # Linux/macOS
   source lookflv_env/bin/activate
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

## 🎬 启动程序

### GUI模式（图形界面）

```bash
python main.py
```

**首次启动效果：**
- 自动检测系统环境
- 加载中文字体配置
- 显示主界面窗口

### CLI模式（命令行）

```bash
# 查看帮助
python main.py --cli --help

# 快速分析FLV文件
python main.py --cli info your_video.flv
```

## 📖 功能使用

### 🎯 GUI模式操作指南

#### 1. 打开FLV文件

**方法A：菜单操作**
- 菜单栏 → 文件 → 打开文件 (或按 `Ctrl+O`)

**方法B：工具栏按钮**
- 点击工具栏上的"打开文件"图标

**方法C：拖拽操作**
- 直接将FLV文件拖拽到窗口中

#### 2. 视频播放功能

文件加载成功后，程序会自动切换到"视频预览"标签页：

**播放控制**
- **播放/暂停**: 点击播放按钮或按空格键
- **停止播放**: 点击停止按钮
- **进度跳转**: 拖拽进度条到目标位置
- **音量调节**: 使用右侧音量滑块

**快捷键**
- `空格`: 播放/暂停
- `Ctrl+O`: 打开文件
- `Esc`: 停止播放

#### 3. 文件信息查看

**左侧文件列表**
- 显示文件基本属性（大小、时长等）
- 双击文件名可重新加载

**右侧详细面板**
- **文件属性**: 文件路径、大小、创建时间
- **视频信息**: 分辨率、帧率、编码格式
- **音频信息**: 采样率、声道数、编码格式

#### 4. 高级分析功能

**时间轴分析**
- 切换到"时间轴"标签页
- 查看音视频数据流时序图
- 分析音画同步情况

**十六进制查看**
- 切换到"十六进制"标签页
- 查看FLV文件原始二进制数据
- 支持标签定位和搜索

**GOP结构分析**
- 切换到"GOP结构"标签页
- 可视化I/P/B帧分布
- 分析关键帧结构

**流监控**
- 实时数据流监控
- 比特率分析
- 错误检测报告

### 🖥️ CLI模式命令参考

#### 基础命令

```bash
# 查看文件基本信息
python main.py --cli info video.flv

# 输出示例:
# 文件: video.flv
# 大小: 15.2 MB
# 时长: 00:02:30
# 视频: H.264, 1920x1080, 25fps
# 音频: AAC, 44.1kHz, 立体声
```

#### 详细分析

```bash
# 详细分析文件结构
python main.py --cli analyze video.flv --detailed

# 输出包含:
# - FLV头部信息
# - 标签统计
# - 时间戳分析
# - 元数据详情
```

#### 文件验证

```bash
# 验证文件完整性
python main.py --cli validate video.flv

# 检查项目:
# - 文件格式正确性
# - 标签结构完整性
# - 音画同步情况
# - 潜在错误检测
```

#### 批量处理

```bash
# 批量分析多个文件
python main.py --cli batch *.flv --output report.txt
```

## 🐛 故障排除

### 常见问题解决

#### ❌ 问题1: GUI无法启动

**错误现象:**
```
qt.qpa.xcb: could not connect to display
```

**解决方案:**
```bash
# WSL用户需要配置X11
# 1. 安装X11服务器（如VcXsrv）
# 2. 启动X11服务器
# 3. 设置显示变量
export DISPLAY=:0

# 或者使用CLI模式
python main.py --cli
```

#### ❌ 问题2: 视频播放失败

**错误现象:**
```
MoviePy error: could not load video
```

**解决方案:**
```bash
# 重新安装moviepy
pip uninstall moviepy
pip install moviepy==1.0.3

# 检查文件是否损坏
python main.py --cli validate your_video.flv
```

#### ❌ 问题3: 中文字符乱码

**错误现象:**
- 界面中文显示为方框或乱码

**解决方案:**
- 程序已自动处理中文字体
- 如仍有问题，确保系统安装了中文字体
- Windows用户确保有"微软雅黑"字体

#### ❌ 问题4: 依赖安装失败

**错误现象:**
```bash
ERROR: Could not install packages due to an EnvironmentError
```

**解决方案:**
```bash
# 使用管理员权限安装
sudo pip install -r requirements.txt

# 或使用用户模式安装
pip install --user -r requirements.txt

# 升级pip
python -m pip install --upgrade pip
```

### 🔍 诊断工具

#### 环境检查脚本

```bash
# 运行环境诊断
python scripts/dependency_check.py

# 输出诊断报告:
# ✅ Python 3.8.10 - OK
# ✅ PyQt5 5.15.9 - OK  
# ✅ moviepy 1.0.3 - OK
# ❌ flvlib - Missing (可选)
```

#### 日志查看

**日志文件位置:** `logs/lookflv_YYYYMMDD.log`

**日志级别说明:**
- `INFO`: 正常操作信息
- `WARNING`: 警告信息（通常可忽略）
- `ERROR`: 错误信息（需要处理）
- `DEBUG`: 调试信息（开发用）

**实时查看日志:**
```bash
# Linux/macOS
tail -f logs/lookflv_$(date +%Y%m%d).log

# Windows
type logs\lookflv_20231201.log
```

## 🎯 下一步

恭喜！你已经成功安装并了解了lookFlv的基本使用方法。

**推荐下一步操作:**

1. **尝试分析你的第一个FLV文件**
   ```bash
   python main.py
   # 打开一个FLV文件开始探索
   ```

2. **查看完整文档**
   - [用户手册](docs/user_manual.md) - 详细功能说明
   - [开发指南](docs/developer_guide.md) - 二次开发参考

3. **加入社区**
   - 提交Issue反馈问题
   - 贡献代码改进项目
   - 分享使用经验

---

**🔗 快速链接:**
- [返回README](README.md)
- [查看用户手册](docs/user_manual.md)
- [报告问题](https://github.com/username/lookFlv/issues)

💡 **提示**: 如果在使用过程中遇到任何问题，请先查看本指南的故障排除部分，或查看日志文件获取详细错误信息。