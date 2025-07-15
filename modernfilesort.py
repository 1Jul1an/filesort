import os
import shutil
import json
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox

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


class FileSortApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("FileSort")
        self.geometry("720x740")
        self.resizable(False, False)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.folder_path = ctk.StringVar()
        self.progress = ctk.DoubleVar()
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
        # Header
        header = ctk.CTkFrame(self, height=80, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(15, 0))

        ctk.CTkLabel(header, text="FileSort", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(10, 0))

        self.theme_switch = ctk.CTkSwitch(header, text="Dark Mode", command=self.toggle_theme)
        self.theme_switch.pack(pady=(10, 0))
        self.theme_switch.select()

        # Main Frame
        main = ctk.CTkFrame(self, corner_radius=15)
        main.pack(fill="both", expand=True, padx=40, pady=20)

        # Folder Selection
        ctk.CTkLabel(main, text="Target Folder", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(10, 5))
        path_frame = ctk.CTkFrame(main, fg_color="transparent")
        path_frame.pack(fill="x", pady=5)
        ctk.CTkEntry(path_frame, textvariable=self.folder_path, placeholder_text="Path to folder...", height=38).pack(side="left", expand=True, fill="x", padx=(0, 10))
        ctk.CTkButton(path_frame, text="Browse", width=100, command=self.browse_folder).pack(side="right")

        # Category Toggles
        ctk.CTkLabel(main, text="Categories", font=ctk.CTkFont(size=16)).pack(anchor="w", pady=(20, 10))
        cat_frame = ctk.CTkFrame(main, fg_color="transparent")
        cat_frame.pack(fill="x", pady=5)
        for i, category in enumerate(self.extensions.keys()):
            var = ctk.BooleanVar(value=True)
            self.check_vars[category] = var
            ctk.CTkSwitch(cat_frame, text=category, variable=var).grid(row=i // 2, column=i % 2, padx=20, pady=8, sticky="w")

        # Start Button + Progress
        ctk.CTkButton(main, text="Start Sorting", command=self.sort_files, height=45, font=ctk.CTkFont(size=14)).pack(pady=25)
        self.progress_bar = ctk.CTkProgressBar(main, variable=self.progress, height=14)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_label = ctk.CTkLabel(main, text="", text_color="gray")
        self.progress_label.pack()

        # Footer
        ctk.CTkLabel(self, text="Created by: https://github.com/1Jul1an", font=ctk.CTkFont(size=12), text_color="gray").pack(side="bottom", pady=10)

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch.get() else "light")

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
            self.progress_label.configure(text=f"{moved} moved · {skipped} skipped")

        messagebox.showinfo("Done", f"Sorting completed.\nMoved: {moved}\nSkipped: {skipped}")


if __name__ == "__main__":
    app = FileSortApp()
    app.mainloop()
