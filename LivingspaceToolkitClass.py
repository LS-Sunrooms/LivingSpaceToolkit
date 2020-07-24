#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module holds the classes and functions for creating the Livingspace style of Sunrooms.

Classes:
    Sunroom
    Studio
    Cathedral

Functions:
    angled
    assume_units
    pitch_input
    pitch_estimate
    sixteenth
    estimate_drip_from_peak
    calculate_armstrong_panels
"""

from math import sin, cos, tan, atan, atan2, pi
from math import floor as m_floor
from math import ceil as m_ceil
from re import compile as re_compile
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s:[%(name)s]:[%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
file_handler = logging.FileHandler('LS Toolkit.log', mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

_units = re_compile(r'\'|ft|feet|\"|in')
end_cuts = ['uncut', 'plum_T_B', 'plum_T']


def angled(pitch, thickness):
    """
    Calculates the angled thickness given pitch and the panel thickness. Pitch has to be in radians.
    :param pitch: float
    :param thickness: float
    :return: float
    """
    angle = None
    try:
        angle = thickness * (sin(pi / 2) / sin(pi / 2 - pitch))
    except ZeroDivisionError as err:
        pass
        # logger.exception(err)
    return angle


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


def estimate_drip_from_peak(peak, estimate_pitch, pitched_wall_length, overhang, thickness, endcut, awall, bwall,
                            cwall):
    """
    This method is used to help estimate the pitch. Since I forgot how to do numerical methods this will have to do. All
    lengths must be in inches, the estimated pitch in radians, and this assumes you are cycling through a list of
    pitches.
    :param peak: float: Peak height of the sunroom in inches
    :param estimate_pitch: float: The estimated pitch of the room in radians
    :param pitched_wall_length: float: The length of the pitched-side wall in inches
    :param overhang: float: The overhang in inches
    :param thickness: float: Roof panel thickness in inches
    :param endcut: str: The endcut type as a string
    :param awall: float: Height of the A-side wall in inches
    :param bwall: float: Height of the B-side wall in inches
    :param cwall: float: Height of the C-side wall in inches
    :return: float: Returns the drip edge height in inches
    """
    wall_height = peak - pitched_wall_length * tan(estimate_pitch)
    soffit = wall_height - overhang * tan(estimate_pitch)
    estimate_drip = Sunroom(overhang=overhang, awall=awall, bwall=bwall, cwall=cwall, thickness=thickness,
                            endcut=endcut)
    drip_edge = estimate_drip.calculate_drip_edge(soffit, estimate_pitch)
    return drip_edge


# noinspection SpellCheckingInspection
def calculate_armstrong_panels(pitch, pitched_wall, unpitched_wall):
    """
    Calculates the number of armstrong boxes for the roof.
    :param pitch: float: The pitch of the roof in radians
    :param pitched_wall: float: The length of the pitched wall in inches
    :param unpitched_wall: float: The length of the unpitched wall in inches
    :return:
    """
    rake_length = pitched_wall / cos(pitch)
    armstrong_area = rake_length * unpitched_wall / 144  # To get area in sq. ft.
    return m_ceil((armstrong_area + (armstrong_area * 0.1)) / 29)


# noinspection SpellCheckingInspection
class Sunroom:
    """
    This class will be the base class for the Studio and Cathedral type of sunrooms.

    ...
    Attributes
    ----------
    overhang: float
        Overhang on sunroom
    awall: float
        length of A-Side wall
    bwall: float
        length of B-Side wall
    cwall: float
        length of C-Side wall
    thickness: float
        Thickness of roof panels

    Methods
    -------
    calculate_drip_edge(soffit, pitch)
        Calculates height of drip edge
    _calculate_panel_length(pitch, pitched_wall)
        Calculates length of roof panels
    _calculate_roof_panels(soffit_wall, panel_length_dict)
        Virtual method to be modefied in inherited classes
    _calculate_hang_rail(panel_dict)
        Virtual method to be modefied in inherited classes
    _calculate_fascia(roof_panel_dict, panel_length_dict)
        Virtual method to be modefied in inherited classes
    calculate_sunroom()
        Virtual method to be modefied in inherited classes
    wall_height_pitch(pitch, soffit_wall_height):
        Virtual method to be modefied in inherited classes
    wall_height_peak_height(soffit_wall_height, peak):
        Virtual method to be modefied in inherited classes
    max_height_pitch(pitch, max_h):
        Virtual method to be modefied in inherited classes
    soffit_height_peak_height(peak, soffit):
        Virtual method to be modefied in inherited classes
    soffit_height_pitch(pitch, soffit):
        Virtual method to be modefied in inherited classes
    drip_edge_peak_height(drip_edge, peak):
        Virtual method to be modefied in inherited classes
    drip_edge_pitch(drip_edge, pitch)
        Virtual method to be modefied in inherited classes
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
        """
        Returns the drip edge height given the soffit and angled thickness. Returns in units of inches.

        :param soffit: float: Soffit height in inches
        :param pitch: float: Pitch in radians
        :return:
        """
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
        """Virtual method to be modefied in inherited classes"""
        pass

    def _calculate_hang_rail(self, panel_dict):
        """Virtual method to be modefied in inherited classes"""
        pass

    def _calculate_fascia(self, roof_panel_dict, panel_length_dict):
        """Virtual method to be modefied in inherited classes"""
        pass

    def calculate_sunroom(self):
        """Virtual method to be modefied in inherited classes"""
        pass

    # Scenarios
    def wall_height_pitch(self, pitch, soffit_wall_height):
        """Virtual method to be modefied in inherited classes"""
        pass

    def wall_height_peak_height(self, soffit_wall_height, peak):
        """Virtual method to be modefied in inherited classes"""
        pass

    def max_height_pitch(self, pitch, max_h):
        """Virtual method to be modefied in inherited classes"""
        pass

    def soffit_height_peak_height(self, peak, soffit):
        """Virtual method to be modefied in inherited classes"""
        pass

    def soffit_height_pitch(self, pitch, soffit):
        """Virtual method to be modefied in inherited classes"""
        pass

    def drip_edge_peak_height(self, drip_edge, peak):
        """Virtual method to be modefied in inherited classes"""
        pass

    def drip_edge_pitch(self, drip_edge, pitch):
        """Virtual method to be modefied in inherited classes"""
        pass


# noinspection SpellCheckingInspection
class Studio(Sunroom):
    """
    Class for creating Studio style sunroom

    ...
    Attributes
    ----------
    overhang: float
        Overhang on sunroom
    awall: float
        length of A-Side wall
    bwall: float
        length of B-Side wall
    cwall: float
        length of C-Side wall
    thickness: float
        Thickness of roof panels

    Methods
    -------
    _calculate_roof_panels(soffit_wall, panel_length_dict)
        Method used to calculate number of roof panels and roof area
    _calculate_hang_rail(panel_dict)
        Method used for calculating length of hang rails
    _calculate_fascia(roof_panel_dict, panel_length_dict)
        Method used for calculating length of fascia
    calculate_sunroom()
        Method used to calculate sunroom properties after scenario has been selected
    wall_height_pitch(pitch, soffit_wall_height):
        Scenario 1
    wall_height_peak_height(soffit_wall_height, peak):
        Scenario 2
    max_height_pitch(pitch, max_h):
        Scenario 3
    soffit_height_peak_height(peak, soffit):
        Scenario 4
    soffit_height_pitch(pitch, soffit):
        Scenario 5
    drip_edge_peak_height(drip_edge, peak):
        Scenario 6
    drip_edge_pitch(drip_edge, pitch)
        Scenario 7
    """

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
        """
        Calculate roof area, number of panels, and side overhang
        :param soffit_wall:
        :param panel_length_dict:
        :return:
        """
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
        """
        Calculate hang rail length
        :param panel_dict:
        :return:
        """
        max_hang_rail_length = False
        roof_panels = panel_dict['Roof Panels']
        hang_rail = roof_panels * 32
        if hang_rail > 216:
            max_hang_rail_length = True
            hang_rail /= 2
        return {'Hang Rail': hang_rail, 'Hang Rail Check': max_hang_rail_length}

    def _calculate_fascia(self, roof_panel_dict, panel_length_dict):
        """
        Calculate fascia length
        :param roof_panel_dict:
        :param panel_length_dict:
        :return:
        """
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
        """Calculate sunroom properties"""
        self.panel_length_dict = self._calculate_panel_length(self.pitch, self.pitched_wall)
        self.roof_panel_dict = self._calculate_roof_panels(self.soffit_wall, self.panel_length_dict)
        self.hang_rail_dict = self._calculate_hang_rail(self.roof_panel_dict)
        self.fascia_dict = self._calculate_fascia(self.roof_panel_dict, self.panel_length_dict)
        self.armstrong_panels = calculate_armstrong_panels(self.pitch, self.pitched_wall, self.soffit_wall)

    # Scenarios
    # Scenario 1
    def wall_height_pitch(self, pitch, soffit_wall_height):
        """This method is designed for Scenario 1: Wall Height and Pitch. Wall Height must be in inches, pitch must be
        in radians."""
        self.pitch = pitch
        self.unpitched_wall = soffit_wall_height
        self.soffit = self.unpitched_wall - self.overhang * tan(self.pitch)
        self.peak = self.unpitched_wall + self.pitched_wall * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=self.pitch, thickness=self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 2
    def wall_height_peak_height(self, soffit_wall_height, peak):
        """This method is designed for Scenario 2: Wall Height and Peak Height. Both heights must be in inches."""
        self.unpitched_wall = soffit_wall_height
        self.peak = peak
        self.pitch = atan((self.peak - self.unpitched_wall) / max(self.awall, self.cwall))
        self.soffit = self.unpitched_wall - self.overhang * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=self.pitch, thickness=self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 3
    def max_height_pitch(self, pitch, max_h):
        """This method is designed for Scenario 3: Max Height and Pitch. The max height must be inches and pitch must be
        radians."""
        self.pitch = pitch
        self.max_h = max_h
        self.unpitched_wall = self.max_h - max(self.awall, self.cwall) * tan(self.pitch) - \
                              angled(pitch=self.pitch, thickness=self.thickness)
        self.soffit = self.unpitched_wall - self.overhang * tan(self.pitch)
        self.peak = self.max_h - angled(pitch=self.pitch, thickness=self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 4
    def soffit_height_peak_height(self, peak, soffit):
        """This method is designed for Scenario 4: Soffit Height and Peak Height. Both heights must be in inches."""
        self.soffit = soffit
        self.peak = peak
        self.pitch = atan((self.peak - self.soffit) / (max(self.awall, self.cwall) + self.overhang))
        self.unpitched_wall = self.soffit + self.overhang * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=self.pitch, thickness=self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 5
    def soffit_height_pitch(self, pitch, soffit):
        """This method is designed for Scenario 5: Soffit Height and Pitch. Soffit height must be in inches and pitch
        must be in radians."""
        self.pitch = pitch
        self.soffit = soffit
        self.unpitched_wall = self.soffit + self.overhang * tan(self.pitch)
        self.peak = self.unpitched_wall + self.pitched_wall * tan(self.pitch)
        self.max_h = self.peak + angled(pitch=self.pitch, thickness=self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)

    # Scenario 6
    def drip_edge_peak_height(self, drip_edge, peak):
        """This method is designed for Scenario 6: Drip Edge and Peak Height. Drip edge and peak height must be in
        inches."""
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
                                               pitched_wall_length=self.pitched_wall, overhang=self.overhang,
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
        """This method is designed for Scenario 7: Drip Edge and Pitch. Drip Edge must be in inches while pitch must be
        in radians."""
        self.pitch = pitch
        self.drip_edge = drip_edge
        self.soffit = self.drip_edge - angled(self.pitch, self.thickness)
        self.unpitched_wall = self.soffit + self.overhang * tan(pitch)
        self.peak = self.unpitched_wall + self.pitched_wall * tan(pitch)
        self.max_h = self.peak + angled(self.pitch, self.thickness)
        self.drip_edge = self.calculate_drip_edge(self.soffit, self.pitch)


# noinspection SpellCheckingInspection
class Cathedral(Sunroom):
    """
    Class for creating Cathedral style sunroom

    ...
    Attributes
    ----------
    overhang: float
        Overhang on sunroom
    awall: float
        length of A-Side wall
    bwall: float
        length of B-Side wall
    cwall: float
        length of C-Side wall
    thickness: float
        Thickness of roof panels

    Methods
    -------
    _calculate_roof_panels(soffit_wall, panel_length_dict)
        Method used to calculate number of roof panels and roof area
    _calculate_hang_rail(panel_dict)
        Method used for calculating length of hang rails
    _calculate_fascia(roof_panel_dict, panel_length_dict)
        Method used for calculating length of fascia
    calculate_sunroom()
        Method used to calculate sunroom properties after scenario has been selected
    wall_height_pitch(pitch, soffit_wall_height):
        Scenario 1
    wall_height_peak_height(soffit_wall_height, peak):
        Scenario 2
    max_height_pitch(pitch, max_h):
        Scenario 3
    soffit_height_peak_height(peak, soffit):
        Scenario 4
    soffit_height_pitch(pitch, soffit):
        Scenario 5
    drip_edge_peak_height(drip_edge, peak):
        Scenario 6
    drip_edge_pitch(drip_edge, pitch)
        Scenario 7
    """

    def __init__(self, overhang, awall, bwall, cwall, thickness, endcut):
        super().__init__(overhang, awall, bwall, cwall, thickness, endcut)
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
        """Calculate roof area, number of panels, and side overhang"""
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
        """Calculate hang rail length"""
        max_hang_rail_length = False
        panel_length = panel_dict['Panel Length']
        hang_rail = panel_length
        if hang_rail > 216:
            max_hang_rail_length = True
            hang_rail /= 2
        return {'Hang Rail': hang_rail, 'Hang Rail Check': max_hang_rail_length}

    def _calculate_fascia(self, roof_panel_dict, panel_length_dict):
        """Calculate fascia length"""
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
        """Calculate sunroom properties"""
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
        """This method is designed for Scenario 1: Wall Height and Pitch. Wall Height must be in inches, pitch must be
            in radians."""
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
        """This method is designed for Scenario 2: Wall Height and Peak Height. Both heights must be in inches."""
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
        """This method is designed for Scenario 3: Max Height and Pitch. The max height must be inches and pitch must be
        radians."""
        self.a_pitch = pitch[0]
        self.c_pitch = pitch[1]
        self.max_h = max_h
        self.peak = (self.bwall * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        self.f_peak = self.max_h - max(angled(self.a_pitch, self.thickness), angled(self.c_pitch, self.thickness)) - \
                      (self.post_width * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch)
        self.a_pitched_wall = self.peak / tan(self.a_pitch)
        self.c_pitched_wall = self.peak / tan(self.c_pitch)
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
        """This method is designed for Scenario 4: Soffit Height and Peak Height. Both heights must be in inches."""
        self.a_soffit = max(soffit[0], soffit[1])
        self.c_soffit = max(soffit[0], soffit[1])
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
        """This method is designed for Scenario 5: Soffit Height and Pitch. Soffit height must be in inches and pitch
         must be in radians."""
        self.a_soffit = max(soffit[0], soffit[1])
        self.c_soffit = max(soffit[0], soffit[1])
        self.a_pitch = pitch[0]
        self.c_pitch = pitch[1]
        self.a_unpitched_wall_h = self.a_soffit + self.overhang * tan(self.a_pitch)
        self.c_unpitched_wall_h = self.a_soffit + self.overhang * tan(self.c_pitch)
        self.peak = (self.bwall * sin(self.a_pitch) * sin(self.c_pitch)) / sin(pi - self.a_pitch - self.c_pitch) + \
                    max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)
        self.a_pitched_wall = (self.peak - max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)) / tan(self.a_pitch)
        self.c_pitched_wall = (self.peak - max(self.a_unpitched_wall_h, self.c_unpitched_wall_h)) / tan(self.c_pitch)
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
        """This method is designed for Scenario 6: Drip Edge and Peak Height. Drip edge and peak height must be in
        inches."""
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
                                               pitched_wall_length=self.bwall / 2 - self.post_width / 2,
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
        """This method is designed for Scenario 7: Drip Edge and Pitch. Drip Edge must be in inches while pitch must be
        in radians."""
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
