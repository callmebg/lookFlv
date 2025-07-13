# -*- coding: utf-8 -*-
"""
Core utilities for lookFlv
通用工具函数
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path


def init_logging(log_level=logging.INFO, log_file=None, console_output=True):
    """
    初始化日志系统
    
    Args:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: 日志文件路径，如果为None则使用默认路径
        console_output: 是否输出到控制台
    """
    # 创建logs目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 设置默认日志文件名
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = log_dir / f"lookflv_{timestamp}.log"
    
    # 配置日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 创建formatter
    formatter = logging.Formatter(log_format, date_format)
    
    # 获取根logger
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # 清除现有的handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 文件handler
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"警告: 无法创建日志文件 {log_file}: {e}")
    
    # 控制台handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 记录初始化信息
    logger.info("日志系统初始化完成")
    logger.info(f"日志级别: {logging.getLevelName(log_level)}")
    logger.info(f"日志文件: {log_file}")
    logger.info(f"控制台输出: {console_output}")
    
    return logger


def get_logger(name):
    """
    获取指定名称的logger
    
    Args:
        name: logger名称，通常使用 __name__
        
    Returns:
        logging.Logger: 配置好的logger实例
    """
    return logging.getLogger(name)


def set_log_level(level):
    """
    动态设置日志级别
    
    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # 更新所有handlers的级别
    for handler in logger.handlers:
        handler.setLevel(level)
    
    logger.info(f"日志级别已更改为: {logging.getLevelName(level)}")


def log_exception(logger, exception, context=""):
    """
    记录异常信息
    
    Args:
        logger: logger实例
        exception: 异常对象
        context: 上下文信息
    """
    if context:
        logger.error(f"{context}: {type(exception).__name__}: {exception}")
    else:
        logger.error(f"{type(exception).__name__}: {exception}")
    
    # 记录详细的异常堆栈
    logger.debug("异常详细信息:", exc_info=True)


def format_file_size(size_bytes):
    """
    格式化文件大小
    
    Args:
        size_bytes: 文件大小（字节）
        
    Returns:
        str: 格式化后的文件大小
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


def format_duration(seconds):
    """
    格式化时长
    
    Args:
        seconds: 秒数
        
    Returns:
        str: 格式化后的时长 (HH:MM:SS)
    """
    if seconds is None or seconds < 0:
        return "00:00:00"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def ensure_directory(path):
    """
    确保目录存在，如果不存在则创建
    
    Args:
        path: 目录路径
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def safe_filename(filename):
    """
    生成安全的文件名，移除非法字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        str: 安全的文件名
    """
    import re
    # 移除或替换非法字符
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 移除首尾空格和点
    safe_name = safe_name.strip('. ')
    # 限制长度
    if len(safe_name) > 200:
        safe_name = safe_name[:200]
    return safe_name if safe_name else "unnamed"