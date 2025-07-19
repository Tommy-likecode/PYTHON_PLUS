Copyright (c) 2025 方跃桐

# Python++ 项目总览

这是一个增强的 Python++ 解释器与极简 GUI 工具链，支持用极简语法开发桌面应用，并一键自动转换、批量转换、打包为 exe。

---

## 目录
- [项目简介](#项目简介)
- [快速开始](#快速开始)
- [python++ 极简GUI语法](#python-极简gui语法)
- [转换器与打包器用法](#转换器与打包器用法)
- [支持的控件、事件、布局](#支持的控件事件布局)
- [注意事项与常见问题](#注意事项与常见问题)
- [项目结构](#项目结构)
- [开发/贡献指南](#开发贡献指南)
- [许可证](#许可证)
- [联系方式](#联系方式)

---

## 项目简介

Python++ 是一个简化 Python 语法、内置强大 GUI 能力的解释器及工具链，支持：
- 极简 GUI 语法，自动生成 Tkinter 代码
- .code 文件一键转换为 .py、.exe
- 批量/递归转换、自动打包、依赖自动安装
- 丰富控件、事件、布局、属性、弹窗、动态控件、线程安全消息等
- 详细日志、自动化测试、完善文档

---

## 快速开始

### 1. 运行 .code 文件（自动转换并运行）
```bash
python console.py yourfile.code
```

### 2. 一键转换 .code 为 .py
```bash
python code_to_py.py yourfile.code
# 或批量转换整个目录
python code_to_py.py yourdir/ -o outputdir/
```

### 3. 一键打包 .code 为 .exe
```bash
python standalone_code_to_exe.py yourfile.code
# 支持命令行参数指定输出名、批量、递归等
```

### 4. 导入库
```bash
add 库名.py
# 本项目自带两个库：gameplus和cmd
```
---

## python++ 极简GUI语法

### 基本语法
```python
window main "窗口标题" 800 600
button btn1 "按钮文本"
label lbl1 "标签文本"
entry ent1 text="默认文本"
pack btn1 side=top pady=10
grid btn1 row=0 column=0
place btn1 x=10 y=10
function onclick
    lbl1.text = "按钮被点击了！"
bind btn1 click onclick
```

### 进阶语法与特性
- 控件自动命名（Label1, Entry1, Button1...）
- 事件绑定：`on_click=函数名` 或 `bind 控件 事件 函数`
- 属性设置：`控件名.属性 = 值`
- 动态添加/删除控件：`add/remove 控件`
- 支持弹窗、对话框、颜色选择、文件选择等
- 支持 pack/grid/place 三种布局
- 线程安全的消息/进度更新

### 示例
```python
window "登录" size=300x200
Label "用户名" color=blue
Entry default="请输入用户名"
Button "登录" on_click=login
function login
    if Entry1.text == "admin":
        info "登录成功！"
    else:
        error "用户名错误"
mainloop
```

---

## 转换器与打包器用法

### 1. .code 转 .py
```bash
python code_to_py.py input.code
python code_to_py.py input.code -o output.py
python code_to_py.py input_dir/ -o output_dir/  # 批量/递归
```
- 支持命令行参数：输入、输出、递归、进度、错误处理

### 2. .code 转 .exe
```bash
python standalone_code_to_exe.py input.code
# 自动转换并用 PyInstaller 打包
# 支持依赖自动安装、详细日志、临时文件管理
```

### 3. 自动运行 .code
```bash
python console.py input.code
# 自动转换为 .py 并运行，失败则回退解释执行
```

---

## 支持的控件、事件、布局

### 控件
- 按钮 (button)
- 标签 (label)
- 输入框 (entry)
- 文本区 (text)
- 列表框 (listbox)
- 下拉框 (combobox)
- 复选框 (checkbox)
- 单选按钮 (radiobutton)
- 图片 (image)
- 进度条 (progress)

### 事件
- 鼠标点击 (click)
- 双击 (double)
- 右键 (right)
- 键盘输入 (key)
- 回车 (enter)
- 焦点 (focus/blur)

### 布局
- pack
- grid
- place

---

## 注意事项与常见问题

1. 需安装 Python 3.6+ 和 tkinter（通常随 Python 安装）
2. 控件名需唯一，函数定义需在事件绑定前
3. 所有坐标均为像素单位
4. 转换/打包过程如遇错误会详细输出日志
5. 支持 Windows/macOS/Linux，打包为 exe 需 Windows
6. 详细用法、参数、语法、控件、事件见本 README

---

## 项目结构

```
python++/
├── interpreter.py            # Python++ 解释器
├── code_to_py.py             # .code 转 .py 工具
├── console.py                # 自动转换并运行 .code
├── standalone_code_to_exe.py # .code 转 .exe（内置转换逻辑）
├── test_converter.py         # 自动化测试脚本
├── README.md                 # 项目总说明（本文件）
├── CONVERTER_README.md       # 转换器说明（已合并）
├── GUI_README.md             # GUI 说明（已合并）
├── ... 其它示例/批量/测试文件
```

---

## 开发/贡献指南

1. Fork 本项目，创建功能分支
2. 按需在 interpreter.py、code_to_py.py 等文件中添加控件/事件/语法
3. 补充/修正文档和示例
4. 提交 Pull Request

---

## 许可证

本项目采用 MIT 许可证。

---

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。 

Made By 方跃桐
未经允许请勿转载！
