# 导入系统相关模块
import sys
import os
# 导入PyQt5应用程序类
from PyQt5.QtWidgets import QApplication

def get_resource_path(relative_path):
    """
    获取资源文件的绝对路径
    用于处理打包后的资源文件路径问题
    
    参数:
        relative_path: 相对路径
    返回:
        资源文件的绝对路径
    """
    # 检查是否在打包环境中运行
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    # 在开发环境中运行
    return os.path.join(os.path.abspath("."), relative_path)

# 添加项目根目录到 Python 路径，确保可以正确导入项目模块
sys.path.insert(0, get_resource_path('src'))

# 导入待办事项控制器
from src.controllers.todo_controller import TodoController

def main():
    """
    应用程序入口函数
    创建并运行待办事项应用程序
    """
    # 创建Qt应用程序实例
    app = QApplication(sys.argv)
    # 创建并初始化控制器
    controller = TodoController()
    # 运行应用程序
    controller.run()
    # 进入应用程序主循环
    sys.exit(app.exec_())

# 当直接运行此文件时执行main函数
if __name__ == '__main__':
    main() 