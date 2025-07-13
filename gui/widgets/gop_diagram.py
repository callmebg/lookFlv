# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QScrollArea, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QFont
import pyqtgraph as pg


class GOPDiagram(QWidget):
    def __init__(self):
        super().__init__()
        self.gop_data = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 设置微软雅黑字体
        font = QFont("Microsoft YaHei", 10)
        
        # 标题
        title = QLabel("GOP 结构分析")
        title.setFont(font)
        title.setStyleSheet("font-weight: bold; font-size: 12px; font-family: 'Microsoft YaHei';")
        layout.addWidget(title)
        
        # 统计信息
        stats_layout = QHBoxLayout()
        
        self.i_frame_label = QLabel("I帧: 0")
        self.i_frame_label.setFont(font)
        self.p_frame_label = QLabel("P帧: 0")
        self.p_frame_label.setFont(font)
        self.b_frame_label = QLabel("B帧: 0")
        self.b_frame_label.setFont(font)
        self.gop_count_label = QLabel("GOP数: 0")
        self.gop_count_label.setFont(font)
        
        stats_layout.addWidget(self.i_frame_label)
        stats_layout.addWidget(self.p_frame_label)
        stats_layout.addWidget(self.b_frame_label)
        stats_layout.addWidget(self.gop_count_label)
        stats_layout.addStretch()
        
        layout.addLayout(stats_layout)
        
        # GOP 可视化区域
        self.scroll_area = QScrollArea()
        self.gop_canvas = GOPCanvas()
        self.scroll_area.setWidget(self.gop_canvas)
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)
        
        # 控制按钮
        control_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setFont(font)
        self.export_btn = QPushButton("导出结构")
        self.export_btn.setFont(font)
        
        control_layout.addWidget(self.refresh_btn)
        control_layout.addWidget(self.export_btn)
        control_layout.addStretch()
        
        layout.addLayout(control_layout)
        
    def update_gop_data(self, gop_data):
        """更新GOP数据"""
        self.gop_data = gop_data
        
        # 统计帧类型
        i_count = sum(1 for gop in gop_data for frame in gop if frame['type'] == 'I')
        p_count = sum(1 for gop in gop_data for frame in gop if frame['type'] == 'P')
        b_count = sum(1 for gop in gop_data for frame in gop if frame['type'] == 'B')
        
        self.i_frame_label.setText(f"I帧: {i_count}")
        self.p_frame_label.setText(f"P帧: {p_count}")
        self.b_frame_label.setText(f"B帧: {b_count}")
        self.gop_count_label.setText(f"GOP数: {len(gop_data)}")
        
        # 更新画布
        self.gop_canvas.set_gop_data(gop_data)
        

class GOPCanvas(QFrame):
    def __init__(self):
        super().__init__()
        self.gop_data = []
        self.setMinimumHeight(200)
        self.setStyleSheet("border: 1px solid #ccc; background-color: white;")
        
    def set_gop_data(self, gop_data):
        """设置GOP数据并重绘"""
        self.gop_data = gop_data
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if not self.gop_data:
            painter.drawText(self.rect(), Qt.AlignCenter, "暂无GOP数据")
            return
            
        # 设置绘图参数
        margin = 20
        gop_height = 30
        frame_width = 15
        frame_height = 20
        gop_spacing = 10
        
        y_start = margin
        
        # 颜色映射
        colors = {
            'I': QColor(255, 0, 0),    # 红色 - I帧
            'P': QColor(0, 255, 0),    # 绿色 - P帧
            'B': QColor(0, 0, 255)     # 蓝色 - B帧
        }
        
        font = QFont("Microsoft YaHei", 8)
        painter.setFont(font)
        
        for gop_idx, gop in enumerate(self.gop_data):
            y_pos = y_start + gop_idx * (gop_height + gop_spacing)
            
            # 绘制GOP标签
            painter.setPen(QPen(Qt.black))
            painter.drawText(5, y_pos + 15, f"GOP {gop_idx + 1}")
            
            # 绘制帧
            x_pos = margin + 80
            for frame_idx, frame in enumerate(gop):
                frame_type = frame.get('type', 'P')
                color = colors.get(frame_type, QColor(128, 128, 128))
                
                # 绘制帧矩形
                painter.setPen(QPen(Qt.black))
                painter.setBrush(QBrush(color))
                
                frame_rect = painter.drawRect(
                    x_pos + frame_idx * (frame_width + 2),
                    y_pos,
                    frame_width,
                    frame_height
                )
                
                # 绘制帧类型文字
                painter.setPen(QPen(Qt.white))
                painter.drawText(
                    x_pos + frame_idx * (frame_width + 2) + 3,
                    y_pos + 14,
                    frame_type
                )
                
        # 绘制图例
        legend_y = self.height() - 60
        painter.setPen(QPen(Qt.black))
        painter.drawText(margin, legend_y, "图例:")
        
        legend_items = [
            ('I帧 (关键帧)', colors['I']),
            ('P帧 (预测帧)', colors['P']),
            ('B帧 (双向帧)', colors['B'])
        ]
        
        for i, (text, color) in enumerate(legend_items):
            x = margin + i * 120
            painter.setBrush(QBrush(color))
            painter.drawRect(x, legend_y + 15, 15, 15)
            painter.setPen(QPen(Qt.black))
            painter.drawText(x + 20, legend_y + 27, text)