import sys
import os
import subprocess
from pathlib import Path
from interpreter import PythonPPInterpreter

def auto_convert_code_file(code_file):
    """自动转换 .code 文件为 .py 文件"""
    try:
        code_path = Path(code_file)
        if not code_path.exists():
            return None, f"文件不存在: {code_file}"
        
        # 生成对应的 .py 文件名
        py_file = code_path.with_suffix('.py')
        
        # 运行转换器
        result = subprocess.run([
            sys.executable, "code_to_py.py", str(code_path)
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            if py_file.exists():
                return str(py_file), None
            else:
                return None, "转换成功但输出文件未生成"
        else:
            return None, f"转换失败: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return None, "转换超时"
    except Exception as e:
        return None, f"转换异常: {str(e)}"

def main():
    interpreter = PythonPPInterpreter()
    if len(sys.argv) == 2 and sys.argv[1].endswith('.code'):
        # 自动转换并运行
        py_file, error = auto_convert_code_file(sys.argv[1])
        if error:
            print(f"[转换错误] {error}")
            print("尝试直接运行 .code 文件...")
            interpreter.run_file(sys.argv[1])
        else:
            print(f"[自动转换] {sys.argv[1]} -> {py_file}")
            print("运行转换后的 Python 文件...")
            try:
                subprocess.run([sys.executable, str(py_file)])
            except Exception as e:
                print(f"[运行错误] {e}")
                print("尝试直接运行 .code 文件...")
                interpreter.run_file(sys.argv[1])
        return
    print('python++ 控制台 (输入 exit 退出, 支持 run/open 多行块, 直接输入 .code 文件名可执行)')
    buffer = []
    in_block = False
    block_type = None
    while True:
        try:
            if not in_block:
                line = input('>>> ')
                if line.strip() in ('exit', 'quit'):
                    break
                if line.strip().endswith('.code') and os.path.exists(line.strip()):
                    # 自动转换并运行
                    py_file, error = auto_convert_code_file(line.strip())
                    if error:
                        print(f"[转换错误] {error}")
                        print("尝试直接运行 .code 文件...")
                        interpreter.run_file(line.strip())
                    else:
                        print(f"[自动转换] {line.strip()} -> {py_file}")
                        print("运行转换后的 Python 文件...")
                        try:
                            subprocess.run([sys.executable, str(py_file)])
                        except Exception as e:
                            print(f"[运行错误] {e}")
                            print("尝试直接运行 .code 文件...")
                            interpreter.run_file(line.strip())
                    continue
                if line.strip().startswith('run') or line.strip().startswith('open '):
                    in_block = True
                    block_type = 'run' if line.strip().startswith('run') else 'open'
                    buffer = [line]
                    continue
                interpreter.run_line(line)
            else:
                line = input('... ')
                if not line.strip():
                    # 空行结束块
                    if block_type == 'run':
                        interpreter.in_run_block = True
                        interpreter.run_block_lines = [l[4:] if l.startswith('    ') else l for l in buffer[1:]]
                        interpreter.exec_run_block()
                        interpreter.in_run_block = False
                    elif block_type == 'open':
                        interpreter.in_open_block = True
                        interpreter.open_block_lines = [l[4:] if l.startswith('    ') else l for l in buffer[1:]]
                        interpreter.open_filename = buffer[0].split(' ',1)[1].strip()
                        interpreter.exec_open_block()
                        interpreter.in_open_block = False
                    in_block = False
                    block_type = None
                    buffer = []
                else:
                    buffer.append(line)
        except KeyboardInterrupt:
            print('\n退出 python++ 控制台')
            break
        except Exception as e:
            print(f'[Error] {e}')

if __name__ == '__main__':
    main() 