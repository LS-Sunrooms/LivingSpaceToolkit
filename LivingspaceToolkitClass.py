#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sin, cos, tan, atan, atan2, pi
from math import floor as m_floor
from math import ceil as m_ceil
from re import compile as re_compile

_units = re_compile(r'\'|ft|feet|\"|in')
end_cuts = ['uncut', 'plum_T_B', 'plum_T']


def angled(pitch, thickness):
    """
    Calculates the angled thickness given pitch and the panel thickness. Pitch has to be in radians.
    :param pitch: float
    :param thickness: float
    :return: float
    """
    return thickness * (sin(pi / 2) / sin(pi / 2 - pitch))


def assume_units(string_in, assume_unit):
    """
    This method takes a value and, if it doesn't have a base unit, attaches a base unit to it.
    :param string_in: str
    :param assume_unit: str
    :return: str
    """
    if _units.search(str(string_in)) is None:
        string_out = string_in + assume_unit
    else:
        string_out = string_in
    return string_out


def pitch_input(p_input):
    """
    Calculates the pitch in radians based on the units the object is in. Needs Units.py object.
    :param p_input: (Units.EngineeringUnits object)
    :return: float
    """
    pitch = None
    if p_input.base_unit == 'in.':
        pitch = atan(p_input.base / 12)
    elif p_input.base_unit == 'deg':
        pitch = p_input.base
    return pitch


def pitch_estimate(number):
    """
    Rounds a number to the nearest 0.5.
    :param number: float
    :return: float
    """
    return round(number * 2) / 2


def sixteenth(number):
    """
    Rounds number to nearest 16th.
    :param number: float
    :return: float
    """
    return round(number * 16) / 16


def estimate_drip_from_peak(peak, estimate_pitch, side_wall_length, overhang, thickness, endcut, awall, bwall, cwall):
    """
    This method is used to help estimate the pitch. Since I forgot how to do numerical methods this will have to do. All
    lengths must be in inches, the estimated pitch in radians, and this assumes you are cycling through a list of
    pitches.
    :param peak: float
    :param estimate_pitch: float
    :param side_wall_length: float
    :param overhang: float
    :param thickness: float
    :param endcut: str
    :param awall: float
    :param bwall: float
    :param cwall: float
    :return: float
    """
    wall_height = peak - side_wall_length * tan(estimate_pitch)
    soffit = wall_height - overhang * tan(estimate_pitch)
    estimate_drip = Sunroom(overhang=overhang, awall=awall, bwall=bwall, cwall=cwall, thickness=thickness,
                            endcut=endcut)
    drip_edge = estimate_drip.calculate_drip_edge(soffit, estimate_pitch)
    return drip_edge


# noinspection SpellCheckingInspection
def calculate_armstrong_panels(pitch, pitched_wall, unpitched_wall):
    rake_length = pitched_wall / cos(pitch)
    armstrong_area = rake_length * unpitched_wall / 144  # To get area in sq. ft.
    return m_ceil((armstrong_area + (armstrong_area * 0.1)) / 29)


# noinspection SpellCheckingInspection
class Sunroom:
    """
    This class will be the base class for the Studio and Cathedral type of sunrooms.
    """

    def __init__(self, overhang, awall, bwall, cwall, thickness, endcut):
        self.overhang = overhang
        self.awall = awall
        self.bwall = bwall
        self.cwall = cwall
        self.thickness = thickness
        if endcut not in end_cuts:
            raise LookupError("The end cut selected isn't available")
        else:
            self.endcut = endcut
        if overhang > 16:
            self.side_overhang = 16
        else:
            self.side_overhang = overhang

    def calculate_drip_edge(self, soffit, pitch):
        angled_thickness = angled(pitch=pitch, thickness=self.thickness)
        if self.endcut == 'plum_T_B':
            drip_edge = soffit + angled_thickness
        else:
            drip_edge = soffit + self.thickness * cos(pitch)
        return drip_edge

    def _calculate_panel_length(self, pitch, pitched_wall):
        max_panel_length = False
        panel_tolerance = False
        if self.endcut == 'uncut':
            p_length = (pitched_wall + self.overhang) / cos(pitch)
        else:
            p_bottom = (pitched_wall + self.overhang) / (cos(pitch))
            p_top = (pitched_wall + self.overhang + self.thickness * sin(pitch)) / cos(pitch)
            p_length = max(p_bottom, p_top)
        if p_length % 12 <= 1:  # This checks to see if the panel length is a maximum 1 inch past the nearest foot
            panel_tolerance = True
            # Returns panel length (in inches) rounded down to nearest foot and adds the 1 inch tolerance
            # CORRECTION: We will NOT add 1 inch. Just round down instead
            # panel_length = mfloor(p_length / 12) * 12 + 1
            panel_length = m_floor(p_length / 12) * 12
        else:
            panel_length = m_ceil(p_length / 12) * 12  # Returns panel length (in inches) rounded up to nearest foot
        if panel_length > 288:
            max_panel_length = True
            panel_length /= 2
        return {'Panel Length': panel_length, 'Max Length Check': max_panel_length, 'Panel Tolerance': panel_tolerance}

    def _calculate_roof_panels(self, soffit_wall, panel_length_dict):
        pass

    def _calculate_hang_rail(self, panel_dict):
        pass

    def _calculate_fascia(self, roof_panel_dict, panel_length_dict):
        pass

    def calculate_sunroom(self):
        pass

    # Scenarios
    def wall_height_pitch(self, pitch, soffit_wall_height):
        pass

    def wall_height_peak_height(self, soffit_wall_height, peak):
        pass

    def max_height_pitch(self, pitch, max_h):
        pass

    def soffit_height_peak_height(self, peak, soffit):
        pass

    def soffit_height_pitch(self, pitch, soffit):
        pass

    def drip_edge_peak_height(self, drip_edge, peak):
        pass

    def drip_edge_pitch(self, drip_edge, pitch):
        pass


# noinspection SpellCheckingInspection
class Studio(Sunroom):
    def __init__(self, overhang, awall, bwall, cwall, thickness, endcut):
        super().__init__(overhang, awall, bwall, cwall, thickness, endcut)
        self.pitched_wall = max(self.awall, self.cwall)
        self.soffit_wall = self.bwall
        self.pitch = None
        self.peak = None
        self.max_h = None
        self.unpitched_wall = None
        self.soffit = None
        self.drip_edge = None
        self.panel_length_dict = None
        self.roof_panel_dict = None
        self.hang_rail_dict = None
        self.fascia_dict = None
        self.armstrong_panels = None

    def _calculate_roof_panels(self, soffit_wall, panel_length_dict):
        minmax_overhang = [False, False]
        roof_width = soffit_wall + self.side_overhang * 2
        roof_panels = m_ceil(roof_width / 32)
        if (roof_panels * 32 - soffit_wall) / 2 < self.side_overhang:
            # Overhang too short
            side_overhang = (roof_panels * 32 - soffit_wall) / 2
            minmax_overhang[0] = True
        elif (roof_panels * 32 - soffit_wall) / 2 > 16:
            # Overhang too long
            side_overhang = (roof_panels * 32 - soffit_wall) / 2
            minmax_overhang[1] = True
        else:
            side_overhang = self.side_overhang
        panel_length = panel_length_dict['Panel Length']
        max_panel_length = panel_length_dict['Max Length Check']
        if max_panel_length is True:
            roof_area = m_ceil(panel_length * 2 * roof_panels * 32)
        else:
            roof_area = m_ceil(panel_length * roof_panels * 32)
        return {'Roof Area': roof_area, 'Roof Panels': roof_panels, 'Side Overhang': side_overhang,
                'Overhang Short Check': minmax_overhang[0], 'Overhang Long Check': minmax_overhang[1]}

    def _calculate_hang_rail(self, panel_dict):
        max_hang_rail_length = False
        roof_panels = panel_dict['Roof Panels']
        hang_rail = roof_panels * 32
        if hang_rail > 216:
            max_hang_rail_length = True
            hang_rail /= 2
        return {'Hang Rail': hang_rail, 'Hang Rail Check': max_hang_rail_length}

    def _calculate_fascia(self, roof_panel_dict, panel_length_dict):
        max_fascia_length = [False, False]
        roof_panels = roof_panel_dict['Roof Panels']
        panel_length = panel_length_dict['Panel Length']
        fascia_wall = roof_panels * 32 + 12
        fascia_sides = panel_length + 6
        if fascia_wall > 216:
            max_fascia_length[0] = True
            fascia_wall /= 2
        if fascia_sides > 216:
            max_fascia_length[1] = True
            fascia_sides /= 2
        return {'Wall Fascia': fascia_wall, 'Side Fascia': fascia_sides, 'Fascia Check': max_fascia_length}

    def calculate_sunroom(self):
        self.panel_length_dict = self._calculate_panel_length(self.pitch, self.pitched_wall)
        self.roof_panel_dict = self._calculate_roof_panels(self.soffit_wall, self.panel_length_dict)
        self.hang_rail_dict = self._calculate_hang_rail(self.roof_panel_dict)
        self.fascia_dict = self._calculate_fascia(self.roof_panel_dict, self.panel_length_dict)
        self.armstrong_panels = calculate_armstrong_panels(self.pitch, self.pitched_wall, self.soffit_wall)

    # Scenarios
    # Scenario 1
    def wall_height_pitch(self, pitch, soffit_wall_height):
        self.pitch = pitch
        self.unpitched_wall = soffit_wall_height
        self.pitched_wall = max(self.awall, self.bwall)
        self.soffit = self.unpitched_wall - self.overhang * tan(self.pitch)
        self.peak = self.unpitched_wall + self.pitched_wall * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=self.pitch, thickness=self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 2
    def wall_height_peak_height(self, soffit_wall_height, peak):
        self.unpitched_wall = soffit_wall_height
        self.peak = peak
        self.pitch = atan((self.peak - self.unpitched_wall) / max(self.awall, self.cwall))
        self.soffit = self.unpitched_wall - self.overhang * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=self.pitch, thickness=self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 3
    def max_height_pitch(self, pitch, max_h):
        self.pitch = pitch
        self.max_h = max_h
        self.unpitched_wall = self.max_h - max(self.awall, self.cwall) * tan(self.pitch) - \
                              angled(pitch=self.pitch, thickness=self.thickness)
        self.soffit = self.unpitched_wall - self.overhang * tan(self.pitch)
        self.peak = self.max_h - angled(pitch=self.pitch, thickness=self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 4
    def soffit_height_peak_height(self, peak, soffit):
        self.soffit = soffit
        self.peak = peak
        self.pitch = atan((self.peak - self.soffit) / (max(self.awall, self.cwall) + self.overhang))
        self.unpitched_wall = self.soffit + self.overhang * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=self.pitch, thickness=self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 5
    def soffit_height_pitch(self, pitch, soffit):
        self.pitch = pitch
        self.soffit = soffit
        self.unpitched_wall = self.soffit + self.overhang * tan(self.pitch)
        self.peak = self.unpitched_wall + self.pitched_wall * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=self.pitch, thickness=self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 6
    def drip_edge_peak_height(self, drip_edge, peak):
        self.peak = peak
        self.drip_edge = drip_edge
        tol = 0.01
        diff = 100
        incr = 0.1
        ratio_pitch = 0.0
        while diff > tol:
            old_ratio_pitch = ratio_pitch
            ratio_pitch += incr
            self.pitch = atan2(ratio_pitch, 12)
            drip_est = estimate_drip_from_peak(peak=self.peak, estimate_pitch=self.pitch,
                                               side_wall_length=self.pitched_wall, overhang=self.overhang,
                                               thickness=self.thickness, endcut=self.endcut, awall=self.awall,
                                               bwall=self.bwall, cwall=self.cwall)
            diff = abs(self.drip_edge - drip_est)
            if ratio_pitch > 12:
                break
            if drip_est < self.drip_edge:
                ratio_pitch = old_ratio_pitch
                incr /= 2
        self.unpitched_wall = peak - self.pitched_wall * tan(self.pitch)
        self.soffit = self.unpitched_wall - self.overhang * tan(self.pitch)
        self.max_h = self.peak + angled(self.pitch, self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 7
    def drip_edge_pitch(self, drip_edge, pitch):
        self.pitch = pitch
        self.drip_edge = drip_edge
        self.soffit = self.drip_edge - angled(self.pitch, self.thickness)
        self.unpitched_wall = self.soffit + self.overhang * tan(pitch)
        self.peak = self.unpitched_wall + self.pitched_wall * tan(pitch)
        self.max_h = self.peak + angled(self.pitch, self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)


# noinspection SpellCheckingInspection
class Cathedral(Sunroom):
    def __init__(self, overhang, awall, bwall, cwall, thickness, endcut):
        super().__init__(overhang, awall, bwall, cwall, thickness, endcut)
        # self.soffit_wall = max(self.awall, self.cwall)
        self.a_unpitched_wall_l = None
        self.c_unpitched_wall_l = None
        self.pitched_wall = self.bwall
        self.a_pitched_wall = None
        self.c_pitched_wall = None
        self.post_width = 3.25
        self.a_pitch = None
        self.c_pitch = None
        self.a_unpitched_wall_h = None
        self.c_unpitched_wall_h = None
        self.peak = None
        self.f_peak = None
        self.max_h = None
        # self.soffit = None
        self.a_soffit = None
        self.c_soffit = None
        self.a_drip_edge = None
        self.c_drip_edge = None
        self.a_panel_length_dict = None
        self.c_panel_length_dict = None
        self.a_roof_panel_dict = None
        self.c_roof_panel_dict = None
        self.a_hang_rail_dict = None
        self.c_hang_rail_dict = None
        self.a_fascia_dict = None
        self.c_fascia_dict = None
        self.a_armstrong_panels = None
        self.c_armstrong_panels = None

    def _calculate_roof_panels(self, soffit_wall, panel_length_dict):
        minmax_overhang = [False, False]
        split = False
        roof_width = soffit_wall + self.side_overhang
        if (roof_width / 32) <= m_floor(roof_width / 32) + .5:
            roof_panels = m_floor(roof_width / 32) + .5
            split = True
        else:
            roof_panels = m_ceil(roof_width / 32)
        if (roof_panels * 32 - soffit_wall) < self.side_overhang:
            # Overhang too short
            side_overhang = roof_panels * 32 - soffit_wall
            minmax_overhang[0] = True
        elif (roof_panels * 32 - soffit_wall) > 16:
            # Overhang too long
            side_overhang = roof_panels * 32 - soffit_wall
            minmax_overhang[1] = True
        else:
            side_overhang = self.side_overhang
        panel_length = panel_length_dict['Panel Length']
        max_panel_length = panel_length_dict['Max Length Check']
        if max_panel_length is True:
            roof_area = m_ceil(panel_length * 2 * roof_panels * 32)
        else:
            roof_area = m_ceil(panel_length * roof_panels * 32)
        return {'Roof Area': roof_area, 'Roof Panels': roof_panels, 'Side Overhang': side_overhang,
                'Overhang Short Check': minmax_overhang[0], 'Overhang Long Check': minmax_overhang[1], 'Split': split}

    def _calculate_hang_rail(self, panel_dict):
        max_hang_rail_length = False
        panel_length = panel_dict['Panel Length']
        hang_rail = panel_length
        if hang_rail > 216:
            max_hang_rail_length = True
            hang_rail /= 2
        return {'Hang Rail': hang_rail, 'Hang Rail Check': max_hang_rail_length}

    def _calculate_fascia(self, roof_panel_dict, panel_length_dict):
        max_fascia_length = [False, False]
        roof_panels = roof_panel_dict['Roof Panels']
        panel_length = panel_length_dict['Panel Length']
        fascia_wall = roof_panels * 32 + 6
        fascia_sides = panel_length + 6
        if fascia_wall > 216:
            max_fascia_length[0] = True
            fascia_wall /= 2
        if fascia_sides > 216:
            max_fascia_length[1] = True
            fascia_sides /= 2
        return {'Wall Fascia': fascia_wall, 'Side Fascia': fascia_sides, 'Fascia Check': max_fascia_length}

    def calculate_sunroom(self):
        self.a_panel_length_dict = self._calculate_panel_length(self.a_pitch, self.a_pitched_wall)
        self.c_panel_length_dict = self._calculate_panel_length(self.c_pitch, self.c_pitched_wall)
        self.a_roof_panel_dict = self._calculate_roof_panels(self.awall, self.a_panel_length_dict)
        self.c_roof_panel_dict = self._calculate_roof_panels(self.cwall, self.c_panel_length_dict)
        self.a_hang_rail_dict = self._calculate_hang_rail(self.a_panel_length_dict)
        self.c_hang_rail_dict = self._calculate_hang_rail(self.c_panel_length_dict)
        self.a_fascia_dict = self._calculate_fascia(self.a_roof_panel_dict, self.a_panel_length_dict)
        self.c_fascia_dict = self._calculate_fascia(self.c_roof_panel_dict, self.c_panel_length_dict)
        self.a_armstrong_panels = calculate_armstrong_panels(self.a_pitch, self.a_pitched_wall, self.awall)
        self.c_armstrong_panels = calculate_armstrong_panels(self.c_pitch, self.c_pitched_wall, self.cwall)

    # Scenarios
    # Scenario 1
    def wall_height_pitch(self, pitch, soffit_wall_height):
        self.a_pitch = pitch[0]
        self.c_pitch = pitch[1]
        self.a_unpitched_wall_h = soffit_wall_height[0]
        self.c_unpitched_wall_h = soffit_wall_height[1]
        self.a_pitched_wall = self.bwall / 2
        self.c_pitched_wall = self.bwall / 2
        self.a_soffit = self.a_unpitched_wall_h - self.overhang * tan(self.a_pitch)
        self.c_soffit = self.c_unpitched_wall_h - self.overhang * tan(self.c_pitch)
        self.peak = (self.pitched_wall * sin(self.a_pitch) * sin(self.c_pitch)) / \
                    sin(pi - self.a_pitch - self.c_pitch) + max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)
        self.a_unpitched_wall_l = (self.peak - max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)) / tan(
            self.a_pitch)
        self.c_unpitched_wall_l = (self.peak - max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)) / tan(
            self.c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        self.f_peak = self.peak - (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch -
                                                                                                  self.c_pitch)
        self.max_h = self.f_peak + max(angled(self.a_pitch, self.thickness), angled(self.c_pitch, self.thickness)) + \
                     (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch)
        self.a_drip_edge = self.calculate_drip_edge(self.a_soffit, self.a_pitch)
        self.c_drip_edge = self.calculate_drip_edge(self.c_soffit, self.c_pitch)

    # Scenario 2
    def wall_height_peak_height(self, soffit_wall_height, peak):
        self.f_peak = peak
        self.a_unpitched_wall_h = soffit_wall_height[0]
        self.c_unpitched_wall_h = soffit_wall_height[1]
        self.a_pitched_wall = self.bwall / 2
        self.c_pitched_wall = self.bwall / 2
        self.a_pitch = atan2(float(self.f_peak - self.a_unpitched_wall_h),
                             float(self.a_pitched_wall - self.post_width / 2))
        self.c_pitch = atan2(float(self.f_peak - self.c_unpitched_wall_h),
                             float(self.c_pitched_wall - self.post_width / 2))
        self.a_soffit = self.a_unpitched_wall_h - self.overhang * tan(self.a_pitch)
        self.c_soffit = self.c_unpitched_wall_h - self.overhang * tan(self.c_pitch)
        a_max_h = self.f_peak + angled(self.a_pitch, self.thickness) + \
                  (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch)
        c_max_h = self.f_peak + angled(self.c_pitch, self.thickness) + \
                  (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch)
        self.max_h = max(a_max_h, c_max_h)
        self.a_drip_edge = self.calculate_drip_edge(self.a_soffit, self.a_pitch)
        self.c_drip_edge = self.calculate_drip_edge(self.c_soffit, self.c_pitch)

    # Scenario 3
    def max_height_pitch(self, pitch, max_h):
        self.a_pitch = pitch[0]
        self.c_pitch = pitch[1]
        self.max_h = max_h
        self.peak = (self.bwall * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        self.f_peak = self.max_h - max(angled(self.a_pitch, self.thickness), angled(self.c_pitch, self.thickness)) - \
                      (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch)
        # a_side_wall = self.peak / tan(self.a_pitch)
        # c_side_wall = self.peak / tan(self.c_pitch)
        # a_wall_height = self.f_peak - self.peak
        self.a_unpitched_wall_h = max_h - max(angled(self.a_pitch, self.thickness),
                                              angled(self.c_pitch, self.thickness)) \
                                  - (self.bwall * sin(self.a_pitch) * sin(self.c_pitch)) / sin(
            pi - self.a_pitch - self.c_pitch)
        self.c_unpitched_wall_h = self.a_unpitched_wall_h
        self.a_soffit = self.a_unpitched_wall_h - self.overhang * tan(self.a_pitch)
        self.c_soffit = self.c_unpitched_wall_h - self.overhang * tan(self.c_pitch)
        self.a_drip_edge = self.calculate_drip_edge(self.a_soffit, self.a_pitch)
        self.c_drip_edge = self.calculate_drip_edge(self.c_soffit, self.c_pitch)

    # Scenario 4
    def soffit_height_peak_height(self, peak, soffit):
        self.a_soffit = max(soffit[0], soffit[0])
        self.c_soffit = max(soffit[0], soffit[0])
        self.f_peak = peak
        self.a_pitched_wall = self.bwall / 2
        self.c_pitched_wall = self.bwall / 2
        self.a_pitch = atan((self.f_peak - self.a_soffit) / (self.a_pitched_wall + self.overhang - self.post_width / 2))
        self.c_pitch = atan((self.f_peak - self.c_soffit) / (self.c_pitched_wall + self.overhang - self.post_width / 2))
        self.a_unpitched_wall_h = self.a_soffit + self.overhang * tan(self.a_pitch)
        self.c_unpitched_wall_h = self.c_soffit + self.overhang * tan(self.c_pitch)
        h = (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch)
        a_max_h = self.f_peak + angled(self.a_pitch, self.thickness) + h
        c_max_h = self.f_peak + angled(self.c_pitch, self.thickness) + h
        self.max_h = max(a_max_h, c_max_h)
        self.a_drip_edge = self.calculate_drip_edge(self.a_soffit, self.a_pitch)
        self.c_drip_edge = self.calculate_drip_edge(self.c_soffit, self.c_pitch)

    # Scenario 5
    def soffit_height_pitch(self, pitch, soffit):
        self.a_soffit = max(soffit[0], soffit[1])
        self.c_soffit = max(soffit[0], soffit[1])
        self.a_pitch = pitch[0]
        self.c_pitch = pitch[1]
        self.a_unpitched_wall_h = self.a_soffit + self.overhang * tan(self.a_pitch)
        self.c_unpitched_wall_h = self.a_soffit + self.overhang * tan(self.c_pitch)
        self.peak = (self.bwall * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch) + \
                    max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)
        self.a_unpitched_wall_l = (self.peak - max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)) / tan(
            self.a_pitch)
        self.c_unpitched_wall_l = (self.peak - max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)) / tan(
            self.c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        self.f_peak = self.peak - (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / \
                      sin(pi - self.a_pitch - self.c_pitch)
        self.max_h = self.f_peak + max(angled(self.a_pitch, self.thickness),
                                       angled(self.c_pitch, self.thickness)) + \
                     (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch)
        self.a_drip_edge = self.calculate_drip_edge(self.a_soffit, self.a_pitch)
        self.c_drip_edge = self.calculate_drip_edge(self.c_soffit, self.c_pitch)

    # Scenario 6
    def drip_edge_peak_height(self, drip_edge, peak):
        self.a_drip_edge = drip_edge
        self.c_drip_edge = drip_edge
        self.f_peak = peak
        tol = 0.01
        diff = 100
        incr = 0.1
        ratio_pitch = 0.0
        pitch = None
        while diff > tol:
            old_ratio_pitch = ratio_pitch
            ratio_pitch += incr
            pitch = atan2(ratio_pitch, 12)
            drip_est = estimate_drip_from_peak(peak=peak, estimate_pitch=pitch,
                                               side_wall_length=self.bwall / 2 - self.post_width / 2,
                                               overhang=self.overhang, thickness=self.thickness, endcut=self.endcut,
                                               awall=self.awall, bwall=self.bwall, cwall=self.cwall)
            diff = abs(drip_edge - drip_est)
            if ratio_pitch > 12:
                break
            if drip_est < drip_edge:
                ratio_pitch = old_ratio_pitch
                incr /= 2
        # Now take the estimated pitch and set it as a ratio then convert back to radians. Its more accurate for some
        # reason
        self.a_unpitched_wall_h = self.f_peak - (self.bwall / 2 - self.post_width / 2) * tan(pitch)
        self.c_unpitched_wall_h = self.a_unpitched_wall_h
        self.a_pitched_wall = self.bwall / 2
        self.c_pitched_wall = self.a_pitched_wall
        soffit = self.a_unpitched_wall_h - self.overhang * tan(pitch)
        self.a_soffit = soffit
        self.c_soffit = soffit
        self.a_pitch = pitch
        self.c_pitch = pitch
        self.max_h = self.f_peak + angled(pitch, self.thickness) + (self.post_width * sin(pitch) * sin(pitch)) / \
                     sin(pi - pitch - pitch)

    # Scenario 7
    def drip_edge_pitch(self, drip_edge, pitch):
        self.a_pitch = pitch[0]
        self.c_pitch = pitch[1]
        self.a_soffit = drip_edge - angled(self.a_pitch, self.thickness)
        self.c_soffit = drip_edge - angled(self.c_pitch, self.thickness)
        soffit = max(self.a_soffit, self.c_soffit)
        self.a_unpitched_wall_h = soffit + self.overhang * tan(self.a_pitch)
        self.c_unpitched_wall_h = soffit + self.overhang * tan(self.c_pitch)
        self.peak = (self.bwall * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch) + \
                    max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)
        self.a_pitched_wall = (self.peak - max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)) / tan(self.a_pitch)
        self.c_pitched_wall = (self.peak - max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)) / tan(self.c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        self.f_peak = self.peak - (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / \
                      sin(pi - self.a_pitch - self.c_pitch)
        self.max_h = self.f_peak + max(angled(self.a_pitch, self.thickness), angled(self.c_pitch, self.thickness)) + \
                     (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch)
        self.a_drip_edge = self.calculate_drip_edge(self.a_soffit, self.a_pitch)
        self.c_drip_edge = self.calculate_drip_edge(self.c_soffit, self.c_pitch)
