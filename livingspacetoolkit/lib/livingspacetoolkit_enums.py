from enum import Enum


class Scenario(Enum):
    WALL_HEIGHT_PITCH = 0
    WALL_HEIGHT_PEAK_HEIGHT = 1
    MAX_HEIGHT_PITCH = 2
    SOFFIT_HEIGHT_PEAK_HEIGHT = 3
    SOFFIT_HEIGHT_PITCH = 4
    DRIP_EDGE_PEAK_HEIGHT = 5
    DRIP_EDGE_PITCH = 6


class PitchType(Enum):
    RATIO = 0
    ANGLE = 1


class RoofingType(Enum):
    ECO_GREEN = 0
    ALUMINUM = 1


class EndCutType(Enum):
    UNCUT_TOP_BOTTOM = 0
    PLUMB_CUT_TOP_BOTTOM = 1
    PLUMB_CUT_TOP = 2


class SunroomType(Enum):
    STUDIO = 0
    CATHEDRAL = 1

# TODO: Make enum for lengths