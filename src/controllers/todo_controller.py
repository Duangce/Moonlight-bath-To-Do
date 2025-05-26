# 导入模型和视图
from src.models.todo_model import TodoModel
from src.views.main_window import MainWindow

class TodoController:
    """
    待办事项控制器类
    负责协调模型和视图之间的交互
    实现MVC架构中的控制器部分
    """
    def __init__(self):
        """
        初始化控制器
        创建模型和视图实例，并建立它们之间的连接
        """
        # 创建模型和视图实例
        self.model = TodoModel()
        self.view = MainWindow()
        
        # 连接视图的信号到控制器的方法
        self.view.add_todo_signal.connect(self.add_todo)      # 添加待办事项信号
        self.view.delete_todo_signal.connect(self.delete_todo)  # 删除待办事项信号
        self.view.toggle_todo_signal.connect(self.toggle_todo)  # 切换状态信号
        self.view.move_todo_signal.connect(self.move_todo)    # 移动待办事项信号
        
        # 初始化视图显示
        self.update_view()
        
    def add_todo(self, text: str):
        """
        处理添加待办事项的请求
        
        参数:
            text: 待办事项的文本内容
        """
        self.model.add_todo(text)
        self.update_view()
        
    def delete_todo(self, index: int):
        """
        处理删除待办事项的请求
        
        参数:
            index: 要删除的待办事项索引
        """
        self.model.delete_todo(index)
        self.update_view()
        
    def toggle_todo(self, index: int):
        """
        处理切换待办事项状态的请求
        
        参数:
            index: 要切换状态的待办事项索引
        """
        self.model.toggle_completed(index)
        self.update_view()

    def move_todo(self, index: int, direction: int):
        """
        处理移动待办事项的请求
        
        参数:
            index: 要移动的待办事项索引
            direction: 移动方向（-1: 向上, 1: 向下, -index: 置顶）
        """
        todos = self.model.todos
        if not todos:
            return

        if direction == -index:  # 置顶
            todo = todos.pop(index)
            todos.insert(0, todo)
        else:
            new_index = index + direction
            if 0 <= new_index < len(todos):
                todos[index], todos[new_index] = todos[new_index], todos[index]
        
        self.model.save_todos()
        self.update_view()
        
    def update_view(self):
        """
        更新视图显示
        将模型中的最新数据传递给视图
        """
        self.view.update_todo_list(self.model.todos)
        
    def run(self):
        """
        运行应用程序
        显示主窗口
        """
        self.view.show() 