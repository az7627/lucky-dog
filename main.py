# coding=UTF-8

import tkinter
import tkinter.messagebox
from os import name as os_name
from os import getcwd
from random import choices, choice
import json
from fractions import Fraction
import logging
import colorlog  # 确保已安装colorlog库

# 配置彩色日志
colorlog.basicConfig(
    format='%(log_color)s[%(asctime)s %(levelname)s]\t %(message)s',
    level=logging.DEBUG,
    log_colors={
        'DEBUG': 'green',
        'INFO': 'cyan',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)

mainWindow = tkinter.Tk()
mainWindow.title("Random-pickup")
mainWindow.geometry("550x350")

try:
    # 读取 JSON 配置文件
    json_path = getcwd() + ("/", "\\")[os_name == "nt"] + "names.json"
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # 解析名字和权重，转换为 Fraction
    students = []
    for item in data:
        name = item.get("name")
        if not name:
            logging.warning("发现无名字的条目，已跳过")
            continue
        weight = item.get("weight", 1)
        try:
            # 将输入的小数或整数转为 Fraction
            weight_frac = Fraction(str(weight))
        except Exception:
            logging.error(f"权重格式错误: {weight}，使用默认值 1")
            weight_frac = Fraction(1)
        students.append({"name": name, "weight": weight_frac})

    if not students:
        raise ValueError("名单为空")

except FileNotFoundError:
    logging.error("""未找到 names.json !
请检查程序所在的目录下是否有一个名为“names.json”的文件，然后再尝试运行一次。
如果您正在使用终端，请 cd 到此程序所在的目录。""")
    tkinter.messagebox.showerror("错误", """未找到 names.json !
请检查程序所在的目录下是否有一个名为“names.json”的文件，然后再尝试运行一次。
如果您正在使用终端，请 cd 到此程序所在的目录。""")
    mainWindow.destroy()
    exit(1)
except PermissionError:
    logging.error("""无法打开 names.json !
请确认您有足够的权限。
或者尝试使用""" + ("root", "Administrator")[os_name == "nt"] + "用户或以" + ("root", "管理员")[os_name == "nt"] + "权限运行此程序。")
    tkinter.messagebox.showerror("错误", """无法打开 names.json !
请确认您有足够的权限。
或者尝试使用""" + ("root", "Administrator")[os_name == "nt"] + "用户或以" + ("root", "管理员")[os_name == "nt"] + "权限运行此程序。")
    mainWindow.destroy()
    exit(1)
except (json.JSONDecodeError, ValueError) as e:
    logging.error(f"配置文件格式错误: {e}")
    tkinter.messagebox.showerror("错误", f"配置文件格式错误: {e}")
    mainWindow.destroy()
    exit(1)
except OSError:
    logging.error("操作系统错误发生。")
    tkinter.messagebox.showerror("错误", "操作系统错误发生。")
    mainWindow.destroy()
    exit(1)
else:
    fontsize = 100

    def random_pick_with_animation():
        """带简单动画的加权随机抽取，抽取后权重减半"""
        if not students:
            return

        # 禁用抽取按钮，防止动画期间重复点击
        pickup_button.config(state=tkinter.DISABLED)

        # 提前确定最终选中的学生
        chosen = choices(students, weights=[s['weight'] for s in students], k=1)[0]
        final_name = chosen['name']

        # 动画参数
        steps = 10          # 变换次数
        interval = 50       # 每次间隔（毫秒）
        names_list = [s['name'] for s in students]  # 用于随机显示的名字池
        step_count = 0

        def animate():
            nonlocal step_count
            # 若主窗口已关闭，终止动画
            if not mainWindow.winfo_exists():
                return

            if step_count < steps:
                # 显示随机名字，颜色为灰色
                random_name = choice(names_list)
                label.config(text=random_name, fg="gray")
                step_count += 1
                mainWindow.after(interval, animate)
            else:
                # 动画结束，显示最终选中名字，颜色恢复为黑色
                label.config(text=final_name, fg="black")
                # 权重减半
                chosen['weight'] *= Fraction(1, 2)
                logging.info(f'抽到了 {final_name}，权重减半为 {chosen["weight"]}')
                # 恢复按钮可用
                pickup_button.config(state=tkinter.NORMAL)

        # 启动动画
        animate()

    def setFont():
        """打开字体设置子窗口"""
        def setFontsize(close: bool) -> None:
            """更改字体大小"""
            global fontsize
            entry_text = entry.get().strip()
            if entry_text.isnumeric() and entry_text != "":
                fontsize = int(entry_text)
                logging.debug("字体大小已成功设置为 %d." % fontsize)
                if close:
                    subWindow.destroy()
            else:
                logging.error('字体大小必须是正整数。')
                tkinter.messagebox.showerror("出错", "字体大小必须是正整数。")

        subWindow = tkinter.Tk()
        subWindow.geometry("300x100")
        subWindow.resizable(0, 0)
        subWindow.title("输入一个字体大小(默认为100):")
        entry = tkinter.Entry(subWindow)
        entry.grid(row=0, column=0, columnspan=3)
        entry.insert(0, str(fontsize))
        ok = tkinter.Button(subWindow, text="确定", font=('Sarasa Mono SC', 12),
                            command=lambda: setFontsize(True))
        cancel = tkinter.Button(subWindow, text="取消", font=('Sarasa Mono SC', 12),
                                command=subWindow.destroy)
        apply = tkinter.Button(subWindow, text="应用", font=('Sarasa Mono SC', 12),
                               command=lambda: setFontsize(False))
        ok.grid(row=1, column=0)
        cancel.grid(row=1, column=1)
        apply.grid(row=1, column=2)

    # 初始化界面
    logging.debug("加载成功! 名单中有 %d 个学生。" % len(students))
    tkinter.messagebox.showinfo("提示", "加载成功! 名单中有 %d 个学生。" % len(students))

    setfont_button = tkinter.Button(mainWindow, text="设置字体大小",
                                    font=('Sarasa Mono SC', 12), command=setFont)
    setfont_button.pack()

    pickup_button = tkinter.Button(mainWindow, text="选取名字",
                                   font=('Sarasa Mono SC', 40),
                                   command=random_pick_with_animation)
    pickup_button.pack()

    label = tkinter.Label(mainWindow, text="", font=(None, fontsize))
    label.pack()

    mainWindow.mainloop()