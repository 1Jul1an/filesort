import flet as ft
import os
import shutil
from pathlib import Path

DEFAULT_EXTENSIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "PDFs": [".pdf"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Office": [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp"],
    "Text": [".txt", ".md", ".csv"],
    "Programs": [".exe", ".msi", ".bat"]
}

def main(page: ft.Page):
    page.title = "FileSort"
    page.window_width = 460
    page.window_height = 530
    page.padding = 32
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "black"
    page.scroll = "adaptive"

    folder_path = ft.TextField(
        label="Target Folder", 
        read_only=True, 
        expand=True, 
        border_radius=10,
        bgcolor="rgba(33,33,33,0.8)",
        border_color="#424242",
        color="#fafafa"
    )
    status_text = ft.Text(size=13, color="#bdbdbd")
    progress_bar = ft.ProgressBar(width=360, value=0, color="#1976d2")

    checkboxes = []
    for cat in DEFAULT_EXTENSIONS:
        cb = ft.Checkbox(
            label=cat,
            value=True,
            fill_color="#1976d2",
            check_color="#fafafa",
            label_style=ft.TextStyle(color="#e0e0e0", size=16),
        )
        checkboxes.append(cb)

    # -- NEU: FilePicker Control für Directory Auswahl --
    picker = ft.FilePicker(on_result=lambda e: (
        setattr(folder_path, "value", e.path if e.path else ""),
        page.update()
    ))

    page.overlay.append(picker)  # WICHTIG: Picker zur Page-Overlay hinzufügen

    def pick_folder(e):
        picker.get_directory_path(dialog_title="Select folder...")

    def start_sorting(e):
        if not folder_path.value:
            status_text.value = "Please select a folder."
            page.update()
            return

        selected_categories = [cb.label for cb in checkboxes if cb.value]
        folder = Path(folder_path.value)
        all_files = list(folder.iterdir())
        total = len(all_files)
        moved, skipped = 0, 0

        for i, file in enumerate(all_files):
            if file.is_file():
                matched = False
                for cat in selected_categories:
                    if file.suffix.lower() in DEFAULT_EXTENSIONS[cat]:
                        target_dir = folder / cat.lower()
                        target_dir.mkdir(exist_ok=True)
                        shutil.move(str(file), target_dir / file.name)
                        moved += 1
                        matched = True
                        break
                if not matched:
                    skipped += 1

            progress_bar.value = (i + 1) / total if total > 0 else 1
            page.update()

        status_text.value = f"Sorting completed. {moved} moved, {skipped} skipped."
        page.update()

    page.add(
        ft.Column([
            ft.Text("FileSort", size=28, weight="bold", color="#fafafa", font_family="Arial"),
            ft.Row([
                folder_path,
                ft.IconButton(icon=ft.Icons.FOLDER_OPEN, on_click=pick_folder, icon_color="#bdbdbd")
            ], spacing=10),
            ft.Text("Categories", weight="bold", size=15, color="#bdbdbd", font_family="Arial"),
            ft.Column(checkboxes, spacing=3, expand=False),
            ft.ElevatedButton(
                "Start Sorting", 
                on_click=start_sorting, 
                height=44, 
                bgcolor="#1976d2", 
                color="#fafafa",
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
            ),
            progress_bar,
            status_text
        ], spacing=18)
    )

if __name__ == "__main__":
    ft.app(target=main)
