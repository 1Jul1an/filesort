# FileSort GUI – Sort your folder with one click

A lean desktop tool to organize files by category with a minimal, modern GUI.  
**Choose between a super-clean modern GUI (Python + Flet) or a no-dependency classic version (pure Tkinter).**

---

## Features

- Select target folder via a native dialog
- Sort files by category: Images, PDFs, Code, Archives, Docs, etc.
- Toggle categories on/off for flexible sorting
- Live progress bar and completion status
- Cross-platform: Windows, macOS, Linux
- Minimal dark-themed interface (Flet)
- Pure Python "just works" version (Tkinter)

---

## How to Run

### 1. Modern Flet Version

> Minimal dark GUI, smooth and clean

**Dependencies:**  
```bash
pip install flet
````

**Start:**

```bash
python modernfilesort.py
```

---

### 2. Classic Tkinter Version

> Requires no external dependencies.
> Works everywhere Python is installed.

**Start:**

```bash
python filesort.py
```

This version uses built-in Tkinter for the GUI, so you don't need to install anything extra.

---

## Customize Categories

* **both Versions:**
  Edit the `filetypes.json` file in the project directory.  
  If it doesn't exist, the app will create one on first start.  
  Changes are applied automatically at next launch.

---

**Enjoy streamlined file sorting – your way!**
