# Windows安装说明

## 为什么在Windows上无法运行？

主要问题包括：

### 1. **PyAV/FFmpeg依赖问题**
- PyAV需要FFmpeg二进制文件
- Windows下FFmpeg安装复杂
- 解决方案：运行 `python scripts/win_runtime_fix.py`

### 2. **PyQt5安装问题**
- 不同Python版本兼容性
- Visual C++运行库依赖
- 解决方案：使用wheel包安装

### 3. **编码问题**
- Windows控制台默认GBK编码
- 中文字符显示异常
- 解决方案：已在代码中修复UTF-8支持

## 快速修复

1. **运行修复脚本**：
   ```cmd
   python scripts/win_runtime_fix.py
   ```

2. **手动安装依赖**：
   ```cmd
   pip install -r requirements.txt
   ```

3. **使用启动脚本**：
   - 双击 `run_gui.bat` - 启动图形界面
   - 双击 `run_cli.bat` - 启动命令行版本

## 常见错误及解决方案

### ImportError: No module named 'PyQt5'
```cmd
pip install PyQt5==5.15.9
```

### ImportError: No module named 'av'
需要先安装FFmpeg：
1. 下载FFmpeg: https://ffmpeg.org/download.html
2. 解压到C:\ffmpeg
3. 添加C:\ffmpeg\bin到PATH
4. 安装PyAV: `pip install av`

### 中文乱码
已修复，如仍有问题请运行：
```cmd
chcp 65001
set PYTHONIOENCODING=utf-8
python main.py
```

### 路径问题
程序已兼容Windows路径分隔符，无需特殊处理。

## 系统要求

- Python 3.7+
- Windows 7/10/11
- 至少1GB可用内存
- 可选：FFmpeg（用于高级视频分析）

## 验证安装

运行测试命令：
```cmd
python -c "import PyQt5; print('PyQt5 OK')"
python -c "from core import get_logger; print('Core modules OK')"
```