# Lucky Dog

*forked from [GitHub Gist / cheny0y0 / random-pickup](https://gist.github.com/cheny0y0/27017ff4c86131e3f8df04b65d9752a3)*

Language: *Simplified Chinese / [English (US)](./README_en_US.md)*

*Translation may not be 100% accurate.*

***

### Overview  
This is a random name picker software designed for classroom all-in-one PCs, allowing teachers to randomly select students. It displays actual names instead of numbers and features tamper-proof functionality.

### Usage Instructions  

0. Set up a Python environment and install the `colorlog` package.  

> [!TIP]  
> Python 3.9.x and later no longer support Windows 7. For Windows 7 systems, install Python 3.8.x.  
> To install the `colorlog` package, use:  
> ```
> pip install colorlog
> ```  
> If downloads are slow:  
> 
> • For users in China:  
>   ```
>   pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
>   ```  
>   Or for one-time use:  
>   ```
>   pip install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple colorlog
>   ```

1. Replace `names.txt` with your class roster, with one name per line.  

> [!TIP]  
> If you have a spreadsheet (.xlsx, .xls, etc.) with one name per row:  
> - Open it in Excel, select all names, copy them, and paste into `names.txt`—it will automatically format to one name per line.  

2. Run `get_name_list_hash.py`. Follow prompts to get the roster’s hash value and replace the `TOGGLE_NAME_LIST_HASH` constant in `gui-zh.py`. The script’s output resembles:  

   ```
   Calculated hash: 1017e1cc7f415846e2a764733e2c7bcfdfa2f5e2074b82e951a80ea15959c541  
   Update hash in gui-zh.py? [Y/n]  
   Successfully updated hash in gui-zh.py.  
   Compile gui-zh.py? [Y/n]      
   Compilation successful. Generated gui-zh.pyc.  
   Delete source file gui-zh.py? [y/N]  
   ```  

> [!NOTE]  
> |Input|[Y/n]|[y/N]|  
> |-|-|-|  
> |Y|Yes|Yes|  
> ||Yes|No|  
> |N|No|No|  

> [!TIP]  
> **If the script fails**, manually generate and replace the hash:  
> In Python terminal, run:  
> ```python  
> import hashlib  
> with open('./names.txt', "rb") as lis:  
>     print(hashlib.sha256(lis.read()).hexdigest())  
> ```  
> Output example:  
> ```  
> 1017e1cc7f415846e2a764733e2c7bcfdfa2f5e2074b82e951a80ea15959c541  
> ```  
> Manually replace `TOGGLE_NAME_LIST_HASH` in `gui-zh.py` (line 12) with this value.  
> Then compile:  
> ```  
> python -m py_compile gui-zh.py  
> ```  

3. For classroom use, **do not** leave the source `gui-zh.py` on the classroom PC (prevents tampering). Only keep `gui-zh.pyc`. Run the compiled `gui-zh.pyc` file.  

> [!TIP]  
> Running `.pyc` requires Python and `colorlog`. Ensure the classroom PC’s Python version **matches the compilation environment’s version**.  

### Troubleshooting  

| Error Message / Symptom | Solution |  
|-|-|  
| `names.txt` not found | Check if `names.txt` is misplaced/deleted. Move it to the same directory as `gui-zh.py` or create a new `names.txt`. |  
| No permission to read `names.txt` | Adjust file permissions or run as administrator. |  
| `gui-zh.py` not found | Ensure `gui-zh.py` is in the same directory as `get_name_list_hash.py`. Redownload if missing. |  
| No permission to write `gui-zh.py` | Adjust permissions or run as administrator. |  
| No permission to write compiled file | Adjust directory permissions or run as administrator. |  
| No permission to delete `gui-zh.py` | Adjust permissions or run as administrator. |  
| "Access denied" / "Someone tried to remove their name..." | Verify `TOGGLE_NAME_LIST_HASH` in `gui-zh.py` matches the SHA-256 of `names.txt`. If mismatched, correct the hash or roster. If using `gui-zh.pyc`, recompile after fixing. |  
| Program freezes after clicking "Pick Name" or "Adjust Size" | Likely caused by text selection in the terminal window. Press <kbd>Esc</kbd> or right-click to deselect. For a permanent fix: <br> • **Windows 10/11**: Install Windows Terminal from Microsoft Store, then set it as default in *Settings > Privacy & security > For developers*. |  

If your issue isn’t listed or remains unresolved, submit an Issue.  