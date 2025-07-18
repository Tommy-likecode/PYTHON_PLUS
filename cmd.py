import subprocess
import os

def run(cmd):
    """运行命令并返回(返回码,输出)"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode, result.stdout.strip()
    except Exception as e:
        return -1, str(e)

def output(cmd):
    """运行命令并返回输出(字符串)"""
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except Exception as e:
        return str(e)

def exists(path):
    """判断文件或目录是否存在"""
    return os.path.exists(path)

def remove(path):
    """删除文件"""
    try:
        os.remove(path)
        return True
    except Exception:
        return False

def mkdir(path):
    """创建目录"""
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception:
        return False 