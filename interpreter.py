import sys
import re
import os
import threading
import pygame
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init()
    COLOR_ERR = Fore.RED + Style.BRIGHT
    COLOR_OK = Fore.GREEN + Style.BRIGHT
    COLOR_RESET = Style.RESET_ALL
except ImportError:
    COLOR_ERR = COLOR_OK = COLOR_RESET = ''

# Tkinter极简弹窗支持
try:
    import tkinter as tk
    from tkinter import messagebox, simpledialog, filedialog, colorchooser, ttk
    from tkinter import Button, Label, Entry, Text, Frame, Menu
    from tkinter.ttk import Combobox, Checkbutton, Radiobutton
except ImportError:
    tk = messagebox = simpledialog = filedialog = colorchooser = ttk = None

PYPP_KEYWORDS = set([
    'let','print','if','for','when','while','do','run','open','input','swap','repeat','use',
    'window','fill','rect','circle','text','flip','update','wait','def','fn',
    'warning','info','error','askyesno','inputbox',
    'gui','button','label','entry','textbox','menu','filedialog','colorchooser','progress',
    'combobox','checkbox','radiobutton','image','pack','grid','place','add','remove'
])

# 全局GUI窗口管理
gui_windows = {}
current_gui_window = None

# 全局GUI控件管理 - 极简语法支持
gui_widgets = {}  # 存储所有控件 {widget_name: widget_object}
widget_counter = {}  # 控件计数器 {widget_type: count}

def create_gui_window(title="Python++ GUI", width=400, height=300):
    global current_gui_window
    if tk is None:
        print(f"{COLOR_ERR}[Error] tkinter不可用{COLOR_RESET}")
        return None
    root = tk.Tk()
    root.title(title)
    root.geometry(f"{width}x{height}")
    current_gui_window = root
    gui_windows[title] = root
    return root

def add_button(text, command, x=10, y=10):
    if current_gui_window and tk is not None:
        btn = Button(current_gui_window, text=text, command=command)
        btn.place(x=x, y=y)
        return btn
    return None

def add_label(text, x=10, y=10):
    if current_gui_window and tk is not None:
        lbl = Label(current_gui_window, text=text)
        lbl.place(x=x, y=y)
        return lbl
    return None

def add_entry(x=10, y=10, width=20):
    if current_gui_window and tk is not None:
        ent = Entry(current_gui_window, width=width)
        ent.place(x=x, y=y)
        return ent
    return None

def add_textbox(x=10, y=10, width=30, height=10):
    if current_gui_window and tk is not None:
        txt = Text(current_gui_window, width=width, height=height)
        txt.place(x=x, y=y)
        return txt
    return None

def add_progressbar(x=10, y=10, width=200):
    if current_gui_window and ttk is not None:
        progress = ttk.Progressbar(current_gui_window, length=width)
        progress.place(x=x, y=y)
        return progress
    return None

def show_file_dialog(title="选择文件", filetypes=None):
    if filedialog is None:
        print(f"{COLOR_ERR}[Error] tkinter不可用{COLOR_RESET}")
        return None
    if filetypes is None:
        filetypes = [("所有文件", "*.*")]
    return filedialog.askopenfilename(title=title, filetypes=filetypes)

def show_save_dialog(title="保存文件", filetypes=None):
    if filedialog is None:
        print(f"{COLOR_ERR}[Error] tkinter不可用{COLOR_RESET}")
        return None
    if filetypes is None:
        filetypes = [("所有文件", "*.*")]
    return filedialog.asksaveasfilename(title=title, filetypes=filetypes)

def show_color_dialog(title="选择颜色"):
    if colorchooser is None:
        print(f"{COLOR_ERR}[Error] tkinter不可用{COLOR_RESET}")
        return None
    return colorchooser.askcolor(title=title)

def show_warning(msg):
    if tk is None or messagebox is None:
        print(f"{COLOR_ERR}[Error] tkinter不可用{COLOR_RESET}")
        return
    if current_gui_window:
        # 如果GUI窗口存在，在主线程中显示
        messagebox.showwarning('警告', msg)
    else:
        # 否则在新线程中显示
        def _():
            root = tk.Tk(); root.withdraw(); messagebox.showwarning('警告', msg); root.destroy()
        threading.Thread(target=_).start()

def show_info(msg):
    if tk is None or messagebox is None:
        print(f"{COLOR_ERR}[Error] tkinter不可用{COLOR_RESET}")
        return
    if current_gui_window:
        # 如果GUI窗口存在，在主线程中显示
        messagebox.showinfo('提示', msg)
    else:
        # 否则在新线程中显示
        def _():
            root = tk.Tk(); root.withdraw(); messagebox.showinfo('提示', msg); root.destroy()
        threading.Thread(target=_).start()

def show_error(msg):
    if tk is None or messagebox is None:
        print(f"{COLOR_ERR}[Error] tkinter不可用{COLOR_RESET}")
        return
    if current_gui_window:
        # 如果GUI窗口存在，在主线程中显示
        messagebox.showerror('错误', msg)
    else:
        # 否则在新线程中显示
        def _():
            root = tk.Tk(); root.withdraw(); messagebox.showerror('错误', msg); root.destroy()
        threading.Thread(target=_).start()

def ask_yesno(msg):
    if tk is None or messagebox is None:
        print(f"{COLOR_ERR}[Error] tkinter不可用{COLOR_RESET}")
        return None
    result = {'val': None}
    def _():
        root = tk.Tk(); root.withdraw(); result['val'] = messagebox.askyesno('确认', msg); root.destroy()
    t = threading.Thread(target=_); t.start(); t.join()
    return result['val']

def input_box(msg):
    if tk is None or simpledialog is None:
        print(f"{COLOR_ERR}[Error] tkinter不可用{COLOR_RESET}")
        return None
    result = {'val': None}
    def _():
        root = tk.Tk(); root.withdraw(); result['val'] = simpledialog.askstring('输入', msg); root.destroy()
    t = threading.Thread(target=_); t.start(); t.join()
    return result['val']

# 极简GUI语法辅助函数
def get_next_widget_name(widget_type):
    """获取下一个控件名称，如 Label1, Button2 等"""
    global widget_counter
    if widget_type not in widget_counter:
        widget_counter[widget_type] = 0
    widget_counter[widget_type] += 1
    return f"{widget_type}{widget_counter[widget_type]}"

def create_widget(widget_type, **kwargs):
    """创建控件并自动命名"""
    global gui_widgets, current_gui_window
    if not current_gui_window:
        print(f"{COLOR_ERR}[Error] 请先创建窗口{COLOR_RESET}")
        return None
    
    widget_name = get_next_widget_name(widget_type)
    
    if widget_type == 'Label':
        widget = Label(current_gui_window, **kwargs)
    elif widget_type == 'Entry':
        widget = Entry(current_gui_window, **kwargs)
    elif widget_type == 'Button':
        widget = Button(current_gui_window, **kwargs)
    elif widget_type == 'Text':
        widget = Text(current_gui_window, **kwargs)
    elif widget_type == 'Combobox':
        widget = Combobox(current_gui_window, **kwargs)
    elif widget_type == 'Checkbutton':
        widget = Checkbutton(current_gui_window, **kwargs)
    elif widget_type == 'Radiobutton':
        widget = Radiobutton(current_gui_window, **kwargs)
    else:
        print(f"{COLOR_ERR}[Error] 不支持的控件类型: {widget_type}{COLOR_RESET}")
        return None
    
    gui_widgets[widget_name] = widget
    return widget_name, widget

def get_widget(widget_name):
    """获取控件对象"""
    global gui_widgets
    return gui_widgets.get(widget_name)

def set_widget_property(widget_name, property_name, value):
    """设置控件属性"""
    widget = get_widget(widget_name)
    if not widget:
        print(f"{COLOR_ERR}[Error] 控件不存在: {widget_name}{COLOR_RESET}")
        return False
    
    try:
        if property_name == 'text':
            widget.delete(0, tk.END) if hasattr(widget, 'delete') else None
            widget.insert(0, value) if hasattr(widget, 'insert') else setattr(widget, 'text', value)
        elif property_name == 'color':
            widget.configure(fg=value)
        elif property_name == 'font':
            widget.configure(font=value)
        elif property_name == 'size':
            widget.configure(font=(None, value))
        else:
            setattr(widget, property_name, value)
        return True
    except Exception as e:
        print(f"{COLOR_ERR}[Error] 设置属性失败: {e}{COLOR_RESET}")
        return False

def get_widget_property(widget_name, property_name):
    """获取控件属性"""
    widget = get_widget(widget_name)
    if not widget:
        print(f"{COLOR_ERR}[Error] 控件不存在: {widget_name}{COLOR_RESET}")
        return None
    
    try:
        if property_name == 'text':
            return widget.get() if hasattr(widget, 'get') else getattr(widget, 'text', '')
        else:
            return getattr(widget, property_name, None)
    except Exception as e:
        print(f"{COLOR_ERR}[Error] 获取属性失败: {e}{COLOR_RESET}")
        return None

def layout_widget(widget_name, layout_type, **kwargs):
    """布局控件"""
    widget = get_widget(widget_name)
    if not widget:
        print(f"{COLOR_ERR}[Error] 控件不存在: {widget_name}{COLOR_RESET}")
        return False
    
    try:
        if layout_type == 'pack':
            widget.pack(**kwargs)
        elif layout_type == 'grid':
            widget.grid(**kwargs)
        elif layout_type == 'place':
            widget.place(**kwargs)
        else:
            print(f"{COLOR_ERR}[Error] 不支持的布局类型: {layout_type}{COLOR_RESET}")
            return False
        return True
    except Exception as e:
        print(f"{COLOR_ERR}[Error] 布局失败: {e}{COLOR_RESET}")
        return False

class PythonPPInterpreter:
    def __init__(self):
        self.variables = {}
        self.exec_env = {}
        self.in_run_block = False
        self.run_block_lines = []
        self.in_multiline_comment = False
        self.in_open_block = False
        self.open_filename = None
        self.open_block_lines = []
        self.pygame_inited = False
        self.screen = None
        self.open_file_obj = None
        self.in_function_block = False # 新增：用于多行函数定义
        self.function_name = None # 新增：用于多行函数定义
        self.function_args = None # 新增：用于多行函数定义
        self.function_lines = [] # 新增：用于多行函数定义

    def ensure_pygame(self):
        if not self.pygame_inited:
            import importlib
            pygame = importlib.import_module('pygame')
            pygame.init()
            self.exec_env['pygame'] = pygame
            self.pygame_inited = True

    def parse_color(self, colorstr):
        colors = {
            'red': (255,0,0), 'green': (0,255,0), 'blue': (0,0,255),
            'black': (0,0,0), 'white': (255,255,255), 'yellow': (255,255,0),
            'gray': (128,128,128), 'grey': (128,128,128),
        }
        colorstr = colorstr.strip()
        if colorstr in colors:
            return colors[colorstr]
        if colorstr.startswith('(') and colorstr.endswith(')'):
            try:
                return tuple(map(int, colorstr[1:-1].split(',')))
            except:
                pass
        return (255,255,255)

    def eval_expr(self, expr):
        expr = re.sub(r'(\d+)\.\.(\d+)', lambda m: f'range({m.group(1)}, {int(m.group(2))+1})', expr)
        for var in self.variables:
            expr = re.sub(rf'\b{var}\b', str(self.variables[var]), expr)
        try:
            return eval(expr, self.exec_env)
        except Exception as e:
            print(f"{COLOR_ERR}[Error] 表达式求值失败: {expr} - {e}{COLOR_RESET}")
            return None

    def call_user_function(self, func_name):
        """调用用户定义的函数"""
        if func_name in self.variables and callable(self.variables[func_name]):
            try:
                self.variables[func_name]()
            except Exception as e:
                print(f"{COLOR_ERR}[Error] 函数调用失败: {func_name} - {e}{COLOR_RESET}")
        else:
            print(f"{COLOR_ERR}[Error] 函数未定义: {func_name}{COLOR_RESET}")

    def run_line(self, line):
        try:
            line = line.rstrip('\n')
            if self.in_multiline_comment:
                if '*/' in line:
                    self.in_multiline_comment = False
                return
            if '/*' in line:
                self.in_multiline_comment = True
                return
            if not line.strip() or line.strip().startswith('#'):
                return
            # run/open 块优先
            if self.in_run_block:
                if line.startswith('    ') or line.startswith('\t'):
                    self.run_block_lines.append(line[4:] if line.startswith('    ') else line[1:])
                    return
                else:
                    self.exec_run_block()
                    self.in_run_block = False
            if self.in_open_block:
                if line.startswith('    ') or line.startswith('\t'):
                    self.open_block_lines.append(line[4:] if line.startswith('    ') else line[1:])
                    return
                else:
                    self.exec_open_block()
                    self.in_open_block = False
            # 函数块处理
            if self.in_function_block:
                if line.startswith('    ') or line.startswith('\t'):
                    self.function_lines.append(line[4:] if line.startswith('    ') else line[1:])
                    return
                else:
                    self.exec_function_block()
                    self.in_function_block = False
            # Tkinter极简语法优先
            if tk and messagebox and line.strip().startswith('warning '):
                msg = line.strip()[8:].strip().strip('"').strip("'")
                show_warning(msg)
                return
            if tk and messagebox and line.strip().startswith('info '):
                msg = line.strip()[5:].strip().strip('"').strip("'")
                show_info(msg)
                return
            if tk and messagebox and line.strip().startswith('error '):
                msg = line.strip()[6:].strip().strip('"').strip("'")
                show_error(msg)
                return
            if tk and messagebox and line.strip().startswith('askyesno '):
                msg = line.strip()[9:].strip().strip('"').strip("'")
                ans = ask_yesno(msg)
                print(f"{COLOR_OK}{ans}{COLOR_RESET}")
                return
            if tk and simpledialog and line.strip().startswith('inputbox '):
                msg = line.strip()[9:].strip().strip('"').strip("'")
                val = input_box(msg)
                print(f"{COLOR_OK}{val}{COLOR_RESET}")
                return
            # 新增GUI语法
            if line.startswith('gui '):
                m = re.match(r'gui "([^"]+)" (\d+)x(\d+)', line)
                if m:
                    title, width, height = m.group(1), int(m.group(2)), int(m.group(3))
                    create_gui_window(title, width, height)
                    print(f"{COLOR_OK}创建GUI窗口: {title} {width}x{height}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] gui 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('button '):
                m = re.match(r'button "([^"]+)" at (\d+),(\d+)', line)
                if m:
                    text, x, y = m.group(1), int(m.group(2)), int(m.group(3))
                    add_button(text, lambda: print(f"{COLOR_OK}按钮被点击: {text}{COLOR_RESET}"), x, y)
                    print(f"{COLOR_OK}添加按钮: {text} at ({x},{y}){COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] button 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('label '):
                m = re.match(r'label "([^"]+)" at (\d+),(\d+)', line)
                if m:
                    text, x, y = m.group(1), int(m.group(2)), int(m.group(3))
                    add_label(text, x, y)
                    print(f"{COLOR_OK}添加标签: {text} at ({x},{y}){COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] label 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('entry '):
                m = re.match(r'entry at (\d+),(\d+) width (\d+)', line)
                if m:
                    x, y, width = int(m.group(1)), int(m.group(2)), int(m.group(3))
                    add_entry(x, y, width)
                    print(f"{COLOR_OK}添加输入框 at ({x},{y}) width {width}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] entry 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('textbox '):
                m = re.match(r'textbox at (\d+),(\d+) size (\d+)x(\d+)', line)
                if m:
                    x, y, width, height = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
                    add_textbox(x, y, width, height)
                    print(f"{COLOR_OK}添加文本框 at ({x},{y}) size {width}x{height}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] textbox 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('progress '):
                m = re.match(r'progress at (\d+),(\d+) width (\d+)', line)
                if m:
                    x, y, width = int(m.group(1)), int(m.group(2)), int(m.group(3))
                    add_progressbar(x, y, width)
                    print(f"{COLOR_OK}添加进度条 at ({x},{y}) width {width}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] progress 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('filedialog '):
                m = re.match(r'filedialog "([^"]+)"', line)
                if m:
                    title = m.group(1)
                    filename = show_file_dialog(title)
                    if filename:
                        print(f"{COLOR_OK}选择文件: {filename}{COLOR_RESET}")
                    else:
                        print(f"{COLOR_OK}未选择文件{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] filedialog 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('savefile '):
                m = re.match(r'savefile "([^"]+)"', line)
                if m:
                    title = m.group(1)
                    filename = show_save_dialog(title)
                    if filename:
                        print(f"{COLOR_OK}保存文件: {filename}{COLOR_RESET}")
                    else:
                        print(f"{COLOR_OK}未选择保存位置{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] savefile 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('colorchooser '):
                m = re.match(r'colorchooser "([^"]+)"', line)
                if m:
                    title = m.group(1)
                    color = show_color_dialog(title)
                    if color[0]:
                        print(f"{COLOR_OK}选择颜色: RGB{color[0]}{COLOR_RESET}")
                    else:
                        print(f"{COLOR_OK}未选择颜色{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] colorchooser 语法错误: {line}{COLOR_RESET}")
                return
            elif line.strip() == 'gui mainloop':
                if current_gui_window:
                    print(f"{COLOR_OK}启动GUI主循环{COLOR_RESET}")
                    current_gui_window.mainloop()
                else:
                    print(f"{COLOR_ERR}[Error] 没有活动的GUI窗口{COLOR_RESET}")
                return

            # 极简GUI语法 - 优先级最高
            # window "标题" size=400x300
            if line.startswith('window '):
                m = re.match(r'window "([^"]+)" size=(\d+)x(\d+)', line)
                if m:
                    title, width, height = m.group(1), int(m.group(2)), int(m.group(3))
                    create_gui_window(title, width, height)
                    print(f"{COLOR_OK}创建窗口: {title} {width}x{height}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] window 语法错误: {line}{COLOR_RESET}")
                return
            
            # Label "文本" [color=red] [font=微软雅黑] [size=12]
            elif line.startswith('Label '):
                m = re.match(r'Label "([^"]+)"(.*)', line)
                if m:
                    text = m.group(1)
                    options = m.group(2)
                    kwargs = {'text': text}
                    
                    # 解析选项
                    if 'color=' in options:
                        color_match = re.search(r'color=(\w+)', options)
                        if color_match:
                            kwargs['fg'] = color_match.group(1)
                    if 'font=' in options:
                        font_match = re.search(r'font=([^ ]+)', options)
                        if font_match:
                            kwargs['font'] = font_match.group(1)
                    if 'size=' in options:
                        size_match = re.search(r'size=(\d+)', options)
                        if size_match:
                            size = int(size_match.group(1))
                            kwargs['font'] = (kwargs.get('font', None), size)
                    
                    result = create_widget('Label', **kwargs)
                    if result:
                        widget_name, widget = result
                        print(f"{COLOR_OK}创建标签: {widget_name} = {text}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] Label 语法错误: {line}{COLOR_RESET}")
                return
            
            # Entry [default="默认值"] [width=20]
            elif line.startswith('Entry') and not re.match(r'^\w+\.', line):
                m = re.match(r'Entry(.*)', line)
                if m:
                    options = m.group(1)
                    kwargs = {}
                    
                    if 'width=' in options:
                        width_match = re.search(r'width=(\d+)', options)
                        if width_match:
                            kwargs['width'] = int(width_match.group(1))
                    
                    result = create_widget('Entry', **kwargs)
                    if result:
                        widget_name, widget = result
                        
                        # 设置默认值
                        if 'default=' in options:
                            default_match = re.search(r'default="([^"]+)"', options)
                            if default_match:
                                default_value = default_match.group(1)
                                widget.insert(0, default_value)
                        
                        print(f"{COLOR_OK}创建输入框: {widget_name}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] Entry 语法错误: {line}{COLOR_RESET}")
                return
            
            # Button "文本" on_click=函数名
            elif line.startswith('Button '):
                m = re.match(r'Button "([^"]+)"(.*)', line)
                if m:
                    text = m.group(1)
                    options = m.group(2)
                    kwargs = {'text': text}
                    
                    # 解析事件绑定
                    if 'on_click=' in options:
                        click_match = re.search(r'on_click=(\w+)', options)
                        if click_match:
                            func_name = click_match.group(1)
                            # 这里需要延迟绑定，因为函数可能还没定义
                            kwargs['command'] = lambda f=func_name: self.call_user_function(f)
                    
                    result = create_widget('Button', **kwargs)
                    if result:
                        widget_name, widget = result
                        print(f"{COLOR_OK}创建按钮: {widget_name} = {text}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] Button 语法错误: {line}{COLOR_RESET}")
                return
            
            # Combobox ["选项1", "选项2", "选项3"]
            elif line.startswith('Combobox '):
                m = re.match(r'Combobox \[(.*)\]', line)
                if m:
                    options_str = m.group(1)
                    # 解析选项列表
                    options = []
                    for opt in re.findall(r'"([^"]+)"', options_str):
                        options.append(opt)
                    
                    kwargs = {'values': options}
                    if options:
                        kwargs['state'] = 'readonly'
                    
                    result = create_widget('Combobox', **kwargs)
                    if result:
                        widget_name, widget = result
                        print(f"{COLOR_OK}创建下拉框: {widget_name} = {options}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] Combobox 语法错误: {line}{COLOR_RESET}")
                return
            
            # Checkbox "文本" [checked]
            elif line.startswith('Checkbox '):
                m = re.match(r'Checkbox "([^"]+)"(.*)', line)
                if m:
                    text = m.group(1)
                    options = m.group(2)
                    kwargs = {'text': text}
                    
                    if 'checked' in options:
                        kwargs['variable'] = tk.BooleanVar(value=True)
                    else:
                        kwargs['variable'] = tk.BooleanVar(value=False)
                    
                    result = create_widget('Checkbutton', **kwargs)
                    if result:
                        widget_name, widget = result
                        print(f"{COLOR_OK}创建复选框: {widget_name} = {text}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] Checkbox 语法错误: {line}{COLOR_RESET}")
                return
            
            # 属性设置: Label1.text = "新内容"
            elif re.match(r'^\w+\.\w+\s*=', line):
                m = re.match(r'(\w+)\.(\w+)\s*=\s*(.+)', line)
                if m:
                    widget_name, property_name, value = m.group(1), m.group(2), m.group(3)
                    # 去除引号
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    if set_widget_property(widget_name, property_name, value):
                        print(f"{COLOR_OK}设置属性: {widget_name}.{property_name} = {value}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] 属性设置语法错误: {line}{COLOR_RESET}")
                return
            
            # 布局: Label1.pack left
            elif re.match(r'^\w+\.(pack|grid|place)', line):
                m = re.match(r'(\w+)\.(pack|grid|place)(.*)', line)
                if m:
                    widget_name, layout_type, options = m.group(1), m.group(2), m.group(3)
                    kwargs = {}
                    
                    if layout_type == 'pack':
                        if 'left' in options:
                            kwargs['side'] = 'left'
                        elif 'right' in options:
                            kwargs['side'] = 'right'
                        elif 'top' in options:
                            kwargs['side'] = 'top'
                        elif 'bottom' in options:
                            kwargs['side'] = 'bottom'
                    elif layout_type == 'grid':
                        # grid row col
                        grid_match = re.search(r'(\d+)\s+(\d+)', options)
                        if grid_match:
                            kwargs['row'] = int(grid_match.group(1))
                            kwargs['column'] = int(grid_match.group(2))
                    elif layout_type == 'place':
                        # place x y
                        place_match = re.search(r'(\d+)\s+(\d+)', options)
                        if place_match:
                            kwargs['x'] = int(place_match.group(1))
                            kwargs['y'] = int(place_match.group(2))
                    
                    if layout_widget(widget_name, layout_type, **kwargs):
                        print(f"{COLOR_OK}布局控件: {widget_name}.{layout_type}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] 布局语法错误: {line}{COLOR_RESET}")
                return
            
            # 动态添加: add Button "新按钮"
            elif line.startswith('add '):
                m = re.match(r'add\s+(Button|Label|Entry|Combobox|Checkbox)\s+(.+)', line)
                if m:
                    widget_type, rest = m.group(1), m.group(2)
                    if widget_type == 'Checkbox':
                        widget_type = 'Checkbutton'
                    
                    # 解析参数
                    if widget_type == 'Button':
                        text_match = re.match(r'"([^"]+)"', rest)
                        if text_match:
                            text = text_match.group(1)
                            result = create_widget(widget_type, text=text)
                            if result:
                                widget_name, widget = result
                                print(f"{COLOR_OK}动态添加按钮: {widget_name}{COLOR_RESET}")
                    elif widget_type == 'Label':
                        text_match = re.match(r'"([^"]+)"', rest)
                        if text_match:
                            text = text_match.group(1)
                            result = create_widget(widget_type, text=text)
                            if result:
                                widget_name, widget = result
                                print(f"{COLOR_OK}动态添加标签: {widget_name}{COLOR_RESET}")
                    elif widget_type == 'Entry':
                        result = create_widget(widget_type)
                        if result:
                            widget_name, widget = result
                            print(f"{COLOR_OK}动态添加输入框: {widget_name}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] add 语法错误: {line}{COLOR_RESET}")
                return
            
            # 删除控件: remove Label1
            elif line.startswith('remove '):
                m = re.match(r'remove (\w+)', line)
                if m:
                    widget_name = m.group(1)
                    widget = get_widget(widget_name)
                    if widget:
                        widget.destroy()
                        del gui_widgets[widget_name]
                        print(f"{COLOR_OK}删除控件: {widget_name}{COLOR_RESET}")
                    else:
                        print(f"{COLOR_ERR}[Error] 控件不存在: {widget_name}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] remove 语法错误: {line}{COLOR_RESET}")
                return
            
            # 启动GUI主循环
            elif line.strip() == 'mainloop':
                if current_gui_window:
                    print(f"{COLOR_OK}启动GUI主循环{COLOR_RESET}")
                    current_gui_window.mainloop()
                else:
                    print(f"{COLOR_ERR}[Error] 没有活动的GUI窗口{COLOR_RESET}")
                return
            # pygame 语法优先
            if line.startswith('window '):
                self.ensure_pygame()
                m = re.match(r'window (\d+)x(\d+)', line)
                if m:
                    w, h = int(m.group(1)), int(m.group(2))
                    pygame = self.exec_env['pygame']
                    self.screen = pygame.display.set_mode((w, h))
                    self.exec_env['screen'] = self.screen
                else:
                    print(f"{COLOR_ERR}[Error] window 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('fill '):
                self.ensure_pygame()
                color = self.parse_color(line[5:].strip())
                if self.screen:
                    self.screen.fill(color)
                else:
                    print(f"{COLOR_ERR}[Error] fill 之前请先 window ...{COLOR_RESET}")
                return
            elif line.startswith('rect '):
                self.ensure_pygame()
                m = re.match(r'rect (\d+),(\d+),(\d+),(\d+) (.+)', line)
                if m:
                    x, y, w, h = map(int, m.group(1,2,3,4))
                    color = self.parse_color(m.group(5))
                    pygame = self.exec_env['pygame']
                    if self.screen:
                        pygame.draw.rect(self.screen, color, (x, y, w, h))
                    else:
                        print(f"{COLOR_ERR}[Error] rect 之前请先 window ...{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] rect 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('circle '):
                self.ensure_pygame()
                m = re.match(r'circle (\d+),(\d+),(\d+) (.+)', line)
                if m:
                    x, y, r = map(int, m.group(1,2,3))
                    color = self.parse_color(m.group(4))
                    pygame = self.exec_env['pygame']
                    if self.screen:
                        pygame.draw.circle(self.screen, color, (x, y), r)
                    else:
                        print(f"{COLOR_ERR}[Error] circle 之前请先 window ...{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] circle 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('text '):
                self.ensure_pygame()
                m = re.match(r"text (\d+),(\d+) '(.+)' (\w+|\(.+\)) (\d+)", line)
                if m:
                    x, y = int(m.group(1)), int(m.group(2))
                    txt = m.group(3)
                    color = self.parse_color(m.group(4))
                    size = int(m.group(5))
                    pygame = self.exec_env['pygame']
                    font = pygame.font.SysFont(None, size)
                    img = font.render(txt, True, color)
                    if self.screen:
                        self.screen.blit(img, (x, y))
                    else:
                        print(f"{COLOR_ERR}[Error] text 之前请先 window ...{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] text 语法错误: {line}{COLOR_RESET}")
                return
            elif line in ('flip', 'update'):
                self.ensure_pygame()
                pygame = self.exec_env['pygame']
                pygame.display.flip()
                return
            elif line == 'wait quit':
                self.ensure_pygame()
                pygame = self.exec_env['pygame']
                running = True
                while running:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                pygame.quit()
                return
            # 其它自定义语法优先
            if line.startswith('swap '):
                m = re.match(r'swap (\w+),\s*(\w+)', line)
                if m:
                    a, b = m.group(1), m.group(2)
                    if a in PYPP_KEYWORDS or b in PYPP_KEYWORDS:
                        print(f"{COLOR_ERR}[Error] 关键字不能作为变量名: {a} 或 {b}{COLOR_RESET}")
                        return
                    self.variables[a], self.variables[b] = self.variables.get(b), self.variables.get(a)
                    self.exec_env[a], self.exec_env[b] = self.variables[a], self.variables[b]
                else:
                    print(f"{COLOR_ERR}[Error] swap 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('input '):
                var = line[6:].strip()
                if var in PYPP_KEYWORDS:
                    print(f"{COLOR_ERR}[Error] 关键字不能作为变量名: {var}{COLOR_RESET}")
                    return
                value = input(f"输入 {var}: ")
                if value == '':
                    value = None
                else:
                    for typ in (int, float):
                        try:
                            value = typ(value)
                            break
                        except:
                            continue
                    if isinstance(value, str):
                        if value.lower() in ('true','false'):
                            value = value.lower() == 'true'
                self.variables[var] = value
                self.exec_env[var] = value
                return
            elif re.match(r'^(\w+)\+\+$', line):
                m = re.match(r'^(\w+)\+\+$', line)
                if m:
                    var = m.group(1)
                    if var in PYPP_KEYWORDS:
                        print(f"{COLOR_ERR}[Error] 关键字不能作为变量名: {var}{COLOR_RESET}")
                        return
                    self.variables[var] = self.variables.get(var, 0) + 1
                    self.exec_env[var] = self.variables[var]
                else:
                    print(f"{COLOR_ERR}[Error] 自增语法错误: {line}{COLOR_RESET}")
                return
            elif re.match(r'^(\w+)--$', line):
                m = re.match(r'^(\w+)--$', line)
                if m:
                    var = m.group(1)
                    if var in PYPP_KEYWORDS:
                        print(f"{COLOR_ERR}[Error] 关键字不能作为变量名: {var}{COLOR_RESET}")
                        return
                    self.variables[var] = self.variables.get(var, 0) - 1
                    self.exec_env[var] = self.variables[var]
                else:
                    print(f"{COLOR_ERR}[Error] 自减语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('if '):
                m = re.match(r'if (.+?) then (.+?)( else (.+))?$', line)
                if m:
                    cond, then_part, _, else_part = m.group(1), m.group(2), m.group(3), m.group(4)
                    if self.eval_expr(cond):
                        self.run_line(then_part)
                    elif else_part:
                        self.run_line(else_part)
                else:
                    m2 = re.match(r'if (.+):(.+)', line)
                    if m2:
                        cond, body = m2.group(1), m2.group(2)
                        if self.eval_expr(cond):
                            self.run_line(body)
                    else:
                        print(f"{COLOR_ERR}[Error] if 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('when '):
                m = re.match(r'when (.+):(.+)', line)
                if m:
                    cond, body = m.group(1), m.group(2)
                    if self.eval_expr(cond):
                        self.run_line(body)
                else:
                    print(f"{COLOR_ERR}[Error] when 语法错误: {line}{COLOR_RESET}")
                return
            elif re.match(r'^for (\w+):(\d+):(.+)', line):
                m = re.match(r'^for (\w+):(\d+):(.+)', line)
                if m:
                    var, end, body = m.group(1), int(m.group(2)), m.group(3)
                    if var in PYPP_KEYWORDS:
                        print(f"{COLOR_ERR}[Error] 关键字不能作为变量名: {var}{COLOR_RESET}")
                        return
                    for v in range(end):
                        self.variables[var] = v
                        self.exec_env[var] = v
                        self.run_line(body)
                else:
                    print(f"{COLOR_ERR}[Error] for 语法错误: {line}{COLOR_RESET}")
                return
            # repeat n: run 多行块
            m = re.match(r'^repeat (\d+):\s*run$', line)
            if m:
                n = int(m.group(1))
                block_lines = []
                # 收集run块内容
                while True:
                    next_line = next(self.line_iter, None)
                    if next_line is None:
                        break
                    if next_line.startswith('    ') or next_line.startswith('\t'):
                        block_lines.append(next_line[4:] if next_line.startswith('    ') else next_line[1:])
                    else:
                        # 非缩进行，放回去
                        self.line_iter = self._prepend_line(self.line_iter, next_line)
                        break
                for _ in range(n):
                    for bline in block_lines:
                        self.run_line(bline)
                return
            elif re.match(r'^repeat (\d+):(.+)', line):
                m = re.match(r'^repeat (\d+):(.+)', line)
                if m:
                    n, body = int(m.group(1)), m.group(2)
                    for _ in range(n):
                        self.run_line(body.strip())
                else:
                    print(f"{COLOR_ERR}[Error] repeat 语法错误: {line}{COLOR_RESET}")
                return
            elif re.match(r'^while (.+):(.+)', line):
                m = re.match(r'^while (.+):(.+)', line)
                if m:
                    cond, body = m.group(1), m.group(2)
                    while self.eval_expr(cond):
                        self.run_line(body)
                else:
                    print(f"{COLOR_ERR}[Error] while 语法错误: {line}{COLOR_RESET}")
                return
            elif re.match(r'^(def|fn) (\w+)\((.*?)\)\s*=\s*(.+)', line):
                m = re.match(r'^(def|fn) (\w+)\((.*?)\)\s*=\s*(.+)', line)
                if m:
                    name, args, expr = m.group(2), m.group(3), m.group(4)
                    if name in PYPP_KEYWORDS:
                        print(f"{COLOR_ERR}[Error] 关键字不能作为函数名: {name}{COLOR_RESET}")
                        return
                    code = f"def {name}({args}):\n    return {expr}"
                    try:
                        exec(code, self.exec_env, self.variables)
                    except Exception as e:
                        print(f"{COLOR_ERR}[Error] 单行函数定义错误: {e}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] 单行函数定义语法错误: {line}{COLOR_RESET}")
                return
            elif re.match(r'^(def|fn) (\w+)\(.*\):', line):
                # 多行函数定义开始
                m = re.match(r'^(def|fn) (\w+)\((.*)\):', line)
                if m:
                    name, args = m.group(2), m.group(3)
                    if name in PYPP_KEYWORDS:
                        print(f"{COLOR_ERR}[Error] 关键字不能作为函数名: {name}{COLOR_RESET}")
                        return
                    # 开始收集函数体
                    self.in_function_block = True
                    self.function_name = name
                    self.function_args = args
                    self.function_lines = []
                    print(f"{COLOR_OK}开始定义函数: {name}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] 函数定义语法错误: {line}{COLOR_RESET}")
                return
            elif re.match(r'^use (.+) as (.+):', line):
                m = re.match(r'^use (.+) as (.+):', line)
                if m:
                    res, var = m.group(1), m.group(2)
                    code = f"with {res} as {var}:\n    pass"
                    try:
                        exec(code, self.exec_env, self.variables)
                    except Exception as e:
                        print(f"{COLOR_ERR}[Error] use 语法错误: {e}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] use 语法错误: {line}{COLOR_RESET}")
                return
            # let 支持函数定义: let add(a, b) = a + b
            m = re.match(r'let\s+(\w+)\((.*?)\)\s*=\s*(.+)', line)
            if m:
                name, args, expr = m.group(1), m.group(2), m.group(3)
                if name in PYPP_KEYWORDS:
                    print(f"{COLOR_ERR}[Error] 关键字不能作为函数名: {name}{COLOR_RESET}")
                    return
                code = f"def {name}({args}):\n    return {expr}"
                try:
                    exec(code, self.exec_env, self.variables)
                except Exception as e:
                    print(f"{COLOR_ERR}[Error] let函数定义错误: {e}{COLOR_RESET}")
                return
            elif line.startswith('let '):
                m = re.match(r'let ((?:\w+,? ?)+)=(.+)', line)
                if m:
                    vars_part, expr_part = m.group(1), m.group(2)
                    vars_list = [v.strip() for v in vars_part.split(',')]
                    exprs = [e.strip() for e in expr_part.split(',')]
                    for v in vars_list:
                        if v in PYPP_KEYWORDS:
                            print(f"{COLOR_ERR}[Error] 关键字不能作为变量名: {v}{COLOR_RESET}")
                            return
                    if len(vars_list) == len(exprs):
                        for v, e in zip(vars_list, exprs):
                            value = self.eval_expr(e)
                            self.variables[v] = value
                            self.exec_env[v] = value
                    else:
                        value = self.eval_expr(expr_part)
                        self.variables[vars_list[0]] = value
                        self.exec_env[vars_list[0]] = value
                else:
                    print(f"{COLOR_ERR}[Error] let 语法错误: {line}{COLOR_RESET}")
                return
            elif line.startswith('print '):
                expr = line[6:].strip()
                value = self.eval_expr(expr)
                print(f"{COLOR_OK}{value}{COLOR_RESET}")
                return
            elif line.startswith('do '):
                code = line[3:].strip()
                try:
                    exec(code, self.exec_env, self.variables)
                except Exception as e:
                    print(f"{COLOR_ERR}[Error] do 执行错误: {e}{COLOR_RESET}")
                return
            elif line.startswith('run'):
                self.in_run_block = True
                self.run_block_lines = []
                return
            elif line.startswith('open '):
                m = re.match(r'open (.+)', line)
                if m:
                    self.in_open_block = True
                    self.open_filename = m.group(1).strip()
                    self.open_block_lines = []
                else:
                    print(f"{COLOR_ERR}[Error] open 语法错误: {line}{COLOR_RESET}")
                return
            # add 导入库功能
            if line.strip().startswith('add '):
                m = re.match(r'add (\w+)(?: as (\w+))?', line.strip())
                if m:
                    lib = m.group(1)
                    alias = m.group(2) if m.group(2) else m.group(1)
                    try:
                        self.exec_env[alias] = __import__(lib)
                        print(f"{COLOR_OK}已导入库: {lib} as {alias}{COLOR_RESET}")
                    except Exception as e:
                        print(f"{COLOR_ERR}[Error] 导入库失败: {lib} ({e}){COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] add 语法错误: {line}{COLOR_RESET}")
                return
            # output 语法糖，等价于print
            if line.strip().startswith('output '):
                expr = line.strip()[7:].strip()
                self.run_line(f'print {expr}')
                return
            # 省略 print，直接输出表达式
            m = re.match(r'^[a-zA-Z_][\w\[\]\(\)\+\-\*/%<>=!&|^,\. ]*$', line)
            if m and not re.match(r'^(def|fn|for|if|when|while|let|print|do|run|open|input|swap|repeat|use|window|fill|rect|circle|text|flip|update|wait|warning|info|error|askyesno|inputbox)', line):
                try:
                    value = self.eval_expr(line)
                    if value is not None:
                        print(f"{COLOR_OK}{value}{COLOR_RESET}")
                except Exception:
                    pass
                return
            # 其它行直接当 Python 代码
            try:
                exec(line, self.exec_env, self.variables)
            except Exception as e:
                print(f"{COLOR_ERR}[Error] Python 代码执行错误: {e}{COLOR_RESET}")
            # pause 指令，暂停n秒
            if line.strip().startswith('pause'):
                m = re.match(r'pause\s*(\d*\.?\d*)', line.strip())
                if m:
                    t = float(m.group(1)) if m.group(1) else 1.0
                    import time
                    time.sleep(t)
                    print(f"{COLOR_OK}暂停{t}秒{COLOR_RESET}")
                else:
                    print(f"{COLOR_ERR}[Error] pause 语法错误: {line}{COLOR_RESET}")
                return
        except Exception as e:
            print(f"{COLOR_ERR}[Interpreter Error] {e}{COLOR_RESET}")

    def exec_run_block(self):
        code = '\n'.join(self.run_block_lines)
        try:
            exec(code, self.exec_env, self.variables)
        except Exception as e:
            print(f"{COLOR_ERR}[Error] run块执行错误: {e}{COLOR_RESET}")

    def exec_open_block(self):
        if not self.open_filename:
            print(f"{COLOR_ERR}[Error] open 块未指定文件名{COLOR_RESET}")
            return
        try:
            with open(self.open_filename, 'r', encoding='utf-8') as f:
                local_vars = dict(self.variables)
                local_vars['f'] = f
                code = '\n'.join(self.open_block_lines)
                try:
                    exec(code, self.exec_env, local_vars)
                except Exception as e:
                    print(f"{COLOR_ERR}[Error] open块执行错误: {e}{COLOR_RESET}")
                for k, v in local_vars.items():
                    if k != 'f':
                        self.variables[k] = v
                        self.exec_env[k] = v
        except FileNotFoundError:
            print(f"{COLOR_ERR}[Error] 文件不存在: {self.open_filename}{COLOR_RESET}")
        except PermissionError:
            print(f"{COLOR_ERR}[Error] 文件权限不足: {self.open_filename}{COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_ERR}[Error] open 块执行错误: {e}{COLOR_RESET}")

    def exec_function_block(self):
        if not self.function_name:
            print(f"{COLOR_ERR}[Error] 函数块未指定函数名{COLOR_RESET}")
            return
        
        # 构建函数体代码
        func_code = f"def {self.function_name}({self.function_args}):\n"
        for line in self.function_lines:
            if line.strip():  # 跳过空行
                func_code += f"    {line}\n"
        
        try:
            # 将全局变量添加到执行环境
            exec_env = dict(self.exec_env)
            exec_env.update({
                'current_gui_window': current_gui_window,
                'gui_widgets': gui_widgets,
                'get_widget_property': get_widget_property,
                'set_widget_property': set_widget_property,
                'show_info': show_info,
                'show_error': show_error,
                'show_warning': show_warning,
                'ask_yesno': ask_yesno,
                'input_box': input_box
            })
            exec(func_code, exec_env, self.variables)
            print(f"{COLOR_OK}函数定义成功: {self.function_name}{COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_ERR}[Error] 函数定义错误: {e}{COLOR_RESET}")
            print(f"{COLOR_ERR}函数代码: {func_code}{COLOR_RESET}")

    def run_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    self.run_line(line)
            if self.in_run_block:
                self.exec_run_block()
                self.in_run_block = False
            if self.in_open_block:
                self.exec_open_block()
                self.in_open_block = False
            if self.in_function_block:
                self.exec_function_block()
                self.in_function_block = False
        except Exception as e:
            print(f"{COLOR_ERR}[Interpreter Error] {e}{COLOR_RESET}")
        finally:
            if self.pygame_inited:
                try:
                    self.exec_env['pygame'].quit()
                except:
                    pass
            if self.open_file_obj:
                try:
                    self.open_file_obj.close()
                except:
                    pass

if __name__ == '__main__':
    if len(sys.argv) != 2 or not sys.argv[1].endswith('.code'):
        print('用法: python interpreter.py 文件名.code')
        os.system('pause')
        sys.exit(1)
    interpreter = PythonPPInterpreter()
    interpreter.run_file(sys.argv[1]) 