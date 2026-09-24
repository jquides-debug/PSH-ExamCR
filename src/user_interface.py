import abc
import enum
import os
import re
from pathlib import Path
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import typing as tp
import platform

import file_handling
import scoring
import str_utils

YPADDING = 4
XPADDING = 7
APP_NAME = "PSH-Examination Checker"
INK = "#64121e"
ACCENT = "#ae2034"
MUTED = "#626773"
LINE = "#eadde0"
PAPER = "#fcf8f8"


def configure_theme(app: tk.Tk):
    """Apply the PSH website palette to the native desktop controls."""
    app.configure(background=PAPER)
    app.option_add("*Frame.background", "#ffffff")
    style = ttk.Style(app)
    style.theme_use("clam")
    style.configure(".", font=("Arial", 10), background="#ffffff",
                    foreground=INK)
    style.configure("TLabel", foreground=MUTED)
    style.configure("Heading.TLabel", font=("Arial", 10, "bold"), foreground=INK)
    style.configure("Brand.TLabel", font=("Arial", 13, "bold"), foreground=INK)
    style.configure("Hero.TLabel", font=("Georgia", 27), background=PAPER,
                    foreground=INK)
    style.configure("Badge.TLabel", font=("Arial", 9, "bold"),
                    background="#f3e2e5", foreground=ACCENT, padding=(12, 6))
    style.configure("Path.TLabel", background=PAPER, padding=8)
    style.configure("TButton", padding=(12, 8), background="#ffffff",
                    foreground=INK, bordercolor=LINE, borderwidth=1)
    style.map("TButton", background=[("active", "#f3e2e5")],
              foreground=[("disabled", "#969099")])
    style.configure("Primary.TButton", background=INK, foreground="#ffffff",
                    font=("Arial", 10, "bold"), padding=(22, 11))
    style.map("Primary.TButton",
              background=[("disabled", "#eadde0"), ("active", ACCENT)],
              foreground=[("disabled", "#76636a"), ("!disabled", "#ffffff")])
    style.configure("TCheckbutton", foreground=INK, padding=3)
    style.map("TCheckbutton", background=[("active", PAPER)],
              foreground=[("disabled", "#969099")])
    style.configure("TSeparator", background=LINE)
    style.configure("Horizontal.TProgressbar", background=ACCENT,
                    troughcolor=PAPER, bordercolor=LINE)


def create_card(parent: tk.Misc, number: str, title: str) -> tk.Frame:
    card = tk.Frame(parent, highlightbackground=LINE, highlightthickness=1,
                    padx=12, pady=12)
    tk.Frame(card, background=ACCENT, width=32, height=3).pack(anchor="w", padx=7)
    ttk.Label(card, text=f"{number}  /  {title}", style="Heading.TLabel").pack(
        anchor="w", padx=7, pady=(12, 14))
    return card

PackTarget = tk.Misc


def prompt_folder(message: str = "Select Folder", default: str = "./") -> Path:
    """Prompt the user to select a folder."""
    folderpath = filedialog.askdirectory(initialdir=default, title=message)
    return Path(folderpath)


def prompt_file(message: str = "Select File",
                default: str = "./",
                filetypes: tp.Optional[tp.List[tp.Tuple[str, str]]] = None
                ) -> Path:
    """Prompt the user to select a file."""
    filepath = filedialog.askopenfilename(initialdir=default,
                                          title=message,
                                          filetypes=filetypes)
    return Path(filepath)


T = tp.TypeVar("T", bound=tk.Widget)


def pack(widget: T, *args: tp.Any, **kwargs: tp.Any) -> T:
    """Pack the widget into its root and return it."""
    widget.pack(*args, **kwargs)
    return widget


def create_and_pack_label(parent: PackTarget,
                          text: str,
                          heading: bool = False,
                          inline: bool = False) -> ttk.Label:
    """Create a label using the predefined font settings, pack it, and return it."""
    font_opt = {"style": "Heading.TLabel"} if heading else {}
    pady_opt = {"pady": (YPADDING * 2, 0)} if heading else {"pady": YPADDING}
    label = ttk.Label(parent,
                      text=text,
                      justify=tk.LEFT,
                      anchor="w",
                      **font_opt)
    if not inline:
        label.bind("<Configure>", lambda event: label.configure(
            wraplength=max(100, event.width)))
    return pack(label,
                fill=tk.X if not inline else None,
                expand=False,
                padx=XPADDING,
                side=tk.LEFT if inline else None,
                **pady_opt)


class PickerWidget(abc.ABC):
    """File picker widget (browse button and file path)."""
    value: tp.Optional[Path]

    def __init__(self,
                 parent: PackTarget,
                 placeholder: str,
                 on_change: tp.Optional[tp.Callable] = None):
        internal_padding = int(XPADDING * 0.66)
        external_padding = XPADDING
        pack_opts = {"side": tk.LEFT, "pady": external_padding}

        self.__on_change = on_change
        self.__placeholder = placeholder

        container = tk.Frame(parent)
        self.__browse_button = pack(ttk.Button(container,
                                               text="Browse",
                                               command=self._prompt,
                                               padding=internal_padding),
                                    **pack_opts,
                                    padx=(external_padding, 0))

        self.__display_text = tk.StringVar()
        pack(ttk.Label(container,
                       textvariable=self.__display_text,
                       width=20,
                       justify=tk.LEFT,
                       anchor="w",
                       style="Path.TLabel",
                       padding=internal_padding),
             **pack_opts,
             padx=external_padding,
             fill=tk.X,
             expand=True)

        self.__display_text.set(placeholder)
        pack(container, fill=tk.X)
        self.value = None

    @abc.abstractmethod
    def _prompt(self):
        ...

    def _on_select(self, selection: Path):
        self.value = selection if str(selection).strip() != "." else None

        display_text = str_utils.trim_middle_to_len(
            str(selection), 45,
            3) if self.value is not None else self.__placeholder
        self.__display_text.set(display_text)

        if self.__on_change is not None:
            self.__on_change()

    def disable(self):
        self.__browse_button.configure(state=tk.DISABLED)

    def clear(self):
        self.value = None
        self.__display_text.set(self.__placeholder)
        if self.__on_change is not None:
            self.__on_change()


class FolderPickerWidget(PickerWidget):
    def __init__(self,
                 parent: PackTarget,
                 on_change: tp.Optional[tp.Callable] = None):
        super().__init__(parent, "No Folder Selected", on_change)

    def _prompt(self):
        super()._on_select(prompt_folder())


class FilePickerWidget(PickerWidget):
    def __init__(self,
                 parent: PackTarget,
                 filetypes: tp.Optional[tp.List[tp.Tuple[str, str]]] = None,
                 on_change: tp.Optional[tp.Callable] = None):
        self.__filetypes = filetypes
        super().__init__(parent, "No File Selected", on_change)

    def _prompt(self):
        super()._on_select(prompt_file(filetypes=self.__filetypes))


class CheckboxWidget():
    """File picker widget (browse button and file path)."""
    value: bool

    def __init__(self,
                 parent: PackTarget,
                 label: str,
                 on_change: tp.Optional[tp.Callable] = None,
                 reduce_padding_above: bool = False):
        self.__on_change = on_change
        self.__raw_value = tk.IntVar(parent, 0)

        internal_padding = int(XPADDING * 0.33)
        external_padding = XPADDING
        top_padding = external_padding if not reduce_padding_above else 0
        pack_opts = {"side": tk.LEFT, "pady": (top_padding, external_padding)}

        frame = tk.Frame(parent)
        self.__checkbox = pack(ttk.Checkbutton(frame,
                                               text=label,
                                               command=self.__on_update,
                                               variable=self.__raw_value,
                                               padding=internal_padding),
                               **pack_opts,
                               padx=(external_padding, 0))
        frame.pack(fill=tk.X)

        self.value = False

    def __on_update(self):
        self.value = bool(self.__raw_value.get())
        if self.__on_change is not None:
            self.__on_change()

    def disable(self):
        self.__checkbox.configure(state=tk.DISABLED)


class SelectWidget():
    """Select (combobox) dropdown menu widget."""
    value: str

    def __init__(self,
                 parent: PackTarget,
                 label: str,
                 options: tp.List[str],
                 on_change: tp.Optional[tp.Callable] = None):
        self.__raw_value = tk.StringVar()
        self.__on_change = on_change

        container = tk.Frame(parent)
        create_and_pack_label(container, label, inline=True)
        self.__combobox = pack(ttk.Combobox(container,
                                            width=16,
                                            state="readonly",
                                            textvariable=self.__raw_value,
                                            values=options),
                               side=tk.RIGHT, padx=XPADDING)
        self.__combobox.current(0)

        self.__raw_value.trace_add("write", self.__on_update)
        self.value = self.__raw_value.get()
        pack(container, fill=tk.X)

    def __on_update(self, *args: tp.Any):
        self.value = self.__raw_value.get()
        if (self.__on_change is not None):
            self.__on_change()

    def disable(self):
        self.__combobox.configure(state=tk.DISABLED)


class FormVariantSelection(enum.Enum):
    VARIANT_150_Q = enum.auto()


class InputFolderPickerWidget():
    folder: tp.Optional[Path]
    multi_answers_as_f: bool
    empty_answers_as_g: bool
    form_variant: FormVariantSelection

    def __init__(self,
                 parent: PackTarget,
                 on_change: tp.Optional[tp.Callable] = None):
        self.__on_change = on_change

        container = tk.Frame(parent)

        create_and_pack_label(container, "Select Input Folder", heading=True)
        create_and_pack_label(
            container,
            "Choose your scanned answer sheets. All images in this folder are processed; subfolders are ignored."
        )

        self.__input_folder_picker = FolderPickerWidget(
            container, self.__on_update)
        self.__multi_answers_as_f_checkbox = CheckboxWidget(
            container, "Save multiple answers as 'F'",
            self.__on_update)
        self.__empty_answers_as_g_checkbox = CheckboxWidget(
            container, "Save empty answers as 'G'",
            self.__on_update, True)
        create_and_pack_label(container, "Answer sheet: 150 questions")

        pack(container, fill=tk.X)

        self.folder = None
        self.multi_answers_as_f = False
        self.empty_answers_as_g = False
        self.form_variant = FormVariantSelection.VARIANT_150_Q

    def __on_update(self, *args: tp.Any):
        self.folder = self.__input_folder_picker.value
        self.multi_answers_as_f = self.__multi_answers_as_f_checkbox.value
        self.empty_answers_as_g = self.__empty_answers_as_g_checkbox.value

        if self.__on_change is not None:
            self.__on_change()

    def disable(self):
        self.__input_folder_picker.disable()
        self.__multi_answers_as_f_checkbox.disable()
        self.__empty_answers_as_g_checkbox.disable()

    def clear_folder(self):
        self.__input_folder_picker.clear()


class OutputFolderPickerWidget():
    folder: tp.Optional[Path]
    sort_results: bool
    output_mcta: bool
    sort_toggle_count: int

    def __init__(self,
                 parent: PackTarget,
                 on_change: tp.Optional[tp.Callable] = None):
        self.__on_change = on_change

        container = tk.Frame(parent)

        create_and_pack_label(container, "Select Output Folder", heading=True)
        create_and_pack_label(container,
                              "Save CSV files and an Excel review workbook. Multiple answers are highlighted red in Excel.")

        self.__output_folder_picker = FolderPickerWidget(
            container, self.__on_update)
        self.__sort_results_checkbox = CheckboxWidget(
            container, "Sort results by Examinee ID",
            self.__on_sort_update)
        self.__output_mcta_checkbox = CheckboxWidget(
            container, "Output additional files for MCTA.",
            self.__on_update, reduce_padding_above=True)

        pack(container, fill=tk.X)

        self.folder = None
        self.sort_results = False
        self.output_mcta = False
        self.sort_toggle_count = 0

    def __on_sort_update(self):
        self.sort_toggle_count += 1
        self.__on_update()

    def __on_update(self):
        self.folder = self.__output_folder_picker.value
        self.sort_results = self.__sort_results_checkbox.value
        self.output_mcta = self.__output_mcta_checkbox.value

        if self.__on_change is not None:
            self.__on_change()

    def disable(self):
        self.__output_folder_picker.disable()
        self.__sort_results_checkbox.disable()
        self.__output_mcta_checkbox.disable()

    def clear_folder(self):
        self.__output_folder_picker.clear()


class AnswerKeyPickerWidget():
    file: tp.Optional[Path]

    def __init__(self,
                 parent: PackTarget,
                 on_change: tp.Optional[tp.Callable] = None):
        self.__on_change = on_change

        container = tk.Frame(parent)

        create_and_pack_label(container,
                              "Answer key CSV (optional)",
                              heading=True)
        create_and_pack_label(
            container,
            "Select a CSV file containing one answer key for scoring.\nSee 'Help' for formatting instructions."
        )

        self.__answer_key_picker = FilePickerWidget(container,
                                                    [("CSV Files", "*.csv")],
                                                    self.__on_update)

        pack(container, fill=tk.X)

        self.file = None

    def __on_update(self):
        self.file = self.__answer_key_picker.value
        if self.__on_change is not None:
            self.__on_change()

    def disable(self):
        self.__answer_key_picker.disable()


def enable_table_sorting(table: ttk.Treeview, numeric_columns=()):
    """Sort rows in place, preserving item identities, selection and tags."""
    titles = {column: table.heading(column, "text") for column in table["columns"]}
    state = {"column": None, "descending": False}

    def apply_sort():
        column = state["column"]
        if column is None:
            return
        valid, missing = [], []
        for item in table.get_children():
            value = table.set(item, column).strip()
            if column in numeric_columns:
                try:
                    key = float(value)
                except ValueError:
                    missing.append(item)
                    continue
            else:
                # Natural order: Q2 before Q10, scan2 before scan10.
                key = tuple((1, int(part)) if part.isdigit() else (0, part.casefold())
                            for part in re.split(r"(\d+)", value))
            valid.append((key, item))
        ordered = [item for _, item in sorted(
            valid, key=lambda pair: pair[0], reverse=state["descending"])] + missing
        for position, item in enumerate(ordered):
            table.move(item, "", position)
        for name, title in titles.items():
            marker = (" ▼" if state["descending"] else " ▲") if name == column else ""
            table.heading(name, text=title + marker)

    def toggle(column):
        state["descending"] = not state["descending"] if state["column"] == column else False
        state["column"] = column
        apply_sort()

    for column in titles:
        table.heading(column, command=lambda name=column: toggle(name))
    return apply_sort


class ResultsWindow(tk.Toplevel):
    """Browse saved examinees and review one answer sheet at a time."""

    def __init__(self, parent, results, scores, workbook_path, rejected_count, answer_key=None):
        super().__init__(parent)
        self.title(f"{APP_NAME} - Results")
        self.geometry("1280x700")
        self.minsize(1100, 520)
        self.configure(background=PAPER)
        ttk.Label(self, text="Examination results", style="Hero.TLabel").pack(
            anchor="w", padx=24, pady=(20, 8))
        ttk.Label(self, background=PAPER,
                  text=f"{results.row_count} examinees  |  {rejected_count} rejected scans  |  Select an examinee to review answers.").pack(
            anchor="w", padx=24, pady=(0, 16))
        body = tk.Frame(self, background=PAPER)
        body.pack(fill=tk.BOTH, expand=True, padx=24)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.columnconfigure(2, weight=2)
        body.rowconfigure(0, weight=1)
        left = tk.Frame(body)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        right = tk.Frame(body)
        right.grid(row=0, column=1, columnspan=2, sticky="nsew")
        for frame in (left, right):
            frame.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)

        self.examinees = ttk.Treeview(left, columns=("id", "source", "score"),
                                     show="headings", selectmode="browse")
        for name, title, width in (("id", "Examinee ID", 150),
                                   ("source", "Source File", 200),
                                   ("score", "Score (%)", 100)):
            self.examinees.heading(name, text=title)
            self.examinees.column(name, width=width, minwidth=70)
        self.answers = ttk.Treeview(right, columns=("question", "answer", "comparison", "key", "result"),
                                    show="headings", selectmode="browse")
        for column, title, width in (("question", "Question", 80),
                                     ("answer", "Detected answer", 130),
                                     ("comparison", "", 45),
                                     ("key", "Answer key", 110),
                                     ("result", "Result", 110)):
            self.answers.heading(column, text=title)
            self.answers.column(column, width=width, minwidth=40, anchor="center")
        self.answers.tag_configure("incorrect", background="#ffc7ce", foreground="#9c0006")
        self.answers.tag_configure("multiple", background="#ffc7ce", foreground="#9c0006")
        enable_table_sorting(self.examinees, numeric_columns=("score",))
        sort_answers = enable_table_sorting(self.answers)
        for frame, table in ((left, self.examinees), (right, self.answers)):
            table.grid(row=0, column=0, sticky="nsew")
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")
            horizontal = ttk.Scrollbar(frame, orient="horizontal", command=table.xview)
            horizontal.grid(row=1, column=0, sticky="ew")
            table.configure(yscrollcommand=scrollbar.set, xscrollcommand=horizontal.set)

        headings = results.data[0]
        id_index = headings.index("Examinee ID")
        source_index = headings.index("Source File")
        score_lookup = {}
        question_scores = {}
        correct_answers = {}
        if answer_key is not None and answer_key.row_count == 1:
            correct_answers = dict(zip(answer_key.data[0][answer_key.first_question_column_index:],
                                       answer_key.data[1][answer_key.first_question_column_index:]))
        if scores is not None:
            score_headings = scores.data[0]
            for row in scores.data[1:]:
                score_lookup[row[score_headings.index("Source File")]] = row[
                    score_headings.index("Total Score (%)")]
                question_scores[row[score_headings.index("Source File")]] = dict(zip(
                    score_headings[scores.first_question_column_index:],
                    row[scores.first_question_column_index:]))
        for index, row in enumerate(results.data[1:]):
            self.examinees.insert("", "end", iid=str(index), values=(
                row[id_index], row[source_index], score_lookup.get(row[source_index], "Not scored")))

        def select_examinee(event=None):
            for item in self.answers.get_children():
                self.answers.delete(item)
            selection = self.examinees.selection()
            if not selection:
                return
            row = results.data[int(selection[0]) + 1]
            for question, answer in zip(headings[results.first_question_column_index:],
                                        row[results.first_question_column_index:]):
                multiple = answer == "F" or (answer.startswith("[") and "|" in answer)
                score = question_scores.get(row[source_index], {}).get(question)
                result = "Correct" if score == "1" else "Incorrect" if score == "0" else "Not scored"
                tag = "incorrect" if score == "0" else "multiple" if multiple else ""
                self.answers.insert("", "end", values=(
                    question, answer or "Blank", "?" if score == "0" else "=" if score == "1" else "?",
                    correct_answers.get(question, "?"), result), tags=(tag,) if tag else ())
            sort_answers()

        self.examinees.bind("<<TreeviewSelect>>", select_examinee)
        if results.row_count:
            self.examinees.selection_set("0")
            select_examinee()
        footer = tk.Frame(self, background=PAPER)
        footer.pack(fill=tk.X, padx=24, pady=16)
        ttk.Label(footer, text="Red: multiple answers / incorrect results",
                  background=PAPER).pack(side=tk.LEFT)

        def open_path(path):
            try:
                if platform.system() == "Windows":
                    os.startfile(str(path))
                else:
                    subprocess.Popen(["open" if platform.system() == "Darwin" else "xdg-open", str(path)])
            except OSError as error:
                messagebox.showerror("Unable to open file", str(error), parent=self)

        ttk.Button(footer, text="Another batch", command=self.destroy).pack(side=tk.RIGHT, padx=(8, 0))
        ttk.Button(footer, text="Open Excel", style="Primary.TButton",
                   command=lambda: open_path(workbook_path)).pack(side=tk.RIGHT)
        ttk.Button(footer, text="Open output folder",
                   command=lambda: open_path(workbook_path.parent)).pack(side=tk.RIGHT, padx=8)


class ProgressTrackerWidget:
    def __init__(self, parent: PackTarget, maximum: int):
        self.maximum = maximum
        self.value = 0
        self.parent = parent
        self.results_shown = False
        pack_opts = {
            "fill": tk.X,
            "expand": 1,
            "padx": XPADDING,
            "pady": YPADDING
        }
        self.status_text = tk.StringVar(parent)
        status_label = pack(ttk.Label(parent, textvariable=self.status_text,
                                      width=20, justify=tk.LEFT), **pack_opts)
        status_label.bind("<Configure>", lambda event: status_label.configure(
            wraplength=max(100, event.width)))
        self.progress_bar = pack(
            ttk.Progressbar(parent, maximum=maximum, mode="determinate"),
            **pack_opts)
        self.close_when_changes = tk.IntVar(parent, name="Ready to Close")

    def step_progress(self, step: int = 1):
        self.value += step
        self.progress_bar.step(step)
        self.parent.update()
        self.parent.update_idletasks()

    def set_status(self, status: str, show_count: bool = True):
        new_status = f"{status} ({self.value + 1}/{self.maximum})" if show_count else status
        self.status_text.set(new_status)

    def set_ready_to_close(self):
        self.close_when_changes.set(1)

    def show_results(self, results, scores, workbook_path, rejected_count, answer_key=None):
        self.progress_bar.configure(value=self.maximum)
        window = ResultsWindow(self.parent, results, scores, workbook_path, rejected_count, answer_key)
        window.lift()
        self.parent.wait_window(window)
        self.results_shown = True

    def show_exit_button_and_wait(self):
        # Closing the results window already requests a return to setup.
        if self.results_shown:
            return
        close_button = ttk.Button(self.parent,
                                  text="Back to setup",
                                  command=self.set_ready_to_close)
        close_button.pack(padx=XPADDING, pady=YPADDING)
        close_button.wait_variable("Ready to Close")


class MainWindow:
    root: tk.Tk
    input_folder: Path
    output_folder: Path
    multi_answers_as_f: bool
    empty_answers_as_g: bool
    keys_file: tp.Optional[Path]
    arrangement_map: tp.Optional[Path]
    sort_results: bool
    output_mcta: bool
    debug_mode: bool = False
    form_variant: FormVariantSelection
    cancelled: bool = False

    def __init__(self):
        app: tk.Tk = tk.Tk()
        configure_theme(app)
        self.__app = app
        app.title(APP_NAME)
        app.geometry("1280x780")
        app.minsize(1200, 760)

        app.protocol("WM_DELETE_WINDOW", self.__on_close)

        header = tk.Frame(app)
        header.pack(fill=tk.X)
        brand = tk.Frame(header)
        brand.pack(side=tk.LEFT, padx=26, pady=14)
        logo = tk.PhotoImage(file=str(Path(__file__).parent / "assets" / "psh-logo.png"))
        factor = max(1, (max(logo.width(), logo.height()) + 55) // 56)
        self.__logo = logo.subsample(factor, factor)
        app.iconphoto(True, self.__logo)
        ttk.Label(brand, image=self.__logo).pack(side=tk.LEFT, padx=(0, 14))
        brand_text = tk.Frame(brand)
        brand_text.pack(side=tk.LEFT)
        ttk.Label(brand_text, text="Philippine Society of Hypertension",
                  style="Brand.TLabel").pack(anchor="w")
        ttk.Label(brand_text, text=APP_NAME).pack(
            anchor="w", pady=(5, 0))
        ttk.Label(header, text="150 QUESTIONS", style="Badge.TLabel").pack(
            side=tk.RIGHT, padx=26)
        ttk.Separator(app).pack(fill=tk.X)
        hero = tk.Frame(app, background=PAPER)
        hero.pack(fill=tk.X, padx=26, pady=(18, 16))
        ttk.Label(hero, text="Examination Test Checker", style="Hero.TLabel").pack(anchor="w")
        ttk.Label(hero, text="Prepare your scans, add an answer key, and review your results.",
                  background=PAPER).pack(anchor="w", pady=(6, 0))

        workspace = tk.Frame(app, background=PAPER)
        workspace.pack(fill=tk.BOTH, expand=True, padx=26, pady=(0, 18))
        workspace.rowconfigure(0, weight=1)
        for column in range(3):
            workspace.columnconfigure(column, weight=1, uniform="panels")

        folders = create_card(workspace, "01", "Scans & output")
        folders.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        references = create_card(workspace, "02", "Answer key")
        references.grid(row=0, column=1, sticky="nsew", padx=(0, 8))
        summary = create_card(workspace, "03", "Review & run")
        summary.grid(row=0, column=2, sticky="nsew")

        self.__input_folder_picker = InputFolderPickerWidget(
            folders, self.__on_update)
        ttk.Separator(folders).pack(fill=tk.X, padx=XPADDING, pady=12)
        self.__answer_key_picker = AnswerKeyPickerWidget(references, self.__on_update)
        create_and_pack_label(references, "Use one answer key per batch.")
        self.__output_folder_picker = OutputFolderPickerWidget(
            folders, self.__on_update)

        self.__status_text = tk.StringVar()
        create_and_pack_label(summary, "Configuration summary", heading=True)
        status = ttk.Label(summary, textvariable=self.__status_text,
                           justify=tk.LEFT, anchor="nw")
        status.pack(fill=tk.BOTH, expand=True, padx=XPADDING, pady=12)
        status.bind("<Configure>", lambda event: status.configure(
            wraplength=max(100, event.width)))
        self.__progress_frame = tk.Frame(summary)
        self.__progress_frame.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Separator(app).pack(fill=tk.X)
        buttons_frame = tk.Frame(app)

        # "Open Help" Button
        pack(ttk.Button(buttons_frame,
                        text="Help",
                        command=self.__show_help),
             padx=XPADDING,
             pady=YPADDING,
             side=tk.LEFT)
        # "Open Sheet" button
        pack(ttk.Button(buttons_frame,
                        text="Print Form",
                        command=self.__show_sheet),
             padx=XPADDING,
             pady=YPADDING,
             side=tk.LEFT)

        self.__confirm_button = pack(ttk.Button(buttons_frame,
                                                text="Process sheets",
                                                style="Primary.TButton",
                                                command=self.__confirm,
                                                state=tk.DISABLED),
                                     padx=XPADDING,
                                     pady=YPADDING,
                                     side=tk.RIGHT)
        pack(buttons_frame, fill=tk.X, padx=26, pady=(0, 10))
        self.__on_update()

        self.__ready_to_continue = tk.IntVar(name="Ready to Continue")

    def wait_for_batch(self):
        """Wait until the user selects folders and starts the next run."""
        self.__ready_to_continue.set(0)
        self.__app.wait_variable(self.__ready_to_continue)
        return not self.cancelled

    def reset_for_next_batch(self):
        for child in self.__progress_frame.winfo_children():
            child.destroy()

        def enable(widget):
            for child in widget.winfo_children():
                if isinstance(child, (ttk.Button, ttk.Checkbutton)):
                    child.configure(state=tk.NORMAL)
                enable(child)

        enable(self.__app)
        self.__input_folder_picker.clear_folder()
        self.__output_folder_picker.clear_folder()
        # Do not retain runnable paths from the previous batch.
        for name in ("input_folder", "output_folder"):
            if hasattr(self, name):
                delattr(self, name)
        self.__on_update()

    def __on_update(self):
        ok_to_submit = True
        new_status = ""

        input_folder = self.__input_folder_picker.folder
        if input_folder is None:
            new_status += "❌ Input folder is required.\n"
            ok_to_submit = False
        else:
            self.input_folder = input_folder
            images = file_handling.filter_images(
                file_handling.list_file_paths(input_folder))
            if len(images) == 0:
                new_status += "❌ No image files found in selected input folder.\n"
                ok_to_submit = False
            else:
                new_status += f"✔ Input folder selected. {len(images)} image files found.\n"

        self.form_variant = self.__input_folder_picker.form_variant
        new_status += "Using 150-question answer sheet.\n"

        output_folder = self.__output_folder_picker.folder
        if output_folder is None:
            new_status += "❌ Output folder is required.\n"
            ok_to_submit = False
        else:
            self.output_folder = output_folder
            new_status += f"✔ Output folder selected.\n"

        keys_file = self.__answer_key_picker.file
        self.keys_file = None
        if keys_file:
            if scoring.verify_answer_key_sheet(keys_file):
                self.keys_file = keys_file
                new_status += f"✔ Selected answer keys file appears to be valid.\n"
            else:
                new_status += f"❌ Selected answer keys file is not valid.\n"
                ok_to_submit = False

        self.arrangement_map = None

        self.multi_answers_as_f = self.__input_folder_picker.multi_answers_as_f
        if self.multi_answers_as_f:
            new_status += f"Questions with multiple answers selected will be output as 'F'.\n"
        else:
            new_status += f"Questions with multiple answers selected will be output in '[A|B]' form.\n"

        self.empty_answers_as_g = self.__input_folder_picker.empty_answers_as_g
        if self.empty_answers_as_g:
            new_status += f"Unanswered questions will be output as 'G'.\n"
        else:
            new_status += f"Unanswered questions will be left as blank cells.\n"

        self.sort_results = self.__output_folder_picker.sort_results
        if self.sort_results:
            new_status += "Results will be sorted by Examinee ID\n"
        else:
            new_status += f"Input sort order will be maintained.\n"


        self.output_mcta = self.__output_folder_picker.output_mcta
        if self.output_mcta:
            new_status += "Additional files will be output for use with analysis software."

        if self.__output_folder_picker.sort_toggle_count > 15:
            new_status += "WARNING: Debug mode enabled. Restart to disable."
            self.debug_mode = True

        self.__status_text.set(new_status)
        self.__confirm_button.configure(
            state=tk.NORMAL if ok_to_submit else tk.DISABLED)
        return ok_to_submit

    def __disable_all(self):
        self.__confirm_button.configure(state=tk.DISABLED)
        self.__input_folder_picker.disable()
        self.__output_folder_picker.disable()
        self.__answer_key_picker.disable()

    def __confirm(self):
        if self.__on_update():
            self.__disable_all()
            self.__ready_to_continue.set(1)

    def __show_help(self):
        try:
            manual = (Path(__file__).parent / "assets" / "manual.md").read_text(
                encoding="utf-8")
        except OSError as error:
            messagebox.showerror("Help unavailable", str(error), parent=self.__app)
            return
        window = tk.Toplevel(self.__app)
        window.title(f"{APP_NAME} - User guide")
        window.geometry("850x700")
        window.minsize(600, 400)
        window.configure(background=PAPER)
        frame = tk.Frame(window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text = tk.Text(frame, wrap="word", font=("Arial", 11), background="white",
                       foreground=MUTED, relief="flat", padx=20, pady=16,
                       spacing3=8, cursor="arrow")
        scroll = ttk.Scrollbar(frame, command=text.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.configure(yscrollcommand=scroll.set)
        text.pack(fill=tk.BOTH, expand=True)
        text.tag_configure("title", font=("Georgia", 23), foreground=INK, spacing3=16)
        text.tag_configure("heading", font=("Arial", 13, "bold"), foreground=INK,
                           spacing1=12, spacing3=10)
        text.tag_configure("code", font=("Courier New", 10), background=PAPER)
        in_code = False
        for line in manual.splitlines():
            if line.startswith("```"):
                in_code = not in_code
                continue
            tag = "code" if in_code else "title" if line.startswith("# ") else (
                "heading" if line.startswith("## ") else "")
            content = line if in_code else line.lstrip("#").lstrip().replace("**", "").replace("`", "")
            text.insert(tk.END, content + "\n", tag)
        text.configure(state=tk.DISABLED)
        ttk.Button(window, text="Close guide", command=window.destroy).pack(pady=(0, 16))
        window.bind("<Escape>", lambda event: window.destroy())

    def __show_sheet(self):
        helpfile = str(Path(__file__).parent / "assets" /
                       "multiple_choice_sheet_150q.pdf")
        if platform.system() in ('Darwin', 'Linux'):
            subprocess.Popen(['open', helpfile])
        else:
            subprocess.Popen([helpfile], shell=True)

    def __on_close(self):
        self.cancelled = True
        self.__ready_to_continue.set(1)
        self.__app.destroy()

    def create_and_pack_progress(self, maximum: int) -> ProgressTrackerWidget:
        return ProgressTrackerWidget(self.__progress_frame, maximum)
