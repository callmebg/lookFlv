# -*- coding: utf-8 -*-
"""
FLV 文件处理器
用于加载、解析和处理FLV视频文件
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import struct

try:
    import flvlib
    from flvlib import tags
except ImportError:
    flvlib = None

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    VideoFileClip = None

from core import get_logger, format_file_size, format_duration

logger = get_logger(__name__)


class FLVFileHandler:
    """FLV文件处理器"""
    
    def __init__(self):
        self.file_path = None
        self.file_info = {}
        self.metadata = {}
        self.tags_data = []
        self.video_clip = None
        
    def load_file(self, file_path: str) -> bool:
        """
        加载FLV文件
        
        Args:
            file_path: FLV文件路径
            
        Returns:
            bool: 加载是否成功
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                logger.error(f"文件不存在: {file_path}")
                return False
                
            if not file_path.suffix.lower() == '.flv':
                logger.warning(f"文件可能不是FLV格式: {file_path}")
                
            self.file_path = file_path
            
            # 获取基本文件信息
            self._get_basic_info()
            
            # 解析FLV结构
            if flvlib:
                self._parse_flv_structure()
            else:
                logger.warning("flvlib未安装，跳过FLV结构解析")
                
            # 加载视频文件用于播放
            if VideoFileClip:
                self._load_video_clip()
            else:
                logger.warning("moviepy未安装，无法播放视频")
                
            logger.info(f"成功加载FLV文件: {file_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"加载FLV文件失败: {e}")
            return False
            
    def _get_basic_info(self):
        """获取基本文件信息"""
        stat = self.file_path.stat()
        self.file_info = {
            '文件路径': str(self.file_path),
            '文件名': self.file_path.name,
            '文件大小': format_file_size(stat.st_size),
            '文件大小_字节': stat.st_size,
            '创建时间': stat.st_ctime,
            '修改时间': stat.st_mtime,
            '文件格式': 'FLV'
        }
        
    def _parse_flv_structure(self):
        """解析FLV文件结构"""
        try:
            with open(self.file_path, 'rb') as f:
                flv_file = flvlib.FLV(f)
                
                # 读取FLV头部
                header = flv_file.header
                self.file_info.update({
                    'FLV版本': header.version,
                    '包含视频': header.has_video,
                    '包含音频': header.has_audio,
                })
                
                # 解析标签
                self.tags_data = []
                video_count = 0
                audio_count = 0
                script_count = 0
                total_duration = 0
                
                for tag in flv_file.iter_tags():
                    tag_info = {
                        '类型': tag.__class__.__name__,
                        '时间戳': tag.timestamp,
                        '数据大小': tag.size,
                    }
                    
                    if isinstance(tag, tags.VideoTag):
                        video_count += 1
                        tag_info.update({
                            '编解码器': tag.codec,
                            '帧类型': tag.frame_type,
                        })
                    elif isinstance(tag, tags.AudioTag):
                        audio_count += 1
                        tag_info.update({
                            '编解码器': tag.codec,
                            '采样率': tag.sample_rate,
                            '声道': tag.channels,
                        })
                    elif isinstance(tag, tags.ScriptTag):
                        script_count += 1
                        # 尝试解析元数据
                        if hasattr(tag, 'name') and tag.name == 'onMetaData':
                            try:
                                self.metadata = tag.variable
                            except:
                                pass
                    
                    self.tags_data.append(tag_info)
                    total_duration = max(total_duration, tag.timestamp)
                
                # 更新统计信息
                self.file_info.update({
                    '视频标签数': video_count,
                    '音频标签数': audio_count,
                    '脚本标签数': script_count,
                    '总标签数': len(self.tags_data),
                    '持续时间': format_duration(total_duration / 1000),
                    '持续时间_秒': total_duration / 1000,
                })
                
                # 从元数据获取更多信息
                if self.metadata:
                    self._parse_metadata()
                    
        except Exception as e:
            logger.error(f"解析FLV结构失败: {e}")
            
    def _parse_metadata(self):
        """解析元数据"""
        if not self.metadata:
            return
            
        try:
            # 视频信息
            if 'width' in self.metadata and 'height' in self.metadata:
                self.file_info['分辨率'] = f"{int(self.metadata['width'])}x{int(self.metadata['height'])}"
                
            if 'framerate' in self.metadata:
                self.file_info['帧率'] = f"{self.metadata['framerate']:.2f} fps"
                
            if 'videodatarate' in self.metadata:
                self.file_info['视频比特率'] = f"{self.metadata['videodatarate']:.0f} kbps"
                
            # 音频信息
            if 'audiodatarate' in self.metadata:
                self.file_info['音频比特率'] = f"{self.metadata['audiodatarate']:.0f} kbps"
                
            if 'audiosamplerate' in self.metadata:
                self.file_info['音频采样率'] = f"{self.metadata['audiosamplerate']:.0f} Hz"
                
            # 其他信息
            if 'duration' in self.metadata:
                duration = self.metadata['duration']
                self.file_info['持续时间'] = format_duration(duration)
                self.file_info['持续时间_秒'] = duration
                
            if 'filesize' in self.metadata:
                self.file_info['元数据文件大小'] = format_file_size(self.metadata['filesize'])
                
        except Exception as e:
            logger.error(f"解析元数据失败: {e}")
            
    def _load_video_clip(self):
        """加载视频文件用于播放"""
        try:
            self.video_clip = VideoFileClip(str(self.file_path))
            
            # 更新视频信息
            if self.video_clip.duration:
                self.file_info['视频时长'] = format_duration(self.video_clip.duration)
                
            if hasattr(self.video_clip, 'fps') and self.video_clip.fps:
                self.file_info['视频帧率'] = f"{self.video_clip.fps:.2f} fps"
                
            if hasattr(self.video_clip, 'size') and self.video_clip.size:
                w, h = self.video_clip.size
                self.file_info['视频分辨率'] = f"{w}x{h}"
                
        except Exception as e:
            logger.error(f"加载视频文件失败: {e}")
            self.video_clip = None
            
    def get_frame_at_time(self, time_seconds: float):
        """
        获取指定时间的视频帧
        
        Args:
            time_seconds: 时间（秒）
            
        Returns:
            numpy.ndarray: 视频帧数据，如果失败返回None
        """
        if not self.video_clip:
            return None
            
        try:
            # 确保时间在有效范围内
            duration = self.video_clip.duration
            time_seconds = max(0, min(time_seconds, duration))
            
            # 获取帧
            frame = self.video_clip.get_frame(time_seconds)
            return frame
            
        except Exception as e:
            logger.error(f"获取视频帧失败: {e}")
            return None
            
    def get_file_info(self) -> Dict[str, Any]:
        """获取文件信息"""
        return self.file_info.copy()
        
    def get_metadata(self) -> Dict[str, Any]:
        """获取元数据"""
        return self.metadata.copy()
        
    def get_tags_data(self) -> List[Dict[str, Any]]:
        """获取标签数据"""
        return self.tags_data.copy()
        
    def close(self):
        """关闭文件并释放资源"""
        if self.video_clip:
            try:
                self.video_clip.close()
            except:
                pass
            self.video_clip = None
            
        self.file_path = None
        self.file_info = {}
        self.metadata = {}
        self.tags_data = []
        
    def __del__(self):
        """析构函数"""
        self.close()