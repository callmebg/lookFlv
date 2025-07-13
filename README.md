# lookFlv
查看flv文件的小工具

# 项目结构
lookFlv/
├── core/                      # 核心解析引擎
│   ├── parser/                # 二进制解析层
│   │   ├── flv_header.py      # FLV头结构解析 (struct)
│   │   ├── tag_parser.py      # Tag解析器 (construct)
│   │   ├── es_processor.py    # ES流处理器 (PyAV)
│   │   └── rtmp_sniffer.py    # RTMP抓包工具 (librtmp)
│   │
│   ├── analysis/              # 分析逻辑层
│   │   ├── metadata_extractor.py  # 元数据提取 (flvlib)
│   │   ├── sync_analyzer.py   # 音画同步分析
│   │   ├── gop_visualizer.py  # GOP结构生成
│   │   └── error_detector.py  # 错误检测引擎
│   │
│   └── utils/                 # 核心工具
│       ├── binary_utils.py    # 二进制操作辅助
│       ├── timestamp_conv.py  # 时间戳转换
│       └── logging_system.py  # 日志处理 (log4cxx)
│
├── services/                  # 高级服务模块
│   ├── conversion_service.py  # 格式转换 (moviepy)
│   ├── report_generator.py    # 报告生成 (Jinja2)
│   ├── ai_analyser.py         # AI分析模块 (TensorFlow/PyTorch)
│   └── cloud_sync.py          # 云同步接口
│
├── gui/                       # 图形界面 (PyQt5)
│   ├── main_window.py         # 主窗口
│   ├── widgets/               
│   │   ├── hex_viewer.py      # 十六进制视图 (QHexView)
│   │   ├── timeline_chart.py  # 时间轴图表 (PyQtGraph)
│   │   ├── gop_diagram.py     # GOP结构图
│   │   └── stream_monitor.py  # 实时流仪表盘
│   │
│   ├── resources/             # 界面资源
│   │   ├── icons/
│   │   └── style.qss          # 样式表
│   │
│   └── dialogs/               # 对话框
│       ├── settings_dialog.py
│       └── export_dialog.py
│
├── plugins/                   # 插件系统
│   ├── plugin_manager.py      # 插件管理器
│   ├── avs3_parser.py         # AVS3解析插件
│   └── vvc_parser.py          # VVC解析插件 (ctypes集成VVDecc)
│
├── tests/                     # 测试套件
│   ├── unit_tests/            # 单元测试
│   │   ├── test_flv_parser.py
│   │   └── test_sync_analysis.py
│   │
│   ├── integration_tests/     # 集成测试
│   │   ├── test_full_analysis.py
│   │   └── test_stream_capture.py
│   │
│   └── sample_files/          # 测试样本
│       ├── valid_samples/
│       └── error_samples/
│
├── scripts/                   # 辅助脚本
│   ├── dependency_check.py    # 环境检查
│   ├── win_runtime_fix.py     # Windows运行库修复
│   └── build_installer.py     # 打包脚本
│
├── docs/                      # 文档
│   ├── developer_guide.md     # 开发文档
│   └── user_manual.md         # 用户手册
│
├── main.py                    # 程序入口
├── config.py                  # 全局配置
├── requirements.txt           # 依赖清单
└── .env                       # 环境变量
