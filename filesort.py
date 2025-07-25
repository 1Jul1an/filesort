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
    "Text": [".txt", ".md", ".csv"],
    "Programs": [".exe", ".msi", ".bat"]
}


class FileSortApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FileSort")
        self.geometry("700x720")
        self.resizable(False, False)

        self.folder_path = tk.StringVar()
        self.progress = tk.DoubleVar()
        self.extensions = {}
        self.check_vars = {}

        self.load_extensions()
        self.build_ui()

    def load_extensions(self):
        if os.path.exists(EXTENSION_FILE):
            with open(EXTENSION_FILE, "r") as f:
                self.extensions = json.load(f)
        else:
            self.extensions = DEFAULT_EXTENSIONS
            with open(EXTENSION_FILE, "w") as f:
                json.dump(self.extensions, f, indent=2)

    def build_ui(self):
        padding = {"padx": 20, "pady": 10}

        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", **padding)

        ttk.Label(header, text="FileSort", font=("Segoe UI", 20, "bold")).pack(anchor="center")

        # Main Frame
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=30, pady=15)

        # Folder Selection
        ttk.Label(main, text="Target Folder:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(10, 0))
        path_frame = ttk.Frame(main)
        path_frame.pack(fill="x", pady=5)
        ttk.Entry(path_frame, textvariable=self.folder_path, width=60).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ttk.Button(path_frame, text="Browse", command=self.browse_folder).pack(side="right")

        # Category Toggles
        ttk.Label(main, text="Categories:", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(20, 5))
        cat_frame = ttk.Frame(main)
        cat_frame.pack(fill="x")
        for i, category in enumerate(self.extensions.keys()):
            var = tk.BooleanVar(value=True)
            self.check_vars[category] = var
            ttk.Checkbutton(cat_frame, text=category, variable=var).grid(row=i // 2, column=i % 2, sticky="w", padx=10, pady=4)

        # Start Button
        ttk.Button(main, text="Start Sorting", command=self.sort_files).pack(pady=20)

        # Progress
        self.progress_bar = ttk.Progressbar(main, variable=self.progress, maximum=1)
        self.progress_bar.pack(fill="x", padx=10)
        self.progress_label = ttk.Label(main, text="", foreground="gray")
        self.progress_label.pack()

        # Footer
        ttk.Label(self, text="Created by: https://github.com/1Jul1an", foreground="gray").pack(side="bottom", pady=10)

    def browse_folder(self):
        selected = filedialog.askdirectory()
        if selected:
            self.folder_path.set(selected)

    def sort_files(self):
        folder = Path(self.folder_path.get())
        if not folder.exists() or not folder.is_dir():
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        all_files = list(folder.iterdir())
        total = len(all_files)
        moved, skipped = 0, 0
        self.progress.set(0)

        for i, file in enumerate(all_files):
            if file.is_file():
                matched = False
                for category, extensions in self.extensions.items():
                    if self.check_vars[category].get() and file.suffix.lower() in extensions:
                        target_dir = folder / category.lower()
                        target_dir.mkdir(exist_ok=True)
                        shutil.move(str(file), target_dir / file.name)
                        moved += 1
                        matched = True
                        break
                if not matched:
                    skipped += 1
            self.progress.set((i + 1) / total)
            self.progress_label.config(text=f"{moved} moved · {skipped} skipped")

        messagebox.showinfo("Done", f"Sorting completed.\nMoved: {moved}\nSkipped: {skipped}")


if __name__ == "__main__":
    app = FileSortApp()
    app.mainloop()
