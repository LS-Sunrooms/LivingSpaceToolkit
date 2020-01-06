#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import re

list_ = re.compile(r'\'|ft|feet|\"|in')


# noinspection SpellCheckingInspection
class CommonCalcs:
    """
    This class performs many of the common calculations between scenarios for use in Studio.py and Cathedral.py. It uses
    the math and re packages.
    """

    def __init__(self, wall_length, side_wall_length, pitch, soffit, overhang, tabwidget, thickness, endcut, peak,
                 max_h, wall_height):
        """
        Initiallizes common variables used in methods. The pitch has to be in radians. The floats are in inches.
        :param wall_length: float
        :param side_wall_length: float
        :param pitch: float
        :param soffit: float
        :param overhang: float
        :param tabwidget: int
        :param thickness: float
        :param endcut: str
        """
        self.wall_length = wall_length
        self.side_wall_length = side_wall_length
        self.pitch = pitch
        self.soffit = soffit
        self.overhang = overhang
        self.tabWidget = tabwidget
        self.endcut = endcut
        self.panel_thickness = thickness
        self.angled_thickness = angled(pitch=pitch, thickness=thickness)
        if self.overhang > 16:
            self.side_overhang = 16
        else:
            self.side_overhang = self.overhang
        self.peak = peak
        self.max_h = max_h
        self.wall_height = wall_height

    def drip_edge(self):
        """
        Returns the drip edge height given the soffit and angled thickness. Returns in units of inches.
        :return: float
        """
        if self.endcut == 'plum_T_B':
            drip = self.soffit + self.angled_thickness
        else:
            drip = self.soffit + self.panel_thickness * math.cos(self.pitch)
        return drip

    def panel_length(self):
        """
        Calculates the panel length and if it exceeds the max allowed panel length.
        :return: [float, bool]
        """
        max_panel_length = False
        panel_tolerance = False
        if self.endcut == 'uncut':
            p_length = (self.side_wall_length + self.overhang) / math.cos(self.pitch)
        else:
            p_bottom = (self.side_wall_length + self.overhang) / (math.cos(self.pitch))
            p_top = (self.side_wall_length + self.overhang + self.panel_thickness * math.sin(
                self.pitch)) / math.cos(self.pitch)
            p_length = max(p_bottom, p_top)
        if p_length % 12 <= 1:  # This checks to see if the panel length is a maximum 1 inch past the nearest foot
            panel_tolerance = True
            # Returns panel length (in inches) rounded down to nearest foot and adds the 1 inch tolerance
            panel_length = math.floor(p_length / 12) * 12 + 1
        else:
            panel_length = math.ceil(p_length / 12) * 12  # Returns panel length (in inches) rounded up to nearest foot
        if panel_length > 288:
            max_panel_length = True
            panel_length /= 2
        return [panel_length, max_panel_length, panel_tolerance]

    def roof_panels(self):
        """
        Calculates the roof area, number  of panels, and the side overhang.
        :return: [float, int, float]
        """
        minmax_overhang = [False, False]
        split = False
        if self.tabWidget == 0:  # Studio Tab
            roof_width = self.wall_length + self.side_overhang * 2
        elif self.tabWidget == 1:  # Cathedral Tab
            roof_width = self.wall_length + self.side_overhang
        if self.tabWidget == 1 and ((roof_width/32) <= round((roof_width/32)*2)/2):
            roof_panels = round((roof_width/32)*2)/2
            split = True
        else:
            roof_panels = math.ceil(roof_width / 32)
        if self.tabWidget == 0:  # Studio Tab
            if (roof_panels * 32 - self.wall_length) / 2 < self.side_overhang:
                # Overhang too short
                side_overhang = (roof_panels * 32 - self.wall_length) / 2
                minmax_overhang[0] = True
            elif (roof_panels * 32 - self.wall_length) / 2 > 16:
                # Overhang too long
                side_overhang = (roof_panels * 32 - self.wall_length) / 2
                minmax_overhang[1] = True
            else:
                side_overhang = self.side_overhang
        elif self.tabWidget == 1:  # Cathedral Tab
            if (roof_panels * 32 - self.wall_length) < self.side_overhang:
                # Overhang too short
                side_overhang = roof_panels * 32 - self.wall_length
                minmax_overhang[0] = True
            elif (roof_panels * 32 - self.wall_length) > 16:
                # Overhang too long
                side_overhang = roof_panels * 32 - self.wall_length
                minmax_overhang[1] = True
            else:
                side_overhang = self.side_overhang
        panel_length, max_panel_length = self.panel_length()[0:2]
        if max_panel_length is True:
            roof_area = math.ceil(panel_length * 2 * roof_panels * 32)
        else:
            roof_area = math.ceil(panel_length * roof_panels * 32)
        return [roof_area, roof_panels, side_overhang, minmax_overhang, split]

    def hang_rail(self):
        """
        Calculates the hang rail length and if it exceeds the maximum allowed length.
        :return: [float, bool]
        """
        max_hang_rail_length = False
        roof_panels = self.roof_panels()[1]
        panel_length = self.panel_length()[0]
        hang_rail = 0
        if self.tabWidget == 0:  # Studio Tab
            hang_rail = roof_panels * 32
        elif self.tabWidget == 1:  # Cathedral Tab
            hang_rail = panel_length
        if hang_rail > 216:
            max_hang_rail_length = True
            hang_rail /= 2
        return [hang_rail, max_hang_rail_length]

    def fascia(self):
        """
        Calculates the length of the fascia on the forward wall and sides and if they exceed the maximum allowed length.
        :return: [float, float, [bool, bool]]
        """
        max_fascia_length = [False, False]
        roof_panels = self.roof_panels()[1]
        panel_length = self.panel_length()[0]
        fascia_wall = 0
        if self.tabWidget == 0:  # Studio Tab
            fascia_wall = roof_panels * 32 + 12
        elif self.tabWidget == 1:  # Cathedral Tab
            fascia_wall = roof_panels * 32 + 6
        fascia_sides = panel_length + 6
        if fascia_wall > 216:
            max_fascia_length[0] = True
            fascia_wall /= 2
        if fascia_sides > 216:
            max_fascia_length[1] = True
            fascia_sides /= 2
        return [fascia_wall, fascia_sides, max_fascia_length]

    def armstrong_panels(self):
        """
        Calculates the number of armstrong boxes for the roof.
        :return: int
        """
        rake_length = self.side_wall_length / math.cos(self.pitch)
        armstrong_area = rake_length * self.wall_length / 144  # To get area in sq. ft.
        return math.ceil((armstrong_area + (armstrong_area * 0.1)) / 29)


def angled(pitch, thickness):
    """
    Calculates the angled thickness given pitch and the panel thickness. Pitch has to be in radians.
    :param pitch: float
    :param thickness: float
    :return: float
    """
    return thickness * (math.sin(math.pi / 2) / math.sin(math.pi / 2 - pitch))


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
        pitch = math.atan(pitch_input.base / 12)
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


def estimate_drip_from_peak(peak, estimate_pitch, wall_length, side_wall_length, overhang, thickness, tab, endcut):
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
    wall_height = peak - side_wall_length * math.tan(estimate_pitch)
    soffit = wall_height - overhang * math.tan(estimate_pitch)
    max_h = peak + angled(estimate_pitch, thickness)
    estimate_drip = CommonCalcs(wall_length, side_wall_length, estimate_pitch, soffit, overhang, tab, thickness, endcut,
                                peak, max_h, wall_height)
    return estimate_drip.drip_edge()
