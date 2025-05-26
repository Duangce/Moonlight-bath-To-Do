import json
import os
from typing import Dict

class SettingsModel:
    """
    设置管理类
    负责保存和加载应用程序设置
    """
    def __init__(self):
        """初始化设置管理器"""
        self.settings_file = 'settings.json'
        self.default_settings = {
            'window_width': 400,
            'window_height': 600,
            'opacity': 100,
            'always_on_top': True,
            'todo_item_height': 60  # 每个待办事项的固定高度
        }
        self.settings = self.load_settings()

    def load_settings(self) -> Dict:
        """
        加载设置
        如果设置文件不存在，则使用默认设置
        """
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # 确保所有默认设置都存在
                    for key, value in self.default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
        return self.default_settings.copy()

    def save_settings(self, settings: Dict):
        """
        保存设置到文件
        
        参数:
            settings: 要保存的设置字典
        """
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            self.settings = settings
        except Exception as e:
            print(f"Error saving settings: {str(e)}")

    def get_setting(self, key: str, default=None):
        """
        获取指定设置项的值
        
        参数:
            key: 设置项的键
            default: 默认值
        返回:
            设置项的值
        """
        return self.settings.get(key, default)

    def update_setting(self, key: str, value):
        """
        更新设置项的值
        
        参数:
            key: 设置项的键
            value: 新的值
        """
        self.settings[key] = value
        self.save_settings(self.settings) 