#!/usr/bin/env python3

import hashlib
import re
import py_compile
import os
import sys

class InteractionUtils:
    @staticmethod
    def confirm(prompt: str, default: str = 'Y') -> bool:
        '''
        显示确认提示，等待用户输入
        
        :param prompt: 提示文本
        :param default: 默认选项（'Y' 或 'N'）
        :return: 用户确认返回 True，否则返回 False
        '''
        # 验证默认值
        default = default.upper()
        if default not in ('Y', 'N'):
            raise ValueError("default 必须是 'Y' 或 'N'")
        
        # 构建完整的提示信息
        options = f"[{'Y' if default == 'Y' else 'y'}/{'N' if default == 'N' else 'n'}]"
        full_prompt = f"{prompt} {options} "
        
        # 获取并处理用户输入
        user_input = input(full_prompt).strip().upper()
        
        # 处理空输入（使用默认值）
        if user_input == '':
            return default == 'Y'
        
        # 检查有效输入
        if user_input not in ('Y', 'N'):
            print(f"无效输入: '{user_input}'，请选择 Y 或 N. 若不输入内容则默认选择 {default}")
            return InteractionUtils.confirm(prompt, default)  # 递归重新提示
        
        return user_input == 'Y'

def get_names_hash():
    """读取names.txt并计算其哈希值，处理可能的错误"""
    try:
        with open('./names.txt', "rb") as lis:
            content = lis.read()
            new_hash = hashlib.sha256(content).hexdigest()
            print(f"计算出的哈希值: {new_hash}")
            return new_hash
    except FileNotFoundError:
        print("错误: names.txt 文件未找到。")
        print("请确保 names.txt 文件与脚本在同一目录下。")
        sys.exit(1)
    except PermissionError:
        print("错误: 没有权限读取 names.txt 文件。")
        print("请确认您有足够的权限访问该文件。")
        sys.exit(1)
    except Exception as e:
        print(f"读取 names.txt 时发生错误: {e}")
        sys.exit(1)

def update_gui_hash(new_hash):
    """更新gui-zh.py中的哈希值"""
    try:
        # 读取gui-zh.py内容
        with open('gui-zh.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修复正则表达式模式 - 允许空格变化
        pattern = r"(TOGGLE_NAME_LIST_HASH\s*:\s*str\s*=\s*)'[a-f0-9]{64}'"
        
        # 检查是否已经包含新哈希值
        if f"'{new_hash}'" in content:
            print("哈希值未变化，无需更新。")
            return True
        
        # 替换哈希值
        updated_content = re.sub(pattern, rf"\1'{new_hash}'", content)
        
        # 检查是否成功替换
        if updated_content == content:
            print("警告: 未找到需要替换的哈希值行，可能格式已更改。")
            print("尝试匹配的行格式应为: TOGGLE_NAME_LIST_HASH: str = '64位哈希值'")
            
            # 查找并显示实际行
            for line in content.splitlines():
                if "TOGGLE_NAME_LIST_HASH" in line:
                    print(f"实际找到的行: {line}")
                    break
            
            if not InteractionUtils.confirm('继续操作吗?', default='N'):
                print("操作取消。")
                return False
        
        # 尝试写入文件
        try:
            with open('gui-zh.py', 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("成功更新 gui-zh.py 中的哈希值。")
            return True
        except PermissionError:
            print("错误: 没有权限写入 gui-zh.py 文件。")
            print("请确认您有足够的权限修改该文件。")
            return False
        except Exception as e:
            print(f"写入 gui-zh.py 时发生错误: {e}")
            return False
            
    except FileNotFoundError:
        print("错误: gui-zh.py 文件未找到。")
        return False
    except PermissionError:
        print("错误: 没有权限读取 gui-zh.py 文件。")
        return False
    except Exception as e:
        print(f"更新 gui-zh.py 时发生错误: {e}")
        return False

def compile_gui():
    """编译gui-zh.py文件"""
    try:
        # 编译文件
        py_compile.compile('gui-zh.py', cfile='gui-zh.pyc')
        print("编译成功，生成 gui-zh.pyc")
        return True
    except PermissionError:
        print("错误: 没有权限写入编译文件。")
        print("请确认您有足够的权限在当前目录创建文件。")
        return False
    except Exception as e:
        print(f"编译失败: {e}")
        return False

def delete_source_file():
    """删除源文件gui-zh.py"""
    try:
        os.remove('gui-zh.py')
        print("已删除源文件。")
        return True
    except PermissionError:
        print("错误: 没有权限删除 gui-zh.py 文件。")
        return False
    except FileNotFoundError:
        print("警告: gui-zh.py 文件不存在，可能已被删除。")
        return False
    except Exception as e:
        print(f"删除源文件时发生错误: {e}")
        return False

# 主程序
if __name__ == "__main__":
    # 获取names.txt的哈希值
    new_hash = get_names_hash()
    
    # 询问是否更新gui-zh.py中的哈希值
    if InteractionUtils.confirm('同时更改 gui-zh.py 中的哈希值?'):
        if update_gui_hash(new_hash):
            # 询问是否编译
            if InteractionUtils.confirm('是否编译 gui-zh.py?'):
                if compile_gui():
                    # 询问是否删除源文件
                    if InteractionUtils.confirm('是否删除源文件 gui-zh.py?', default='N'):
                        delete_source_file()
                else:
                    print("编译失败，保留源文件。")
    else:
        print("用户取消操作。")