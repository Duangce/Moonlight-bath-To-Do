import os
import sys
import shutil
import subprocess

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    if os.path.exists('todo_app.spec'):
        os.remove('todo_app.spec')

def build_exe():
    """构建可执行文件"""
    # 确保在正确的目录中
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 清理旧的构建文件
    clean_build_dirs()
    
    # PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--name=todo_app',
        '--windowed',  # 不显示控制台窗口
        '--onefile',   # 打包成单个文件
        '--clean',     # 清理临时文件
        '--add-data=src;src',  # 添加源代码目录
        '--icon=resources/icon.ico' if os.path.exists('resources/icon.ico') else '',  # 如果有图标就添加
        'src/main.py'  # 主程序入口
    ]
    
    # 移除空字符串
    cmd = [x for x in cmd if x]
    
    # 执行打包命令
    try:
        subprocess.run(cmd, check=True)
        print("\n打包完成！")
        print("可执行文件位置: dist/todo_app.exe")
    except subprocess.CalledProcessError as e:
        print(f"\n打包失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    build_exe() 