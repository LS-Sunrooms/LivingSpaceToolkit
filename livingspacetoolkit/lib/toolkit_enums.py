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

class SunroomSide(Enum):
    A_SIDE = auto()
    B_SIDE = auto()
    C_SIDE = auto()


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
    SOFFIT_HEIGHT = auto()
    WALL_HEIGHT = auto()
    WALL_WIDTH = auto()
    PANEL = auto()
    HANG_RAIL = auto()
    FASCIA = auto()