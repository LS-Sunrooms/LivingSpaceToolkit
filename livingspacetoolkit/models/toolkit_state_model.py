import logging
from dataclasses import dataclass, field
from typing import Dict

from livingspacetoolkit.lib.toolkit_enums import (Scenario, RoofingType, EndCutType, SunroomType, LengthType, PitchType,
                                                  RoofSide)
from livingspacetoolkit.lib import ToolkitLength, ToolkitPitch


@dataclass()
class ToolkitStateModel:
    sunroom_type: SunroomType = SunroomType.STUDIO
    scenario: Scenario | None = None
    pitch: Dict[RoofSide, ToolkitPitch] = field(default_factory=lambda:{
        RoofSide.A_SIDE: ToolkitPitch(PitchType.RATIO, RoofSide.A_SIDE),
        RoofSide.B_SIDE: ToolkitPitch(PitchType.RATIO, RoofSide.B_SIDE),
        RoofSide.C_SIDE: ToolkitPitch(PitchType.RATIO, RoofSide.C_SIDE),
    })
    overhang: ToolkitLength = field(default_factory=lambda: ToolkitLength(LengthType.OVERHANG))
    roofing_type: RoofingType | None = None
    thickness: ToolkitLength = field(default_factory=lambda: ToolkitLength(LengthType.THICKNESS))
    end_cuts: EndCutType | None = None
    fascia: bool = False
    wall_heights: Dict[LengthType, ToolkitLength] = field(default_factory=lambda:{
        LengthType.PEAK_HEIGHT: ToolkitLength(LengthType.PEAK_HEIGHT),
        LengthType.MAX_HEIGHT: ToolkitLength(LengthType.MAX_HEIGHT),
        LengthType.DRIP_EDGE_HEIGHT: ToolkitLength(LengthType.DRIP_EDGE_HEIGHT),
        LengthType.A_SIDE_SOFFIT_HEIGHT: ToolkitLength(LengthType.A_SIDE_SOFFIT_HEIGHT),
        LengthType.B_SIDE_SOFFIT_HEIGHT: ToolkitLength(LengthType.B_SIDE_SOFFIT_HEIGHT),
        LengthType.C_SIDE_SOFFIT_HEIGHT: ToolkitLength(LengthType.C_SIDE_SOFFIT_HEIGHT),
        LengthType.A_WALL_HEIGHT: ToolkitLength(LengthType.A_WALL_HEIGHT),
        LengthType.B_WALL_HEIGHT: ToolkitLength(LengthType.B_WALL_HEIGHT),
        LengthType.C_WALL_HEIGHT: ToolkitLength(LengthType.C_WALL_HEIGHT),
    })
    floor_walls: Dict[LengthType, ToolkitLength] = field(default_factory=lambda: {
        LengthType.A_WALL_WIDTH: ToolkitLength(LengthType.A_WALL_WIDTH),
        LengthType.B_WALL_WIDTH: ToolkitLength(LengthType.B_WALL_WIDTH),
        LengthType.C_WALL_WIDTH: ToolkitLength(LengthType.C_WALL_WIDTH),
    })