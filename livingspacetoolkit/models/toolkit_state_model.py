import logging
from dataclasses import dataclass, field
from typing import Dict, List

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

    def default_state(self) -> None:
        self.sunroom_type = SunroomType.STUDIO
        self.scenario = None
        for roof_side in self.pitch:
            self.pitch[roof_side].pitch_type = PitchType.RATIO
            self.pitch[roof_side].pitch_value = 0
            self.pitch[roof_side].modified = False
        self.overhang.length = 0
        self.overhang.modified = False
        self.roofing_type = None
        self.thickness.length = 0
        self.thickness.modified = False
        self.end_cuts = None
        self.fascia = False
        for length_type in self.wall_heights:
            self.wall_heights[length_type].length = 0
            self.wall_heights[length_type].modified = False
        for length_type in self.floor_walls:
            self.floor_walls[length_type].length = 0
            self.floor_walls[length_type].modified = False

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
        for wall in self.floor_walls:
            if not self.floor_walls[wall].modified:
                raise TypeError(f"Please input a value for the {wall.name}.")
        pitch_list: List[RoofSide] = []
        wall_height_list: List[LengthType] = []
        match self.scenario:
            case Scenario.WALL_HEIGHT_PITCH:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        pitch_list.append(RoofSide.B_SIDE)
                        wall_height_list.append(LengthType.B_WALL_HEIGHT)
                    case SunroomType.CATHEDRAL:
                        pitch_list.append(RoofSide.A_SIDE)
                        pitch_list.append(RoofSide.C_SIDE)
                        wall_height_list.append(LengthType.A_WALL_HEIGHT)
                        wall_height_list.append(LengthType.C_WALL_HEIGHT)
            case Scenario.WALL_HEIGHT_PEAK_HEIGHT:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        wall_height_list.append(LengthType.B_WALL_HEIGHT)
                    case SunroomType.CATHEDRAL:
                        wall_height_list.append(LengthType.A_WALL_HEIGHT)
                        wall_height_list.append(LengthType.C_WALL_HEIGHT)
                wall_height_list.append(LengthType.PEAK_HEIGHT)
            case Scenario.MAX_HEIGHT_PITCH:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        pitch_list.append(RoofSide.B_SIDE)
                    case SunroomType.CATHEDRAL:
                        pitch_list.append(RoofSide.A_SIDE)
                        pitch_list.append(RoofSide.C_SIDE)
                wall_height_list.append(LengthType.MAX_HEIGHT)
            case Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        wall_height_list.append(LengthType.B_SIDE_SOFFIT_HEIGHT)
                    case SunroomType.CATHEDRAL:
                        wall_height_list.append(LengthType.A_SIDE_SOFFIT_HEIGHT)
                        wall_height_list.append(LengthType.C_SIDE_SOFFIT_HEIGHT)
                wall_height_list.append(LengthType.PEAK_HEIGHT)
            case Scenario.SOFFIT_HEIGHT_PITCH:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        pitch_list.append(RoofSide.B_SIDE)
                        wall_height_list.append(LengthType.B_SIDE_SOFFIT_HEIGHT)
                    case SunroomType.CATHEDRAL:
                        pitch_list.append(RoofSide.A_SIDE)
                        pitch_list.append(RoofSide.C_SIDE)
                        wall_height_list.append(LengthType.A_SIDE_SOFFIT_HEIGHT)
                        wall_height_list.append(LengthType.C_SIDE_SOFFIT_HEIGHT)
            case Scenario.DRIP_EDGE_PEAK_HEIGHT:
                wall_height_list.append(LengthType.PEAK_HEIGHT)
                wall_height_list.append(LengthType.DRIP_EDGE_HEIGHT)
            case Scenario.DRIP_EDGE_PITCH:
                match self.sunroom_type:
                    case SunroomType.STUDIO:
                        pitch_list.append(RoofSide.B_SIDE)
                    case SunroomType.CATHEDRAL:
                        pitch_list.append(RoofSide.A_SIDE)
                        pitch_list.append(RoofSide.C_SIDE)
                wall_height_list.append(LengthType.DRIP_EDGE_HEIGHT)
        if len(pitch_list) > 0:
            for roof_side in pitch_list:
                if not self.pitch[roof_side].modified:
                    raise TypeError(f"Please input a value for the {roof_side.name} pitch.")
        if len(wall_height_list) > 0:
            for length_type in wall_height_list:
                if not self.wall_heights[length_type].modified:
                    raise TypeError(f"Please input a value for the {length_type.name}.")
