from collections.abc import MutableMapping
from tkinter import Event, EventType, Grid, Misc, Pack, Place, Text
from tkinter.ttk import Frame, Style
from typing import Any, Iterable, NamedTuple, Optional
from weakref import WeakKeyDictionary

from ttk_text.utils import parse_padding

__all__ = ["ThemedText", "ThemedTextFrame"]

_UPDATE_STYLE_ONLY_EVENTS = ("<FocusIn>", "<FocusOut>", "<Enter>", "<Leave>")

_TRANSITION_STATE_EVENTS = _UPDATE_STYLE_ONLY_EVENTS + ("<ButtonPress-1>", "<ButtonRelease-1>")


class BoundText(NamedTuple):
    """
    A bound text widget tuple for managing text widgets and their original instances.

    :ivar widget: Original widget instance, used to determine which widget's event when receiving events
    :ivar proxy: Text widget instance, which may be the super of the widget or the widget itself
    """

    widget: Text
    proxy: Text


class BoundWidget(NamedTuple):
    """
    A bound widget tuple for managing widgets and their state penetration.

    :ivar instance: Widget instance
    :ivar penetration_state: Whether to allow state penetration to ThemedTextFrame
                        True: Widget events modify the frame state (e.g., decorative components)
                        False: Only bind events, do not modify frame state (e.g., scrollbars)
    """

    instance: Misc
    penetration_state: bool


class ThemedTextFrame(Frame):
    """
    A themed text frame providing ttk-style text container.

    This class is a ttk Frame responsible for managing bound text widgets and state transitions,
    automatically updating styles through bound event listeners.

    Features:
        - Supports themed text widget styling
        - Automatically handles focus, hover, and pressed states
        - Supports binding multiple widgets for complex interaction states

    State Management:
        - focus: Activated when the widget gains focus
        - hover: Activated when mouse hovers
        - pressed: Activated when mouse is pressed

    Important Note:
        The frame automatically updates its own state. For example, when the mouse hovers over other widgets
        inside the frame, the frame will automatically remove its own hover state. Since there is no direct
        way to detect this behavior, all internal components need to be event-bound to ensure styles are
        correctly updated to the text widget. This is the purpose of `penetration_state=False`: even if
        widget events don't modify the frame state, they need to be bound to trigger style updates.

    Example:
        .. code-block:: python

            # Create a themed text frame
            frame = ThemedTextFrame(root)
            frame.pack(fill="both", expand=True)

            # Configure grid weights to make the text area expandable
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)

            # Create a text widget and bind it to the frame
            text = Text(frame)
            frame.bind_text(text)
            text.grid(row=0, column=0, sticky="nsew")

            # Add a scrollbar and bind it (non-penetrating state)
            scrollbar = Scrollbar(frame)
            scrollbar.grid(row=0, column=1, sticky="ns")
            frame.bind_widget(scrollbar, penetration_state=False)

    Style Options:
        - style: ttk style name (default="ThemedText.TEntry")
        - class_: Widget class name (default="ThemedText")
    """

    def __init__(self, master: Optional[Misc] = None, **kwargs):
        """
        Initialize a ThemedTextFrame instance.

        :param master: Parent widget, default is None
        :param kwargs: Configuration options passed to Frame

        .. note::
            If style is not specified, "ThemedText.TEntry" will be used.
            If class_ is not specified, "ThemedText" will be used.
        """
        if not kwargs.get("style"):
            kwargs["style"] = "ThemedText.TEntry"
        if not kwargs.get("class_"):
            kwargs["class_"] = "ThemedText"
        super().__init__(master, **kwargs)
        self.__style = Style(self)
        self.__bound_text: Optional[BoundText] = None
        self.__bound_widgets: MutableMapping[Misc, BoundWidget] = WeakKeyDictionary()
        self.__update_stateful_style_task_id: Optional[str] = None

        self.bind_widget(self, penetration_state=True)
        self.bind("<<ThemeChanged>>", self.__on_theme_changed, "+")

    def bind_widget(self, widget: Misc, *, penetration_state: bool = False):
        """
        Bind a widget to the frame so its events can trigger style updates.

        :param widget: Widget instance to bind
        :param penetration_state: Whether widget events modify the frame state

        .. note::
            - For functional components like scrollbars, set penetration_state=False
              so widget events do not modify the frame state but still trigger style updates
            - For decorative components, set penetration_state=True
              so widget events modify the frame state and trigger style updates

            Default is False, suitable for most functional components.
            Since the frame automatically updates its own state, all internal components
            need to be event-bound to ensure styles are correctly updated to the text widget.
            This is the main purpose of penetration_state=False.
        """
        if not widget.winfo_exists():
            raise ValueError("Widget does not exist")
        self.__bound_widgets[widget] = BoundWidget(widget, penetration_state)

        if penetration_state:
            for sequence in _TRANSITION_STATE_EVENTS:
                widget.bind(sequence, self.__handle_state_transition, "+")
        else:
            for sequence in _UPDATE_STYLE_ONLY_EVENTS:
                widget.bind(sequence, self.__handle_style_update, "+")

        widget.bind("<Destroy>", self.__on_bound_widget_destroy, "+")

    def bind_text(self, text: Text, proxy: Optional[Text] = None):
        """
        Bind a text widget to the frame.

        :param text: Text widget instance
        :param proxy: Optional proxy text (can be a super widget of text)

        .. note::
            This method configures the text widget with a flat style (no border or highlight),
            and binds it to the frame to receive state change events.
        """
        if proxy is None:
            proxy = text
        if not proxy.winfo_exists():
            raise ValueError(f"Text widget {proxy} does not exist or has been destroyed")
        self.__bound_text = BoundText(text, proxy)
        proxy.configure(
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
        )
        self.bind_widget(text, penetration_state=True)
        self.update_style()

    def __on_bound_widget_destroy(self, event: Event):
        if event.widget in self.__bound_widgets:
            del self.__bound_widgets[event.widget]

        if self.__bound_text and event.widget is self.__bound_text.widget:
            self.__bound_text = None

    def __handle_state_transition(self, event: Event):
        # Older versions of Python do not support the `match` statement.
        bound_widget = self.__bound_widgets.get(event.widget)
        if bound_widget is None:
            return
        if bound_widget.penetration_state:
            if event.type == EventType.FocusIn:
                self.state(["focus"])
            elif event.type == EventType.FocusOut:
                self.state(["!focus"])
            elif event.type == EventType.Enter:
                self.state(["hover"])
            elif event.type == EventType.Leave:
                # If the pointer hovers over the root widget, tk will automatically restore the hover state later
                self.state(["!hover"])
            elif event.type == EventType.ButtonPress and event.num == 1:
                self.state(["pressed"])
            elif event.type == EventType.ButtonRelease and event.num == 1:
                self.state(["!pressed"])
        self.__handle_style_update(event)

    def __handle_style_update(self, _: Event):
        if self.__update_stateful_style_task_id is not None:
            self.after_cancel(self.__update_stateful_style_task_id)
        # noinspection PyTypeChecker
        self.__update_stateful_style_task_id = self.after_idle(self.__update_stateful_style)

    def __on_theme_changed(self, event: Event):
        if event.widget != self:
            return
        # Prevents style updates after widget destruction.
        self.update_style()

    def __lookup(self, option: str, state: Optional[Iterable[str]] = None, default=None) -> Any:
        result = self.__style.lookup(self.cget("style"), option, state)
        if not result:  # Avoid ""
            return default
        return result

    def update_style(self):
        if self.__bound_text:
            proxy = self.__bound_text.proxy
            proxy.configure(
                selectbackground=self.__lookup("selectbackground", state=["focus"]),
                selectforeground=self.__lookup("selectforeground", state=["focus"]),
                insertwidth=self.__lookup("insertwidth", state=["focus"], default=1),
                font=self.__lookup("font", default="TkDefaultFont"),
            )
            if text_padding := parse_padding(self.__lookup("textpadding")):
                proxy.grid(padx=text_padding.to_padx(), pady=text_padding.to_pady())
            else:
                proxy.grid(padx=0, pady=0)
        self.configure(
            padding=self.__lookup("padding", default="1"),
            borderwidth=self.__lookup("borderwidth", default="1"),
        )
        self.__update_stateful_style()

    def __update_stateful_style(self):
        if self.__update_stateful_style_task_id is not None:
            self.after_cancel(self.__update_stateful_style_task_id)
            self.__update_stateful_style_task_id = None
        if self.__bound_text:
            state = self.state()
            self.__bound_text.proxy.configure(
                background=self.__lookup("fieldbackground", state),
                foreground=self.__lookup("foreground", state),
            )


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

    def __init__(self, master: Optional[Misc] = None, **kwargs):
        """
        Initialize a themed text widget.

        :param master: Parent widget (default=None)
        :param style: ttk style name (default='ThemedText.TEntry')
        :param class_: Widget class name (default='ThemedText')
        :param kw: Additional Text widget configuration options

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
        self.frame.bind_text(self, super())
        self.__copy_geometry_methods()

    def __copy_geometry_methods(self):
        """
        Copy geometry methods of self.frame without overriding Text methods.
        """

        for m in (vars(Pack).keys() | vars(Grid).keys() | vars(Place).keys()).difference(vars(Text).keys()):
            if m[0] != "_" and m != "config" and m != "configure":
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
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
