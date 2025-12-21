import logging
import re

from .toolkit_enums import LengthType

logger = logging.getLogger(name="livingspacetoolkit")


class ToolkitLength:

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

    def __init__(self, length_type: LengthType):
        self._length = 0
        self._length_type = length_type

    def __repr__(self) -> str:
        return f"ToolkitLength({self.length_type}).length({self.length})"

    def __eq__(self, other):
        if isinstance(other, ToolkitLength):
            return self.length_type == other.length_type and self.length == other.length
        return NotImplementedError

    def __lt__(self, other):
        if isinstance(other, ToolkitLength):
            return self.length_type == other.length_type and self.length < other.length
        return NotImplementedError

    def __gt__(self, other):
        if isinstance(other, ToolkitLength):
            return self.length_type == other.length_type and self.length > other.length
        return NotImplementedError

    def __add__(self, other):
        if isinstance(other, ToolkitLength):
            if self.length_type == other.length_type:
                return  self.length + other.length
            else:
                return ValueError("The length type must be the same.")
        return NotImplementedError

    def __sub__(self, other):
        if isinstance(other, ToolkitLength):
            if self.length_type == other.length_type:
                return  self.length - other.length
            else:
                return ValueError("The length type must be the same.")
        return NotImplementedError

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value) -> None:
        # TODO: Need to add verification logic
        if not value:
            raise ValueError("Length cannot be empty")
        if self._is_negative_measurement(value):
            raise ValueError(f"Length cannot be negative: {value}")
        self._length = self._parse_imperial_to_inches(value)

    @property
    def length_type(self) -> LengthType:
        return self._length_type



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

    def _is_negative_measurement(self, text: str) -> bool:
        return bool(self.NEGATIVE_MEASUREMENT_REGEX.match(text))
