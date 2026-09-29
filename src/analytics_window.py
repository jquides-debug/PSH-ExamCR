"""Native Tk charts and an interactive question-analysis window."""
import tkinter as tk
from tkinter import ttk

from exam_analytics import RESPONSE_LABELS, build_analytics


INK = "#64121e"
ACCENT = "#ae2034"
MUTED = "#626773"
PAPER = "#fcf8f8"
GREEN = "#28745b"


def percent_text(value):
    return "Not scored" if value is None else f"{value:.1f}%"


class BarChart(tk.Canvas):
    """Resizable horizontal bars with explicit counts, labels and zero states."""

    def __init__(self, parent):
        super().__init__(parent, background="white", highlightthickness=0,
                         width=360, height=300)
        self.bars = []
        self.empty_message = "No data available."
        self.bind("<Configure>", self.redraw)

    def set_bars(self, bars, empty_message="No data available."):
        # Each bar is (label, numeric value, displayed value, color).
        self.bars = bars
        self.empty_message = empty_message
        self.redraw()

    def redraw(self, event=None):
        self.delete("all")
        width, height = self.winfo_width(), self.winfo_height()
        if not self.bars or not any(bar[1] for bar in self.bars):
            self.create_text(width / 2, height / 2, text=self.empty_message,
                             fill=MUTED, width=max(100, width - 40),
                             font=("Arial", 11), justify="center")
            return
        maximum = max(bar[1] for bar in self.bars)
        left, right = 94, max(120, width - 125)
        step = min(42, max(18, (height - 42) / len(self.bars)))
        for index, (label, value, display, color) in enumerate(self.bars):
            y = 16 + index * step
            self.create_text(left - 10, y + step / 2, text=label, anchor="e",
                             fill=INK, font=("Arial", 10))
            self.create_rectangle(left, y + 5, right, y + step - 5,
                                  fill=PAPER, outline="")
            if value:
                self.create_rectangle(left, y + 5,
                                      left + (right - left) * value / maximum,
                                      y + step - 5, fill=color, outline="")
            self.create_text(right + 10, y + step / 2, text=display, anchor="w",
                             fill=MUTED, font=("Arial", 10))
        self.create_text(left, 22 + len(self.bars) * step,
                         text=f"Count scale: 0 to {maximum}", anchor="nw",
                         fill=MUTED, font=("Arial", 9))


class AnalyticsWindow(tk.Toplevel):
    def __init__(self, parent, results, scores, rejected_count, answer_key=None):
        super().__init__(parent)
        self.title("PSH-Examination Checker - Analytics")
        self.geometry("1160x820")
        self.minsize(980, 740)
        self.configure(background=PAPER)
        self.analytics = build_analytics(results, scores, answer_key)
        batch = self.analytics
        ttk.Label(self, text="Examination analytics", style="Hero.TLabel").pack(
            anchor="w", padx=24, pady=(18, 6))
        self._label(self,
                    f"{batch.scan_count} processed scans  |  {len(batch.percentages)} scored  |  "
                    f"{batch.missing_count} without a scan  |  {rejected_count} rejected scans",
                    background=PAPER).pack(anchor="w", padx=24)
        self._label(self,
                    "Counts use processed scans; repeat scans of an ID count separately. "
                    "Missing and rejected scans are excluded.", background=PAPER).pack(
                        anchor="w", padx=24, pady=(4, 12))
        summary = tk.Frame(self, background=PAPER)
        summary.pack(fill="x", padx=24, pady=(0, 14))
        metrics = (("Questions analyzed", str(len(batch.questions))),
                   ("Average score", percent_text(batch.mean_score)),
                   ("Median score", percent_text(batch.median_score)),
                   ("Score range", f"{min(batch.percentages):.1f}% - {max(batch.percentages):.1f}%"
                    if batch.percentages else "Not scored"))
        for index, (label, value) in enumerate(metrics):
            summary.columnconfigure(index, weight=1, uniform="metric")
            card = tk.Frame(summary, background="white", padx=14, pady=12)
            card.grid(row=0, column=index, sticky="nsew", padx=(0, 8))
            self._label(card, label).pack(anchor="w")
            self._label(card, value, foreground=INK, font=("Arial", 18, "bold")).pack(
                anchor="w", pady=(6, 0))

        footer = tk.Frame(self, background=PAPER)
        footer.pack(side="bottom", fill="x", padx=24, pady=12)
        ttk.Button(footer, text="Close analytics", command=self.destroy).pack(side="right")
        self._label(footer, "Response frequencies are available without an answer key.",
                    background=PAPER).pack(side="left")
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=24)
        overview = tk.Frame(notebook, padx=12, pady=12)
        detail = tk.Frame(notebook, padx=12, pady=12)
        notebook.add(overview, text="  Performance overview  ")
        notebook.add(detail, text="  Questions & responses  ")
        self._overview(overview)
        self._questions(detail)
        self.bind("<Escape>", lambda event: self.destroy())

    @staticmethod
    def _label(parent, text, **kwargs):
        label = ttk.Label(parent, text=text, **kwargs)
        label.bind("<Configure>", lambda event: label.configure(
            wraplength=max(100, event.width)))
        return label

    def _overview(self, parent):
        batch = self.analytics
        self._label(parent,
                    "Grades follow the batch's saved scores. Blank and multiple responses count as "
                    "incorrect when graded against a single-choice key. Questions without grades "
                    "are excluded from the ranking.").pack(fill="x", pady=(0, 12))
        charts = tk.Frame(parent)
        charts.pack(fill="both", expand=True)
        for index, title in enumerate(("Score distribution", "Most-missed questions (top 10)")):
            charts.columnconfigure(index, weight=1, uniform="chart")
            card = tk.Frame(charts)
            card.grid(row=0, column=index, sticky="nsew", padx=6)
            self._label(card, title, style="Heading.TLabel").pack(anchor="w", pady=8)
            chart = BarChart(card)
            chart.pack(fill="both", expand=True)
            if index == 0:
                chart.set_bars([(label, count, str(count), ACCENT)
                                for label, count in batch.score_distribution],
                               "No scored scans. Process a batch with an answer key to see score distribution.")
            else:
                chart.set_bars([(q.name, q.incorrect,
                                 f"{q.incorrect} ({q.incorrect_percent:.1f}%)", ACCENT)
                                for q in batch.hardest_questions[:10]],
                               "No incorrect answers in the scored questions." if batch.hardest_questions
                               else "No graded questions. Process a batch with an answer key to see the ranking.")
        charts.rowconfigure(0, weight=1)
        self._label(parent,
                    "Score bars count scans. Missed-question bars show incorrect counts and the "
                    "percentage of graded responses for that question; ties follow question order.").pack(
                        fill="x", pady=(12, 0))

    def _questions(self, parent):
        batch = self.analytics
        self._label(parent, "Select a question to see how often each response was detected. "
                    "Click a heading to sort.").pack(fill="x", pady=(0, 6))
        body = tk.Frame(parent)
        body.pack(fill="both", expand=True)
        body.columnconfigure(0, weight=3, uniform="detail")
        body.columnconfigure(1, weight=2, uniform="detail")
        body.rowconfigure(0, weight=1)
        table_frame = tk.Frame(body)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        response_panel = tk.Frame(body)
        response_panel.grid(row=0, column=1, sticky="nsew")
        columns = ("question", "key", "correct", "incorrect", "missed", "blank", "multiple")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings",
                                  selectmode="browse", height=6)
        for name, title in zip(columns, ("Question", "Answer key", "Correct", "Incorrect",
                                         "Incorrect (%)", "Blank", "Multiple")):
            self.table.heading(name, text=title,
                               command=lambda col=name: self._sort_questions(col))
            self.table.column(name, width=80, minwidth=65, anchor="center")
        horizontal = ttk.Scrollbar(table_frame, orient="horizontal", command=self.table.xview)
        horizontal.pack(side="bottom", fill="x")
        scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set, xscrollcommand=horizontal.set)
        scroll.pack(side="right", fill="y")
        self.table.pack(side="left", fill="both", expand=True)
        ordered = batch.hardest_questions + [q for q in batch.questions if not q.graded]
        self.question_lookup = {q.name: q for q in ordered}
        for q in ordered:
            self.table.insert("", "end", iid=q.name, values=(
                q.name, q.key or "Unavailable", q.correct if q.graded else "Not scored",
                q.incorrect if q.graded else "Not scored", percent_text(q.incorrect_percent),
                q.responses["Blank"], q.responses["Multiple"]))
        self.sort_descending = {}
        controls = tk.Frame(response_panel)
        controls.pack(fill="x", pady=(0, 4))
        self.response_title = self._label(controls, "", style="Heading.TLabel")
        self.response_title.pack(fill="x", pady=(0, 6))
        ttk.Button(controls, text="All questions", command=self._all_responses).pack(anchor="w")
        self.response_note = self._label(response_panel, "")
        self.response_note.pack(side="bottom", fill="x", pady=(4, 0))
        self.response_chart = BarChart(response_panel)
        self.response_chart.configure(height=250)
        self.response_chart.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self._select_question)
        self._all_responses()

    def _sort_questions(self, column):
        def value(name):
            q = self.question_lookup[name]
            return {"question": int(q.name[1:]), "key": q.key,
                    "correct": q.correct if q.graded else None,
                    "incorrect": q.incorrect if q.graded else None,
                    "missed": q.incorrect_percent, "blank": q.responses["Blank"],
                    "multiple": q.responses["Multiple"]}[column]
        children = self.table.get_children()
        reverse = self.sort_descending.get(column, False)
        ordered = sorted((name for name in children if value(name) is not None),
                         key=value, reverse=reverse)
        ordered += [name for name in children if value(name) is None]
        for index, name in enumerate(ordered):
            self.table.move(name, "", index)
        self.sort_descending[column] = not reverse

    def _all_responses(self):
        self.table.selection_remove(*self.table.selection())
        self._show_responses("All analyzed questions", self.analytics.response_totals)

    def _select_question(self, event=None):
        selected = self.table.selection()
        if selected:
            q = self.question_lookup[selected[0]]
            self._show_responses(f"{q.name} responses", q.responses, q.key)

    def _show_responses(self, title, counts, key=""):
        total = sum(counts.values())
        self.response_title.configure(text=f"{title}  |  {total} responses")
        bars = [(label, counts[label],
                 f"{counts[label]} ({100 * counts[label] / total:.1f}%)" if total else "0",
                 GREEN if label == key else ACCENT) for label in RESPONSE_LABELS]
        self.response_chart.set_bars(bars, "No processed responses available.")
        self.response_note.configure(
            text=(f"Answer key: {key}. Green marks the correct choice. " if key in RESPONSE_LABELS[:5]
                  else "") + "Each response is counted once. Blank includes G; Multiple includes F "
                 "and combinations such as [A|B].")
