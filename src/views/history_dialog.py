from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QHeaderView)
from PyQt5.QtCore import Qt

class HistoryDialog(QDialog):
    """历史记录查看对话框"""
    
    def __init__(self, history_model, parent=None):
        super().__init__(parent)
        self.history_model = history_model
        self.current_sort = {'column': 'completed_time', 'reverse': False}
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("已完成待办事项历史")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout()
        
        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["待办事项", "创建时间", "完成时间", "持续时间(天)"])
        
        # 设置表格列宽
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # 待办事项列自适应宽度
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        # 设置表头可点击
        header.sectionClicked.connect(self.on_header_clicked)
        
        # 添加数据
        self.update_table()
        
        layout.addWidget(self.table)
        
        # 添加关闭按钮
        button_layout = QHBoxLayout()
        close_button = QPushButton("关闭")
        close_button.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def update_table(self):
        """更新表格数据"""
        history = self.history_model.get_history(
            self.current_sort['column'],
            self.current_sort['reverse']
        )
        
        self.table.setRowCount(len(history))
        for row, item in enumerate(history):
            self.table.setItem(row, 0, QTableWidgetItem(item['text']))
            self.table.setItem(row, 1, QTableWidgetItem(item['created_time']))
            self.table.setItem(row, 2, QTableWidgetItem(item['completed_time']))
            self.table.setItem(row, 3, QTableWidgetItem(str(item['duration'])))
    
    def on_header_clicked(self, column):
        """处理表头点击事件"""
        column_names = ['text', 'created_time', 'completed_time', 'duration']
        clicked_column = column_names[column]
        
        # 如果点击的是当前排序列，则切换排序方向
        if clicked_column == self.current_sort['column']:
            self.current_sort['reverse'] = not self.current_sort['reverse']
        else:
            self.current_sort['column'] = clicked_column
            self.current_sort['reverse'] = False
        
        self.update_table() 