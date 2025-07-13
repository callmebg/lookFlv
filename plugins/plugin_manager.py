# plugins/plugin_manager.py
class AnalysisPlugin:
    PLUGIN_API_VERSION = 1.0
    
    def __init__(self):
        self.name = "Unnamed Plugin"
        
    def register_hooks(self, hook_manager):
        """
        注册钩子函数到以下位置：
        - pre_tag_parse: Tag解析前
        - post_es_extract: ES提取后
        - report_generate: 报告生成时
        """
        pass