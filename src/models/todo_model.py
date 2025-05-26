# 导入所需的模块
import json
import os
from datetime import datetime
from typing import List, Dict

class TodoModel:
    """
    待办事项数据模型类
    负责待办事项数据的存储、加载和管理
    """
    def __init__(self):
        """
        初始化待办事项模型
        创建空列表并加载已保存的待办事项
        """
        self.todos: List[Dict] = []  # 存储待办事项的列表
        self.data_file = 'todos.json'  # 数据文件路径
        self.load_todos()  # 加载已保存的待办事项

    def add_todo(self, text: str) -> Dict:
        """
        添加新的待办事项
        
        参数:
            text: 待办事项的文本内容
        返回:
            新创建的待办事项字典
        """
        todo = {
            'text': text,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),  # 创建时间
            'completed': False  # 完成状态
        }
        self.todos.append(todo)
        self.save_todos()  # 保存到文件
        return todo

    def delete_todo(self, index: int) -> bool:
        """
        删除指定索引的待办事项
        
        参数:
            index: 要删除的待办事项索引
        返回:
            删除是否成功
        """
        try:
            self.todos.pop(index)
            self.save_todos()
            return True
        except IndexError:
            return False

    def toggle_completed(self, index: int) -> bool:
        """
        切换待办事项的完成状态
        
        参数:
            index: 要切换状态的待办事项索引
        返回:
            切换是否成功
        """
        try:
            self.todos[index]['completed'] = not self.todos[index]['completed']
            self.save_todos()
            return True
        except IndexError:
            return False

    def save_todos(self):
        """
        将待办事项列表保存到文件
        使用JSON格式存储，支持中文
        """
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)

    def load_todos(self):
        """
        从文件加载待办事项列表
        如果文件不存在或加载失败，则创建空列表
        """
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.todos = json.load(f)
        except Exception as e:
            print(f"Error loading todos: {str(e)}")
            self.todos = [] 