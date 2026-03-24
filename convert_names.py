import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import os

def convert_txt_to_json():
    """选择 txt 文件，转换为 json 名单文件"""
    # 选择 txt 文件
    txt_file = filedialog.askopenfilename(
        title="选择名单文件 (.txt)",
        filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
    )
    if not txt_file:
        return

    try:
        # 读取 txt 文件，统计姓名出现次数
        name_counts = {}
        with open(txt_file, 'r', encoding='utf-8') as f:
            for line in f:
                name = line.strip()
                if name:  # 跳过空行
                    name_counts[name] = name_counts.get(name, 0) + 1

        if not name_counts:
            messagebox.showerror("错误", "文件中没有有效姓名（空文件或全为空行）")
            return

        # 构建 JSON 数据
        json_data = []
        for name, count in name_counts.items():
            json_data.append({"name": name, "weight": float(count)})

        # 选择保存路径（默认同目录同名 .json）
        default_json = os.path.splitext(txt_file)[0] + ".json"
        json_file = filedialog.asksaveasfilename(
            title="保存 JSON 文件",
            defaultextension=".json",
            filetypes=[("JSON 文件", "*.json")],
            initialfile=os.path.basename(default_json)
        )
        if not json_file:
            return

        # 写入 JSON 文件
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("成功", f"转换完成！\n共 {len(json_data)} 人。\n保存至：{json_file}")

    except Exception as e:
        messagebox.showerror("错误", f"转换失败：{e}")

# 创建主窗口
root = tk.Tk()
root.title("名单转换工具（txt → json）")
root.geometry("500x300")
root.resizable(False, False)

# 设置大号字体（适合大屏幕）
font_style = ("微软雅黑", 16)

# 说明标签
label = tk.Label(root, text="将 TXT 名单文件转换为 JSON 名单文件\n（每行一个姓名，重复次数自动转为权重）",
                 font=("微软雅黑", 12), justify="left")
label.pack(pady=30)

# 转换按钮（大尺寸）
btn = tk.Button(root, text="选择 TXT 文件并转换", command=convert_txt_to_json,
                font=font_style, bg="#4CAF50", fg="white", padx=20, pady=10)
btn.pack(pady=20)

# 状态提示（可选）
status = tk.Label(root, text="", font=("微软雅黑", 10), fg="gray")
status.pack(pady=10)

# 进入主循环
root.mainloop()