import logging

from .toolkit_enums import LengthType, PitchType, RoofSide

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



class ToolkitPitch:
    def __init__(self, pitch_type: PitchType, roof_side: RoofSide):
        # TODO: self._angle needs to be an EngineeringUnit class object.
        self._pitch_type = pitch_type
        self._roof_side = roof_side
        self._angle: float = 0.0

    def __repr__(self) -> str:
        return f"ToolkitPitch({self.pitch_type}, {self.roof_side}).angle({self.angle})"

    @property
    def angle(self) -> float:
        return self._angle

    @angle.setter
    def angle(self, value) -> None:
        # TODO: Need to verify and convert input.
        if not value:
            raise ValueError("Angle cannot be empty")
        self._angle = value

    @property
    def pitch_type(self) -> PitchType:
        return self._pitch_type

    @pitch_type.setter
    def pitch_type(self, pitch_type: PitchType) -> None:
        self._pitch_type = pitch_type

    @property
    def roof_side(self) -> RoofSide:
        return self._roof_side
