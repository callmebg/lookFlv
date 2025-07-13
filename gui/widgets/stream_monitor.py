# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QPushButton, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QFont


class StreamMonitor(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 设置微软雅黑字体
        font = QFont("Microsoft YaHei", 10)
        
        # 标题
        title = QLabel("流监控")
        title.setFont(font)
        title.setStyleSheet("font-weight: bold; font-size: 12px; font-family: 'Microsoft YaHei';")
        layout.addWidget(title)
        
        # 实时状态
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("状态: 就绪")
        self.status_label.setFont(font)
        self.fps_label = QLabel("FPS: 0")
        self.fps_label.setFont(font)
        self.bitrate_label = QLabel("比特率: 0 kbps")
        self.bitrate_label.setFont(font)
        
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        status_layout.addWidget(self.fps_label)
        status_layout.addWidget(self.bitrate_label)
        
        layout.addLayout(status_layout)
        
        # 数据表格
        self.data_table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.data_table)
        
        # 控制按钮
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("开始监控")
        self.start_btn.setFont(font)
        self.stop_btn = QPushButton("停止监控")
        self.stop_btn.setFont(font)
        self.clear_btn = QPushButton("清空数据")
        self.clear_btn.setFont(font)
        
        self.start_btn.clicked.connect(self.start_monitoring)
        self.stop_btn.clicked.connect(self.stop_monitoring)
        self.clear_btn.clicked.connect(self.clear_data)
        
        control_layout.addWidget(self.start_btn)
        control_layout.addWidget(self.stop_btn)
        control_layout.addWidget(self.clear_btn)
        control_layout.addStretch()
        
        layout.addLayout(control_layout)
        
    def setup_table(self):
        headers = ["时间", "类型", "大小(B)", "时间戳", "状态"]
        self.data_table.setColumnCount(len(headers))
        self.data_table.setHorizontalHeaderLabels(headers)
        
        # 设置列宽
        self.data_table.setColumnWidth(0, 80)
        self.data_table.setColumnWidth(1, 60)
        self.data_table.setColumnWidth(2, 80)
        self.data_table.setColumnWidth(3, 80)
        self.data_table.setColumnWidth(4, 60)
        
    def start_monitoring(self):
        """开始监控"""
        self.status_label.setText("状态: 监控中")
        self.status_label.setStyleSheet("color: green;")
        self.update_timer.start(1000)  # 每秒更新
        
    def stop_monitoring(self):
        """停止监控"""
        self.status_label.setText("状态: 已停止")
        self.status_label.setStyleSheet("color: red;")
        self.update_timer.stop()
        
    def clear_data(self):
        """清空数据"""
        self.data_table.setRowCount(0)
        
    def update_data(self):
        """更新监控数据"""
        # TODO: 实现实际的数据更新逻辑
        pass
        
    def add_data_row(self, time_str, data_type, size, timestamp, status):
        """添加数据行"""
        row = self.data_table.rowCount()
        self.data_table.insertRow(row)
        
        self.data_table.setItem(row, 0, QTableWidgetItem(time_str))
        self.data_table.setItem(row, 1, QTableWidgetItem(data_type))
        self.data_table.setItem(row, 2, QTableWidgetItem(str(size)))
        self.data_table.setItem(row, 3, QTableWidgetItem(str(timestamp)))
        self.data_table.setItem(row, 4, QTableWidgetItem(status))
        
        # 根据状态设置颜色
        if status == "正常":
            color = QColor(0, 255, 0, 50)
        elif status == "警告":
            color = QColor(255, 255, 0, 50)
        else:
            color = QColor(255, 0, 0, 50)
            
        for col in range(5):
            item = self.data_table.item(row, col)
            if item:
                item.setBackground(color)