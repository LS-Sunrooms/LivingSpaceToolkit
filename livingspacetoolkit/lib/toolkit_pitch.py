import logging
import re
from math import atan, radians

from .toolkit_enums import PitchType, RoofSide

logger = logging.getLogger(name="livingspacetoolkit")


class ToolkitPitch:
    ANGLE_REGEX = re.compile(
        r"""
        ^\s*
        (?P<value>\d+(?:\.\d+)?)   # Integer or decimal number
        \s*
        (?:deg)?                   # Optional 'deg'
        \s*$
        """,
        re.IGNORECASE | re.VERBOSE
    )

    NUMBER_REGEX = re.compile(
        r"""
        ^\s*
        (?:
            # Mixed number: 1 1/2
            (?P<whole>\d+)\s+(?P<num>\d+)\s*/\s*(?P<den>\d+)
            |
            # Fraction only: 1/2
            (?P<fnum>\d+)\s*/\s*(?P<fden>\d+)
            |
            # Decimal or integer
            (?P<dec>\d+(?:\.\d+)?)
        )
        \s*$
        """,
        re.VERBOSE
    )

    NEGATIVE_INPUT_REGEX = re.compile(r"^\s*-\s*\d")
    def __init__(self, pitch_type: PitchType, roof_side: RoofSide):
        self._pitch_type = pitch_type
        self._roof_side = roof_side
        self._pitch_value: float = 0.0

    def __repr__(self) -> str:
        return f"ToolkitPitch({self.pitch_type}, {self.roof_side}).pitch_value({self.pitch_value})"

    def __eq__(self, other):
        if isinstance(other, ToolkitPitch):
            return (self.pitch_type == other.pitch_type and self.roof_side == other.roof_side
                    and self.pitch_value == other.pitch_value)
        return NotImplementedError

    def __lt__(self, other):
        if isinstance(other, ToolkitPitch):
            return (self.pitch_type == other.pitch_type and self.roof_side == other.roof_side
                    and self.pitch_value < other.pitch_value)
        return NotImplementedError

    def __gt__(self, other):
        if isinstance(other, ToolkitPitch):
            return (self.pitch_type == other.pitch_type and self.roof_side == other.roof_side
                    and self.pitch_value > other.pitch_value)
        return NotImplementedError

    def __add__(self, other):
        if isinstance(other, ToolkitPitch):
            if self.pitch_type == other.pitch_type and self.roof_side == other.roof_side:
                return self.pitch_value + other.pitch_value
            else:
                return ValueError("The pitch type and roof sides must be the same.")
        return NotImplementedError

    def __sub__(self, other):
        if isinstance(other, ToolkitPitch):
            if self.pitch_type == other.pitch_type and self.roof_side == other.roof_side:
                return self.pitch_value - other.pitch_value
            else:
                return ValueError("The pitch type and roof sides must be the same.")
        return NotImplementedError

    @property
    def pitch_value(self) -> float:
        return self._pitch_value

    @pitch_value.setter
    def pitch_value(self, value: str) -> None:
        if not value:
            raise ValueError("Angle/Ratio cannot be empty")
        if self._is_negative_input(value):
            raise ValueError(f"Input cannot be negative: {value}")
        match self.pitch_type:
            case PitchType.ANGLE:
                angle = self.parse_angle(value)
                if angle >= 60:
                    raise ValueError(f"Angle is too high: {angle}")
                self._pitch_value = radians(angle)
            case PitchType.RATIO:
                ratio = self.parse_number(value)
                if ratio >= 21:
                    raise ValueError(f"Ratio is too high: {ratio}")
                self._pitch_value = atan(ratio/12)

    @property
    def pitch_type(self) -> PitchType:
        return self._pitch_type

    @pitch_type.setter
    def pitch_type(self, pitch_type: PitchType) -> None:
        self._pitch_type = pitch_type

    @property
    def roof_side(self) -> RoofSide:
        return self._roof_side

    def parse_angle(self, text: str) -> float:
        m = self.ANGLE_REGEX.match(text)
        if not m:
            raise ValueError(f"Invalid angle format: {text}")
        return float(m.group("value"))

    def parse_number(self, text: str) -> float:
        m = self.NUMBER_REGEX.match(text)
        if not m:
            raise ValueError(f"Invalid number format: {text}")

        if m.group("dec"):
            return float(m.group("dec"))

        if m.group("whole"):
            return int(m.group("whole")) + int(m.group("num")) / int(m.group("den"))

        return int(m.group("fnum")) / int(m.group("fden"))

    def _is_negative_input(self, text: str) -> bool:
        return bool(self.NEGATIVE_INPUT_REGEX.match(text))