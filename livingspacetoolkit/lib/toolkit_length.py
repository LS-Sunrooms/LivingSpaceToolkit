import re

from .toolkit_enums import LengthType, SunroomSide
from livingspacetoolkit.config.log_config import logger


class ToolkitLength:
    """This class is used for all length calculations. It includes regex to convert imperial units into inches, the
    ability to determine which side sunroom the length is for, and what type of feature the length is for."""

    IMPERIAL_REGEX = re.compile(
        r"""
        ^\s*

        # -------- FEET (optional) --------
        (?:
            (?:(?P<f_whole>\d+)\s+)?                 
            (?:
                (?P<f_num>\d+)\s*/\s*(?P<f_den>\d+)  
                |
                (?P<f_int>\d+)                       
            )
            \s*
            (?:'|ft\.?|feet)
        )?

        \s*

        # -------- OPTIONAL SEPARATOR --------
        (?:
            \s*(?:-|–|—|to)\s*
        )?

        # -------- INCHES (optional) --------
        (?:
            (?:(?P<i_whole>\d+)\s+)?                 
            (?:
                (?P<i_num>\d+)\s*/\s*(?P<i_den>\d+)  
                |
                (?P<i_int>\d+)                       
            )
            \s?
            (?:"|in\.?|inches|inch)?
        )?

        \s*$
        """,
        re.IGNORECASE | re.VERBOSE
    )
    BARE_NUMBER_REGEX = re.compile(
    r"""
    ^\s*
    (?P<value>\d+(?:\.\d+)?)     # Integer or decimal
    \s*
    (?:"|in\.?|inches)?          # Optional inches unit
    \s*$
    """,
    re.IGNORECASE | re.VERBOSE
    )
    NEGATIVE_MEASUREMENT_REGEX = re.compile(r"^\s*-\s*\d")

    def __init__(self, length_type: LengthType, sunroom_side: SunroomSide | None = None):
        self._length: float = 0
        self._length_type = length_type
        self._sunroom_side = sunroom_side
        self._modified: bool = False

    def __repr__(self) -> str:
        return f"ToolkitLength({self.length_type}, {self.sunroom_side}).length({self.length})"

    def __eq__(self, other):
        if isinstance(other, ToolkitLength):
            return (self.length_type == other.length_type and self.sunroom_side == other.sunroom_side
                    and self.length == other.length)
        return NotImplementedError

    def __lt__(self, other):
        if isinstance(other, ToolkitLength):
            return (self.length_type == other.length_type and self.sunroom_side == other.sunroom_side
                    and self.length < other.length)
        return NotImplementedError

    def __gt__(self, other):
        if isinstance(other, ToolkitLength):
            return (self.length_type == other.length_type and self.sunroom_side == other.sunroom_side
                    and self.length > other.length)
        return NotImplementedError

    def __add__(self, other):
        if isinstance(other, ToolkitLength):
            if self.length_type == other.length_type and self.sunroom_side == other.sunroom_side:
                return  self.length + other.length
            else:
                return ValueError("The length type and sunroom side must be the same.")
        return NotImplementedError

    def __sub__(self, other):
        if isinstance(other, ToolkitLength):
            if self.length_type == other.length_type and self.sunroom_side == other.sunroom_side:
                return  self.length - other.length
            else:
                return ValueError("The length type and sunroom side must be the same.")
        return NotImplementedError

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value: str|float|int) -> None:
        if isinstance(value, str) and not value:
            raise ValueError("Length cannot be empty")
        if self._is_negative_measurement(value):
            raise ValueError(f"Length cannot be negative: {value}")
        self._length = self._check_business_logic(value)
        self.modified = True

    @property
    def length_type(self) -> LengthType:
        return self._length_type

    @property
    def sunroom_side(self) -> SunroomSide:
        return self._sunroom_side

    @sunroom_side.setter
    def sunroom_side(self, value: SunroomSide) -> None:
        self._sunroom_side = value

    @property
    def modified(self) -> bool:
        return self._modified

    @modified.setter
    def modified(self, value: bool) -> None:
        self._modified = value

    def _parse_imperial_to_inches(self, text: str) -> float:
        # ---- Case 1: Bare number → inches ----
        m = self.BARE_NUMBER_REGEX.match(text)
        if m:
            return float(m.group("value"))
        # ---- Case 2: Imperial measurement ----
        match = self.IMPERIAL_REGEX.match(text)
        if not match:
            raise ValueError(f"Invalid imperial format: {text}")

        def to_float(whole, num, den, integer):
            value = 0.0
            if integer:
                value += float(integer)
            if num and den:
                value += int(num) / int(den)
            if whole:
                value += int(whole)
            return value

        feet = to_float(
            match.group("f_whole"),
            match.group("f_num"),
            match.group("f_den"),
            match.group("f_int"),
        )

        inches = to_float(
            match.group("i_whole"),
            match.group("i_num"),
            match.group("i_den"),
            match.group("i_int"),
        )

        return feet * 12 + inches

    def _is_negative_measurement(self, value: str|float|int) -> bool:
        if isinstance(value, float|int):
            value = str(value) # Just turn it into a string and keep it simple.
        return bool(self.NEGATIVE_MEASUREMENT_REGEX.match(value))

    def _check_business_logic(self, value: str|float|int) -> float:
        if isinstance(value, float|int):
            value = str(value)
        length = self._parse_imperial_to_inches(value)
        if self.length_type == LengthType.HANG_RAIL and length > 216:
            # Business logic. Hang rails and Fascia cannot exceed 216". Raise a ValueError, divide them in half,
            # try again
            logger.warning(f"The hang rails are too long: {length}")
            raise ValueError("Hang rails are too long. Divide them in half")
        elif self.length_type == LengthType.FASCIA and length > 216:
            logger.warning(f"The fascia is too long: {length}")
            raise ValueError("Fascia is too long. Divide them in half")
        elif self.length_type == LengthType.PANEL and length > 288:
            # Business logic. The maximum panel length is 288 in.
            logger.warning(f"The panel length has exceeded the max allowable: {length}")
            raise ValueError("The panel length has exceeded the max allowable.")
        else:
            return length
