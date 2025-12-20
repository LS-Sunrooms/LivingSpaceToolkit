import logging

from .toolkit_enums import LengthType

logger = logging.getLogger(name="livingspacetoolkit")


class ToolkitLength:
    def __init__(self, length_type: LengthType):
        # TODO: self._length needs to be an EngineeringUnit class object.
        self._length = ''
        self._length_type = length_type

    def __repr__(self) -> str:
        return f"ToolkitLength({self.length_type}).length({self.length})"

    def __eq__(self, other):
        if isinstance(other, ToolkitLength):
            return self.length_type == other.length_type and self.length == other.length
        return NotImplementedError

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value) -> None:
        # TODO: Need to add verification logic
        if not value:
            raise ValueError("Length cannot be empty")
        self._length = value

    @property
    def length_type(self) -> LengthType:
        return self._length_type