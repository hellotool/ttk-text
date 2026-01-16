import inspect
import os
import sys
import tkinter.scrolledtext
from tkinter import Misc, StringVar, Text, Tk
from tkinter.font import nametofont
from tkinter.ttk import Combobox, Entry, Frame, Label, LabelFrame, Sizegrip, Style

from ttk_text import ThemedText, ThemedTextFrame
from ttk_text.scrolled_text import ScrolledText

try:
    import sv_ttk
except ModuleNotFoundError:
    sv_ttk = None

SUN_VALLEY_THEMES = ("sun-valley-light", "sun-valley-dark")
FOREST_THEMES = ("forest-light", "forest-dark")
AZURE_THEMES = ("azure-light", "azure-dark")


def enable_dpi_aware():
    if sys.platform == "win32":
        from ctypes import windll

        windll.user32.SetProcessDPIAware()


def fix_sv_ttk(style: Style):
    if sv_ttk is None:
        return
    # Fix font size in high DPI
    for name in ("SunValleyBodyFont", "SunValleyCaptionFont"):
        font = nametofont(name)
        if font.cget("size") < 0:
            font.configure(size=-int(font.cget("size") * 0.75))
    if sv_ttk.get_theme() == "light":
        style.configure("ThemedText.TEntry", fieldbackground="#fdfdfd", textpadding=5)
        style.map(
            "ThemedText.TEntry",
            fieldbackground=[
                ("hover", "!focus", "#f9f9f9"),
            ],
            foreground=[
                ("pressed", style.lookup("TEntry", "foreground")),
            ],
        )
    else:
        style.configure("ThemedText.TEntry", fieldbackground="#292929", textpadding=5)
        style.map(
            "ThemedText.TEntry",
            fieldbackground=[
                ("hover", "!focus", "#2f2f2f"),
                ("focus", "#1c1c1c"),
            ],
            foreground=[
                ("pressed", style.lookup("TEntry", "foreground")),
            ],
        )


def fix_forest_ttk(style: Style):
    if style.theme_use() == "forest-light":
        style.configure(
            "ThemedText.TEntry",
            fieldbackground="#ffffff",
            textpadding=5,
            font="TkTextFont",
        )
    else:
        style.configure(
            "ThemedText.TEntry",
            fieldbackground="#313131",
            textpadding=5,
            font="TkTextFont",
        )


def fix_azure_ttk(style: Style):
    if style.theme_use() == "azure-light":
        style.configure("ThemedText.TEntry", fieldbackground="#ffffff", textpadding=5)
    else:
        style.configure("ThemedText.TEntry", fieldbackground="#333333", textpadding=5)


def create_themed_text_labelframe(parent: Misc):
    frame = LabelFrame(parent, text="ThemedText")
    text = ThemedText(frame)
    text.pack(fill="both", expand=True, padx="4p", pady="4p")
    if doc := inspect.getdoc(ThemedText):
        text.insert("1.0", doc)
    frame.propagate(False)
    return frame


def create_scrolled_text_labelframe(parent: Misc):
    frame = LabelFrame(parent, text="ScrolledText")
    text = ScrolledText(frame)
    text.pack(fill="both", expand=True, padx="4p", pady="4p")
    if doc := inspect.getdoc(ScrolledText):
        text.insert("1.0", doc)
    frame.propagate(False)
    return frame


def create_horizontal_scrollable_scrolled_text_labelframe(parent: Misc):
    frame = LabelFrame(parent, text="ScrolledText(horizontal=True)")
    text = ScrolledText(frame, horizontal=True, wrap="none")
    text.pack(fill="both", expand=True, padx="4p", pady="4p")
    if doc := inspect.getdoc(ScrolledText):
        text.insert("1.0", doc)
    frame.propagate(False)
    return frame


def create_themed_text_frame_labelframe(parent: Misc):
    frame = LabelFrame(parent, text="ThemedTextFrame + tkinter.Text")
    text_frame = ThemedTextFrame(frame)
    text_frame.pack(fill="both", expand=True, padx="4p", pady="4p")
    text_frame.grid_rowconfigure(1, weight=1)
    text_frame.grid_columnconfigure(1, weight=1)
    text = Text(text_frame)
    text.grid(row=1, column=1, sticky="nsew")
    text_frame.bind_text(text)
    if doc := inspect.getdoc(ThemedTextFrame):
        text.insert("1.0", doc)
    frame.propagate(False)
    return frame


def create_themed_text_frame_tkinter_scrolledtext_labelframe(parent: Misc):
    frame = LabelFrame(parent, text="ThemedTextFrame + tkinter.scrolledtext.ScrolledText")
    text_frame = ThemedTextFrame(frame)
    text_frame.pack(fill="both", expand=True, padx="4p", pady="4p")
    text_frame.grid_rowconfigure(1, weight=1)
    text_frame.grid_columnconfigure(1, weight=1)
    text = tkinter.scrolledtext.ScrolledText(text_frame)
    text.grid(row=1, column=1, sticky="nsew")
    text_frame.bind_text(text)
    if doc := inspect.getdoc(ThemedTextFrame):
        text.insert("1.0", doc)
    frame.propagate(False)
    return frame


def main():
    enable_dpi_aware()

    root = Tk()
    root.title("ThemedText")
    root.configure(padx="4p", pady="4p")
    fraction = root.tk.call("tk", "scaling") * 0.75
    root.geometry(f"{round(800 * fraction)}x{round(600 * fraction)}")
    root.update()

    background_frame = Frame(root)
    background_frame.place(relheight=1, relwidth=1, bordermode="outside")

    style = Style(root)

    if sv_ttk:  # Initialize sv themes
        sv_ttk.get_theme()

    lazy_load_themes = {}
    if os.path.exists("external-themes/forest-ttk-theme/forest-light.tcl"):
        lazy_load_themes["forest-light"] = "external-themes/forest-ttk-theme/forest-light.tcl"

    if os.path.exists("external-themes/forest-ttk-theme/forest-dark.tcl"):
        lazy_load_themes["forest-dark"] = "external-themes/forest-ttk-theme/forest-dark.tcl"

    if os.path.exists("external-themes/azure-ttk-theme/azure.tcl"):
        lazy_load_themes["azure-dark"] = "external-themes/azure-ttk-theme/azure.tcl"
        lazy_load_themes["azure-light"] = "external-themes/azure-ttk-theme/azure.tcl"

    theme_variable = StringVar(root, value=style.theme_use())
    theme_names = [*style.theme_names(), *lazy_load_themes.keys()]
    theme_names.sort()

    def on_theme_variable_changed(*_):
        theme_name = theme_variable.get()
        if theme_name not in style.theme_names() and theme_name in lazy_load_themes:
            root.tk.call("source", lazy_load_themes[theme_name])

        if theme_name in style.theme_names():
            style.theme_use(theme_name)
            if theme_name in AZURE_THEMES:
                root.tk.call("set_theme", theme_name.replace("azure-", ""))
        else:
            theme_variable.set(style.theme_use())

    theme_variable.trace_add("write", on_theme_variable_changed)

    def on_theme_changed(*_):
        # Fix theme
        theme_name = style.theme_use()
        if theme_name in SUN_VALLEY_THEMES:
            fix_sv_ttk(style)
        elif theme_name in FOREST_THEMES:
            fix_forest_ttk(style)
        elif theme_name in AZURE_THEMES:
            fix_azure_ttk(style)

    root.bind("<<ThemeChanged>>", on_theme_changed)

    sizegrip = Sizegrip(root)
    sizegrip.place(relx=1, rely=1, anchor="se", bordermode="outside")

    root.grid_columnconfigure([0, 1, 2], weight=1)
    root.grid_rowconfigure([2, 3], weight=1)

    options_frame = LabelFrame(root, text="Options")
    options_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", padx="4p", pady="4p")

    theme_label = Label(options_frame, text="Theme:")
    theme_label.grid(row=0, column=0, padx="4p", pady="4p")

    theme_combobox = Combobox(options_frame, textvariable=theme_variable, values=theme_names, state="readonly")
    theme_combobox.grid(row=0, column=1, padx="4p", pady="4p")

    entry_frame = LabelFrame(root, text="Tkinter Entry")
    entry_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx="4p", pady="4p")

    entry = Entry(entry_frame, width=40)
    entry.insert(1, "Hello, Entry!")
    entry.pack(fill="x", padx="4p", pady="4p")
    create_themed_text_labelframe(root).grid(
        row=2,
        column=0,
        sticky="nsew",
        padx="4p",
        pady="4p",
    )

    create_scrolled_text_labelframe(root).grid(
        row=2,
        column=1,
        sticky="nsew",
        padx="4p",
        pady="4p",
    )
    create_horizontal_scrollable_scrolled_text_labelframe(root).grid(
        row=2,
        column=2,
        sticky="nsew",
        padx="4p",
        pady="4p",
    )
    create_themed_text_frame_labelframe(root).grid(
        row=3,
        column=0,
        sticky="nsew",
        padx="4p",
        pady="4p",
    )

    create_themed_text_frame_tkinter_scrolledtext_labelframe(root).grid(
        row=3,
        column=1,
        sticky="nsew",
        padx="4p",
        pady="4p",
    )

    root.mainloop()


if __name__ == "__main__":
    main()
