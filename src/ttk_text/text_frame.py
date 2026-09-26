from tkinter import Event, EventType, Misc, Text
from tkinter.ttk import Frame, Style
from typing import TYPE_CHECKING, Any, Iterable, NamedTuple, Optional
from weakref import WeakKeyDictionary

from ttk_text._utils import parse_padding

if TYPE_CHECKING:
    from collections.abc import MutableMapping

_UPDATE_STYLE_ONLY_EVENTS = ("<FocusIn>", "<FocusOut>", "<Enter>", "<Leave>")

_TRANSITION_STATE_EVENTS = (*_UPDATE_STYLE_ONLY_EVENTS, "<ButtonPress-1>", "<ButtonRelease-1>")


__all__ = ["ThemedTextFrame"]


class _BoundText(NamedTuple):
    """
    A bound text widget tuple for managing text widgets and their original instances.

    :ivar widget: Original widget instance, used to determine which widget's event when receiving events
    :ivar proxy: Text widget instance, which may be the super of the widget or the widget itself
    :ivar enable_inactive_select: Display selection when the widget is inactive
    :ivar enable_t_entry_database_compat: Compatibility with tk_setPalette
    """

    widget: Text
    proxy: Text
    enable_inactive_select: bool
    enable_t_entry_database_compat: bool


class _BoundWidget(NamedTuple):
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
            - If ``style`` is not specified, "ThemedText.TEntry" will be used.
            - If ``class_`` is not specified, "ThemedText" will be used.
            - If ``takefocus`` is not specified, ``takefocus`` will be set to False.
        """
        if not kwargs.get("style"):
            kwargs["style"] = "ThemedText.TEntry"
        if not kwargs.get("class_"):
            kwargs["class_"] = "ThemedText"
        if "takefocus" not in kwargs:
            kwargs["takefocus"] = False
        super().__init__(master, **kwargs)
        self.__style = Style(self)
        self.__bound_text: Optional[_BoundText] = None
        self.__bound_widgets: MutableMapping[Misc, _BoundWidget] = WeakKeyDictionary()
        self.__update_stateful_style_task_id: Optional[str] = None

        self.bind_widget(self, penetration_state=True)
        self.bind("<<ThemeChanged>>", self.__on_theme_changed, "+")

    def bind_widget(self, widget: Misc, *, penetration_state: bool = False) -> None:
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
        self.__bound_widgets[widget] = _BoundWidget(widget, penetration_state)

        if penetration_state:
            for sequence in _TRANSITION_STATE_EVENTS:
                widget.bind(sequence, self.__handle_state_transition, "+")
        else:
            for sequence in _UPDATE_STYLE_ONLY_EVENTS:
                widget.bind(sequence, self.__handle_style_update, "+")

        widget.bind("<Destroy>", self.__on_bound_widget_destroy, "+")

    def bind_text(
        self,
        text: Text,
        proxy: Optional[Text] = None,
        *,
        enable_inactive_select: bool = True,
        enable_t_entry_database_compat: bool = True,
    ) -> None:
        """
        Bind a text widget to the frame.

        :param text: Text widget instance
        :param proxy: Optional proxy text (can be a super widget of text)
        :param enable_inactive_select: Display selection when the widget is inactive
        :param enable_t_entry_database_compat: Compatibility with tk_setPalette

        .. note::
            This method configures the text widget with a flat style (no border or highlight),
            and binds it to the frame to receive state change events.
        """
        if proxy is None:
            proxy = text
        if not proxy.winfo_exists():
            raise ValueError(f"Text widget {proxy} does not exist or has been destroyed")
        self.__bound_text = _BoundText(
            text,
            proxy,
            enable_inactive_select=enable_inactive_select,
            enable_t_entry_database_compat=enable_t_entry_database_compat,
        )
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
                self.state(["focus", "active"])
            elif event.type == EventType.FocusOut:
                self.state(["!focus", "active"])
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
        self.__update_stateful_style_debounce()

    def __on_theme_changed(self, event: Event):
        if event.widget != self:
            return
        # Prevents style updates after widget destruction.
        self.update_style()

    def __lookup(self, option: str, *, state: Optional[Iterable[str]] = None, default: Any = None) -> Any:
        result = self.__style.lookup(self.cget("style"), option, state)
        if not result:  # Avoid ""
            return default
        return result

    def update_style(self) -> None:
        if bound_text := self.__bound_text:
            proxy = bound_text.proxy
            proxy.configure(
                selectbackground=self.__lookup("selectbackground", state=["focus"]),
                insertwidth=self.__lookup("insertwidth", state=["focus"], default=1),
                font=self.__lookup("font", default="TkDefaultFont"),
            )
            if bound_text.enable_inactive_select:
                proxy.configure(inactiveselectbackground=self.__lookup("selectbackground"))

            if text_padding := parse_padding(self.__lookup("textpadding")):
                proxy.grid(padx=text_padding.to_padx(), pady=text_padding.to_pady())
            else:
                proxy.grid(padx=0, pady=0)
        self.configure(
            padding=self.__lookup("padding", default="1"),
            borderwidth=self.__lookup("borderwidth", default="1"),
        )
        self.__update_stateful_style()

    def __update_stateful_style_debounce(self):
        if self.__update_stateful_style_task_id is not None:
            self.after_cancel(self.__update_stateful_style_task_id)
        self.__update_stateful_style_task_id = self.after_idle(self.__update_stateful_style)

    def __update_stateful_style(self):
        if self.__update_stateful_style_task_id is not None:
            self.after_cancel(self.__update_stateful_style_task_id)
            self.__update_stateful_style_task_id = None
        if self.__bound_text:
            state = self.state()
            self.__bound_text.proxy.configure(
                background=self.__lookup("fieldbackground", state=state),
                foreground=self.option_get("foreground", "TEntry")  # Compatible with tk_setPalette
                or self.__lookup("foreground", state=state),
                selectforeground=self.__lookup("selectforeground", state=state),
            )
