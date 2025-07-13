# main.py
# -*- coding: utf-8 -*-
import sys
import os

# 设置环境变量确保UTF-8编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

# 清理重复的TERM环境变量
if 'TERM' in os.environ and os.environ['TERM'].count('xterm-256color') > 1:
    os.environ['TERM'] = 'xterm-256color'

if sys.platform.startswith('win'):
    # Windows环境下设置控制台编码
    os.system('chcp 65001 > nul')

from core import init_logging, get_logger

if __name__ == "__main__":
    init_logging()
    logger = get_logger(__name__)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("cli")
        from cli.analyser import run_cli
        run_cli(sys.argv[2:])
    else:
        print("gui")
        try:
            import os
            # 检查是否在WSL或无头环境
            if os.environ.get('WSL_DISTRO_NAME') or not os.environ.get('DISPLAY'):
                print("检测到WSL或无显示环境，GUI模式可能无法正常工作")
                print("建议使用CLI模式: python main.py --cli")
                
            from PyQt5.QtWidgets import QApplication
            from PyQt5.QtCore import QTextCodec
            from PyQt5.QtGui import QFont, QFontDatabase
            from gui.main_window import MainWindow
            
            app = QApplication(sys.argv)
            
            # 设置编码支持中文
            QTextCodec.setCodecForLocale(QTextCodec.codecForName("UTF-8"))
            
            # 强制设置微软雅黑字体
            font_db = QFontDatabase()
            chinese_fonts = [
                "Microsoft YaHei",    # 微软雅黑 - 第一优先级
                "Microsoft YaHei UI", # 微软雅黑UI - 第二优先级  
                "SimHei",             # 黑体 - 备用
                "PingFang SC",        # macOS
                "Noto Sans CJK SC",   # Linux
                "WenQuanYi Micro Hei", # Linux备用
                "SimSun",             # 宋体
                "DejaVu Sans"         # 最后备用字体
            ]
            
            selected_font = None
            for font_name in chinese_fonts:
                if font_name in font_db.families():
                    selected_font = font_name
                    break
            
            if selected_font:
                app_font = QFont(selected_font, 9)
                app_font.setStyleHint(QFont.SansSerif)
                app.setFont(app_font)
                print(f"应用字体设置为: {selected_font}")
            else:
                print("使用系统默认字体")
            
            # 设置应用程序属性
            app.setApplicationName("FLV Analyzer - lookFlv")
            app.setApplicationDisplayName("FLV分析器")
            
            window = MainWindow()
            window.show()
            sys.exit(app.exec_())
            
        except ImportError as e:
            logger.error(f"GUI依赖缺失: {e}")
            print("错误: 无法启动GUI模式，请安装PyQt5依赖")
            print("运行: pip install PyQt5 pyqtgraph")
            sys.exit(1)
        except Exception as e:
            logger.error(f"GUI启动失败: {e}")
            print(f"错误: GUI启动失败 - {e}")
            print("可能的解决方案:")
            print("1. 在WSL中使用: python main.py --cli")
            print("2. 设置X11转发: export DISPLAY=:0")
            print("3. 安装X11服务器 (如VcXsrv)")
            sys.exit(1)