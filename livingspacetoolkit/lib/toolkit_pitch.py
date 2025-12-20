import logging

from .toolkit_enums import PitchType, RoofSide

logger = logging.getLogger(name="livingspacetoolkit")


class ToolkitPitch:
    def __init__(self, pitch_type: PitchType, roof_side: RoofSide):
        # TODO: self._angle needs to be an EngineeringUnit class object.
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
    def pitch_value(self, value) -> None:
        # TODO: Need to verify and convert input.
        if not value:
            raise ValueError("Angle/Ratio cannot be empty")
        self._pitch_value = value

    @property
    def pitch_type(self) -> PitchType:
        return self._pitch_type

    @pitch_type.setter
    def pitch_type(self, pitch_type: PitchType) -> None:
        self._pitch_type = pitch_type

    @property
    def roof_side(self) -> RoofSide:
        return self._roof_side