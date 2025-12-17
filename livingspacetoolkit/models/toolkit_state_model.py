import logging
from dataclasses import dataclass, field
from typing import List

from livingspacetoolkit.lib.toolkit_enums import Scenario, RoofingType, EndCutType, SunroomType, LengthType
from livingspacetoolkit.lib.toolkit_input_class import ToolkitLength, ToolkitPitch


@dataclass()
class ToolkitStateModel:
    sunroom_type: SunroomType = SunroomType.STUDIO
    scenario: Scenario | None = None
    pitch: List[ToolkitPitch] = field(default_factory=list)
    overhang: ToolkitLength = field(default_factory=lambda: ToolkitLength(LengthType.OVERHANG))
    roofing_type: RoofingType | None = None
    thickness: ToolkitLength = field(default_factory=lambda: ToolkitLength(LengthType.THICKNESS))
    end_cuts: EndCutType | None = None
    fascia: bool = False
    wall_heights: List[ToolkitLength] = field(default_factory=list)
    floor_walls: List[ToolkitLength] = field(default_factory=lambda: [
        ToolkitLength(LengthType.A_WALL_WIDTH),
        ToolkitLength(LengthType.B_WALL_WIDTH),
        ToolkitLength(LengthType.C_WALL_WIDTH),
    ])