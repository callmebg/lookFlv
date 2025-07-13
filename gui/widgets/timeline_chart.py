# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import pyqtgraph as pg


class TimelineChart(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 设置微软雅黑字体
        font = QFont("Microsoft YaHei", 10)
        
        # 标题
        title = QLabel("时间轴分析")
        title.setFont(font)
        title.setStyleSheet("font-weight: bold; font-size: 12px; font-family: 'Microsoft YaHei';")
        layout.addWidget(title)
        
        # 图表区域
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', '数据大小 (KB)')
        self.plot_widget.setLabel('bottom', '时间 (秒)')
        self.plot_widget.setTitle('FLV 数据流分析')
        layout.addWidget(self.plot_widget)
        
        # 控制按钮
        control_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.setFont(font)
        self.export_btn = QPushButton("导出")
        self.export_btn.setFont(font)
        
        control_layout.addWidget(self.refresh_btn)
        control_layout.addWidget(self.export_btn)
        control_layout.addStretch()
        
        layout.addLayout(control_layout)
        
    def update_chart(self, time_data, size_data):
        """更新时间轴图表数据"""
        self.plot_widget.clear()
        self.plot_widget.plot(time_data, size_data, pen='b', name='数据流')