import os
import tkinter as tk
from tkinter import filedialog, messagebox
import win32com.client

from extractors.catia_extractor import CatiaExtractor
from core.comparator import DrawingComparator
from reports.excel_reporter import ExcelReporter


class App:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CATIA Drawing Comparator")

        self.folder_path = tk.StringVar()
        self.selected_ref = tk.StringVar()
        self.selected_cmp = tk.StringVar()

        self._build_ui()

# ─────────────────────────────────────────
# UI CONSTRUCTION
# ─────────────────────────────────────────

    def _build_ui(self):
        tk.Button(self.root, text="Select Folder", command=self._select_folder).pack(pady=5)
        tk.Label(self.root, textvariable=self.folder_path).pack()

        self.listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=60)
        self.listbox.pack(pady=10)

        tk.Label(self.root, text="Reference Drawing:").pack()
        self.ref_menu = tk.OptionMenu(self.root, self.selected_ref, "")
        self.ref_menu.pack()

        tk.Label(self.root, text="Drawing to Compare:").pack()
        self.cmp_menu = tk.OptionMenu(self.root, self.selected_cmp, "")
        self.cmp_menu.pack()

        tk.Button(self.root, text="Run Comparison", command=self._run).pack(pady=15)

# ─────────────────────────────────────────
# EVENT HANDLERS
# ─────────────────────────────────────────

    def _select_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        self.folder_path.set(folder)

        files = [f for f in os.listdir(folder) if f.lower().endswith(".catdrawing")]
        if not files:
            messagebox.showerror("Error", "No .CATDrawing files found in selected folder.")
            return

        self._update_menu(self.ref_menu, self.selected_ref, files)
        self._update_menu(self.cmp_menu, self.selected_cmp, files)

    def _run(self):
        folder = self.folder_path.get()
        ref_file = self.selected_ref.get()
        cmp_file = self.selected_cmp.get()

        if not folder or not ref_file or not cmp_file:
            messagebox.showerror("Error", "Please select a folder and both drawings.")
            return

        if ref_file == cmp_file:
            messagebox.showwarning("Warning", "Reference and compared drawings are the same file.")
            return

        path_ref = os.path.join(folder, ref_file)
        path_cmp = os.path.join(folder, cmp_file)

        try:
            ref_dims, cmp_dims = self._extract_dimensions(path_ref, path_cmp)
        except Exception as e:
            messagebox.showerror("Extraction Error", f"Failed to extract drawing data:\n{e}")
            return

        results = DrawingComparator().compare(ref_dims, cmp_dims)

        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",filetypes=[("Excel files", "*.xlsx")])
        if not save_path:
            return

        try:
            ExcelReporter().generate(results, save_path)
            messagebox.showinfo("Done", f"Report saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Report Error", f"Failed to save report:\n{e}")

# ─────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────

    def _extract_dimensions(self, path_ref: str, path_cmp: str):
        catia = win32com.client.Dispatch("CATIA.Application")
        doc_ref = catia.Documents.Open(path_ref)
        doc_cmp = catia.Documents.Open(path_cmp)

        ref_dims = CatiaExtractor(doc_ref).extract()
        cmp_dims = CatiaExtractor(doc_cmp).extract()

        return ref_dims, cmp_dims

    def _update_menu(self, menu: tk.OptionMenu, variable: tk.StringVar, options: list):
        menu["menu"].delete(0, "end")
        for opt in options:
            menu["menu"].add_command(label=opt, command=lambda v=opt: variable.set(v))
            if options:
                variable.set(options[0])