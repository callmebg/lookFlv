import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QTableWidget, QTableWidgetItem, QTreeWidget, 
                             QTreeWidgetItem, QLabel, QFrame, QMenuBar, QMenu, 
                             QAction, QToolBar, QStatusBar, QFileDialog, QMessageBox,
                             QHeaderView, QAbstractItemView, QTabWidget, QTextEdit,
                             QProgressBar, QPushButton, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QPixmap, QFont, QIcon, QPalette, QColor, QFontDatabase

from .widgets.timeline_chart import TimelineChart
from .widgets.hex_viewer import HexViewer
from .widgets.stream_monitor import StreamMonitor
from .widgets.gop_diagram import GOPDiagram
from .widgets.video_player import VideoPlayer
from core.flv_handler import FLVFileHandler
from core import get_logger

logger = get_logger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_files = []
        self.flv_handler = FLVFileHandler()  # FLV文件处理器
        
        # 设置中文字体
        self.setup_chinese_font()
        
        self.init_ui()
        
    def setup_chinese_font(self):
        """设置中文字体支持 - 强制使用微软雅黑"""
        # 强制优先使用微软雅黑
        font_families = [
            "Microsoft YaHei",    # 微软雅黑 - 第一优先级
            "Microsoft YaHei UI", # 微软雅黑UI - 第二优先级
            "SimHei",             # 黑体 - 备用
            "PingFang SC",        # macOS
            "Noto Sans CJK SC",   # Linux
            "WenQuanYi Micro Hei", # Linux备用
            "SimSun",             # 宋体
            "DejaVu Sans"         # 最后备用字体
        ]
        
        font_db = QFontDatabase()
        available_fonts = font_db.families()
        
        selected_font = None
        for font_family in font_families:
            if font_family in available_fonts:
                selected_font = font_family
                break
        
        if selected_font:
            # 设置窗口默认字体
            self.default_font = QFont(selected_font, 9)
            self.default_font.setStyleHint(QFont.SansSerif)
            self.setFont(self.default_font)
            
            # 设置按钮字体
            self.button_font = QFont(selected_font, 9)
            self.button_font.setStyleHint(QFont.SansSerif)
            
            # 设置标签字体
            self.label_font = QFont(selected_font, 9)
            self.label_font.setStyleHint(QFont.SansSerif)
            
            print(f"已设置中文字体: {selected_font}")
        else:
            # 使用系统默认字体但确保支持Unicode
            self.default_font = QFont()
            self.default_font.setPointSize(9)
            self.default_font.setStyleHint(QFont.SansSerif)
            self.setFont(self.default_font)
            
            self.button_font = self.default_font
            self.label_font = self.default_font
            print("使用系统默认字体")
        
    def init_ui(self):
        self.setWindowTitle("FLV Analyzer - lookFlv")
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # 创建主分割器
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # 左侧文件列表区域
        self.create_file_list_panel(main_splitter)
        
        # 中间视频预览区域
        self.create_video_preview_panel(main_splitter)
        
        # 右侧属性面板
        self.create_properties_panel(main_splitter)
        
        # 设置分割器比例
        main_splitter.setSizes([400, 600, 400])
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建状态栏
        self.create_status_bar()
        
        # 加载样式
        self.load_styles()
        
    def create_file_list_panel(self, parent):
        # 创建左侧面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # 文件列表标题
        title_label = QLabel("文件列表")
        title_label.setFont(self.label_font)
        # 确保标签使用UTF-8编码
        title_label.setText("文件列表")
        left_layout.addWidget(title_label)
        
        # 文件表格
        self.file_table = QTableWidget()
        self.setup_file_table()
        left_layout.addWidget(self.file_table)
        
        parent.addWidget(left_panel)
        
    def setup_file_table(self):
        headers = ["文件名", "大小", "时长", "视频编码", "音频编码", "分辨率", "帧率", "比特率", "创建时间"]
        self.file_table.setColumnCount(len(headers))
        self.file_table.setHorizontalHeaderLabels(headers)
        
        # 设置表格属性
        self.file_table.setAlternatingRowColors(True)
        self.file_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.file_table.setSelectionMode(QAbstractItemView.SingleSelection)
        
        # 自适应列宽
        header = self.file_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        
        # 连接选择信号
        self.file_table.itemSelectionChanged.connect(self.on_file_selected)
        
    def create_video_preview_panel(self, parent):
        # 创建中间面板
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标签页
        self.center_tabs = QTabWidget()
        
        # 视频预览标签页 - 使用视频播放器组件
        self.video_player = VideoPlayer()
        self.center_tabs.addTab(self.video_player, "视频预览")
        
        # 时间轴图表标签页
        self.timeline_chart = TimelineChart()
        self.center_tabs.addTab(self.timeline_chart, "时间轴分析")
        
        # 十六进制查看器标签页
        self.hex_viewer = HexViewer()
        self.center_tabs.addTab(self.hex_viewer, "十六进制查看")
        
        center_layout.addWidget(self.center_tabs)
        parent.addWidget(center_panel)
        
    def create_properties_panel(self, parent):
        # 创建右侧面板
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标签页
        self.right_tabs = QTabWidget()
        
        # 文件属性标签页
        self.create_file_properties_tab()
        
        # 流监控标签页
        self.stream_monitor = StreamMonitor()
        self.right_tabs.addTab(self.stream_monitor, "流监控")
        
        # GOP结构标签页
        self.gop_diagram = GOPDiagram()
        self.right_tabs.addTab(self.gop_diagram, "GOP结构")
        
        right_layout.addWidget(self.right_tabs)
        parent.addWidget(right_panel)
        
    def create_file_properties_tab(self):
        properties_widget = QWidget()
        properties_layout = QVBoxLayout(properties_widget)
        
        # 基本信息组
        basic_group = QGroupBox("基本信息")
        basic_layout = QGridLayout(basic_group)
        
        self.info_labels = {}
        info_fields = [
            "文件路径", "文件大小", "持续时间", "创建时间", 
            "修改时间", "文件格式", "元数据版本"
        ]
        
        for i, field in enumerate(info_fields):
            label = QLabel(f"{field}:")
            label.setFont(self.label_font)
            value = QLabel("-")
            value.setFont(self.label_font)
            value.setStyleSheet("color: #666;")
            basic_layout.addWidget(label, i, 0)
            basic_layout.addWidget(value, i, 1)
            self.info_labels[field] = value
            
        properties_layout.addWidget(basic_group)
        
        # 视频信息组
        video_group = QGroupBox("视频信息")
        video_layout = QGridLayout(video_group)
        
        video_fields = [
            "编解码器", "分辨率", "帧率", "比特率",
            "总帧数", "关键帧数", "颜色空间", "像素格式"
        ]
        
        for i, field in enumerate(video_fields):
            label = QLabel(f"{field}:")
            label.setFont(self.label_font)
            value = QLabel("-")
            value.setFont(self.label_font)
            value.setStyleSheet("color: #666;")
            video_layout.addWidget(label, i, 0)
            video_layout.addWidget(value, i, 1)
            self.info_labels[f"视频_{field}"] = value
            
        properties_layout.addWidget(video_group)
        
        # 音频信息组
        audio_group = QGroupBox("音频信息")
        audio_layout = QGridLayout(audio_group)
        
        audio_fields = [
            "编解码器", "采样率", "比特率", "声道数",
            "位深度", "编码格式", "总样本数"
        ]
        
        for i, field in enumerate(audio_fields):
            label = QLabel(f"{field}:")
            label.setFont(self.label_font)
            value = QLabel("-")
            value.setFont(self.label_font)
            value.setStyleSheet("color: #666;")
            audio_layout.addWidget(label, i, 0)
            audio_layout.addWidget(value, i, 1)
            self.info_labels[f"音频_{field}"] = value
            
        properties_layout.addWidget(audio_group)
        
        properties_layout.addStretch()
        
        self.right_tabs.addTab(properties_widget, "文件属性")
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')
        
        open_action = QAction('打开文件(&O)...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        open_folder_action = QAction('打开文件夹(&D)...', self)
        open_folder_action.setShortcut('Ctrl+Shift+O')
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        export_action = QAction('导出分析报告(&E)...', self)
        export_action.setShortcut('Ctrl+E')
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 视图菜单
        view_menu = menubar.addMenu('视图(&V)')
        
        refresh_action = QAction('刷新(&R)', self)
        refresh_action.setShortcut('F5')
        view_menu.addAction(refresh_action)
        
        # 工具菜单
        tools_menu = menubar.addMenu('工具(&T)')
        
        settings_action = QAction('设置(&S)...', self)
        tools_menu.addAction(settings_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')
        
        about_action = QAction('关于(&A)...', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        toolbar = self.addToolBar('主工具栏')
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        # 打开文件
        open_action = QAction('打开文件', self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        # 打开文件夹
        open_folder_action = QAction('打开文件夹', self)
        open_folder_action.triggered.connect(self.open_folder)
        toolbar.addAction(open_folder_action)
        
        toolbar.addSeparator()
        
        # 刷新
        refresh_action = QAction('刷新', self)
        toolbar.addAction(refresh_action)
        
    def create_status_bar(self):
        self.statusBar().showMessage('就绪')
        
        # 添加永久组件
        self.status_progress = QProgressBar()
        self.status_progress.setVisible(False)
        self.status_progress.setMaximumWidth(200)
        self.statusBar().addPermanentWidget(self.status_progress)
        
    def load_styles(self):
        # 强制使用微软雅黑字体
        font_family = "Microsoft YaHei"
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #f0f0f0;
                font-family: "{font_family}";
                font-size: 9pt;
            }}
            QPushButton {{
                font-family: "{font_family}";
                font-size: 9pt;
                padding: 5px 10px;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: #fff;
            }}
            QPushButton:hover {{
                background-color: #e6f3ff;
            }}
            QLabel {{
                font-family: "{font_family}";
                font-size: 9pt;
            }}
            QTableWidget {{
                gridline-color: #d0d0d0;
                background-color: white;
                alternate-background-color: #f8f8f8;
                font-family: "{font_family}";
                font-size: 9pt;
            }}
            QTableWidget::item {{
                padding: 5px;
                font-family: "{font_family}";
            }}
            QTableWidget::item:selected {{
                background-color: #316AC5;
                color: white;
            }}
            QGroupBox {{
                font-weight: bold;
                font-family: "{font_family}";
                font-size: 9pt;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                font-family: "{font_family}";
            }}
            QTabWidget::pane {{
                border: 1px solid #ccc;
                top: -1px;
            }}
            QTabBar::tab {{
                background-color: #e0e0e0;
                border: 1px solid #ccc;
                padding: 5px 10px;
                margin-right: 2px;
                font-family: "{font_family}";
                font-size: 9pt;
            }}
            QTabBar::tab:selected {{
                background-color: white;
                border-bottom-color: white;
            }}
            QLineEdit {{
                font-family: "{font_family}";
                font-size: 9pt;
                padding: 3px;
                border: 1px solid #ccc;
                border-radius: 2px;
            }}
            QTextEdit {{
                font-family: "{font_family}";
                font-size: 9pt;
            }}
            QProgressBar {{
                font-family: "{font_family}";
                font-size: 8pt;
            }}
            QMenuBar {{
                font-family: "{font_family}";
                font-size: 9pt;
            }}
            QMenu {{
                font-family: "{font_family}";
                font-size: 9pt;
            }}
            QStatusBar {{
                font-family: "{font_family}";
                font-size: 8pt;
            }}
        """)
        
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, '打开FLV文件', '', 'FLV文件 (*.flv);;所有文件 (*)')
        if file_path:
            self.load_flv_file(file_path)
            
    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, '选择文件夹')
        if folder_path:
            self.load_flv_folder(folder_path)
            
    def load_flv_file(self, file_path):
        """加载FLV文件"""
        try:
            self.statusBar().showMessage(f'正在加载: {os.path.basename(file_path)}')
            logger.info(f"开始加载FLV文件: {file_path}")
            
            # 使用FLV处理器加载文件
            if self.flv_handler.load_file(file_path):
                # 获取文件信息
                file_info = self.flv_handler.get_file_info()
                
                # 更新文件列表
                self._add_file_to_table(file_info)
                
                # 加载视频到播放器
                if self.video_player.load_video(self.flv_handler):
                    self.statusBar().showMessage(f'已加载: {os.path.basename(file_path)}')
                    # 更新属性面板
                    self._update_properties_panel(file_info)
                    # 切换到视频预览标签页
                    self.center_tabs.setCurrentIndex(0)
                else:
                    self.statusBar().showMessage('视频加载失败')
                    QMessageBox.warning(self, '警告', '无法播放此FLV文件，但可以查看文件信息')
            else:
                self.statusBar().showMessage('文件加载失败')
                QMessageBox.critical(self, '错误', '无法加载FLV文件，请检查文件格式')
                
        except Exception as e:
            logger.error(f"加载FLV文件失败: {e}")
            self.statusBar().showMessage('加载失败')
            QMessageBox.critical(self, '错误', f'加载文件时发生错误：{str(e)}')
        
    def load_flv_folder(self, folder_path):
        # TODO: 实现文件夹加载逻辑
        self.statusBar().showMessage(f'正在扫描文件夹: {folder_path}')
        
    def on_file_selected(self):
        # TODO: 实现文件选择处理逻辑
        current_row = self.file_table.currentRow()
        if current_row >= 0:
            file_name = self.file_table.item(current_row, 0).text()
            self.statusBar().showMessage(f'已选择: {file_name}')
            
    def show_about(self):
        QMessageBox.about(self, '关于 lookFlv', 
                         'lookFlv - FLV文件分析工具\n\n'
                         '版本: 1.0.0\n'
                         '用于分析和查看FLV视频文件的详细信息。')
                         
    def _add_file_to_table(self, file_info):
        """添加文件信息到表格"""
        try:
            row = self.file_table.rowCount()
            self.file_table.insertRow(row)
            
            # 文件信息列
            items = [
                file_info.get('文件名', ''),
                file_info.get('文件大小', ''),
                file_info.get('持续时间', ''),
                file_info.get('视频编码', 'H.264'),  # 默认值
                file_info.get('音频编码', 'AAC'),    # 默认值
                file_info.get('分辨率', file_info.get('视频分辨率', '')),
                file_info.get('帧率', file_info.get('视频帧率', '')),
                file_info.get('视频比特率', ''),
                str(file_info.get('创建时间', ''))
            ]
            
            for col, item_text in enumerate(items):
                item = QTableWidgetItem(str(item_text))
                item.setFont(self.label_font)
                self.file_table.setItem(row, col, item)
                
        except Exception as e:
            logger.error(f"添加文件到表格失败: {e}")
            
    def _update_properties_panel(self, file_info):
        """更新属性面板"""
        try:
            # 更新基本信息
            basic_fields = [
                "文件路径", "文件大小", "持续时间", "创建时间", 
                "修改时间", "文件格式", "元数据版本"
            ]
            
            for field in basic_fields:
                if field in self.info_labels and field in file_info:
                    self.info_labels[field].setText(str(file_info[field]))
                    
            # 更新视频信息
            video_mapping = {
                "编解码器": "视频编码",
                "分辨率": "分辨率",
                "帧率": "视频帧率", 
                "比特率": "视频比特率",
                "总帧数": "总帧数",
                "关键帧数": "关键帧数",
                "颜色空间": "颜色空间",
                "像素格式": "像素格式"
            }
            
            for ui_field, data_field in video_mapping.items():
                label_key = f"视频_{ui_field}"
                if label_key in self.info_labels:
                    value = file_info.get(data_field, '-')
                    self.info_labels[label_key].setText(str(value))
                    
            # 更新音频信息
            audio_mapping = {
                "编解码器": "音频编码",
                "采样率": "音频采样率",
                "比特率": "音频比特率", 
                "声道数": "声道数",
                "位深度": "位深度",
                "编码格式": "编码格式",
                "总样本数": "总样本数"
            }
            
            for ui_field, data_field in audio_mapping.items():
                label_key = f"音频_{ui_field}"
                if label_key in self.info_labels:
                    value = file_info.get(data_field, '-')
                    self.info_labels[label_key].setText(str(value))
                    
        except Exception as e:
            logger.error(f"更新属性面板失败: {e}")
            
    def closeEvent(self, event):
        """窗口关闭事件"""
        try:
            # 关闭视频播放器
            if hasattr(self, 'video_player'):
                self.video_player.close_video()
                
            # 关闭FLV处理器
            if hasattr(self, 'flv_handler'):
                self.flv_handler.close()
                
            event.accept()
        except Exception as e:
            logger.error(f"关闭窗口时发生错误: {e}")
            event.accept()