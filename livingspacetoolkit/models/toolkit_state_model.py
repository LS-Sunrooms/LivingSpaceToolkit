from dataclasses import dataclass, field
from typing import Dict, List

from livingspacetoolkit.config.log_config import logger
from livingspacetoolkit.lib.toolkit_enums import (Scenario, RoofingType, EndCutType, SunroomType, LengthType, PitchType,
                                                  SunroomSide)
from livingspacetoolkit.lib import ToolkitLength, ToolkitPitch


@dataclass()
class ToolkitStateModel:
    """This model records the user input from the GUI. The input recorded is dependent on the scenario selected. This is
    also where the sunroom heights and roof pitch is saved from calculations made from each scenario class."""
    sunroom_type: SunroomType = SunroomType.STUDIO
    scenario: Scenario | None = None
    pitch: Dict[SunroomSide, ToolkitPitch] = field(default_factory=lambda:{
        SunroomSide.A_SIDE: ToolkitPitch(PitchType.RATIO, SunroomSide.A_SIDE),
        SunroomSide.B_SIDE: ToolkitPitch(PitchType.RATIO, SunroomSide.B_SIDE),
        SunroomSide.C_SIDE: ToolkitPitch(PitchType.RATIO, SunroomSide.C_SIDE),
    })
    overhang: ToolkitLength = field(default_factory=lambda: ToolkitLength(LengthType.OVERHANG))
    roofing_type: RoofingType | None = None
    thickness: ToolkitLength = field(default_factory=lambda: ToolkitLength(LengthType.THICKNESS))
    end_cuts: EndCutType | None = None
    fascia: bool = False
    wall_heights: Dict[tuple[SunroomSide | None, LengthType], ToolkitLength] = field(default_factory=lambda:{
        (None,LengthType.PEAK_HEIGHT): ToolkitLength(LengthType.PEAK_HEIGHT),
        (None,LengthType.MAX_HEIGHT): ToolkitLength(LengthType.MAX_HEIGHT),
        (SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT): ToolkitLength(LengthType.DRIP_EDGE_HEIGHT,
                                                                         SunroomSide.A_SIDE),
        (SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT): ToolkitLength(LengthType.DRIP_EDGE_HEIGHT,
                                                                         SunroomSide.B_SIDE),
        (SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT): ToolkitLength(LengthType.DRIP_EDGE_HEIGHT,
                                                                         SunroomSide.C_SIDE),
        (SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT): ToolkitLength(LengthType.SOFFIT_HEIGHT, SunroomSide.A_SIDE),
        (SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT): ToolkitLength(LengthType.SOFFIT_HEIGHT, SunroomSide.B_SIDE),
        (SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT): ToolkitLength(LengthType.SOFFIT_HEIGHT, SunroomSide.C_SIDE),
        (SunroomSide.A_SIDE, LengthType.WALL_HEIGHT): ToolkitLength(LengthType.WALL_HEIGHT, SunroomSide.A_SIDE),
        (SunroomSide.B_SIDE, LengthType.WALL_HEIGHT): ToolkitLength(LengthType.WALL_HEIGHT, SunroomSide.B_SIDE),
        (SunroomSide.C_SIDE, LengthType.WALL_HEIGHT): ToolkitLength(LengthType.WALL_HEIGHT,SunroomSide.C_SIDE),
    })
    floor_walls: Dict[SunroomSide, ToolkitLength] = field(default_factory=lambda: {
        SunroomSide.A_SIDE: ToolkitLength(LengthType.WALL_WIDTH, SunroomSide.A_SIDE),
        SunroomSide.B_SIDE: ToolkitLength(LengthType.WALL_WIDTH, SunroomSide.B_SIDE),
        SunroomSide.C_SIDE: ToolkitLength(LengthType.WALL_WIDTH, SunroomSide.C_SIDE),
    })

    def default_state(self, sunroom: SunroomType|None = None, scenario: Scenario|None = None) -> None:
        if sunroom is None:
            self.sunroom_type = SunroomType.STUDIO
        else:
            self.sunroom_type = sunroom
        self.scenario = scenario
        for sunroom_side in self.pitch:
            self.pitch[sunroom_side].pitch_type = PitchType.RATIO
            self.pitch[sunroom_side].pitch_value = 0
            self.pitch[sunroom_side].modified = False
        self.overhang.length = 0
        self.overhang.modified = False
        self.roofing_type = None
        self.thickness.length = 0
        self.thickness.modified = False
        self.end_cuts = None
        self.fascia = False
        for sunroom_side in self.wall_heights:
            self.wall_heights[sunroom_side].length = 0
            self.wall_heights[sunroom_side].modified = False
        for sunroom_side in self.floor_walls:
            self.floor_walls[sunroom_side].length = 0
            self.floor_walls[sunroom_side].modified = False

    def check_calculation_ready(self) -> None:
        if self.scenario is None:
            raise TypeError("Please select a scenario.")
        if self.roofing_type is None:
            raise TypeError("Please select a roofing type.")
        if self.end_cuts is None:
            raise TypeError("Please select an end cut type.")
        if not self.overhang.modified:
            raise TypeError(f"Please input a value for the {self.overhang.length_type.name}.")
        if not self.thickness.modified:
            raise TypeError(f"Please input a value for the {self.thickness.length_type.name}.")
        for sunroom_side in self.floor_walls:
            if not self.floor_walls[sunroom_side].modified:
                raise TypeError(f"Please input a value for the {sunroom_side.name} WALL_HEIGHT.")
        pitch_list: List[SunroomSide] = []
        wall_height_list: List[tuple[SunroomSide|None, LengthType]] = []
        match self.scenario:
            case Scenario.WALL_HEIGHT_PITCH:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        pitch_list.append(SunroomSide.B_SIDE)
                        wall_height_list.append((SunroomSide.B_SIDE, LengthType.WALL_HEIGHT))
                    case SunroomType.CATHEDRAL:
                        pitch_list.append(SunroomSide.A_SIDE)
                        pitch_list.append(SunroomSide.C_SIDE)
                        wall_height_list.append((SunroomSide.A_SIDE, LengthType.WALL_HEIGHT))
                        wall_height_list.append((SunroomSide.C_SIDE, LengthType.WALL_HEIGHT))
            case Scenario.WALL_HEIGHT_PEAK_HEIGHT:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        wall_height_list.append((SunroomSide.B_SIDE, LengthType.WALL_HEIGHT))
                    case SunroomType.CATHEDRAL:
                        wall_height_list.append((SunroomSide.A_SIDE, LengthType.WALL_HEIGHT))
                        wall_height_list.append((SunroomSide.C_SIDE, LengthType.WALL_HEIGHT))
                wall_height_list.append((None, LengthType.PEAK_HEIGHT))
            case Scenario.MAX_HEIGHT_PITCH:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        pitch_list.append(SunroomSide.B_SIDE)
                    case SunroomType.CATHEDRAL:
                        pitch_list.append(SunroomSide.A_SIDE)
                        pitch_list.append(SunroomSide.C_SIDE)
                wall_height_list.append((None, LengthType.MAX_HEIGHT))
            case Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        wall_height_list.append((SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT))
                    case SunroomType.CATHEDRAL:
                        wall_height_list.append((SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT))
                        wall_height_list.append((SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT))
                wall_height_list.append((None, LengthType.PEAK_HEIGHT))
            case Scenario.SOFFIT_HEIGHT_PITCH:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        pitch_list.append(SunroomSide.B_SIDE)
                        wall_height_list.append((SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT))
                    case SunroomType.CATHEDRAL:
                        pitch_list.append(SunroomSide.A_SIDE)
                        pitch_list.append(SunroomSide.C_SIDE)
                        wall_height_list.append((SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT))
                        wall_height_list.append((SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT))
            case Scenario.DRIP_EDGE_PEAK_HEIGHT:
                wall_height_list.append((None, LengthType.PEAK_HEIGHT))
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        wall_height_list.append((SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT))
                    case SunroomType.CATHEDRAL:
                        wall_height_list.append((SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT))
                        wall_height_list.append((SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT))
            case Scenario.DRIP_EDGE_PITCH:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        pitch_list.append(SunroomSide.B_SIDE)
                        wall_height_list.append((SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT))
                    case SunroomType.CATHEDRAL:
                        pitch_list.append(SunroomSide.A_SIDE)
                        pitch_list.append(SunroomSide.C_SIDE)
                        wall_height_list.append((SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT))
                        wall_height_list.append((SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT))
        if len(pitch_list) > 0:
            for sunroom_side in pitch_list:
                if not self.pitch[sunroom_side].modified:
                    raise TypeError(f"Please input a value for the {sunroom_side.name} pitch.")
        if len(wall_height_list) > 0:
            for sunroom_side in wall_height_list:
                if not self.wall_heights[sunroom_side].modified:
                    if sunroom_side[0] is None:
                        raise TypeError(f"Please input a value for the {sunroom_side[1].name}.")
                    else:
                        raise TypeError(f"Please input a value for the {sunroom_side[0].name} {sunroom_side[1].name}.")
