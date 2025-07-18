#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python++ Code to Python Converter
将 .code 文件转换为可执行的 .py 文件
"""

import os
import sys
import re
import argparse
from pathlib import Path

class CodeToPythonConverter:
    def __init__(self):
        self.indent_level = 0
        self.in_function = False
        self.function_name = ""
        self.function_params = []
        
    def convert_code_to_python(self, code_content):
        """将 .code 内容转换为 Python 代码"""
        lines = code_content.split('\n')
        python_lines = []
        
        # 添加必要的导入
        python_lines.extend([
            "#!/usr/bin/env python3",
            "# -*- coding: utf-8 -*-",
            "",
            "import tkinter as tk",
            "from tkinter import ttk, messagebox, filedialog, simpledialog",
            "import threading",
            "import time",
            "",
            "# GUI 控制管理器",
            "class GUIControlManager:",
            "    def __init__(self):",
            "        self.controls = {}",
            "        self.windows = {}",
            "        self.root = None",
            "",
            "    def create_window(self, name, title, width=800, height=600):",
            "        if name not in self.windows:",
            "            window = tk.Tk() if self.root is None else tk.Toplevel(self.root)",
            "            if self.root is None:",
            "                self.root = window",
            "            window.title(title)",
            "            window.geometry(f'{width}x{height}')",
            "            self.windows[name] = window",
            "        return self.windows[name]",
            "",
            "    def create_control(self, control_type, name, parent='main', **kwargs):",
            "        if parent not in self.windows:",
            "            parent = 'main'",
            "        parent_window = self.windows[parent]",
            "        ",
            "        if control_type == 'button':",
            "            control = tk.Button(parent_window, **kwargs)",
            "        elif control_type == 'label':",
            "            control = tk.Label(parent_window, **kwargs)",
            "        elif control_type == 'entry':",
            "            control = tk.Entry(parent_window, **kwargs)",
            "        elif control_type == 'text':",
            "            control = tk.Text(parent_window, **kwargs)",
            "        elif control_type == 'listbox':",
            "            control = tk.Listbox(parent_window, **kwargs)",
            "        elif control_type == 'combobox':",
            "            control = ttk.Combobox(parent_window, **kwargs)",
            "        elif control_type == 'checkbox':",
            "            control = tk.Checkbutton(parent_window, **kwargs)",
            "        elif control_type == 'radiobutton':",
            "            control = tk.Radiobutton(parent_window, **kwargs)",
            "        elif control_type == 'image':",
            "            control = tk.Label(parent_window, **kwargs)",
            "        else:",
            "            control = tk.Label(parent_window, text=f'Unknown control: {control_type}')",
            "        ",
            "        self.controls[name] = control",
            "        return control",
            "",
            "    def set_property(self, control_name, property_name, value):",
            "        if control_name in self.controls:",
            "            control = self.controls[control_name]",
            "            if hasattr(control, property_name):",
            "                setattr(control, property_name, value)",
            "",
            "    def get_property(self, control_name, property_name):",
            "        if control_name in self.controls:",
            "            control = self.controls[control_name]",
            "            if hasattr(control, property_name):",
            "                return getattr(control, property_name)",
            "        return None",
            "",
            "    def bind_event(self, control_name, event, handler):",
            "        if control_name in self.controls:",
            "            control = self.controls[control_name]",
            "            control.bind(event, handler)",
            "",
            "    def layout(self, control_name, method='pack', **kwargs):",
            "        if control_name in self.controls:",
            "            control = self.controls[control_name]",
            "            if method == 'pack':",
            "                control.pack(**kwargs)",
            "            elif method == 'grid':",
            "                control.grid(**kwargs)",
            "            elif method == 'place':",
            "                control.place(**kwargs)",
            "",
            "    def remove_control(self, control_name):",
            "        if control_name in self.controls:",
            "            control = self.controls[control_name]",
            "            control.destroy()",
            "            del self.controls[control_name]",
            "",
            "    def show_message(self, title, message, message_type='info'):",
            "        if message_type == 'info':",
            "            messagebox.showinfo(title, message)",
            "        elif message_type == 'warning':",
            "            messagebox.showwarning(title, message)",
            "        elif message_type == 'error':",
            "            messagebox.showerror(title, message)",
            "        elif message_type == 'question':",
            "            return messagebox.askyesno(title, message)",
            "",
            "    def show_input_dialog(self, title, prompt):",
            "        return simpledialog.askstring(title, prompt)",
            "",
            "    def show_file_dialog(self, title, file_types):",
            "        return filedialog.askopenfilename(title=title, filetypes=file_types)",
            "",
            "    def run(self):",
            "        if self.root:",
            "            self.root.mainloop()",
            "",
            "# 全局 GUI 管理器",
            "gui = GUIControlManager()",
            "",
            "# 主程序开始",
            "def main():",
        ])
        
        self.indent_level = 1
        in_function = False
        function_name = ""
        function_body = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # 处理函数定义
            if line.startswith('function '):
                if in_function:
                    # 结束前一个函数
                    python_lines.append('    ' * self.indent_level + f"def {function_name}():")
                    for body_line in function_body:
                        python_lines.append('    ' * (self.indent_level + 1) + body_line)
                    python_lines.append('')
                
                # 开始新函数
                parts = line.split()
                function_name = parts[1]
                in_function = True
                function_body = []
                continue
            
            # 如果在函数内部
            if in_function:
                # 检查是否是函数结束（空行或新的函数定义）
                if not line or line.startswith('function '):
                    # 结束当前函数
                    python_lines.append('    ' * self.indent_level + f"def {function_name}():")
                    for body_line in function_body:
                        python_lines.append('    ' * (self.indent_level + 1) + body_line)
                    python_lines.append('')
                    
                    if line.startswith('function '):
                        # 开始新函数
                        parts = line.split()
                        function_name = parts[1]
                        function_body = []
                    else:
                        in_function = False
                        function_name = ""
                        function_body = []
                else:
                    python_line = self.convert_line(line)
                    if python_line:
                        function_body.append(python_line)
                continue
            
            # 普通代码行
            python_line = self.convert_line(line)
            if python_line:
                python_lines.append('    ' * self.indent_level + python_line)
        
        # 处理最后一个函数
        if in_function and function_body:
            python_lines.append('    ' * self.indent_level + f"def {function_name}():")
            for body_line in function_body:
                python_lines.append('    ' * (self.indent_level + 1) + body_line)
            python_lines.append('')
        
        # 添加主程序调用
        python_lines.extend([
            "",
            "if __name__ == '__main__':",
            "    main()",
            "    gui.run()",
        ])
        
        return '\n'.join(python_lines)
    
    def convert_line(self, line):
        """转换单行代码"""
        # 窗口创建
        if line.startswith('window '):
            return self.convert_window_creation(line)
        
        # 控件创建
        elif line.startswith(('button ', 'label ', 'entry ', 'text ', 'listbox ', 
                             'combobox ', 'checkbox ', 'radiobutton ', 'image ')):
            return self.convert_control_creation(line)
        
        # 属性设置
        elif '=' in line and '.' in line:
            return self.convert_property_setting(line)
        
        # 事件绑定
        elif line.startswith('bind '):
            return self.convert_event_binding(line)
        
        # 布局
        elif line.startswith(('pack ', 'grid ', 'place ')):
            return self.convert_layout(line)
        
        # 函数定义
        elif line.startswith('function '):
            return self.convert_function_definition(line)
        
        # 函数调用
        elif '(' in line and line.endswith(')'):
            return self.convert_function_call(line)
        
        # 变量赋值
        elif '=' in line and not line.startswith(('if ', 'for ', 'while ')):
            return self.convert_assignment(line)
        
        # 条件语句
        elif line.startswith('if '):
            return self.convert_if_statement(line)
        
        # 循环语句
        elif line.startswith(('for ', 'while ')):
            return self.convert_loop_statement(line)
        
        # 其他语句
        else:
            return line
    
    def convert_window_creation(self, line):
        """转换窗口创建"""
        # window main "My App" 800 600
        parts = line.split()
        if len(parts) >= 3:
            name = parts[1]
            title = parts[2].strip('"')
            width = parts[3] if len(parts) > 3 else '800'
            height = parts[4] if len(parts) > 4 else '600'
            return f"gui.create_window('{name}', '{title}', {width}, {height})"
        return None
    
    def convert_control_creation(self, line):
        """转换控件创建"""
        # button btn1 "Click Me" text="Hello" command=onclick
        parts = line.split()
        control_type = parts[0]
        name = parts[1]
        
        # 提取参数
        params = {}
        text_param = None
        
        for part in parts[2:]:
            if '=' in part:
                key, value = part.split('=', 1)
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                params[key] = value
            else:
                # 第一个非名称参数通常是文本
                if text_param is None:
                    text_param = part.strip('"')
        
        # 设置文本参数
        if text_param:
            params['text'] = text_param
        
        # 构建参数字符串
        if params:
            param_str = ", ".join([f"{k}='{v}'" for k, v in params.items()])
            return f"gui.create_control('{control_type}', '{name}', {param_str})"
        else:
            return f"gui.create_control('{control_type}', '{name}')"
    
    def convert_property_setting(self, line):
        """转换属性设置"""
        # btn1.text = "New Text"
        parts = line.split('=')
        if len(parts) == 2:
            control_prop = parts[0].strip()
            value = parts[1].strip()
            
            if '.' in control_prop:
                control_name, prop_name = control_prop.split('.', 1)
                if value.startswith('"') and value.endswith('"'):
                    value = f"'{value[1:-1]}'"
                return f"gui.set_property('{control_name}', '{prop_name}', {value})"
        return None
    
    def convert_event_binding(self, line):
        """转换事件绑定"""
        # bind btn1 click onclick
        parts = line.split()
        if len(parts) >= 4:
            control_name = parts[1]
            event = parts[2]
            handler = parts[3]
            
            # 事件名称映射
            event_map = {
                'click': 'Button-1',
                'double': 'Double-Button-1',
                'right': 'Button-3',
                'key': 'Key',
                'enter': 'Return',
                'focus': 'FocusIn',
                'blur': 'FocusOut'
            }
            
            tk_event = event_map.get(event, f'<{event}>')
            return f"gui.bind_event('{control_name}', '{tk_event}', {handler})"
        return None
    
    def convert_layout(self, line):
        """转换布局"""
        # pack btn1 side=left fill=x
        parts = line.split()
        method = parts[0]
        control_name = parts[1]
        
        params = {}
        for part in parts[2:]:
            if '=' in part:
                key, value = part.split('=', 1)
                params[key] = value
        
        param_str = ", ".join([f"{k}='{v}'" for k, v in params.items()])
        return f"gui.layout('{control_name}', '{method}', {param_str})"
    
    def convert_function_definition(self, line):
        """转换函数定义"""
        # function onclick
        parts = line.split()
        if len(parts) >= 2:
            func_name = parts[1]
            self.in_function = True
            self.function_name = func_name
            self.function_params = []
            return f"def {func_name}():"
        return None
    
    def convert_function_call(self, line):
        """转换函数调用"""
        # onclick()
        if line.endswith('()'):
            func_name = line[:-2]
            return f"{func_name}()"
        return line
    
    def convert_assignment(self, line):
        """转换变量赋值"""
        # x = 10
        return line
    
    def convert_if_statement(self, line):
        """转换条件语句"""
        # if x > 10
        return line + ':'
    
    def convert_loop_statement(self, line):
        """转换循环语句"""
        # for i in range(10)
        return line + ':'

def convert_file(input_file, output_file=None):
    """转换单个文件"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code_content = f.read()
        
        converter = CodeToPythonConverter()
        python_content = converter.convert_code_to_python(code_content)
        
        if output_file is None:
            output_file = input_file.replace('.code', '.py')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(python_content)
        
        print(f"[SUCCESS] 转换成功: {input_file} -> {output_file}")
        return True
        
    except Exception as e:
        print(f"[ERROR] 转换失败: {input_file} - {str(e)}")
        return False

def convert_directory(input_dir, output_dir=None):
    """转换目录中的所有 .code 文件"""
    input_path = Path(input_dir)
    
    if output_dir is None:
        output_dir = input_dir
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    success_count = 0
    total_count = 0
    
    for code_file in input_path.glob('*.code'):
        total_count += 1
        output_file = output_path / f"{code_file.stem}.py"
        
        if convert_file(str(code_file), str(output_file)):
            success_count += 1
    
    print(f"\n转换完成: {success_count}/{total_count} 个文件成功转换")
    return success_count, total_count

def main():
    parser = argparse.ArgumentParser(description='将 .code 文件转换为 .py 文件')
    parser.add_argument('input', help='输入文件或目录')
    parser.add_argument('-o', '--output', help='输出文件或目录')
    parser.add_argument('-r', '--recursive', action='store_true', help='递归处理子目录')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"错误: 输入路径不存在: {args.input}")
        return 1
    
    if input_path.is_file():
        if input_path.suffix != '.code':
            print(f"错误: 输入文件必须是 .code 文件: {args.input}")
            return 1
        
        success = convert_file(str(input_path), args.output)
        return 0 if success else 1
    
    elif input_path.is_dir():
        success_count, total_count = convert_directory(str(input_path), args.output)
        return 0 if success_count == total_count else 1
    
    return 1

if __name__ == '__main__':
    sys.exit(main()) 