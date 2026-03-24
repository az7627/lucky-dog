# coding=UTF-8

import tkinter as tk
from tkinter import ttk, messagebox, font
import json
from fractions import Fraction
from random import choices, choice
import logging
import colorlog
from os import name as os_name, getcwd

# 尝试导入 Sun Valley 主题
try:
    import sv_ttk
    SV_TTK_AVAILABLE = True
except ImportError:
    SV_TTK_AVAILABLE = True
    logging.warning("未安装 sv-ttk 主题库，将使用默认主题。可通过 'pip install sv-ttk' 安装以获得现代化外观。")

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

# 默认配置
DEFAULT_CONFIG = {
    "font_family": "Sarasa Mono SC",
    "font_size": 100,
    "animation_enabled": True,
    "animation_steps": 10,
    "animation_interval": 50
}

# ========== 防篡改开关（硬编码） ==========
LOCK_NAMES = True   # True: 名单配置在 GUI 中不可编辑；False: 可编辑
LOCK_CONFIG = False  # True: 程序设置在 GUI 中不可编辑；False: 可编辑
# ========================================

CONFIG_FILE = getcwd() + ("/", "\\")[os_name == "nt"] + "config.json"
NAMES_FILE = getcwd() + ("/", "\\")[os_name == "nt"] + "names.json"

# 加载配置（用于全局变量）
def load_config():
    config = DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            config.update(loaded)
    except FileNotFoundError:
        logging.info("未找到 config.json，将使用默认配置。")
    except Exception as e:
        logging.error(f"读取 config.json 失败: {e}")
    return config

# 加载名单（从文件，返回原始权重）
def load_names_from_file():
    students = []
    try:
        with open(NAMES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for item in data:
            name = item.get("name")
            if not name:
                continue
            weight = item.get("weight", 1)
            try:
                weight_frac = Fraction(str(weight))
            except:
                weight_frac = Fraction(1)
            students.append({"name": name, "weight": weight_frac})
        if not students:
            raise ValueError("名单为空")
    except FileNotFoundError:
        logging.error(f"未找到 {NAMES_FILE}，请创建该文件。")
        messagebox.showerror("错误", f"未找到 {NAMES_FILE}，程序将退出。")
        exit(1)
    except Exception as e:
        logging.error(f"加载名单失败: {e}")
        messagebox.showerror("错误", f"加载名单失败: {e}")
        exit(1)
    return students

# 初始化全局变量
config = load_config()
students = load_names_from_file()

# 主窗口
mainWindow = tk.Tk()
mainWindow.title("Random-pickup")
mainWindow.geometry("550x350")

# 应用 Sun Valley 主题
if SV_TTK_AVAILABLE:
    sv_ttk.set_theme("light")  # 可选 "dark"
    logging.info("已应用 Sun Valley 主题。")
else:
    logging.info("使用默认 ttk 主题。")

# 全局变量
font_family = config["font_family"]
fontsize = config["font_size"]
animation_enabled = config["animation_enabled"]
animation_steps = config["animation_steps"]
animation_interval = config["animation_interval"]

def save_config_to_file(cfg):
    """保存配置到 config.json"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, ensure_ascii=False, indent=4)
        logging.info("配置已保存。")
    except Exception as e:
        logging.error(f"保存配置失败: {e}")
        messagebox.showerror("错误", f"保存配置失败: {e}")

def save_names_to_file(names_list):
    """将原始名单（未减半）保存到 names.json"""
    try:
        data = [{"name": s["name"], "weight": float(s["weight"])} for s in names_list]
        with open(NAMES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info("名单已保存。")
    except Exception as e:
        logging.error(f"保存名单失败: {e}")
        messagebox.showerror("错误", f"保存名单失败: {e}")

def random_pick_with_animation():
    """带动画的随机抽取（根据配置决定是否播放动画）"""
    if not students:
        return

    # 禁用按钮
    pickup_button.config(state=tk.DISABLED)

    # 提前确定结果
    chosen = choices(students, weights=[s['weight'] for s in students], k=1)[0]
    final_name = chosen['name']

    if not animation_enabled:
        # 无动画：直接显示结果
        label.config(text=final_name, fg="black")
        chosen['weight'] *= Fraction(1, 2)
        logging.info(f'抽到了 {final_name}，权重减半为 {chosen["weight"]}')
        pickup_button.config(state=tk.NORMAL)
        return

    # 动画参数
    steps = animation_steps
    interval = animation_interval
    names_list = [s['name'] for s in students]
    step_count = 0

    def animate():
        nonlocal step_count
        if not mainWindow.winfo_exists():
            return
        if step_count < steps:
            random_name = choice(names_list)
            label.config(text=random_name, fg="gray")
            step_count += 1
            mainWindow.after(interval, animate)
        else:
            label.config(text=final_name, fg="black")
            chosen['weight'] *= Fraction(1, 2)
            logging.info(f'抽到了 {final_name}，权重减半为 {chosen["weight"]}')
            pickup_button.config(state=tk.NORMAL)

    animate()

def open_options():
    """打开配置窗口（从文件重新读取数据）"""
    # 重新从文件读取原始配置和原始名单
    current_config = load_config()  # 从文件读取最新配置
    original_names = load_names_from_file()  # 从文件读取原始名单（未减半）

    opt = tk.Toplevel(mainWindow)
    opt.title("选项")
    opt.geometry("700x500")
    opt.resizable(True, True)

    # 使用 Notebook 创建选项卡
    notebook = ttk.Notebook(opt)
    notebook.pack(fill='both', expand=True, padx=5, pady=5)

    # ----- 选项卡1：名单管理 -----
    frame_list = ttk.Frame(notebook)
    notebook.add(frame_list, text="名单管理")

    # 如果名单被锁定，在顶部添加浅红色横幅
    if LOCK_NAMES:
        lock_label = tk.Label(frame_list, text="🔒 名单配置文件已被锁定", 
                            bg="#FFCCCC", fg="#8B0000",  # 浅红背景，深红文字
                            font=('', 10, 'bold'), relief='ridge', padx=5, pady=3)
        lock_label.pack(fill=tk.X, pady=(0, 5))
    
    # 左右分割：左侧Treeview，右侧编辑面板
    paned = ttk.PanedWindow(frame_list, orient=tk.HORIZONTAL)
    paned.pack(fill=tk.BOTH, expand=True)

    # 左侧框架（只放 Treeview，按钮移到整体底部）
    left_frame = ttk.Frame(paned)
    paned.add(left_frame, weight=3)

    # Treeview
    columns = ('name', 'weight')
    tree = ttk.Treeview(left_frame, columns=columns, show='headings', selectmode='browse')
    tree.heading('name', text='姓名')
    tree.heading('weight', text='权重（原始）')
    tree.column('name', width=150)
    tree.column('weight', width=80)

    scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 填充原始数据
    for s in original_names:
        tree.insert('', tk.END, values=(s['name'], float(s['weight'])))

    # 右侧编辑面板
    right_frame = ttk.Frame(paned, width=200, relief=tk.SUNKEN, borderwidth=2)
    paned.add(right_frame, weight=1)

    # 编辑标签和输入框
    ttk.Label(right_frame, text="编辑选中项", font=('', 12, 'bold')).pack(pady=10)

    ttk.Label(right_frame, text="姓名:").pack(anchor=tk.W, padx=5)
    name_var = tk.StringVar()
    name_entry = ttk.Entry(right_frame, textvariable=name_var, width=20)
    name_entry.pack(padx=5, pady=2, fill=tk.X)

    ttk.Label(right_frame, text="权重:").pack(anchor=tk.W, padx=5)
    weight_var = tk.StringVar()
    weight_entry = ttk.Entry(right_frame, textvariable=weight_var, width=20)
    weight_entry.pack(padx=5, pady=2, fill=tk.X)

    def update_selected():
        """将编辑框的值更新到当前选中的行（无弹窗）"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("错误", "请先选择要编辑的行")
            return
        name = name_var.get().strip()
        if not name:
            messagebox.showerror("错误", "姓名不能为空")
            return
        try:
            weight = float(weight_var.get())
            if weight <= 0:
                raise ValueError
        except:
            messagebox.showerror("错误", "权重必须为正数")
            return

        # 更新原始列表中的对应项
        item = tree.item(selected[0])
        old_name = item['values'][0]
        for s in original_names:
            if s['name'] == old_name:
                s['name'] = name
                s['weight'] = Fraction(str(weight))
                break
        # 更新Treeview显示
        tree.item(selected[0], values=(name, weight))
        # 不弹出成功提示

    update_button = ttk.Button(right_frame, text="更新", command=update_selected)
    update_button.pack(pady=10)

    # 当选中Treeview行时，自动填充编辑框
    def on_tree_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            name, weight = item['values']
            name_var.set(name)
            weight_var.set(str(weight))
        else:
            name_var.set("")
            weight_var.set("")

    tree.bind('<<TreeviewSelect>>', on_tree_select)

    # ----- 选项卡2：程序设置 -----
    frame_settings = ttk.Frame(notebook)
    notebook.add(frame_settings, text="程序设置")

    # 如果设置被锁定，在顶部添加浅红色横幅
    if LOCK_CONFIG:
        lock_label = tk.Label(frame_list, text="🔒 配置文件已被锁定", 
                            bg="#FFCCCC", fg="#8B0000",  # 浅红背景，深红文字
                            font=('', 10, 'bold'), relief='ridge', padx=5, pady=3)
        lock_label.pack(fill=tk.X, pady=(0, 5))

    # 字体选择
    ttk.Label(frame_settings, text="字体:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    fonts = list(font.families())
    font_var = tk.StringVar(value=current_config["font_family"])
    font_combo = ttk.Combobox(frame_settings, textvariable=font_var, values=fonts, state='normal')
    font_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    # 字体大小
    ttk.Label(frame_settings, text="字体大小:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    size_var = tk.IntVar(value=current_config["font_size"])
    size_spin = ttk.Spinbox(frame_settings, from_=10, to=300, textvariable=size_var, width=10)
    size_spin.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    # 动画开关
    anim_var = tk.BooleanVar(value=current_config["animation_enabled"])
    anim_check = ttk.Checkbutton(frame_settings, text="开启动画", variable=anim_var)
    anim_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

    # 动画步数
    ttk.Label(frame_settings, text="动画步数:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
    steps_var = tk.IntVar(value=current_config["animation_steps"])
    steps_spin = ttk.Spinbox(frame_settings, from_=1, to=50, textvariable=steps_var, width=10)
    steps_spin.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)

    # 动画间隔(ms)
    ttk.Label(frame_settings, text="动画间隔(ms):").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
    interval_var = tk.IntVar(value=current_config["animation_interval"])
    interval_spin = ttk.Spinbox(frame_settings, from_=10, to=500, textvariable=interval_var, width=10)
    interval_spin.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)

    # 如果设置被锁定，禁用所有控件
    if LOCK_CONFIG:
        for widget in (font_combo, size_spin, anim_check, steps_spin, interval_spin):
            widget.config(state='disabled')

    # ---------- 底部全局按钮区域 ----------
    bottom_frame = ttk.Frame(opt)
    bottom_frame.pack(fill=tk.X, pady=10, padx=5)

    # 左侧按钮（添加、删除）
    left_buttons = ttk.Frame(bottom_frame)
    left_buttons.pack(side=tk.LEFT)

    def add_student():
        """添加学生（弹窗，无成功提示）"""
        add_win = tk.Toplevel(opt)
        add_win.title("添加学生")
        add_win.geometry("420x70")
        add_win.resizable(False, False)

        # 一行布局
        frame = ttk.Frame(add_win)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="姓名:").grid(row=0, column=0, padx=5)
        name_entry = ttk.Entry(frame, width=15)
        name_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="权重:").grid(row=0, column=2, padx=5)
        weight_entry = ttk.Entry(frame, width=8)
        weight_entry.insert(0, "1")
        weight_entry.grid(row=0, column=3, padx=5)

        def do_add():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("错误", "姓名不能为空")
                return
            try:
                weight = float(weight_entry.get())
                if weight <= 0:
                    raise ValueError
            except:
                messagebox.showerror("错误", "权重必须为正数")
                return
            # 添加到原始列表和 tree
            original_names.append({"name": name, "weight": Fraction(str(weight))})
            tree.insert('', tk.END, values=(name, weight))
            add_win.destroy()
            # 不弹出成功提示

        ttk.Button(frame, text="确定", command=do_add).grid(row=0, column=4, padx=10)

        name_entry.focus_set()
        add_win.bind('<Return>', lambda e: do_add())

    def delete_student():
        """删除选中学生（无成功提示）"""
        selected = tree.selection()
        if not selected:
            messagebox.showerror("错误", "请先选择要删除的行")
            return
        if messagebox.askyesno("确认", "确定要删除选中项吗？"):
            item = tree.item(selected[0])
            name = item['values'][0]
            # 从原始列表中移除
            for i, s in enumerate(original_names):
                if s['name'] == name:
                    del original_names[i]
                    break
            tree.delete(selected[0])
            # 清空编辑框
            name_var.set("")
            weight_var.set("")
            # 不弹出成功提示

    add_btn = ttk.Button(left_buttons, text="添加", command=add_student)
    add_btn.pack(side=tk.LEFT, padx=5)
    del_btn = ttk.Button(left_buttons, text="删除", command=delete_student)
    del_btn.pack(side=tk.LEFT, padx=5)

    # 如果名单被锁定，禁用添加/删除按钮、右侧编辑框及更新按钮
    if LOCK_NAMES:
        tree.config(selectmode='none')          # 禁止选择
        name_entry.config(state='disabled')
        weight_entry.config(state='disabled')
        update_button.config(state='disabled')
        add_btn.config(state='disabled')
        del_btn.config(state='disabled')

    # 右侧按钮（确定、取消、应用）
    right_buttons = ttk.Frame(bottom_frame)
    right_buttons.pack(side=tk.RIGHT)

    def apply_changes():
        """应用更改：保存到文件，并立即更新内存中的全局变量和学生列表"""
        nonlocal current_config

        # 更新配置字典（仅当设置未被锁定时才从控件读取）
        new_config = {
            "font_family": font_var.get() if not LOCK_CONFIG else current_config["font_family"],
            "font_size": size_var.get() if not LOCK_CONFIG else current_config["font_size"],
            "animation_enabled": anim_var.get() if not LOCK_CONFIG else current_config["animation_enabled"],
            "animation_steps": steps_var.get() if not LOCK_CONFIG else current_config["animation_steps"],
            "animation_interval": interval_var.get() if not LOCK_CONFIG else current_config["animation_interval"]
        }

        # 保存配置到文件（如果未锁定则保存，否则跳过）
        if not LOCK_CONFIG:
            save_config_to_file(new_config)
        else:
            logging.info("配置已锁定，忽略保存操作。")

        # 保存原始名单到文件（如果未锁定则保存，否则跳过）
        if not LOCK_NAMES:
            save_names_to_file(original_names)
        else:
            logging.info("名单已锁定，忽略保存操作。")

        # 重新加载内存中的全局变量和学生列表（从文件）
        global config, students, font_family, fontsize, animation_enabled, animation_steps, animation_interval
        config = load_config()
        students = load_names_from_file()
        font_family = config["font_family"]
        fontsize = config["font_size"]
        animation_enabled = config["animation_enabled"]
        animation_steps = config["animation_steps"]
        animation_interval = config["animation_interval"]

        # 更新主窗口标签字体
        try:
            label.config(font=(font_family, fontsize))
        except:
            label.config(font=(None, fontsize))

        current_config = new_config
        # 不弹出成功提示（已删除）

    def ok_and_close():
        apply_changes()
        opt.destroy()

    # 右侧按钮顺序：确定、取消、应用（从左到右）
    ttk.Button(right_buttons, text="确定", command=ok_and_close).pack(side=tk.LEFT, padx=5)
    ttk.Button(right_buttons, text="取消", command=opt.destroy).pack(side=tk.LEFT, padx=5)
    ttk.Button(right_buttons, text="应用", command=apply_changes).pack(side=tk.LEFT, padx=5)

# 主界面布局
options_button = ttk.Button(mainWindow, text="选项...", command=open_options)
options_button.pack(anchor=tk.NE, padx=10, pady=5)

# 选取名字按钮：使用 Sun Valley 蓝色主题按钮，并增大尺寸
if SV_TTK_AVAILABLE:
    ttk.Style().configure('Accent.TButton', font=('Arial', '40'))
    pickup_button = ttk.Button(mainWindow, text="选取名字", command=random_pick_with_animation,
                               style='Accent.TButton', padding=(20, 10))
else:
    pickup_button = ttk.Button(mainWindow, text="选取名字", command=random_pick_with_animation,
                               padding=(20, 10))
pickup_button.pack(pady=20)

label = tk.Label(mainWindow, text="", font=(font_family, fontsize))
label.pack()

mainWindow.mainloop()