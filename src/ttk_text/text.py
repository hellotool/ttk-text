from tkinter import Grid, Misc, Pack, Place, Text
from typing import Optional

from ttk_text.text_frame import ThemedTextFrame

__all__ = ["ThemedText"]


class ThemedText(Text):
    """
    A themed text widget combining Tkinter Text with ttk Frame styling.

    This widget provides native Tkinter Text functionality with ttk theme support.
    Inherits from `tkinter.Text` while embedding a ThemedTextFrame for style management.

    Style Elements:
        - Style name: 'ThemedText.TEntry' (configurable via style parameter)
        - Theme states: [focus, hover, pressed] with automatic state transitions

    Default Events:
        <FocusIn>       - Activates focus styling
        <FocusOut>      - Deactivates focus styling
        <Enter>         - Applies hover state
        <Leave>         - Clears hover state
        <ButtonPress-1> - Sets pressed state (left mouse down)
        <ButtonRelease-1> - Clears pressed state (left mouse up)
        <<ThemeChanged>> - Handles theme reload events

    Geometry Management:
        Proxies all ttk.Frame geometry methods (pack/grid/place) while maintaining
        native Text widget functionality. Use standard geometry managers as with
        regular ttk widgets.

    Inheritance Chain:
        ThemedText → tkinter.Text → tkinter.Widget → tkinter.BaseWidget → object
    """

    def __init__(
        self,
        master: Optional[Misc] = None,
        *,
        enable_inactive_select: bool = True,
        enable_t_entry_database_compat: bool = True,
        **kwargs,
    ):
        """
        Initialize a themed text widget.

        :param master: Parent widget (default=None)
        :param style: ttk style name (default='ThemedText.TEntry')
        :param class_: Widget class name (default='ThemedText')
        :param enable_inactive_select: Display selection when the widget is inactive
        :param enable_t_entry_database_compat: Compatibility with tk_setPalette
        :param kwargs: Additional Text widget configuration options

        .. note::
            Extract frame-related configuration from kwargs (class, style, relief, padding, borderwidth),
            remaining configuration is passed to the Text widget.
        """
        frame_kwargs = {
            "class": kwargs.pop("class", None),
            "style": kwargs.pop("style", None),
            "relief": kwargs.pop("relief", None),
            "padding": kwargs.pop("padding", None),
            "borderwidth": kwargs.pop("borderwidth", None),
        }

        self.frame = ThemedTextFrame(master, **frame_kwargs)
        super().__init__(self.frame, **kwargs)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.grid(row=1, column=1, sticky="nsew")

        # Use super() as a proxy to ensure direct calls to Text base class methods
        # Bypass methods that may be overridden in ThemedText (e.g., grid/configure)
        self.frame.bind_text(
            self,
            ThemedText.text_proxy(self),
            enable_inactive_select=enable_inactive_select,
            enable_t_entry_database_compat=enable_t_entry_database_compat,
        )
        self.__copy_geometry_methods()

    def text_proxy(self) -> Text:
        """Return the proxy of internal Text widget object."""
        return super()

    def __copy_geometry_methods(self):
        """Copy geometry methods of self.frame without overriding Text methods."""
        for m in (vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()).difference(vars(Text).keys()):
            if m[0] != "_" and m not in {"config", "configure"}:
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):  # pyright: ignore[reportImplicitOverride]
        """
        Return the string representation of the frame.

        :return: String representation of the frame
        """
        return str(self.frame)


def example():
    from tkinter import Tk

    root = Tk()
    root.geometry("300x300")
    root.title("ThemedText")
    text = ThemedText(root)
    text.pack(fill="both", expand=True, padx="7p", pady="7p")
    text.insert("1.0", "Hello, ThemedText!")
    root.mainloop()


if __name__ == "__main__":
    example()
