from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                             QMessageBox, QSystemTrayIcon, QMenu, QDialog, QLabel,
                             QCheckBox, QVBoxLayout, QSpinBox, QSlider, QFrame,
                             QSizePolicy, QMenu, QAction, QScrollArea, QKeySequenceEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect, QTimer
from PyQt5.QtGui import QFont, QIcon, QColor, QCursor, QKeySequence
from src.models.settings_model import SettingsModel
from src.models.history_model import HistoryModel
from src.views.history_dialog import HistoryDialog
from src.models.todo_model import TodoModel
from datetime import datetime
import os

class TodoItemWidget(QFrame):
    """
    自定义待办事项组件
    包含待办事项内容和操作按钮
    """
    move_up_signal = pyqtSignal(int)
    move_down_signal = pyqtSignal(int)
    move_to_top_signal = pyqtSignal(int)
    delete_signal = pyqtSignal(int)
    complete_signal = pyqtSignal(int)

    def __init__(self, index, text, completed=False, settings_model=None, parent=None):
        super().__init__(parent)
        self.index = index
        self.settings_model = settings_model
        self.init_ui(text, completed)
        self.setMouseTracking(True)  # 启用鼠标追踪

    def init_ui(self, text, completed):
        """初始化待办事项界面"""
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin: 2px;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)  # 设置内边距
        
        # 文本标签
        self.text_label = QLabel(text)
        font_size = self.settings_model.get_setting('todo_font_size', 12) if self.settings_model else 12
        text_margin = self.settings_model.get_setting('text_margin', 2) if self.settings_model else 2
        self.text_label.setStyleSheet(f"""
            QLabel {{
                font-size: {font_size}px;
                border: none;
                background: transparent;
                padding-left: {text_margin}em;
            }}
        """)
        if completed:
            self.text_label.setStyleSheet(f"""
                QLabel {{
                    font-size: {font_size}px;
                    color: gray;
                    text-decoration: line-through;
                    border: none;
                    background: transparent;
                    padding-left: {text_margin}em;
                }}
            """)
        
        # 右侧按钮组
        right_buttons = QHBoxLayout()
        right_buttons.setSpacing(2)  # 设置按钮之间的间距
        
        # 控制按钮
        top_btn = QPushButton("置顶")
        up_btn = QPushButton("上移")
        down_btn = QPushButton("下移")
        
        for btn in [top_btn, up_btn, down_btn]:
            btn.setFixedSize(40, 24)
            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #ccc;
                    background: #f0f0f0;
                    border-radius: 3px;
                    padding: 2px;
                }
                QPushButton:hover {
                    background: #e0e0e0;
                    border-color: #999;
                }
            """)
        
        top_btn.clicked.connect(lambda: self.move_to_top_signal.emit(self.index))
        up_btn.clicked.connect(lambda: self.move_up_signal.emit(self.index))
        down_btn.clicked.connect(lambda: self.move_down_signal.emit(self.index))
        
        # 菜单按钮
        menu_btn = QPushButton("⋮")
        menu_btn.setFixedSize(24, 24)
        menu_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #ccc;
                background: #f0f0f0;
                border-radius: 3px;
                font-size: 16px;
            }
            QPushButton:hover {
                background: #e0e0e0;
                border-color: #999;
            }
        """)
        
        # 创建菜单
        menu = QMenu()
        complete_action = QAction("完成", self)
        delete_action = QAction("删除", self)
        
        complete_action.triggered.connect(lambda: self.complete_signal.emit(self.index))
        delete_action.triggered.connect(lambda: self.delete_signal.emit(self.index))
        
        menu.addAction(complete_action)
        menu.addAction(delete_action)
        menu_btn.setMenu(menu)
        
        # 添加所有按钮到右侧按钮组
        right_buttons.addWidget(top_btn)
        right_buttons.addWidget(up_btn)
        right_buttons.addWidget(down_btn)
        right_buttons.addWidget(menu_btn)
        
        # 添加到主布局
        layout.addWidget(self.text_label, 1)
        layout.addLayout(right_buttons)
        
        self.setLayout(layout)

    def enterEvent(self, event):
        """鼠标进入事件"""
        # 创建放大动画
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)  # 动画持续时间（毫秒）
        
        # 获取当前位置和大小
        current_geometry = self.geometry()
        # 计算放大后的位置和大小
        new_geometry = QRect(
            current_geometry.x() - 2,  # 向左偏移
            current_geometry.y() - 2,  # 向上偏移
            current_geometry.width() + 4,  # 宽度增加
            current_geometry.height() + 4   # 高度增加
        )
        
        self.animation.setStartValue(current_geometry)
        self.animation.setEndValue(new_geometry)
        self.animation.start()
        
        # 设置高亮样式
        self.setStyleSheet("""
            QFrame {
                background-color: #f8f8f8;
                border: 1px solid #999;
                border-radius: 5px;
                margin: 2px;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开事件"""
        # 创建缩小动画
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)  # 动画持续时间（毫秒）
        
        # 获取当前位置和大小
        current_geometry = self.geometry()
        # 计算缩小后的位置和大小
        new_geometry = QRect(
            current_geometry.x() + 2,  # 向右偏移
            current_geometry.y() + 2,  # 向下偏移
            current_geometry.width() - 4,  # 宽度减少
            current_geometry.height() - 4   # 高度减少
        )
        
        self.animation.setStartValue(current_geometry)
        self.animation.setEndValue(new_geometry)
        self.animation.start()
        
        # 恢复原始样式
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin: 2px;
            }
        """)
        super().leaveEvent(event)

class SettingsDialog(QDialog):
    """
    设置对话框类
    用于显示和修改应用程序设置
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setFixedSize(300, 450)  # 增加高度以容纳新的按钮
        self.settings_model = SettingsModel()
        self.history_model = HistoryModel()
        self.init_ui()

    def init_ui(self):
        """初始化设置界面"""
        layout = QVBoxLayout()
        
        # 窗口大小设置
        size_layout = QHBoxLayout()
        size_label = QLabel("窗口宽度:")
        self.width_spin = QSpinBox()
        self.width_spin.setRange(200, 800)
        self.width_spin.setValue(self.settings_model.get_setting('window_width', 400))
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.width_spin)
        layout.addLayout(size_layout)

        # 窗口高度设置
        height_layout = QHBoxLayout()
        height_label = QLabel("窗口高度:")
        self.height_spin = QSpinBox()
        self.height_spin.setRange(300, 1200)
        self.height_spin.setValue(self.settings_model.get_setting('window_height', 600))
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.height_spin)
        layout.addLayout(height_layout)
        
        # 透明度设置
        opacity_layout = QHBoxLayout()
        opacity_label = QLabel("透明度:")
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(30, 100)
        self.opacity_slider.setValue(self.settings_model.get_setting('opacity', 100))
        opacity_layout.addWidget(opacity_label)
        opacity_layout.addWidget(self.opacity_slider)
        layout.addLayout(opacity_layout)
        
        # 待办事项字体大小设置
        font_size_layout = QHBoxLayout()
        font_size_label = QLabel("字体大小:")
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 50)
        self.font_size_spin.setValue(self.settings_model.get_setting('todo_font_size', 12))
        font_size_layout.addWidget(font_size_label)
        font_size_layout.addWidget(self.font_size_spin)
        layout.addLayout(font_size_layout)
        
        # 待办事项框高度设置
        item_height_layout = QHBoxLayout()
        item_height_label = QLabel("框高度:")
        self.item_height_spin = QSpinBox()
        self.item_height_spin.setRange(40, 200)
        self.item_height_spin.setValue(self.settings_model.get_setting('todo_item_height', 60))
        item_height_layout.addWidget(item_height_label)
        item_height_layout.addWidget(self.item_height_spin)
        layout.addLayout(item_height_layout)

        # 文本左边距设置
        text_margin_layout = QHBoxLayout()
        text_margin_label = QLabel("文本左边距:")
        self.text_margin_spin = QSpinBox()
        self.text_margin_spin.setRange(0, 20)
        self.text_margin_spin.setValue(self.settings_model.get_setting('text_margin', 2))
        text_margin_layout.addWidget(text_margin_label)
        text_margin_layout.addWidget(self.text_margin_spin)
        layout.addLayout(text_margin_layout)
        
        # 窗口位置设置
        position_layout = QHBoxLayout()
        self.always_on_top = QCheckBox("窗口置顶")
        self.always_on_bottom = QCheckBox("窗口置底")
        self.always_on_top.setChecked(self.settings_model.get_setting('always_on_top', True))
        self.always_on_bottom.setChecked(self.settings_model.get_setting('always_on_bottom', False))
        
        # 连接信号
        self.always_on_top.stateChanged.connect(lambda state: self.on_position_changed('top', state))
        self.always_on_bottom.stateChanged.connect(lambda state: self.on_position_changed('bottom', state))
        
        position_layout.addWidget(self.always_on_top)
        position_layout.addWidget(self.always_on_bottom)
        layout.addLayout(position_layout)
        
        # 添加快捷键设置
        shortcut_layout = QHBoxLayout()
        shortcut_label = QLabel("切换窗口位置快捷键:")
        self.shortcut_edit = QKeySequenceEdit()
        # 从设置中获取快捷键，默认为 Ctrl+Alt
        default_shortcut = self.settings_model.get_setting('position_shortcut', 'Ctrl+Alt')
        self.shortcut_edit.setKeySequence(QKeySequence(default_shortcut))
        shortcut_layout.addWidget(shortcut_label)
        shortcut_layout.addWidget(self.shortcut_edit)
        layout.addLayout(shortcut_layout)
        
        # 添加查看历史记录按钮
        history_button = QPushButton("查看已完成待办事项")
        history_button.clicked.connect(self.show_history)
        layout.addWidget(history_button)
        
        # 添加退出按钮
        quit_button = QPushButton("退出程序")
        quit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        quit_button.clicked.connect(self.confirm_quit)
        layout.addWidget(quit_button)
        
        # 添加确定和取消按钮
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        cancel_button = QPushButton("取消")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)

    def get_settings(self):
        """获取当前设置值"""
        return {
            'window_width': self.width_spin.value(),
            'window_height': self.height_spin.value(),
            'opacity': self.opacity_slider.value(),
            'always_on_top': self.always_on_top.isChecked(),
            'always_on_bottom': self.always_on_bottom.isChecked(),
            'todo_font_size': self.font_size_spin.value(),
            'todo_item_height': self.item_height_spin.value(),
            'text_margin': self.text_margin_spin.value(),
            'position_shortcut': self.shortcut_edit.keySequence().toString()
        }

    def show_history(self):
        """显示历史记录对话框"""
        dialog = HistoryDialog(self.history_model, self)
        dialog.exec_()

    def confirm_quit(self):
        """确认是否退出程序"""
        reply = QMessageBox.question(
            self,
            '确认退出',
            '确定要退出程序吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 获取主窗口实例并调用退出方法
            main_window = self.parent()
            if main_window:
                main_window.close_application()

    def on_position_changed(self, position, state):
        """处理窗口位置选项变化"""
        if state == Qt.Checked:
            # 取消另一个选项
            if position == 'top':
                self.always_on_bottom.setChecked(False)
            elif position == 'bottom':
                self.always_on_top.setChecked(False)

class MainWindow(QMainWindow):
    """
    主窗口类，继承自QMainWindow
    用于创建和管理待办事项应用程序的主界面
    """
    # 定义信号，用于与控制器通信
    add_todo_signal = pyqtSignal(str)      # 添加待办事项信号
    delete_todo_signal = pyqtSignal(int)   # 删除待办事项信号
    toggle_todo_signal = pyqtSignal(int)   # 切换待办事项状态信号
    move_todo_signal = pyqtSignal(int, int)  # 移动待办事项信号

    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.settings_model = SettingsModel()
        self.history_model = HistoryModel()
        self.todo_model = TodoModel()  # 初始化todo_model
        
        # 设置窗口标志，移除任务栏显示和窗口控制按钮
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # 初始化UI
        self.init_ui()
        
        # 应用保存的设置
        self.apply_settings()
        
        # 初始化系统托盘
        self.init_tray_icon()
        
        # 检查是否需要清理旧的历史记录
        self.check_and_clear_history()
        
        # 设置快捷键
        self.setup_shortcut()

    def check_and_clear_history(self):
        """检查并清理旧的历史记录"""
        # 获取今天的日期，用于过滤显示
        today = self.history_model.clear_old_completed_todos()
        # 过滤掉今天之前完成的待办事项
        self.todo_model.todos = [todo for todo in self.todo_model.todos 
                               if not todo['completed'] or 
                               (todo['completed'] and 'completed_time' in todo and 
                                datetime.strptime(todo['completed_time'], '%Y-%m-%d %H:%M:%S').date() == today)]
        self.todo_model.save_todos()

    def on_todo_completed(self, index, todo):
        """处理待办事项完成事件"""
        # 将完成的待办事项添加到历史记录
        created_time = datetime.strptime(todo['created_time'], '%Y-%m-%d %H:%M:%S')
        self.history_model.add_completed_todo(todo['text'], created_time)
        
        # 更新待办事项的完成时间
        todo['completed_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 从当前待办事项列表中移除
        self.todo_model.remove_todo(index)
        # 更新显示
        self.update_todo_list(self.todo_model.todos)

    def apply_settings(self):
        """应用保存的设置"""
        # 设置窗口大小
        width = self.settings_model.get_setting('window_width', 400)
        height = self.settings_model.get_setting('window_height', 600)
        self.setFixedSize(width, height)
        
        # 设置透明度
        opacity = self.settings_model.get_setting('opacity', 100) / 100.0
        self.setWindowOpacity(opacity)
        
        # 设置窗口位置
        flags = Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        
        # 根据设置添加窗口标志
        if self.settings_model.get_setting('always_on_bottom', False):
            flags |= Qt.WindowStaysOnBottomHint
            flags &= ~Qt.WindowStaysOnTopHint
        
        self.setWindowFlags(flags)
        
        # 更新所有待办事项的显示
        if hasattr(self, 'todo_layout'):
            self.update_todo_list(self.todo_model.todos)
            
        # 重新显示窗口以应用新的窗口标志
        self.show()

    def init_tray_icon(self):
        """初始化系统托盘图标"""
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(self.style().SP_ComputerIcon))
        
        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = tray_menu.addAction("显示")
        show_action.triggered.connect(self.show)
        quit_action = tray_menu.addAction("退出")
        quit_action.triggered.connect(self.close_application)
        
        # 设置托盘菜单
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def closeEvent(self, event):
        """
        重写关闭事件
        点击关闭按钮时最小化到系统托盘而不是退出程序
        """
        event.ignore()  # 忽略关闭事件
        self.hide()     # 隐藏窗口

    def close_application(self):
        """完全退出应用程序"""
        self.tray_icon.hide()
        QApplication.quit()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('桌面待办事项')

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)

        # 创建标题栏
        title_bar = QHBoxLayout()
        title_label = QLabel("Moonlight-Bath To Do")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        
        # 创建设置按钮
        settings_button = QPushButton()
        # 使用自定义图标
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons', 'settings.ico')
        settings_button.setIcon(QIcon(icon_path))
        settings_button.setFixedSize(24, 24)
        settings_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                background: #e0e0e0;
                border-radius: 12px;
            }
        """)
        settings_button.clicked.connect(self.show_settings)
        
        title_bar.addWidget(title_label)
        title_bar.addStretch()
        title_bar.addWidget(settings_button)
        layout.addLayout(title_bar)

        # 创建输入区域
        input_layout = QHBoxLayout()
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText('输入待办事项...')
        self.todo_input.returnPressed.connect(self.on_add_clicked)
        
        add_button = QPushButton('添加')
        add_button.clicked.connect(self.on_add_clicked)
        
        input_layout.addWidget(self.todo_input)
        input_layout.addWidget(add_button)
        layout.addLayout(input_layout)

        # 创建待办事项容器
        self.todo_container = QWidget()
        self.todo_layout = QVBoxLayout(self.todo_container)
        self.todo_layout.setSpacing(5)
        self.todo_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.todo_container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        layout.addWidget(self.scroll_area)

        # 设置样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QPushButton {
                padding: 5px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # 获取新的设置值
            new_settings = dialog.get_settings()
            
            # 保存设置
            for key, value in new_settings.items():
                self.settings_model.update_setting(key, value)
            
            # 应用新设置
            self.apply_settings()
            
            # 更新快捷键
            self.setup_shortcut()
            
            self.show()  # 重新显示窗口以应用新的窗口标志

    def mousePressEvent(self, event):
        """处理鼠标按下事件，用于实现窗口拖动"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件，实现窗口拖动"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def on_add_clicked(self):
        """处理添加待办事项的点击事件"""
        text = self.todo_input.text().strip()
        if text:
            self.add_todo_signal.emit(text)  # 发送添加信号
            self.todo_input.clear()  # 清空输入框
        else:
            QMessageBox.warning(self, '警告', '请输入待办事项内容！')

    def on_delete_clicked(self):
        """处理删除待办事项的点击事件"""
        current_row = self.todo_list.currentRow()
        if current_row >= 0:
            self.delete_todo_signal.emit(current_row)  # 发送删除信号
        else:
            QMessageBox.warning(self, '警告', '请先选择要删除的待办事项！')

    def on_item_double_clicked(self, item):
        """处理待办事项的双击事件（用于切换完成状态）"""
        row = self.todo_list.row(item)
        self.toggle_todo_signal.emit(row)  # 发送切换状态信号

    def update_todo_list(self, todos):
        """更新待办事项列表显示"""
        # 清除现有的待办事项
        while self.todo_layout.count():
            item = self.todo_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 设置每个待办事项的固定高度
        todo_height = self.settings_model.get_setting('todo_item_height', 60)
        
        # 添加所有待办事项
        for i, todo in enumerate(todos):
            item = TodoItemWidget(i, todo['text'], todo['completed'], self.settings_model)
            item.setFixedHeight(todo_height)
            
            # 连接信号
            item.move_up_signal.connect(lambda idx: self.move_todo_signal.emit(idx, -1))
            item.move_down_signal.connect(lambda idx: self.move_todo_signal.emit(idx, 1))
            item.move_to_top_signal.connect(lambda idx: self.move_todo_signal.emit(idx, -idx))
            item.delete_signal.connect(self.delete_todo_signal.emit)
            item.complete_signal.connect(self.toggle_todo_signal.emit)
            
            self.todo_layout.addWidget(item)

        # 调整窗口高度
        if len(todos) < 3:
            # 当待办事项少于3个时，窗口高度自适应
            content_height = len(todos) * (todo_height + 5) + 100  # 内容高度（包含边距）
            self.setFixedHeight(content_height)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏滚动条
        else:
            # 当待办事项大于等于3个时，使用固定高度
            fixed_height = 3 * (todo_height + 5) + 100  # 3个待办事项的高度加上边距
            self.setFixedHeight(fixed_height)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 显示滚动条 

    def setup_shortcut(self):
        """设置快捷键"""
        # 获取保存的快捷键
        shortcut = self.settings_model.get_setting('position_shortcut', 'Ctrl+Alt')
        # 创建快捷键动作
        self.toggle_position_action = QAction(self)
        self.toggle_position_action.setShortcut(QKeySequence(shortcut))
        self.toggle_position_action.triggered.connect(self.toggle_window_position)
        self.addAction(self.toggle_position_action)

    def toggle_window_position(self):
        """切换窗口位置"""
        # 获取当前设置
        is_top = self.settings_model.get_setting('always_on_top', True)
        is_bottom = self.settings_model.get_setting('always_on_bottom', False)
        
        # 切换位置
        if is_top:
            self.settings_model.update_setting('always_on_top', False)
            self.settings_model.update_setting('always_on_bottom', True)
        else:
            self.settings_model.update_setting('always_on_top', True)
            self.settings_model.update_setting('always_on_bottom', False)
        
        # 应用新设置
        self.apply_settings() 