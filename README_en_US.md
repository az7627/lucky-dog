# Lucky Dog

*forked from [GitHub Gist / cheny0y0 / random-pickup](https://gist.github.com/cheny0y0/27017ff4c86131e3f8df04b65d9752a3)*

Language: *[简体中文](./README.md) / English (US)*

***

### Overview

This is a random name picker software designed for classroom all-in-one PCs, allowing teachers to randomly select students. The new version supports **weights** (adjustable probability), **animation effects**, **font/theme customization**, and provides a graphical interface for name list and configuration management. It also retains **tamper-proof** features (locking lists/configurations via hard-coded switches, then compiling for distribution).

### How to Use

0. Set up the Python environment and install required dependencies.

> [!TIP]
> 
> Python 3.9.x or higher no longer supports Windows 7. On Windows 7, please install Python 3.8.x.
> 
> Optional dependencies:
> - `colorlog` (colored logging)
> - `sv_ttk` (Sun Valley modern theme)
> 
> Installation command:
> ```
> pip install colorlog sv_ttk
> ```
> 
> If download is too slow (especially for users in China), you can configure the Tsinghua mirror:
> ```
> pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
> ```
> Or use temporarily:
> ```
> pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple colorlog sv_ttk
> ```

1. Prepare the name list.

Use `names.json` to store names and weights in the following format:
```json
[
    {"name": "Zhang San", "weight": 1.0},
    {"name": "Li Si", "weight": 1.5},
    {"name": "Wang Wu", "weight": 2.0}
]
```
- `name`: Student name.
- `weight`: Selection weight. Higher values increase the chance of being picked. Each time a student is selected, their weight is automatically **halved** (a "cool-down" effect to prevent the same person from being picked repeatedly).

> [!TIP]
> 
> If you have a `names.txt` file with one name per line, you can use the included tool `convert_names.py` for one-click conversion:
> - Run `convert_names.py`
> - Select the `.txt` file
> - The program will automatically count duplicates, convert them to weights, and generate `names.json`
> 
> Alternatively, you can add/delete/modify entries directly through the "Options → Name List Management" interface.

2. Configure program parameters (optional).

The program reads `config.json` on startup. Default content:
```json
{
    "font_family": "Sarasa UI SC",
    "font_size": 100,
    "animation_enabled": true,
    "animation_steps": 10,
    "animation_interval": 30
}
```
- `font_family`: Font used to display the selected name (must be installed on the system).
- `font_size`: Font size.
- `animation_enabled`: Whether to enable animation (fast scrolling of names during selection).
- `animation_steps`: Number of animation scroll steps.
- `animation_interval`: Interval between steps (milliseconds).

You can modify these parameters at any time by clicking the **Options...** button in the program interface, then the "Program Settings" tab. Changes are saved automatically.

3. Run the program.

Double-click `main.pyw` (or run `python main.pyw`) to launch the main window. Click the **Pick Name** button to perform a random selection. The result will be displayed in large font in the center.

> [!NOTE]
> 
> To avoid certain students being selected too often or never due to luck, each time a student is picked, their weight is **halved** and saved to `names.json`. Over long-term use, all students' weights will gradually decrease, but the relative ratios remain the same (students with higher initial weights will still be more likely to be selected).

4. (Optional) Tamper-proof deployment.

If you want to prevent students from modifying the name list or program configuration on the classroom computer, you can lock editing via hard-coded switches and then distribute the compiled `.pyc` file.

- Open `main.pyw` and locate the two lines at the beginning:
  ```python
  LOCK_NAMES = False   # True: name list cannot be edited in GUI; False: editable
  LOCK_CONFIG = False  # True: program settings cannot be edited in GUI; False: editable
  ```
- Change the switches you want to lock to `True` (e.g., `LOCK_NAMES = True` and `LOCK_CONFIG = True`).
- Save the file, then compile:
  ```
  python -m py_compile main.pyw
  ```
  After compilation, a `__pycache__\main.cpython-XX.pyc` file will be generated (XX is the Python version number).
- Copy the `.pyc` file to the classroom computer and run it (Python environment and installed dependencies are still required).

> [!TIP]
> 
> After locking, the editing controls in the "Name List Management" and "Program Settings" tabs will be disabled, preventing students from modifying the name list or configuration through the graphical interface. However, directly editing `names.json` or `config.json` can still bypass the lock – for stronger tamper resistance, consider setting these two files to read-only and hidden, or using permission controls.

### Troubleshooting

| Error Message / Symptom | Solution |
| - | - |
| `names.json` file not found | Ensure `names.json` is in the same directory as the program. If not, follow step 1 to create the file. |
| `config.json` file not found | The program will automatically use default configuration and generate the file. Usually no error. If permission issues occur, try running as administrator once. |
| No permission to read/write JSON files | Check file permissions, or run the program with administrator privileges. |
| Font displays as boxes after startup | The system lacks the configured font (e.g., "Sarasa UI SC"). Change to an installed font via "Options → Program Settings", or manually modify `font_family` in `config.json`. |

If the above table does not solve your problem, or you cannot understand the content, please submit an Issue.