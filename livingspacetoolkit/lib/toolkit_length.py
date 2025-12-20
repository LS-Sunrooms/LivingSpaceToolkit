import logging
import re

from .toolkit_enums import LengthType

logger = logging.getLogger(name="livingspacetoolkit")


class ToolkitLength:
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
        self._length = self._convert_to_inches(value)

    @property
    def length_type(self) -> LengthType:
        return self._length_type


    @staticmethod
    def _feet_search(text) -> bool:
        return 'ft' in text or "'" in text or 'feet' in text

    @staticmethod
    def _inch_search(text) -> bool:
        return 'in' in text or '"' in text

    def _convert_to_inches(self, measurement) -> float:
        feet = re.compile(r'(\d*\s*)[\'|ft|fe+t]')
        fract = re.compile(r'(\d*\s?)(\d+\/\d+)')
        ft_or_in = re.compile(r'(\d*\.\d+|\d+)\s?[\"|in|\'|ft|feet]')
        in_fract = re.compile(r'(\d*\s?)(\d+\/\d+)')
        ft_and_in = re.compile(r'(\d+\.?\d*)(\D+)(\d+\.?\d*)')
        ft_and_in_fract = re.compile(r'(\d+\.?\d*)(\s?\d+\/\d+)*(\s?\D+\s?)(\d*\.?\d*)(\s?\d+\/\d+)*')
        base = 0
        try:
            if self._feet_search(measurement) and self._inch_search(measurement):
                c = ft_and_in_fract.search(measurement)
                aa = eval(c.group(1)) * 12
                if c.group(2) is None:
                    bb = 0
                else:
                    bb = eval(c.group(2)) * 12
                cc = eval(c.group(4))
                if c.group(5) is None:
                    dd = 0
                else:
                    dd = eval(c.group(5))
                base = aa + bb + cc + dd
            elif self._feet_search(measurement) or self._inch_search(measurement):
                if self._feet_search(measurement):
                    if '/' in measurement:
                        c = fract.search(measurement)
                        if c.group(1) == '':
                            base = eval(c.group(2)) * 12
                        else:
                            base = (eval(c.group(1)) + eval(c.group(2))) * 12
                    else:
                        c = feet.search(measurement)
                        base = eval(c.group(1)) * 12
                if self._inch_search(measurement):
                    if "/" in measurement:
                        c = in_fract.search(measurement)
                        if c.group(1) == '':
                            base = eval(c.group(2))
                        else:
                            base = eval(c.group(1)) + eval(c.group(2))
                    else:
                        c = ft_or_in.search(measurement)
                        base = eval(c.group(1))
            else:
                if fract.search(measurement) is None:
                    if ft_and_in.search(measurement) is None:
                        base = eval(measurement)
                    else:
                        c = ft_and_in.search(measurement)
                        base = eval(c.group(1)) * 12 + eval(c.group(3))
                else:
                    c = ft_and_in_fract.search(measurement)
                    if c.group(3) == '':
                        base = eval(c.group(1)) * 12 + eval(c.group(4))
                    else:
                        base = eval(c.group(1)) * 12 + eval(c.group(3)) + eval(c.group(4))
            base = float(base)
        except AttributeError:
            raise
        except TypeError:
            raise
        return base