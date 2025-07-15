import os
import shutil
import json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

EXTENSION_FILE = "filetypes.json"

DEFAULT_EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "PDFs": [".pdf"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Office": [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp"],
    "Docs": [".txt", ".md", ".csv"],
    "Executables": [".exe", ".msi", ".bat"]
}

class FileSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🗂️ FileSort – Clean Your Folder")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        self.folder_path = tk.StringVar()

        self.load_extensions()
        self.setup_ui()

    def load_extensions(self):
        if os.path.exists(EXTENSION_FILE):
            with open(EXTENSION_FILE, "r") as f:
                self.extensions = json.load(f)
        else:
            self.extensions = DEFAULT_EXTENSIONS
            with open(EXTENSION_FILE, "w") as f:
                json.dump(self.extensions, f, indent=2)

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Select a folder to sort:").pack(pady=(0, 5))

        path_frame = ttk.Frame(frame)
        path_frame.pack(fill=tk.X, pady=2)

        path_entry = ttk.Entry(path_frame, textvariable=self.folder_path, width=50)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(path_frame, text="Browse", command=self.browse_folder).pack(side=tk.LEFT, padx=5)

        ttk.Label(frame, text="Select categories to sort:").pack(pady=(10, 5))

        self.check_vars = {}
        for category in self.extensions.keys():
            var = tk.BooleanVar(value=True)
            self.check_vars[category] = var
            ttk.Checkbutton(frame, text=category, variable=var).pack(anchor="w")

        ttk.Button(frame, text="Start Sorting", command=self.sort_files).pack(pady=15)

        self.status_label = ttk.Label(frame, text="", foreground="gray")
        self.status_label.pack()

    def browse_folder(self):
        selected = filedialog.askdirectory()
        if selected:
            self.folder_path.set(selected)

    def sort_files(self):
        folder = Path(self.folder_path.get())
        if not folder.exists() or not folder.is_dir():
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        moved_count = 0
        skipped_count = 0

        for file in folder.iterdir():
            if file.is_file():
                matched = False
                for category, extensions in self.extensions.items():
                    if self.check_vars[category].get() and file.suffix.lower() in extensions:
                        target_dir = folder / category.lower()
                        target_dir.mkdir(exist_ok=True)
                        shutil.move(str(file), target_dir / file.name)
                        moved_count += 1
                        matched = True
                        break
                if not matched:
                    skipped_count += 1

        self.status_label.config(text=f"✅ {moved_count} files moved · 🟡 {skipped_count} skipped")
        messagebox.showinfo("Done", f"Sorting complete.\nMoved: {moved_count}\nSkipped: {skipped_count}")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    FileSorterApp(root)
    root.mainloop()
