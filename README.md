# Lucky Dog
*forked from [GitHub Gist / cheny0y0 / random-pickup](https://gist.github.com/cheny0y0/27017ff4c86131e3f8df04b65d9752a3)*

语言: *简体中文 / [English (US)](./README_en_US.md)*

***

### 概述

这是一个随机抽号软件，可用于班级的一体机中，供老师随机抽号使用。可直接显示名字，而非号数，同时具有防篡改的特点。

### 使用方法

0. 配置 Python 环境，并安装 `colorlog` 包。

> [!TIP]
> 
> Python 3.9.x 或更高版本已不再支持 Windows 7 操作系统，在 Windows 7 使用时，请安装 Python 3.8.x.
> 
> 要安装 `colorlog` 包，请在配置 Python 环境后使用以下命令
> 
> ```
> pip install colorlog
> ```
> 
> 若使用以上命令下载过慢，可配置镜像源，然后再安装软件包。
> 
> ```
> pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
> ```
> 
> 或者，若只是临时使用，可直接使用下面这条命令。
> 
> ```
> pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple colorlog
> ```
> 

1. 使用自己班级的名单替换掉 `names.txt`，每个名字一行。

> [!TIP]
> 
> 如果你没有 `.txt` 格式的名单，但有 `.xlsx`, `.xls` 等格式的电子表格，其中每行一个名字，可使用 Excel 打开表格，选中所有名字，复制，然后粘贴到 `names.txt` 中，就自动变为了每个名字一行的文本文档。

2. 运行 `get_name_list_hash.py`，根据提示获取名单的哈希值并替换掉 `gui-zh.py` 中的 `TOGGLE_NAME_LIST_HASH` 常量。运行该脚本后，输出大致如下所示。其中 `[Y/n]` 代表要求你输入 `Y`（不区分大小写）表示同意，或输入 `N`（不区分大小写）表示拒绝。如果不输入任何内容则等同于输入默认值 `Y`。同理可得，`[y/N]` 表示不输入则默认为 `N`

```
计算出的哈希值: 1017e1cc7f415846e2a764733e2c7bcfdfa2f5e2074b82e951a80ea15959c541
同时更改 gui-zh.py 中的哈希值? [Y/n] 
成功更新 gui-zh.py 中的哈希值。
是否编译 gui-zh.py? [Y/n]      
编译成功，生成 gui-zh.pyc
是否删除源文件 gui-zh.py? [y/N]
```

> [!NOTE]
> 
> |输入|[Y/n]|[y/N]|
> |-|-|-|
> |Y|同意|同意|
> ||同意|拒绝|
> |N|拒绝|拒绝|

> [!TIP]
> 
> 若以上脚本**无法**正常运行，可尝试手动获取并替换哈希值。
> 
> 在 Python 终端执行以下命令。
> 
> ```python
> import hashlib
> with open('./names.txt', "rb") as lis:
>         print(hashlib.sha256(lis.read()).hexdigest())
> ```
> 
> 输出示例：
> ```
> 1017e1cc7f415846e2a764733e2c7bcfdfa2f5e2074b82e951a80ea15959c541
> ```
> 
> 手动使用以上内容替换 `gui-zh.py` 第 12 行中常量 `TOGGLE_NAME_LIST_HASH` 的内容。
> 
> 再在终端键入
> 
> ```
> python -m py_compile 

3. 若在班级使用时，建议不要将源代码 `gui-zh.py` 放进班级电脑（防同学篡改名单），而只留下 `gui-zh.pyc`。在班级中使用时运行编译后的 `gui-zh.pyc` 即可。

> [!TIP]
> 
> 运行 `.pyc` 仍需要 Python 环境，仍需要安装相应的依赖（`colorlog`）。需注意，生产环境（班级电脑）的 Python 版本需要和在开发环境编译时所用的版本一致。

### 错误排查

|错误信息 / 错误现象|解决方案|
|-|-|
|names.txt 文件未找到|请检查 `names.txt` 是否位于其他目录下，或已被删除。请将其移动到与 `gui-zh.py` 同级的目录下，或新建一个名为 `names.txt` 的文件。|
|没有权限读取 names.txt 文件|请编辑 `names.txt` 的文件权限。如果你看不懂这句话，请直接使用管理员权限运行本程序。|
|错误: gui-zh.py 文件未找到|请检查 `gui-zh.py` 是否位于其他目录下，或已被删除。请将其移动到与 `get_name_list_hash.py` 同级的目录下。若找不到该文件，请从 GitHub 页面重新下载一个。|
|没有权限写入 gui-zh.py 文件|请编辑 `gui-zh.py` 的文件权限。如果你看不懂这句话，请直接使用管理员权限运行本程序。|
|没有权限写入编译文件|请编辑 `get_name_list_hash` 所在目录的目录权限。如果你看不懂这句话，请直接使用管理员权限运行本程序。|
|没有权限删除 gui-zh.py 文件|请编辑 `gui-zh.py` 的文件权限。如果你看不懂这句话，请直接使用管理员权限运行本程序。|
|你不准继续 / 我猜有人想把自己的名字从名单里删掉...|请确认 `gui-zh.py` 中常量 `TOGGLE_NAME_LIST_HASH` 哈希值是否与 `names.txt` 文件的 SHA-256 值一致。若不一致，请更正 `names.txt` 或 `gui-zh.py` 中 `TOGGLE_NAME_LIST_HASH` 的值。若你正在使用 `gui-zh.pyc` 且确认是 `TOGGLE_NAME_LIST_HASH` 的值错误，而非 `names.txt` 被他人篡改，还需重新编译才可继续使用。可使用 `get_name_list_hash.py` 自动快速修改。|
|*(错误现象)* 程序正常启动，但点击“选取名字”或“更改具体大小”均无反应，随后操作系统提示程序未响应|可能因为在随程序出现的终端中选中了部分内容。因屎山 `conhost.exe` 的傻逼设计，在 conhost 中选中内容会导致终端暂停，进而导致程序暂停，随后操作系统抛出“无响应”。你需要在随程序出现的终端中按下 `ESC` 取消选择，或者单击右键（在触屏设备上可以长按），复制你所选中的内容同时取消选择。如果你想要一劳永逸地避免这种情况，可使用 Windows Terminal 代替 conhost. 对于 Windows 10 及以上操作系统的用户你需要在 Microsoft Store 下载 Windows Terminal，然后在 Windows 设置的“开发者选项”（找不到的可以搜索）中将默认终端从“Windows 控制台主机”改为“Windows Terminal”. 若确实没有该设置选项的，请更新你的操作系统版本。|

若你在上述表格中未找到你遇到的问题，或无法理解以上内容，或按照以上方法操作后仍无法解决问题的，请向我们提交 Issue.