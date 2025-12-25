import logging
from dataclasses import dataclass, field
from typing import Dict

from livingspacetoolkit.lib.toolkit_enums import (SunroomType, LengthType, RoofSide)
from livingspacetoolkit.lib import ToolkitLength

logger = logging.getLogger(name="livingspacetoolkit")


@dataclass
class SunroomModel:
    sunroom_type: SunroomType = SunroomType.STUDIO
    max_panel_length: Dict[RoofSide, bool] = field(default_factory=lambda:{
        RoofSide.A_SIDE: False,
        RoofSide.B_SIDE: False,
        RoofSide.C_SIDE: False
    })
    panel_tolerance: Dict[RoofSide, bool] = field(default_factory=lambda:{
        RoofSide.A_SIDE: False,
        RoofSide.B_SIDE: False,
        RoofSide.C_SIDE: False
    })
    panel_length: Dict[RoofSide, ToolkitLength] = field(default_factory=lambda:{
        RoofSide.A_SIDE: ToolkitLength(LengthType.PANEL),
        RoofSide.B_SIDE: ToolkitLength(LengthType.PANEL),
        RoofSide.C_SIDE: ToolkitLength(LengthType.PANEL)
    })
    roof_area: Dict[RoofSide, int] = field(default_factory=lambda:{
        RoofSide.A_SIDE: 0,
        RoofSide.B_SIDE: 0,
        RoofSide.C_SIDE: 0
    })
    roof_panels: Dict[RoofSide, float] = field(default_factory=lambda:{
        RoofSide.A_SIDE: 0.0,
        RoofSide.B_SIDE: 0.0,
        RoofSide.C_SIDE: 0.0
    })
    roof_panels_split: Dict[RoofSide, bool] = field(default_factory=lambda:{
        RoofSide.A_SIDE: False,
        RoofSide.B_SIDE: False,
        RoofSide.C_SIDE: False
    })
    roof_overhang: Dict[RoofSide, Dict[str,ToolkitLength|bool]] = field(default_factory=lambda:{
        RoofSide.A_SIDE: {'value': ToolkitLength(LengthType.OVERHANG), "short_check": False, "long_check": False},
        RoofSide.B_SIDE: {'value': ToolkitLength(LengthType.OVERHANG), "short_check": False, "long_check": False},
        RoofSide.C_SIDE: {'value': ToolkitLength(LengthType.OVERHANG), "short_check": False, "long_check": False}
    })
    hang_rails: Dict[RoofSide, Dict[str,ToolkitLength|bool]] = field(default_factory=lambda:{
        RoofSide.A_SIDE: {'value': ToolkitLength(LengthType.HANG_RAIL), "max_length": False},
        RoofSide.B_SIDE: {'value': ToolkitLength(LengthType.HANG_RAIL), "max_length": False},
        RoofSide.C_SIDE: {'value': ToolkitLength(LengthType.HANG_RAIL), "max_length": False}
    })
    fascia: Dict[RoofSide, Dict[str,ToolkitLength|bool]] = field(default_factory=lambda:{
        RoofSide.A_SIDE: {'value': ToolkitLength(LengthType.FASCIA), "max_length": False},
        RoofSide.B_SIDE: {'value': ToolkitLength(LengthType.FASCIA), "max_length": False},
        RoofSide.C_SIDE: {'value': ToolkitLength(LengthType.FASCIA), "max_length": False}
    })
    armstrong_panels: int = 0

    def default_state(self, sunroom: SunroomType):
        logger.debug(f"Setting sunroom model to default state for {sunroom.name} sunroom.")
        self.sunroom_type = sunroom
        for roof_side in RoofSide:
            self.max_panel_length[roof_side] = False
            self.panel_tolerance[roof_side] = False
            self.panel_length[roof_side].length = '0'
            self.roof_area[roof_side] = 0
            self.roof_panels[roof_side] = 0.0
            self.roof_panels_split[roof_side] = False
            self.roof_overhang[roof_side]['value'].length = '0'
            self.roof_overhang[roof_side]['short_check'] = False
            self.roof_overhang[roof_side]['long_check'] = False
            self.hang_rails[roof_side]['value'].length = '0'
            self.hang_rails[roof_side]['max_length'] = False
            self.fascia[roof_side]['value'].length = '0'
            self.fascia[roof_side]['max_length'] = False
            self.armstrong_panels = 0