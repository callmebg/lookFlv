# -*- coding: utf-8 -*-
"""
视频播放器组件
用于在GUI中播放和显示视频
"""

import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSlider, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QFont

from core import get_logger

logger = get_logger(__name__)


class VideoPlayer(QWidget):
    """视频播放器组件"""
    
    # 信号
    positionChanged = pyqtSignal(float)  # 播放位置改变
    durationChanged = pyqtSignal(float)  # 总时长改变
    stateChanged = pyqtSignal(str)       # 播放状态改变
    
    def __init__(self):
        super().__init__()
        self.flv_handler = None
        self.duration = 0.0
        self.current_position = 0.0
        self.is_playing = False
        self.playback_timer = QTimer()
        self.playback_timer.timeout.connect(self._update_playback)
        
        # 设置微软雅黑字体
        self.font = QFont("Microsoft YaHei", 9)
        
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 视频显示区域
        self.video_label = QLabel()
        self.video_label.setMinimumSize(400, 300)
        self.video_label.setStyleSheet("""
            QLabel {
                border: 2px solid #ccc;
                background-color: #000;
                color: white;
                font-family: 'Microsoft YaHei';
                font-size: 14px;
            }
        """)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setText("请打开FLV文件")
        self.video_label.setScaledContents(True)
        self.video_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.video_label)
        
        # 进度条
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setMinimum(0)
        self.position_slider.setMaximum(1000)
        self.position_slider.setValue(0)
        self.position_slider.sliderPressed.connect(self._slider_pressed)
        self.position_slider.sliderReleased.connect(self._slider_released)
        self.position_slider.valueChanged.connect(self._slider_value_changed)
        layout.addWidget(self.position_slider)
        
        # 控制按钮区域
        control_layout = QHBoxLayout()
        
        self.play_button = QPushButton("播放")
        self.play_button.setFont(self.font)
        self.play_button.clicked.connect(self.toggle_playback)
        self.play_button.setMinimumWidth(80)
        
        self.stop_button = QPushButton("停止")
        self.stop_button.setFont(self.font)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setMinimumWidth(80)
        
        # 时间标签
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setFont(self.font)
        self.time_label.setMinimumWidth(100)
        
        # 音量控制（简化版本）
        volume_label = QLabel("音量:")
        volume_label.setFont(self.font)
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)
        self.volume_slider.setMaximumWidth(100)
        
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.time_label)
        control_layout.addStretch()
        control_layout.addWidget(volume_label)
        control_layout.addWidget(self.volume_slider)
        
        layout.addLayout(control_layout)
        
        # 状态信息
        self.status_label = QLabel("就绪")
        self.status_label.setFont(self.font)
        self.status_label.setStyleSheet("color: #666; font-size: 10px; font-family: 'Microsoft YaHei';")
        layout.addWidget(self.status_label)
        
        # 禁用控制按钮
        self._set_controls_enabled(False)
        
    def load_video(self, flv_handler):
        """
        加载视频
        
        Args:
            flv_handler: FLV文件处理器实例
        """
        try:
            self.flv_handler = flv_handler
            
            if not flv_handler or not flv_handler.video_clip:
                self.video_label.setText("无法加载视频\n请检查文件格式")
                self.status_label.setText("错误: 无法加载视频")
                self._set_controls_enabled(False)
                return False
                
            # 获取视频信息
            self.duration = flv_handler.video_clip.duration
            self.current_position = 0.0
            
            # 更新界面
            self._update_duration_display()
            self._set_controls_enabled(True)
            
            # 显示第一帧
            self._display_frame_at_position(0.0)
            
            self.status_label.setText(f"已加载: {flv_handler.file_info.get('文件名', 'unknown')}")
            
            # 发送信号
            self.durationChanged.emit(self.duration)
            
            return True
            
        except Exception as e:
            logger.error(f"加载视频失败: {e}")
            self.video_label.setText(f"加载失败\n{str(e)}")
            self.status_label.setText(f"错误: {str(e)}")
            self._set_controls_enabled(False)
            return False
            
    def toggle_playback(self):
        """切换播放/暂停状态"""
        if self.is_playing:
            self.pause()
        else:
            self.play()
            
    def play(self):
        """开始播放"""
        if not self.flv_handler or not self.flv_handler.video_clip:
            return
            
        self.is_playing = True
        self.play_button.setText("暂停")
        self.playback_timer.start(50)  # 20 FPS更新
        self.status_label.setText("播放中...")
        self.stateChanged.emit("playing")
        
    def pause(self):
        """暂停播放"""
        self.is_playing = False
        self.play_button.setText("播放")
        self.playback_timer.stop()
        self.status_label.setText("已暂停")
        self.stateChanged.emit("paused")
        
    def stop(self):
        """停止播放"""
        self.is_playing = False
        self.play_button.setText("播放")
        self.playback_timer.stop()
        self.current_position = 0.0
        self._update_position_display()
        self._display_frame_at_position(0.0)
        self.status_label.setText("已停止")
        self.stateChanged.emit("stopped")
        
    def seek_to_position(self, position: float):
        """
        跳转到指定位置
        
        Args:
            position: 位置（0.0-1.0）
        """
        if not self.flv_handler or not self.flv_handler.video_clip:
            return
            
        self.current_position = position * self.duration
        self._update_position_display()
        self._display_frame_at_position(self.current_position)
        self.positionChanged.emit(self.current_position)
        
    def _update_playback(self):
        """更新播放进度"""
        if not self.is_playing or not self.flv_handler:
            return
            
        # 更新位置
        self.current_position += 0.05  # 50ms步进
        
        if self.current_position >= self.duration:
            # 播放结束
            self.current_position = self.duration
            self.pause()
            
        self._update_position_display()
        self._display_frame_at_position(self.current_position)
        self.positionChanged.emit(self.current_position)
        
    def _display_frame_at_position(self, position: float):
        """在指定位置显示视频帧"""
        if not self.flv_handler:
            return
            
        try:
            # 获取视频帧
            frame = self.flv_handler.get_frame_at_time(position)
            if frame is None:
                return
                
            # 转换为QImage
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            
            # 确保数据类型正确
            if frame.dtype != np.uint8:
                frame = frame.astype(np.uint8)
                
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            
            # 转换为QPixmap并显示
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap)
            
        except Exception as e:
            logger.error(f"显示视频帧失败: {e}")
            
    def _update_position_display(self):
        """更新进度显示"""
        if self.duration > 0:
            # 更新滑块
            position_percent = int((self.current_position / self.duration) * 1000)
            self.position_slider.setValue(position_percent)
            
        # 更新时间标签
        self._update_duration_display()
        
    def _update_duration_display(self):
        """更新时长显示"""
        current_str = self._format_time(self.current_position)
        total_str = self._format_time(self.duration)
        self.time_label.setText(f"{current_str} / {total_str}")
        
    def _format_time(self, seconds: float) -> str:
        """格式化时间显示"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
        
    def _set_controls_enabled(self, enabled: bool):
        """设置控制按钮的启用状态"""
        self.play_button.setEnabled(enabled)
        self.stop_button.setEnabled(enabled)
        self.position_slider.setEnabled(enabled)
        
    def _slider_pressed(self):
        """滑块按下时暂停播放"""
        self._was_playing = self.is_playing
        if self.is_playing:
            self.pause()
            
    def _slider_released(self):
        """滑块释放时恢复播放状态"""
        position_percent = self.position_slider.value() / 1000.0
        self.seek_to_position(position_percent)
        
        if hasattr(self, '_was_playing') and self._was_playing:
            self.play()
            
    def _slider_value_changed(self, value):
        """滑块值改变时更新显示"""
        if not hasattr(self, '_was_playing'):  # 只在拖拽时更新
            return
            
        position_percent = value / 1000.0
        self.current_position = position_percent * self.duration
        self._update_duration_display()
        
    def close_video(self):
        """关闭视频"""
        self.stop()
        if self.flv_handler:
            self.flv_handler.close()
        self.flv_handler = None
        self.video_label.clear()
        self.video_label.setText("请打开FLV文件")
        self._set_controls_enabled(False)
        self.status_label.setText("就绪")
        
    def get_current_position(self) -> float:
        """获取当前播放位置（秒）"""
        return self.current_position
        
    def get_duration(self) -> float:
        """获取总时长（秒）"""
        return self.duration
        
    def is_video_loaded(self) -> bool:
        """检查是否已加载视频"""
        return self.flv_handler is not None and self.flv_handler.video_clip is not None