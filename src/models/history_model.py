import json
import os
from datetime import datetime, timedelta

class HistoryModel:
    """历史记录模型类，用于管理已完成的待办事项"""
    
    def __init__(self):
        self.history_file = "history.json"
        self.history = self.load_history()
    
    def load_history(self):
        """加载历史记录"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """保存历史记录"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def add_completed_todo(self, todo_text, created_time):
        """添加已完成的待办事项到历史记录"""
        completed_time = datetime.now()
        duration = (completed_time - created_time).total_seconds() / (24 * 3600)  # 转换为天
        duration = round(duration, 1)  # 保留一位小数
        
        history_item = {
            'text': todo_text,
            'created_time': created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'completed_time': completed_time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': duration
        }
        
        self.history.append(history_item)
        self.save_history()
    
    def get_history(self, sort_by='completed_time', reverse=False):
        """获取历史记录，支持排序"""
        history = self.history.copy()
        
        if sort_by == 'text':
            history.sort(key=lambda x: x['text'], reverse=reverse)
        elif sort_by == 'created_time':
            history.sort(key=lambda x: x['created_time'], reverse=reverse)
        elif sort_by == 'completed_time':
            history.sort(key=lambda x: x['completed_time'], reverse=reverse)
        elif sort_by == 'duration':
            history.sort(key=lambda x: x['duration'], reverse=reverse)
            
        return history
    
    def clear_old_completed_todos(self):
        """清除旧的历史记录"""
        # 不再删除历史记录，只返回今天的日期用于过滤显示
        return datetime.now().date() 