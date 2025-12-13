import logging
from dataclasses import dataclass, field
from typing import Dict

from livingspacetoolkit.lib.livingspacetoolkit_enums import Scenario, RoofingType, PitchType, EndCutType, SunroomType


@dataclass()
class ToolkitState:
    sunroom_type: SunroomType = SunroomType.STUDIO
    scenario: Scenario | None = None
    pitch: Dict[str, PitchType] | None = None
    pitch_value: Dict[str, str] | None = None
    overhang: str = ''
    roofing_type: RoofingType | None = None
    thickness: str = ''
    end_cuts: EndCutType | None = None
    fascia: bool = False
    wall_heights: Dict[str, str] | None = None
    floor_walls: Dict[str, str] = field(default_factory=lambda: {
        'a_wall': '',
        'b_wall': '',
        'c_wall': '',
    })