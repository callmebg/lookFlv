#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows运行时修复脚本
解决Windows环境下的常见问题
"""

import sys
import os
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    print("=== Python版本检查 ===")
    print(f"Python版本: {sys.version}")
    print(f"平台: {platform.platform()}")
    
    if sys.version_info < (3, 7):
        print("警告: 建议使用Python 3.7或更高版本")
        return False
    
    print("✓ Python版本兼容")
    return True


def check_dependencies():
    """检查依赖包"""
    print("\n=== 依赖包检查 ===")
    
    required_packages = [
        'PyQt5',
        'pyqtgraph', 
        'construct',
        'flvlib',
        'moviepy'
    ]
    
    optional_packages = [
        'av',  # PyAV for FFmpeg
        'tensorflow'  # AI analysis
    ]
    
    missing_required = []
    missing_optional = []
    
    for package in required_packages:
        try:
            __import__(package.lower().replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (必需)")
            missing_required.append(package)
    
    for package in optional_packages:
        try:
            if package == 'av':
                import av
            elif package == 'tensorflow':
                import tensorflow
            print(f"✓ {package} (可选)")
        except ImportError:
            print(f"- {package} (可选)")
            missing_optional.append(package)
    
    return missing_required, missing_optional


def install_dependencies(missing_packages):
    """安装缺失的依赖包"""
    if not missing_packages:
        return True
    
    print(f"\n=== 安装缺失依赖 ===")
    
    for package in missing_packages:
        print(f"正在安装 {package}...")
        try:
            if package == 'PyQt5':
                # Windows下PyQt5安装
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', 
                    'PyQt5==5.15.9', '--no-cache-dir'
                ])
            elif package == 'av':
                # PyAV在Windows下比较复杂，提供说明
                print("PyAV (FFmpeg) 在Windows下需要特殊安装:")
                print("1. 下载FFmpeg: https://ffmpeg.org/download.html")
                print("2. 安装PyAV: pip install av")
                print("3. 或使用conda: conda install av -c conda-forge")
                continue
            else:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', package
                ])
            print(f"✓ {package} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"✗ {package} 安装失败: {e}")
            return False
    
    return True


def fix_encoding():
    """修复Windows编码问题"""
    print("\n=== 编码设置修复 ===")
    
    # 设置环境变量
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Windows控制台编码设置
    if platform.system() == 'Windows':
        try:
            # 设置控制台为UTF-8
            os.system('chcp 65001 > nul')
            print("✓ 控制台编码已设置为UTF-8")
        except Exception as e:
            print(f"警告: 无法设置控制台编码: {e}")
    
    print("✓ Python编码已设置为UTF-8")


def check_ffmpeg():
    """检查FFmpeg安装"""
    print("\n=== FFmpeg检查 ===")
    
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ FFmpeg已安装")
            return True
        else:
            print("✗ FFmpeg未正确安装")
            return False
    except FileNotFoundError:
        print("✗ FFmpeg未找到")
        print("请安装FFmpeg:")
        print("1. 下载: https://ffmpeg.org/download.html")
        print("2. 解压到C:\\ffmpeg")
        print("3. 添加C:\\ffmpeg\\bin到PATH环境变量")
        return False


def create_batch_file():
    """创建Windows启动批处理文件"""
    print("\n=== 创建启动脚本 ===")
    
    batch_content = """@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo Starting FLV Analyzer - lookFlv...
python main.py %*
pause
"""
    
    try:
        with open('run_lookflv.bat', 'w', encoding='utf-8') as f:
            f.write(batch_content)
        print("✓ 已创建 run_lookflv.bat 启动脚本")
        
        # 创建GUI启动脚本
        gui_batch_content = """@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo Starting FLV Analyzer GUI...
python main.py
pause
"""
        with open('run_gui.bat', 'w', encoding='utf-8') as f:
            f.write(gui_batch_content)
        print("✓ 已创建 run_gui.bat GUI启动脚本")
        
        # 创建CLI启动脚本
        cli_batch_content = """@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
echo Starting FLV Analyzer CLI...
python main.py --cli %*
pause
"""
        with open('run_cli.bat', 'w', encoding='utf-8') as f:
            f.write(cli_batch_content)
        print("✓ 已创建 run_cli.bat CLI启动脚本")
        
    except Exception as e:
        print(f"✗ 创建启动脚本失败: {e}")


def main():
    """主函数"""
    print("FLV Analyzer - Windows运行时修复工具")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        print("请升级Python版本后重试")
        return False
    
    # 检查依赖
    missing_required, missing_optional = check_dependencies()
    
    # 安装缺失依赖
    if missing_required:
        print(f"\n发现 {len(missing_required)} 个缺失的必需依赖")
        install_choice = input("是否自动安装？(y/n): ")
        if install_choice.lower() == 'y':
            if not install_dependencies(missing_required):
                print("依赖安装失败，请手动安装")
                return False
    
    # 修复编码
    fix_encoding()
    
    # 检查FFmpeg
    check_ffmpeg()
    
    # 创建启动脚本
    create_batch_file()
    
    print("\n" + "=" * 50)
    print("修复完成!")
    print("\n使用方法:")
    print("1. 双击 run_gui.bat 启动图形界面")
    print("2. 双击 run_cli.bat 启动命令行版本")
    print("3. 或直接运行: python main.py")
    
    if missing_optional:
        print(f"\n可选依赖未安装: {', '.join(missing_optional)}")
        print("这些依赖不影响基本功能的使用")
    
    return True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n用户取消操作")
    except Exception as e:
        print(f"\n修复过程中出现错误: {e}")
        print("请检查Python环境和网络连接")