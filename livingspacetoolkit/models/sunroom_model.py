from dataclasses import dataclass, field
from typing import Dict, List

from livingspacetoolkit.config.log_config import logger
from livingspacetoolkit.lib.toolkit_enums import LengthType, SunroomSide
from livingspacetoolkit.lib import ToolkitLength



@dataclass
class SunroomModel:
    """This model records roof configuration data as it is calculated. The calculations are done with the scenario
    classes and the SunroomBuilder class."""
    max_panel_length: Dict[SunroomSide, bool] = field(default_factory=lambda:{
        SunroomSide.A_SIDE: False,
        SunroomSide.B_SIDE: False,
        SunroomSide.C_SIDE: False
    })
    panel_tolerance: Dict[SunroomSide, bool] = field(default_factory=lambda:{
        SunroomSide.A_SIDE: False,
        SunroomSide.B_SIDE: False,
        SunroomSide.C_SIDE: False
    })
    panel_length: Dict[SunroomSide, ToolkitLength] = field(default_factory=lambda:{
        SunroomSide.A_SIDE: ToolkitLength(LengthType.PANEL),
        SunroomSide.B_SIDE: ToolkitLength(LengthType.PANEL),
        SunroomSide.C_SIDE: ToolkitLength(LengthType.PANEL)
    })
    roof_area: Dict[SunroomSide, int] = field(default_factory=lambda:{
        SunroomSide.A_SIDE: 0,
        SunroomSide.B_SIDE: 0,
        SunroomSide.C_SIDE: 0
    })
    roof_panels: Dict[SunroomSide, float] = field(default_factory=lambda:{
        SunroomSide.A_SIDE: 0.0,
        SunroomSide.B_SIDE: 0.0,
        SunroomSide.C_SIDE: 0.0
    })
    roof_panels_split: Dict[SunroomSide, bool] = field(default_factory=lambda:{
        SunroomSide.A_SIDE: False,
        SunroomSide.B_SIDE: False,
        SunroomSide.C_SIDE: False
    })
    roof_overhang: Dict[SunroomSide, Dict[str, ToolkitLength | bool]] = field(default_factory=lambda:{
        SunroomSide.A_SIDE: {'value': ToolkitLength(LengthType.OVERHANG), "short_check": False, "long_check": False},
        SunroomSide.B_SIDE: {'value': ToolkitLength(LengthType.OVERHANG), "short_check": False, "long_check": False},
        SunroomSide.C_SIDE: {'value': ToolkitLength(LengthType.OVERHANG), "short_check": False, "long_check": False}
    })
    hang_rails: Dict[SunroomSide, Dict[str, ToolkitLength | bool]] = field(default_factory=lambda:{
        SunroomSide.A_SIDE: {'value': ToolkitLength(LengthType.HANG_RAIL), "max_length": False},
        SunroomSide.B_SIDE: {'value': ToolkitLength(LengthType.HANG_RAIL), "max_length": False},
        SunroomSide.C_SIDE: {'value': ToolkitLength(LengthType.HANG_RAIL), "max_length": False}
    })
    gable_wall: Dict[SunroomSide, ToolkitLength] = field(default_factory=lambda: {
        SunroomSide.A_SIDE: ToolkitLength(LengthType.WALL_WIDTH, SunroomSide.A_SIDE),
        SunroomSide.B_SIDE: ToolkitLength(LengthType.WALL_WIDTH, SunroomSide.B_SIDE),
        SunroomSide.C_SIDE: ToolkitLength(LengthType.WALL_WIDTH, SunroomSide.C_SIDE),
    })  # Used for roof panel calculations for cathedral.
    fascia: Dict[SunroomSide, Dict[str, List[ToolkitLength] | bool]] = field(default_factory=lambda:{
        SunroomSide.A_SIDE: {'value': [ToolkitLength(LengthType.FASCIA)], "max_length": False},
        SunroomSide.B_SIDE: {'value': [ToolkitLength(LengthType.FASCIA), ToolkitLength(LengthType.FASCIA)],
                             "max_length": False}, # Cathedral uses both, Studio use the first.
        SunroomSide.C_SIDE: {'value': [ToolkitLength(LengthType.FASCIA)], "max_length": False}
    })
    armstrong_panels: int = 0

    def default_state(self):
        logger.debug("Setting sunroom model to default state.")
        for roof_side in SunroomSide:
            self.max_panel_length[roof_side] = False
            self.panel_tolerance[roof_side] = False
            self.panel_length[roof_side].length = 0
            self.roof_area[roof_side] = 0
            self.roof_panels[roof_side] = 0.0
            self.roof_panels_split[roof_side] = False
            self.roof_overhang[roof_side]['value'].length = 0
            self.roof_overhang[roof_side]['short_check'] = False
            self.roof_overhang[roof_side]['long_check'] = False
            self.hang_rails[roof_side]['value'].length = 0
            self.hang_rails[roof_side]['max_length'] = False
            self.gable_wall[roof_side].length = 0
            for fascia in self.fascia[roof_side]['value']:
                [fascia].length = 0
            self.fascia[roof_side]['max_length'] = False
            self.armstrong_panels = 0