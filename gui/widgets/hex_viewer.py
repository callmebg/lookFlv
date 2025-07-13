# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class HexViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 设置微软雅黑字体
        font = QFont("Microsoft YaHei", 10)
        
        # 标题和搜索
        header_layout = QHBoxLayout()
        
        title = QLabel("十六进制查看器")
        title.setFont(font)
        title.setStyleSheet("font-weight: bold; font-size: 12px; font-family: 'Microsoft YaHei';")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        search_label = QLabel("搜索:")
        search_label.setFont(font)
        self.search_input = QLineEdit()
        self.search_input.setFont(font)
        self.search_input.setMaximumWidth(150)
        search_btn = QPushButton("查找")
        search_btn.setFont(font)
        
        header_layout.addWidget(search_label)
        header_layout.addWidget(self.search_input)
        header_layout.addWidget(search_btn)
        
        layout.addLayout(header_layout)
        
        # 十六进制显示区域
        self.hex_display = QTextEdit()
        self.hex_display.setFont(QFont("Consolas", 10))
        self.hex_display.setReadOnly(True)
        self.hex_display.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555;
            }
        """)
        layout.addWidget(self.hex_display)
        
        # 状态信息
        self.status_label = QLabel("位置: 0x0000 | 选中: 0 字节")
        self.status_label.setFont(font)
        self.status_label.setStyleSheet("color: #666; font-size: 10px; font-family: 'Microsoft YaHei';")
        layout.addWidget(self.status_label)
        
    def load_data(self, data):
        """加载二进制数据并显示为十六进制"""
        hex_text = ""
        for i in range(0, len(data), 16):
            # 地址
            addr = f"{i:08X}: "
            
            # 十六进制数据
            hex_bytes = []
            ascii_chars = []
            
            for j in range(16):
                if i + j < len(data):
                    byte_val = data[i + j]
                    hex_bytes.append(f"{byte_val:02X}")
                    # ASCII 字符显示
                    if 32 <= byte_val <= 126:
                        ascii_chars.append(chr(byte_val))
                    else:
                        ascii_chars.append(".")
                else:
                    hex_bytes.append("  ")
                    ascii_chars.append(" ")
            
            # 格式化行
            hex_part = " ".join(hex_bytes[:8]) + "  " + " ".join(hex_bytes[8:])
            ascii_part = "".join(ascii_chars)
            
            hex_text += f"{addr}{hex_part}  |{ascii_part}|\n"
            
        self.hex_display.setPlainText(hex_text)