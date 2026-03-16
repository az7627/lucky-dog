# coding=UTF-8

import tkinter
import tkinter.messagebox
from os import name as os_name
from os import getcwd
from random import choice
import hashlib
import logging
import colorlog  # 确保已安装colorlog库

TOGGLE_NAME_LIST_HASH: str = '1017e1cc7f415846e2a764733e2c7bcfdfa2f5e2074b82e951a80ea15959c541'

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

try :
    with open(getcwd()+("/", "\\")[os_name=="nt"]+"names.txt", encoding="utf-8") as lis :
        gotLis: list[str] = lis.read().replace("\r", "").split("\n")
    unchosenLis: list[str] = gotLis.copy()
except FileNotFoundError :
    logging.error("""未找到names.txt !
请检查程序所在的目录下是否有一个名为“names.txt”的文件,然后再尝试运行一次。
如果您正在使用终端,请cd到此程序所在的目录。""")
    tkinter.messagebox.showerror("错误", """未找到names.txt !
请检查程序所在的目录下是否有一个名为“names.txt”的文件,然后再尝试运行一次。
如果您正在使用终端,请cd到此程序所在的目录。""")
except PermissionError :
    logging.error("""无法打开names.txt !
请确认您有足够的权限。
或者尝试使用"""+("root", "Administrator")[os_name=="nt"]+"用户或以"+("root", "管理员")[os_name=="nt"]+"权限运行此程序。")
    tkinter.messagebox.showerror("错误", """无法打开names.txt !
请确认您有足够的权限。
或者尝试使用"""+("root", "Administrator")[os_name=="nt"]+"用户或以"+("root", "管理员")[os_name=="nt"]+"权限运行此程序。")
except OSError :
    logging.error("操作系统错误发生。")
    tkinter.messagebox.showerror("错误", "操作系统错误发生。")
else :
    with open('./names.txt', "rb") as lis :
        if hashlib.sha256(lis.read()).hexdigest() != TOGGLE_NAME_LIST_HASH:
            logging.error('你不准继续！')
            logging.error('我猜有人想把自己的名字从名单里删掉。\n没想到吧，我加了校验\n所以，你不准继续抽号。')
            tkinter.messagebox.showinfo("你不准继续", "我猜有人想把自己的名字从名单里删掉。\n没想到吧，我做了校验。\n所以，你不准继续抽号，快把名单改回去（（（")
            raise Exception
    fontsize = 100

    def random() :
        global label, unchosenLis
        if not unchosenLis:
            logging.info('本轮循环已结束，即将开始新的循环。\n')
            tkinter.messagebox.showinfo("提示", "本轮循环已结束，即将开始新的循环。")
            unchosenLis = gotLis.copy()
        chosen: str = choice(unchosenLis)
        logging.info('抽到了 %s' % chosen)
        label.configure(text=chosen, font=('Sarasa Mono SC', fontsize))
        unchosenLis.remove(chosen)

    def setFont() :
        def setFontsize(close: bool) -> None:
            """
            更改抽中的号数的字体大小。
            :param close: 是否关闭 subWindow
            """
            global fontsize
            if entry.get().strip().isnumeric() and entry.get().strip(" 0") != "" :
                fontsize = int(entry.get())
                logging.debug("字体大小已成功设置为 %d. " % fontsize)
                # tkinter.messagebox.showinfo("提示", "字体大小已成功设置为 %d. " % fontsize)
                if close:
                    subWindow.destroy()
            else :
                logging.error('字体大小必须是正整数。')
                tkinter.messagebox.showerror("出错", "字体大小必须是正整数。")
        subWindow = tkinter.Tk()
        subWindow.geometry("300x100")
        subWindow.resizable(0,0)
        subWindow.title("输入一个字体大小(默认为100):")
        entry = tkinter.Entry(subWindow)
        entry.grid(row=0, column=0, columnspan=3)
        entry.insert(0, str(fontsize))
        ok = tkinter.Button(subWindow, text="确定", font=('Sarasa Mono SC', 12), command=lambda: setFontsize(True))
        cancel = tkinter.Button(subWindow, text="取消", font=('Sarasa Mono SC', 12), command=subWindow.destroy)
        apply = tkinter.Button(subWindow, text="应用", font=('Sarasa Mono SC', 12), command=lambda: setFontsize(False))
        ok.grid(row=1, column=0)
        cancel.grid(row=1, column=1)
        apply.grid(row=1, column=2)

    logging.debug("加载成功!列表中有%d个项。" % len(gotLis))
    tkinter.messagebox.showinfo("提示", "加载成功!列表中有%d个项。"%len(gotLis))
    setfont_button = tkinter.Button(mainWindow, text="设置字体大小", font=('Sarasa Mono SC', 12), command=setFont)
    setfont_button.pack()
    pickup_button = tkinter.Button(mainWindow, text="选取名字", font=('Sarasa Mono SC', 40), command=random)
    pickup_button.pack()
    label = tkinter.Label(mainWindow, text="", font=(None, fontsize))
    label.pack()
    mainWindow.mainloop()
