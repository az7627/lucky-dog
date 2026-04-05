# Lucky Dog

*forked from [GitHub Gist / cheny0y0 / random-pickup](https://gist.github.com/cheny0y0/27017ff4c86131e3f8df04b65d9752a3)*

语言: *简体中文 / [English (US)](./README_en_US.md)*

***

### 概述

这是一个随机抽号软件，可用于班级的一体机中，供老师随机抽号使用。新版支持**权重**（可调整中签概率）、**动画效果**、**字体/主题自定义**，并提供图形化的名单和配置管理界面。同时保留了**防篡改**特性（通过硬编码开关锁定名单/配置，编译后分发）。

### 使用方法

0. 配置 Python 环境，并安装所需依赖包。

> [!TIP]
> 
> Python 3.9.x 或更高版本已不再支持 Windows 7 操作系统，在 Windows 7 使用时，请安装 Python 3.8.x。
> 
> 可选的依赖包：
> - `colorlog`（彩色日志）
> - `sv_ttk`（Sun Valley 现代主题）
> 
> 安装命令：
> ```
> pip install colorlog sv_ttk
> ```
> 
> 若下载过慢（尤其对中国用户），可配置清华镜像源：
> ```
> pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
> ```
> 或临时使用：
> ```
> pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple colorlog sv_ttk
> ```

1. 准备名单。

使用 `names.json` 存储名单及权重，格式如下：
```json
[
    {"name": "张三", "weight": 1.0},
    {"name": "李四", "weight": 1.5},
    {"name": "王五", "weight": 2.0}
]
```
- `name`：学生姓名。
- `weight`：抽中权重，数值越大越容易被抽中。每次被抽中后，该学生的权重会自动**减半**（实现“降温”效果，避免同一人连续中签）。

> [!TIP]
> 
> 如果你有每行一个名字的 `names.txt`，可以使用附带工具 `convert_names.py` 一键转换：
> - 运行 `convert_names.py`
> - 选择 `.txt` 文件
> - 程序会自动统计重复次数转为权重并生成 `names.json`
> 
> 也可直接通过程序界面中的“选项 → 名单管理”进行添加/删除/修改。

2. 配置程序参数（可选）。

程序启动时会读取 `config.json`，默认内容如下：
```json
{
    "font_family": "更纱黑体 UI SC",
    "font_size": 100,
    "animation_enabled": true,
    "animation_steps": 10,
    "animation_interval": 30
}
```
- `font_family`：显示抽中姓名的字体（系统中需已安装）。
- `font_size`：字号。
- `animation_enabled`：是否开启动画（抽号时快速滚动姓名）。
- `animation_steps`：动画滚动步数。
- `animation_interval`：每步间隔（毫秒）。

可以在程序界面中点击 **选项...** 按钮，在“程序设置”选项卡中随时修改这些参数，修改后会自动保存。

3. 运行程序。

直接双击 `main.pyw`（或 `python main.pyw`）即可启动主窗口。点击 **选取名字** 按钮进行随机抽取，抽取结果会以大字体显示在中央。

> [!NOTE]
> 
> 为避免有学生因运气问题一直被抽中或一直不被抽中，每次抽取后，被抽中学生的权重会**减半**，并在 `names.json` 中保存。因此长时间使用后，所有学生的权重都会逐渐变小，但彼此间的比例关系保持不变（初始权重越大，依然相对更容易被抽中）。

4. （可选）防篡改部署。

若要在班级电脑上防止学生修改名单或程序配置，可以通过硬编码开关锁定编辑功能，然后编译为 `.pyc` 文件分发。

- 打开 `main.pyw`，找到文件开头的两行：
  ```python
  LOCK_NAMES = False   # True: 名单配置在 GUI 中不可编辑；False: 可编辑
  LOCK_CONFIG = False  # True: 程序设置在 GUI 中不可编辑；False: 可编辑
  ```
- 将需要锁定的开关改为 `True`（例如 `LOCK_NAMES = True` 和 `LOCK_CONFIG = True`）。
- 保存文件，然后编译：
  ```
  python -m py_compile main.pyw
  ```
  编译后会生成 `__pycache__\main.cpython-XX.pyc` 文件（XX 为 Python 版本号）。
- 将 `.pyc` 文件复制到班级电脑，运行即可（仍需 Python 环境和已安装的依赖包）。

> [!TIP]
> 
> 锁定后，程序界面的“名单管理”和“程序设置”选项卡中的编辑控件将变为禁用状态，学生无法通过图形界面修改名单或配置。但直接编辑 `names.json` 或 `config.json` 仍可绕过锁定——若要更进一步地防篡改，建议将这两个文件也设置为只读和隐藏，或使用权限控制。

### 常见问题排查

| 错误信息 / 错误现象 | 解决方案 |
| - | - |
| `names.json` 文件未找到 | 请确保 `names.json` 位于程序同级目录下。若没有，请参考步骤1创建该文件。 |
| `config.json` 文件未找到 | 程序会自动使用默认配置并生成该文件，一般不会报错。若遇到权限问题，请以管理员身份运行一次。 |
| 没有权限读取/写入 JSON 文件 | 检查文件权限，或使用管理员权限运行程序。 |
| 程序启动后字体显示异常（方块） | 表示当前系统缺少配置的字体（如“更纱黑体 UI SC”）。请通过“选项 → 程序设置”选择一个系统中已安装的字体，或手动修改 `config.json` 中的 `font_family`。 |

若上述表格未能解决你的问题，或无法理解以上内容，请提交 Issue。