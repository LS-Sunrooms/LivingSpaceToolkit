#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sin, cos, tan, atan, atan2, pi
from math import floor as m_floor
from math import ceil as m_ceil
from re import compile as re_compile
import Units

list_ = re_compile(r'\'|ft|feet|\"|in')


def main():
    pitch_in = Units.EngineeringUnits(assume_units('5', '"'), u_type='length')
    pitch = pitch_input(pitch_in)
    test = Studio(12, 168, 162, 168, 10.25, 'plum_T_B')
    test.wall_height_pitch(pitch, 95, 168)
    print(test.peak)
    print(test.panel_length())
    print(test.roof_panels())
    print(test.armstrong_panels())


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
    if list_.search(str(string_in)) is None:
        string_out = string_in + assume_unit
    else:
        string_out = string_in
    return string_out


def pitch_input(pitch_input):
    """
    Calculates the pitch in radians based on the units the object is in. Needs Units.py object.
    :param pitch_input: (Units.EngineeringUnits object)
    :return: float
    """
    if pitch_input.base_unit == 'in.':
        pitch = atan(pitch_input.base / 12)
    elif pitch_input.base_unit == 'deg':
        pitch = pitch_input.base
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


def estimate_drip_from_peak(peak, estimate_pitch, wall_length, side_wall_length, overhang, thickness, tab, endcut,
                            awall, bwall, cwall):
    """
    This method is used to help estimate the pitch. Since I forgot how to do numerical methods this will have to do. All
    lengths must be in inches, the estimated pitch in radians, and this assumes you are cycling through a list of
    pitches.
    :param peak: float
    :param estimate_pitch: float
    :param wall_length: float
    :param side_wall_length: float
    :param overhang: float
    :param thickness: float
    :param tab: int
    :param endcut: str
    :return: float <CommonCalcs.drip_edge>
    """
    wall_height = peak - side_wall_length * tan(estimate_pitch)
    soffit = wall_height - overhang * tan(estimate_pitch)
    max_h = peak + angled(estimate_pitch, thickness)
    # estimate_drip = CommonCalcs(wall_length, side_wall_length, estimate_pitch, soffit, overhang, tab, thickness, endcut,
    #                             peak, max_h, wall_height)
    estimate_drip = Sunroom(overhang=overhang, awall=awall, bwall=bwall, cwall=cwall, thickness=thickness,
                            endcut=endcut)
    return estimate_drip.drip_edge()


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
        self.endcut = endcut
        if overhang > 16:
            self.side_overhang = 16
        else:
            self.side_overhang = overhang
        self.pitch = None
        self.peak = None
        self.max_h = None
        self.soffit_wall = None
        self.soffit_wall_height = None
        self.soffit = None
        self.drip_edge = None
        self.pitched_wall = None
        self.tabWidget = None

    def drip_edge(self):
        angled_thickness = angled(pitch=self.pitch, thickness=self.thickness)
        if self.endcut == 'plum_T_B':
            self.drip_edge = self.soffit + angled_thickness
        else:
            self.drip_edge = self.soffit + self.thickness * cos(self.pitch)

    def panel_length(self):
        max_panel_length = False
        panel_tolerance = False
        if self.endcut == 'uncut':
            p_length = (self.pitched_wall + self.overhang) / cos(self.pitch)
        else:
            p_bottom = (self.pitched_wall + self.overhang) / (cos(self.pitch))
            p_top = (self.pitched_wall + self.overhang + self.thickness * sin(self.pitch)) / cos(self.pitch)
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
        return [panel_length, max_panel_length, panel_tolerance]

    def roof_panels(self):
        pass

    def hang_rail(self):
        pass

    def fascia(self):
        pass

    def armstrong_panels(self):
        rake_length = self.pitched_wall / cos(self.pitch)
        armstrong_area = rake_length * self.soffit_wall / 144  # To get area in sq. ft.
        return m_ceil((armstrong_area + (armstrong_area * 0.1)) / 29)

    # Scenarios
    def wall_height_pitch(self, pitch, soffit_wall_height, side_wall_length):
        self.pitch = pitch
        self.soffit_wall_height = soffit_wall_height
        self.soffit = self.soffit_wall_height - self.overhang * tan(self.pitch)
        self.peak = self.soffit_wall_height + side_wall_length * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=pitch, thickness=self.thickness)

    def wall_height_peak_height(self, soffit_wall_height, peak):
        self.soffit_wall_height = soffit_wall_height
        pitch = atan((peak - self.soffit_wall_height) / max(self.awall, self.cwall))
        self.soffit = self.soffit_wall_height - self.overhang * tan(pitch)
        self.max_h = peak + angled(pitch=self.pitch, thickness=self.thickness)

    def max_height_pitch(self, pitch, max_h):
        self.pitch = pitch
        self.soffit_wall_height = max_h - max(self.awall, self.cwall) * tan(self.pitch) - \
                                  angled(pitch=self.pitch, thickness=self.thickness)
        self.soffit = self.soffit_wall_height - self.overhang * tan(self.pitch)
        self.peak = max_h - angled(pitch=self.pitch, thickness=self.thickness)

    def soffit_height_peak_height(self, peak, soffit):
        self.soffit = soffit
        self.peak = peak
        self.pitch = atan((self.peak - self.soffit) / (max(self.awall, self.cwall) + self.overhang))
        self.soffit_wall_height = self.soffit + self.overhang * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=self.pitch, thickness=self.thickness)

    def soffit_height_pitch(self, pitch, soffit):
        self.pitch = pitch
        self.soffit = soffit
        self.soffit_wall_height = self.soffit + self.overhang * tan(self.pitch)
        self.peak = self.soffit_wall_height + self.pitched_wall * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=self.pitch, thickness=self.thickness)

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
            drip_est = estimate_drip_from_peak(peak=self.peak, estimate_pitch=self.pitch, wall_length=self.bwall,
                                               side_wall_length=self.pitched_wall, overhang=self.overhang,
                                               thickness=self.thickness, tab=self.tabWidget,
                                               endcut=self.endcut)
            diff = abs(self.drip_edge - drip_est)
            if ratio_pitch > 12:
                break
            if drip_est < self.drip_edge:
                ratio_pitch = old_ratio_pitch
                incr /= 2
        self.soffit_wall_height = peak - self.pitched_wall * tan(self.pitch)
        self.soffit = self.soffit_wall_height - self.overhang * tan(self.pitch)
        self.max_h = self.peak + angled(self.pitch, self.thickness)

    def drip_edge_pitch(self, drip_edge, pitch):
        self.pitch = pitch
        self.drip_edge = drip_edge
        self.soffit = self.drip_edge - angled(self.pitch, self.thickness)
        self.soffit_wall_height = self.soffit + self.overhang * tan(pitch)
        self.peak = self.soffit_wall_height + self.pitched_wall * tan(pitch)
        self.max_h = self.peak + angled(self.pitch, self.thickness)


# noinspection SpellCheckingInspection
class Studio(Sunroom):
    def __init__(self, overhang, awall, bwall, cwall, thickness, endcut):
        super().__init__(overhang, awall, bwall, cwall, thickness, endcut)
        self.pitched_wall = max(self.awall, self.cwall)
        self.soffit_wall = self.bwall
        self.tabWidget = 0

    def roof_panels(self):
        minmax_overhang = [False, False]
        split = False
        roof_width = self.soffit_wall + self.side_overhang * 2
        roof_panels = m_ceil(roof_width / 32)
        if (roof_panels * 32 - self.soffit_wall) / 2 < self.side_overhang:
            # Overhang too short
            side_overhang = (roof_panels * 32 - self.soffit_wall) / 2
            minmax_overhang[0] = True
        elif (roof_panels * 32 - self.soffit_wall) / 2 > 16:
            # Overhang too long
            side_overhang = (roof_panels * 32 - self.soffit_wall) / 2
            minmax_overhang[1] = True
        else:
            side_overhang = self.side_overhang
        panel_length, max_panel_length = self.panel_length()[0:2]
        if max_panel_length is True:
            roof_area = m_ceil(panel_length * 2 * roof_panels * 32)
        else:
            roof_area = m_ceil(panel_length * roof_panels * 32)
        return [roof_area, roof_panels, side_overhang, minmax_overhang, split]

    def hang_rail(self):
        max_hang_rail_length = False
        roof_panels = self.roof_panels()[1]
        hang_rail = roof_panels * 32
        if hang_rail > 216:
            max_hang_rail_length = True
            hang_rail /= 2
        return [hang_rail, max_hang_rail_length]

    def fascia(self):
        max_fascia_length = [False, False]
        roof_panels = self.roof_panels()[1]
        panel_length = self.panel_length()[0]
        fascia_wall = roof_panels * 32 + 12
        fascia_sides = panel_length + 6
        if fascia_wall > 216:
            max_fascia_length[0] = True
            fascia_wall /= 2
        if fascia_sides > 216:
            max_fascia_length[1] = True
            fascia_sides /= 2
        return [fascia_wall, fascia_sides, max_fascia_length]


# noinspection SpellCheckingInspection
class Cathedral(Sunroom):
    def __init__(self, overhang, awall, bwall, cwall, thickness, endcut):
        super().__init__(overhang, awall, bwall, cwall, thickness, endcut)
        self.soffit_wall = max(self.awall, self.cwall)
        self.post_width = 3.25

    def roof_panels(self):
        minmax_overhang = [False, False]
        split = False
        roof_width = self.soffit_wall + self.side_overhang
        if self.tabWidget == 1 and ((roof_width / 32) <= m_floor(roof_width / 32) + .5):
            roof_panels = m_floor(roof_width / 32) + .5
            split = True
        else:
            roof_panels = m_ceil(roof_width / 32)
        if (roof_panels * 32 - self.soffit_wall) < self.side_overhang:
            # Overhang too short
            side_overhang = roof_panels * 32 - self.soffit_wall
            minmax_overhang[0] = True
        elif (roof_panels * 32 - self.soffit_wall) > 16:
            # Overhang too long
            side_overhang = roof_panels * 32 - self.soffit_wall
            minmax_overhang[1] = True
        else:
            side_overhang = self.side_overhang
        panel_length, max_panel_length = self.panel_length()[0:2]
        if max_panel_length is True:
            roof_area = m_ceil(panel_length * 2 * roof_panels * 32)
        else:
            roof_area = m_ceil(panel_length * roof_panels * 32)
        return [roof_area, roof_panels, side_overhang, minmax_overhang, split]

    def hang_rail(self):
        max_hang_rail_length = False
        panel_length = self.panel_length()[0]
        hang_rail = panel_length
        if hang_rail > 216:
            max_hang_rail_length = True
            hang_rail /= 2
        return [hang_rail, max_hang_rail_length]

    def fascia(self):
        max_fascia_length = [False, False]
        roof_panels = self.roof_panels()[1]
        panel_length = self.panel_length()[0]
        fascia_wall = roof_panels * 32 + 6
        fascia_sides = panel_length + 6
        if fascia_wall > 216:
            max_fascia_length[0] = True
            fascia_wall /= 2
        if fascia_sides > 216:
            max_fascia_length[1] = True
            fascia_sides /= 2
        return [fascia_wall, fascia_sides, max_fascia_length]

    def wall_height_pitch(self, pitch, soffit_wall_height, side_wall_length):
        self.pitch = pitch
        self.soffit_wall_height = soffit_wall_height
        self.soffit = self.soffit_wall_height - self.overhang * tan(self.pitch)
        self.peak = self.soffit_wall_height + side_wall_length * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=pitch, thickness=self.thickness)


if __name__ == '__main__':
    main()
