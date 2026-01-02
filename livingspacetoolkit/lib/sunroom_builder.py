from math import sin, cos
from math import floor as math_floor
from math import ceil as math_ceil

from livingspacetoolkit.config.log_config import logger
from .toolkit_enums import EndCutType, LengthType, SunroomSide, SunroomType
from .toolkit_length import ToolkitLength
from livingspacetoolkit.models import ToolkitStateModel, SunroomModel



class SunroomBuilder:
    """This class calculates components of the roof. This includes the length of the roof panels, how many there are,
    the length of the hang rails, the length of the fascia, the number of Armstrong boxes needed, ect."""
    def __init__(self, toolkit_state_model: ToolkitStateModel, sunroom_model: SunroomModel) -> None:
        self.toolkit_state_model = toolkit_state_model
        self.sunroom_model = sunroom_model

    @staticmethod
    def _calculate_armstrong_panels(pitch, gable_wall, flat_wall) -> int:
        """
        Calculates the number of armstrong boxes for the roof.
        :param pitch: float: The pitch of the roof in radians
        :param gable_wall: float: The length of the pitched wall in inches
        :param flat_wall: float: The length of the unpitched wall in inches
        :return:
        """
        rake_length = gable_wall / cos(pitch)
        armstrong_area = rake_length * flat_wall / 144  # To get area in sq. ft.
        return math_ceil((armstrong_area + (armstrong_area * 0.1)) / 29)

    def _calculate_panel_length(self, roof_side: SunroomSide) -> None:
        panel_length = ToolkitLength(LengthType.PANEL)
        gable_wall = self.sunroom_model.gable_wall[roof_side].length
        overhang = self.toolkit_state_model.overhang.length
        thickness = self.toolkit_state_model.thickness.length
        pitch = self.toolkit_state_model.pitch[roof_side].pitch_value
        if self.toolkit_state_model.end_cuts == EndCutType.UNCUT_TOP_BOTTOM:
            p_length = (gable_wall + overhang) / cos(pitch)
        else:
            p_bottom = (gable_wall + overhang) / cos(pitch)
            p_top = (gable_wall + overhang + thickness * sin(pitch)) / cos(pitch)
            p_length = max(p_bottom, p_top)
        if p_length % 12 <= 1:  # This checks to see if the panel length is a maximum 1inch past the nearest foot
            self.sunroom_model.panel_tolerance[roof_side] = True
            # Returns panel length (in inches) rounded down to nearest foot and adds the 1inch tolerance
            # CORRECTION: We will NOT add 1 inch. Just round down instead
            # panel_length = mfloor(p_length / 12) * 12 + 1
            value = math_floor(p_length / 12) * 12
        else:
            # Returns panel length (in inches) rounded up to nearest foot
            value = math_ceil(p_length / 12) * 12
        try:
            panel_length.length = value
        except ValueError as err:
            logger.warning(err)
            self.sunroom_model.max_panel_length[roof_side] = True
            panel_length.length = value/2
        self.sunroom_model.panel_length[roof_side].length = panel_length.length

    def _calculate_roof_panels(self, roof_side: SunroomSide):
        """
        Calculate roof area, number of panels, and side overhang
        :param roof_side:
        :return:
        """
        overhang = self.toolkit_state_model.overhang.length
        flat_wall = self.toolkit_state_model.floor_walls[roof_side].length
        panel_length = self.sunroom_model.panel_length[roof_side].length
        max_panel_length = self.sunroom_model.max_panel_length[roof_side]
        roof_panels = 0
        if overhang > 16:
            side_overhang = 16
        else:
            side_overhang = overhang
        # TODO: This doesn't account for when the gable side overhang is negative from calculations.
        side_overhang_limit = 0
        side_overhang_roof_side = []
        match self.toolkit_state_model.sunroom_type:
            case SunroomType.STUDIO:
                roof_width = flat_wall + side_overhang * 2
                roof_panels = math_ceil(roof_width / 32)
                side_overhang_limit = (roof_panels * 32 - flat_wall) / 2
                side_overhang_roof_side = [SunroomSide.A_SIDE, SunroomSide.C_SIDE]
            case SunroomType.CATHEDRAL:
                roof_width = flat_wall + side_overhang
                if (roof_width / 32) == math_floor(roof_width / 32):
                    # If the roof width/32 is exactly a whole number then keep it a whole number
                    roof_panels = math_floor(roof_width / 32)
                elif (roof_width / 32) <= math_floor(roof_width / 32) + 0.5:
                    # If the roof width/32 is less than #.5 then cut it in half
                    roof_panels = math_floor(roof_width / 32) + 0.5
                    self.sunroom_model.roof_panels_split[roof_side] = True
                else:
                    # if the roof width/32 is greater than #.5 then add a panel
                    roof_panels = math_ceil(roof_width / 32)
                side_overhang_limit = roof_panels * 32 - flat_wall
                side_overhang_roof_side = [SunroomSide.B_SIDE]
            case _:
                raise NotImplementedError
        self.sunroom_model.roof_panels[roof_side] = roof_panels
        for overhang_side in side_overhang_roof_side:
            if side_overhang_limit < side_overhang:
                # Overhang too short
                self.sunroom_model.roof_overhang[overhang_side]["short_check"] = True
                self.sunroom_model.roof_overhang[overhang_side]["value"].length = side_overhang_limit
            elif side_overhang_limit > 16:
                # Overhang too long
                self.sunroom_model.roof_overhang[overhang_side]["long_check"] = True
                self.sunroom_model.roof_overhang[overhang_side]["value"].length = side_overhang_limit
            else:
                self.sunroom_model.roof_overhang[overhang_side]["value"].length = side_overhang
        if max_panel_length:
            self.sunroom_model.roof_area[roof_side] = math_ceil((panel_length * 2 * roof_panels * 32) / 144)
        else:
            self.sunroom_model.roof_area[roof_side] = math_ceil((panel_length * roof_panels * 32) / 144)

    def _calculate_hang_rail(self, roof_side: SunroomSide):
        hang_rails = 0
        match self.toolkit_state_model.sunroom_type:
            case SunroomType.STUDIO:
                hang_rails = self.sunroom_model.roof_panels[roof_side] * 32
            case SunroomType.CATHEDRAL:
                hang_rails = self.sunroom_model.panel_length[roof_side].length
        try:
            self.sunroom_model.hang_rails[roof_side]["value"].length = hang_rails
        except ValueError as err:
            logger.warning(err)
            self.sunroom_model.hang_rails[roof_side]["max_length"] = True
            self.sunroom_model.hang_rails[roof_side]["value"].length = hang_rails / 2

    def _calculate_fascia(self, roof_side: SunroomSide):
        roof_panels = self.sunroom_model.roof_panels[roof_side]
        panel_length = self.sunroom_model.panel_length[roof_side].length
        fascia_flat_wall = 0
        fascia_half_gable = panel_length + 6
        match self.toolkit_state_model.sunroom_type:
            case SunroomType.STUDIO:
                fascia_flat_wall = roof_panels * 32 + 12
            case SunroomType.CATHEDRAL:
                fascia_flat_wall = roof_panels * 32 + 6
        try:
            self.sunroom_model.fascia[roof_side]["value"][0].length = fascia_flat_wall
        except ValueError as err:
            logger.warning(err)
            self.sunroom_model.fascia[roof_side]["max_length"] = True
            self.sunroom_model.fascia[roof_side]["value"][0].length = fascia_flat_wall / 2
        match roof_side:
            case SunroomSide.A_SIDE | SunroomSide.C_SIDE:
                try:
                    self.sunroom_model.fascia[SunroomSide.B_SIDE]["value"][0].length = fascia_half_gable
                    self.sunroom_model.fascia[SunroomSide.B_SIDE]["value"][1].length = fascia_half_gable
                except ValueError as err:
                    logger.warning(err)
                    self.sunroom_model.fascia[SunroomSide.B_SIDE]["max_length"] = True
                    self.sunroom_model.fascia[SunroomSide.B_SIDE]["value"][0].length = fascia_half_gable / 2
                    self.sunroom_model.fascia[SunroomSide.B_SIDE]["value"][1].length = fascia_half_gable / 2
            case SunroomSide.B_SIDE:
                try:
                    self.sunroom_model.fascia[SunroomSide.A_SIDE]["value"][0].length = fascia_half_gable
                except ValueError as err:
                    logger.warning(err)
                    self.sunroom_model.fascia[SunroomSide.A_SIDE]["max_length"] = True
                    self.sunroom_model.fascia[SunroomSide.A_SIDE]["value"][0].length = fascia_half_gable / 2
                try:
                    self.sunroom_model.fascia[SunroomSide.C_SIDE]["value"][0].length = fascia_half_gable
                except ValueError as err:
                    logger.warning(err)
                    self.sunroom_model.fascia[SunroomSide.C_SIDE]["max_length"] = True
                    self.sunroom_model.fascia[SunroomSide.C_SIDE]["value"][0].length = fascia_half_gable / 2



    def build_roof_components(self) -> None:
        match self.toolkit_state_model.sunroom_type:
            case SunroomType.STUDIO:
                self._calculate_panel_length(SunroomSide.B_SIDE)
                self._calculate_roof_panels(SunroomSide.B_SIDE)
                self._calculate_hang_rail(SunroomSide.B_SIDE)
                self._calculate_fascia(SunroomSide.B_SIDE)
                pitch = self.toolkit_state_model.pitch[SunroomSide.B_SIDE].pitch_value
                flat_wall = self.toolkit_state_model.floor_walls[SunroomSide.B_SIDE].length
                gable_wall = self.sunroom_model.gable_wall[SunroomSide.B_SIDE].length
                armstrong_b_side = self._calculate_armstrong_panels(pitch, gable_wall, flat_wall)
                self.sunroom_model.armstrong_panels = armstrong_b_side
            case SunroomType.CATHEDRAL:
                self._calculate_panel_length(SunroomSide.A_SIDE)
                self._calculate_panel_length(SunroomSide.C_SIDE)
                self._calculate_roof_panels(SunroomSide.A_SIDE)
                self._calculate_roof_panels(SunroomSide.C_SIDE)
                self._calculate_hang_rail(SunroomSide.A_SIDE)
                self._calculate_hang_rail(SunroomSide.C_SIDE)
                self._calculate_fascia(SunroomSide.A_SIDE)
                self._calculate_fascia(SunroomSide.C_SIDE)

                pitch_a_side = self.toolkit_state_model.pitch[SunroomSide.A_SIDE].pitch_value
                flat_wall_a_side = self.toolkit_state_model.floor_walls[SunroomSide.A_SIDE].length
                gable_wall_a_side = self.sunroom_model.gable_wall[SunroomSide.A_SIDE].length
                pitch_c_side = self.toolkit_state_model.pitch[SunroomSide.C_SIDE].pitch_value
                flat_wall_c_side = self.toolkit_state_model.floor_walls[SunroomSide.C_SIDE].length
                gable_wall_c_side = self.sunroom_model.gable_wall[SunroomSide.C_SIDE].length

                armstrong_a_side = self._calculate_armstrong_panels(pitch_a_side, gable_wall_a_side, flat_wall_a_side)
                armstrong_c_side = self._calculate_armstrong_panels(pitch_c_side, gable_wall_c_side, flat_wall_c_side)
                self.sunroom_model.armstrong_panels = armstrong_a_side + armstrong_c_side