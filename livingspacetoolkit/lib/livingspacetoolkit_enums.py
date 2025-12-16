from enum import Enum, auto


class Scenario(Enum):
    WALL_HEIGHT_PITCH = auto()
    WALL_HEIGHT_PEAK_HEIGHT = auto()
    MAX_HEIGHT_PITCH = auto()
    SOFFIT_HEIGHT_PEAK_HEIGHT = auto()
    SOFFIT_HEIGHT_PITCH = auto()
    DRIP_EDGE_PEAK_HEIGHT = auto()
    DRIP_EDGE_PITCH = auto()


class PitchType(Enum):
    RATIO = auto()
    ANGLE = auto()


class RoofingType(Enum):
    ECO_GREEN = auto()
    ALUMINUM = auto()


class EndCutType(Enum):
    UNCUT_TOP_BOTTOM = auto()
    PLUMB_CUT_TOP_BOTTOM = auto()
    PLUMB_CUT_TOP = auto()


class SunroomType(Enum):
    # These numbers are assigned based on which tab they are on.
    STUDIO = 0
    CATHEDRAL = 1

class LengthType(Enum):
    OVERHANG = auto()
    THICKNESS = auto()
    PEAK_HEIGHT = auto()
    MAX_HEIGHT = auto()
    DRIP_EDGE_HEIGHT = auto()
    A_SIDE_SOFFIT_HEIGHT = auto()
    B_SIDE_SOFFIT_HEIGHT = auto()
    C_SIDE_SOFFIT_HEIGHT = auto()
    A_WALL_HEIGHT = auto()
    B_WALL_HEIGHT = auto()
    C_WALL_HEIGHT = auto()
    A_WALL_WIDTH = auto()
    B_WALL_WIDTH  = auto()
    C_WALL_WIDTH = auto()