from collections.abc import Sequence
from typing import NamedTuple, Optional, Tuple, Union

ScreenDistance = Union[float, str]


class Padding(NamedTuple):
    left: ScreenDistance
    top: ScreenDistance
    right: ScreenDistance
    bottom: ScreenDistance

    def to_padx(self) -> Tuple[ScreenDistance, ScreenDistance]:
        return self.left, self.right

    def to_pady(self) -> Tuple[ScreenDistance, ScreenDistance]:
        return self.top, self.bottom


def parse_padding(value: Union[ScreenDistance, Tuple[ScreenDistance, ...], None]) -> Optional[Padding]:
    if value is None:
        return None

    if isinstance(value, int) or isinstance(value, float):
        return Padding(value, value, value, value)

    parts: Sequence[ScreenDistance] = value.split() if isinstance(value, str) else value
    padding = (*parts, None, None, None, None)

    left = padding[0] if padding[0] is not None else 0
    top = padding[1] if padding[1] is not None else left
    right = padding[2] if padding[2] is not None else left
    bottom = padding[3] if padding[3] is not None else top
    return Padding(left, top, right, bottom)
