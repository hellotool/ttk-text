<div align="center">

# Themed Tkinter Text

**Repository:**
[![GitHub Main Repository](https://img.shields.io/badge/GitHub-Main%20repo-0969da?logo=github)][repository-github]
[![GitCode Mirror Repository](https://img.shields.io/badge/GitCode-Mirror%20Repo-DA203E?logo=gitcode)][repository-gitcode]

**Language**:
[简体中文](./README.zh-CN.md) |
**English** |
<small>More translations are welcome!</small>

</div>

Themed Tkinter Text widget with modern styling support.

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](./CODE_OF_CONDUCT.md)
[![MIT License](https://img.shields.io/github/license/Jesse205/ttk-text)](./LICENSE)
[![Testing](https://github.com/Jesse205/ttk-text/actions/workflows/testing.yml/badge.svg)](https://github.com/Jesse205/ttk-text/actions/workflows/testing.yml)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ttk-text)
[![PyPI - Version](https://img.shields.io/pypi/v/ttk-text)](https://pypi.org/project/ttk-text/)

## Features

- 🎨 Theme-aware text widget that automatically adapts to ttk themes
- 📜 Built-in ScrolledText component with vertical/horizontal scrollbars
- 🖥️ Native integration with ttk styles and themes
- 🔄 Dynamic theme switching support

## Screenshots

<div>
<img src="./doc/images/screenshots/windows11.webp" alt="Windows 11" width="338.7">
<img src="./doc/images/screenshots/windows10.webp" alt="Windows 10" width="337">
<img src="./doc/images/screenshots/windows7.webp" alt="Windows 7" width="350.7">
</div>

Example screenshots of Windows 11, Windows 10, and Windows 7.

## Usage

### Installation

You can install ttk-text using your preferred package manager.

Since ttk-text is currently unstable, I **strongly recommend installing it in a virtual environment and pinning the exact version** to avoid version conflicts.

```bash
# Using pip
pip install ttk-text

# Using uv
uv add ttk-text

# Using PDM
pdm add ttk-text

# Using Poetry
poetry add ttk-text
```

### Using the Widgets

ttk-text provides three widgets:

- `ttk_text.ThemedTextFrame`: A Frame for rendering the textbox style, which will bind to a Text widget.
- `ttk_text.ThemedText`: A themed Text widget, as a replacement for `tkinter.Text`.
- `ttk_text.scrolled_text.ScrolledText`: An extension of `ThemedText` with vertical/horizontal scrollbars, as a replacement for `tkinter.scrolledtext.ScrolledText`.

#### Using `ThemedText` and `ScrolledText`

You can use `ThemedText` and `ScrolledText` just like you would use `tkinter.Text`.

Here's an example:

```python
from tkinter import Tk
from ttk_text import ThemedText
from ttk_text.scrolled_text import ScrolledText

root = Tk()

themed_text = ThemedText(root)
themed_text.pack(fill="both", expand=True, padx="7p", pady="7p")

scrolled_text = ScrolledText(root)
scrolled_text.pack(fill="both", expand=True, padx="7p", pady=(0, "7p"))

root.mainloop()
```

> [!NOTE]
>
> Currently, ttk style properties will override attributes you set such as `selectbackground`.

#### Adding Additional Components to `ThemedText` and `ScrolledText`

`ThemedText` itself doesn't handle theming; instead, it wraps itself in a `ThemedTextFrame` and lets the `ThemedTextFrame` handle theming. You can access this `ThemedTextFrame` via `ThemedText#frame`.

`ThemedText` positions itself at grid position (1, 1) within `ThemedText#frame`.

Layout of `ThemedText#frame`:

| Column/Row |   0   |      1       |   2   |
| :--------: | :---: | :----------: | :---: |
|     0      |       |              |       |
|     1      |       | `ThemedText` |       |
|     2      |       |              |       |

`ScrolledText` also adds scrollbars and a frame for corner junction aesthetics.

Layout of `ScrolledText#frame`:

| Column/Row |   0   |                1                 |               2                |
| :--------: | :---: | :------------------------------: | :----------------------------: |
|     0      |       |                                  |                                |
|     1      |       |           `ThemedText`           | `Scrollbar(orient="vertical")` |
|     2      |       | `Scrollbar(orient="horizontal")` |            `Frame`             |

You can place other components around (1, 1) like with `ScrolledText`, and call `ThemedText#frame.bind_widget()` to bind the component.

#### Using `ThemedTextFrame`

You can use `ThemedTextFrame` to theme third-party Text components.

After adding the component, you need to call `ThemedText#frame.bind_text()` to bind the third-party Text component.

For example, using `tkinter.scrolledtext.ScrolledText`:

```python
import tkinter.scrolledtext
from tkinter import Tk

from ttk_text import ThemedTextFrame

root = Tk()

text_frame = ThemedTextFrame(root)
text_frame.pack(fill="both", expand=True, padx="7p", pady="7p")
text_frame.grid_rowconfigure(1, weight=1)
text_frame.grid_columnconfigure(1, weight=1)

text = tkinter.scrolledtext.ScrolledText(text_frame)
text.grid(row=1, column=1, sticky="nsew")

text_frame.bind_text(text)

root.mainloop()
```

> [!NOTE]
>
> `ThemedTextFrame` internally requires grid layout, **you cannot use pack or place layouts**.

### Styling Configuration

You can use style name `ThemedText.TEntry` to configure styling.

| Property           | Description                        |
| ------------------ | ---------------------------------- |
| `borderwidth`      | `ThemedTextFrame` border width     |
| `padding`          | `ThemedTextFrame` internal padding |
| `fieldbackground`  | `Text` background color            |
| `foreground`       | `Text` font color                  |
| `textpadding`      | `Text` external padding            |
| `insertwidth`      | `Text` cursor width                |
| `selectbackground` | `Text` selection background color  |
| `selectforeground` | `Text` selection font color        |

For example, to set the border width to `1.5p`:

```python
from tkinter.ttk import Style

style = Style()
style.configure("ThemedText.TEntry", borderwidth="1.5p")
```

### Theme Compatibility

Some third-party themes may not be fully compatible with ttk-text. You can call the following function after setting the theme:

<details>
<summary>Sun Valley ttk theme</summary>

```python
from tkinter import Tk
from tkinter.ttk import Style
import sv_ttk


def fix_sv_ttk(style: Style):
    if sv_ttk.get_theme() == "light":
        style.configure("ThemedText.TEntry", fieldbackground="#fdfdfd", textpadding=5)
        style.map(
            "ThemedText.TEntry",
            fieldbackground=[
                ("hover", "!focus", "#f9f9f9"),
            ],
            foreground=[
                ("pressed", style.lookup("TEntry", "foreground")),
            ]
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
            ]
        )


# Example
app = Tk()
sv_ttk.set_theme("light")
fix_sv_ttk(Style())
app.mainloop()
```

</details>

<details>
<summary>Azure-ttk-theme</summary>

```python
from tkinter import Tk
from tkinter.ttk import Style


def fix_azure_ttk(style: Style):
    if style.theme_use() == "azure-light":
        style.configure("ThemedText.TEntry", fieldbackground="#ffffff", textpadding=5)
    else:
        style.configure("ThemedText.TEntry", fieldbackground="#333333", textpadding=5)


# Example
app = Tk()
app.tk.call("source", "azure.tcl")
Style().theme_use("azure-light")
app.tk.call("set_theme", "light")
fix_azure_ttk(Style())
app.mainloop()
```

</details>

<details>
<summary>Forest-ttk-theme</summary>

```python
from tkinter import Tk
from tkinter.ttk import Style


def fix_forest_ttk(style: Style):
    if style.theme_use() == "forest-light":
        style.configure("ThemedText.TEntry", fieldbackground="#ffffff", textpadding=5, font="TkTextFont")
    else:
        style.configure("ThemedText.TEntry", fieldbackground="#313131", textpadding=5, font="TkTextFont")


# Example
app = Tk()
app.tk.call("source", "external-themes/forest-ttk-theme/forest-light.tcl")
Style().theme_use("forest-light")
fix_forest_ttk(Style())
app.mainloop()
```

</details>

## Contributing

See [CONTRIBUTING.md](https://github.com/Jesse205/TtkText/blob/main/CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License, see the [LICENSE](./LICENSE) file for details.

[repository-github]: https://github.com/hellotool/ttk-text/
[repository-gitcode]: https://gitcode.com/hellotool/ttk-text/
