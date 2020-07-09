#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import sin, cos, tan, atan, atan2, pi
from math import floor as mfloor
from math import ceil as mceil
from re import compile as re_compile

list_ = re_compile(r'\'|ft|feet|\"|in')


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
            drip = self.soffit + self.panel_thickness * cos(self.pitch)
        return drip

    def panel_length(self):
        """
        Calculates the panel length and if it exceeds the max allowed panel length.
        :return: [float, bool]
        """
        max_panel_length = False
        panel_tolerance = False
        if self.endcut == 'uncut':
            p_length = (self.side_wall_length + self.overhang) / cos(self.pitch)
        else:
            p_bottom = (self.side_wall_length + self.overhang) / (cos(self.pitch))
            p_top = (self.side_wall_length + self.overhang + self.panel_thickness * sin(
                self.pitch)) / cos(self.pitch)
            p_length = max(p_bottom, p_top)
        if p_length % 12 <= 1:  # This checks to see if the panel length is a maximum 1 inch past the nearest foot
            panel_tolerance = True
            # Returns panel length (in inches) rounded down to nearest foot and adds the 1 inch tolerance
            # CORRECTION: We will NOT add 1 inch. Just round down instead
            # panel_length = mfloor(p_length / 12) * 12 + 1
            panel_length = mfloor(p_length / 12) * 12
        else:
            panel_length = mceil(p_length / 12) * 12  # Returns panel length (in inches) rounded up to nearest foot
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
        if self.tabWidget == 1 and ((roof_width / 32) <= mfloor(roof_width / 32) + .5):
            roof_panels = mfloor(roof_width / 32) + .5
            split = True
        else:
            roof_panels = mceil(roof_width / 32)
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
            roof_area = mceil(panel_length * 2 * roof_panels * 32)
        else:
            roof_area = mceil(panel_length * roof_panels * 32)
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
        rake_length = self.side_wall_length / cos(self.pitch)
        armstrong_area = rake_length * self.wall_length / 144  # To get area in sq. ft.
        return mceil((armstrong_area + (armstrong_area * 0.1)) / 29)


class StudioCalcs:
    """
    This class performs the calculations for a studio style sunroom. It works in conjunction with CommonCalcs.py.
    Pitch of the roof is needed but calculated separately and needs to be in radians.
    """

    def __init__(self, overhang, awall, bwall, cwall, panel_thickness, endcut):
        """
        Initiallizes common variables used in methods. Floats are in inches.
        :param overhang: float
        :param awall: float
        :param bwall: float
        :param cwall: float
        :param panel_thickness: float
        :param endcut: str
        """
        self.awall = awall
        self.bwall = bwall
        self.cwall = cwall
        self.panel_thickness = panel_thickness
        self.tabwidget = 0
        self.endcut = endcut
        self.overhang = overhang
        self.side_wall = max(self.awall, self.cwall)

    def wall_height_pitch(self, pitch, b_wall_height):
        """
        This method is designed for Scenario 1: Wall Height and Pitch. Wall Height must be in inches, pitch must be in
        radians. It returns the results where the length is in inches and pitch in radians.
        :param pitch: float
        :param b_wall_height: float
        :return: class <CommonCalcs.CommonCalcs>
        """
        soffit = b_wall_height - self.overhang * tan(pitch)
        peak = b_wall_height + self.side_wall * tan(pitch)
        max_h = peak + angled(pitch=pitch, thickness=self.panel_thickness)
        common = CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
                             overhang=self.overhang, tabwidget=self.tabwidget, thickness=self.panel_thickness,
                             endcut=self.endcut, peak=peak, max_h=max_h, wall_height=b_wall_height)
        return common

    def wall_height_peak_height(self, b_wall_height, peak):
        """
        This method is designed for Scenario 2: Wall Height and Peak Height. Both heights must be in inches. It returns
        the results where the length is in inches and pitch in radians.
        :param b_wall_height: float
        :param peak: float
        :return: class <CommonCalcs.CommonCalcs>
        """
        pitch = atan((peak - b_wall_height) / max(self.awall, self.cwall))
        soffit = b_wall_height - self.overhang * tan(pitch)
        max_h = peak + angled(pitch=pitch, thickness=self.panel_thickness)
        common = CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
                             overhang=self.overhang, tabwidget=self.tabwidget, thickness=self.panel_thickness,
                             endcut=self.endcut, peak=peak, max_h=max_h, wall_height=b_wall_height)
        return common

    def max_height_pitch(self, pitch, max_h):
        """
        This method is designed for Scenario 3: Max Height and Pitch. The max height must be inches and pitch must be
        radians. It returns the results where the length is in inches and pitch in radians.
        :param pitch: float
        :param max_h: float
        :return: class <CommonCalcs.CommonCalcs>
        """
        b_wall_height = max_h - max(self.awall, self.cwall) * tan(pitch) - \
                        angled(pitch=pitch, thickness=self.panel_thickness)
        soffit = b_wall_height - self.overhang * tan(pitch)
        peak = max_h - angled(pitch=pitch, thickness=self.panel_thickness)
        common = CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
                             overhang=self.overhang, tabwidget=self.tabwidget, thickness=self.panel_thickness,
                             endcut=self.endcut, peak=peak, max_h=max_h, wall_height=b_wall_height)
        return common

    def soffit_height_peak_height(self, peak, soffit):
        """
        This method is designed for Scenario 4: Soffit Height and Peak Height. Both heights must be in inches. It
        returns the results where the length is in inches and pitch in radians.
        :param peak: float
        :param soffit: float
        :return: class <CommonCalcs.CommonCalcs>
        """
        pitch = atan((peak - soffit) / (max(self.awall, self.cwall) + self.overhang))
        b_wall_height = soffit + self.overhang * tan(pitch)
        max_h = peak + angled(pitch=pitch, thickness=self.panel_thickness)
        common = CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
                             overhang=self.overhang, tabwidget=self.tabwidget, thickness=self.panel_thickness,
                             endcut=self.endcut, peak=peak, max_h=max_h, wall_height=b_wall_height)
        return common

    def soffit_height_pitch(self, pitch, soffit):
        """
        This method is designed for Scenario 5: Soffit Height and Pitch. Soffit height must be in inches and pitch must
        be in radians. It returns the results where the length is in inches and pitch in radians.
        :param pitch: float
        :param soffit: float
        :return: class <CommonCalcs.CommonCalcs>
        """
        b_wall_height = soffit + self.overhang * tan(pitch)
        peak = b_wall_height + self.side_wall * tan(pitch)
        max_h = peak + angled(pitch=pitch, thickness=self.panel_thickness)
        common = CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
                             overhang=self.overhang, tabwidget=self.tabwidget, thickness=self.panel_thickness,
                             endcut=self.endcut, peak=peak, max_h=max_h, wall_height=b_wall_height)
        return common

    def drip_edge_peak_height(self, drip_edge, peak):
        """
        This method is designed for Scenario 6: Drip Edge and Peak Height. Drip edge and peak height must be in inches.
        It cycles through a number of pitches and passes them into CommonCalcs.py to determine the estimated drip edge.
        Once it gets an estimated drip edge close to the given one it uses that pitch for all calculations.
        :param drip_edge: float
        :param peak: float
        :return: class <CommonCalcs.CommonCalcs>
        """
        tol = 0.01
        diff = 100
        incr = 0.1
        ratio_pitch = 0.0
        while diff > tol:
            old_ratio_pitch = ratio_pitch
            ratio_pitch += incr
            pitch = atan2(ratio_pitch, 12)
            drip_est = estimate_drip_from_peak(peak=peak, estimate_pitch=pitch, wall_length=self.bwall,
                                               side_wall_length=self.side_wall, overhang=self.overhang,
                                               thickness=self.panel_thickness, tab=self.tabwidget,
                                               endcut=self.endcut)
            diff = abs(drip_edge - drip_est)
            if ratio_pitch > 12:
                break
            if drip_est < drip_edge:
                ratio_pitch = old_ratio_pitch
                incr /= 2
        b_wall_height = peak - self.side_wall * tan(pitch)
        soffit = b_wall_height - self.overhang * tan(pitch)
        max_h = peak + angled(pitch, self.panel_thickness)
        common = CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
                             overhang=self.overhang, tabwidget=self.tabwidget, thickness=self.panel_thickness,
                             endcut=self.endcut, peak=peak, max_h=max_h, wall_height=b_wall_height)
        return common

    def drip_edge_pitch(self, drip_edge, pitch):
        """
        This method is designed for Scenario 7: Drip Edge and Pitch. Drip Edge must be in inches while pitch must be in
        radians. It returns the results where the length is in inches and pitch in radians.
        :param drip_edge: float
        :param pitch: float
        :return: class <CommonCalcs.CommonCalcs>
        """
        soffit = drip_edge - angled(pitch, self.panel_thickness)
        b_wall_height = soffit + self.overhang * tan(pitch)
        peak = b_wall_height + self.side_wall * tan(pitch)
        max_h = peak + angled(pitch, self.panel_thickness)
        common = CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
                             overhang=self.overhang, tabwidget=self.tabwidget, thickness=self.panel_thickness,
                             endcut=self.endcut, peak=peak, max_h=max_h, wall_height=b_wall_height)
        return common


class CathedralCalcs:
    """
    This class performs the calculations for a cathedral style sunroom. It works in conjunction with CommonCalcs.py.
    Pitch of the roof is needed but calculated separately and needs to be in radians.
    """

    def __init__(self, overhang, awall, bwall, cwall, panel_thickness, endcut):
        """
        Initiallizes common variables used in methods. Floats are in inches.
        :param overhang: float
        :param awall: float
        :param bwall: float
        :param cwall: float
        :param panel_thickness: float
        :param endcut: str
        """
        self.overhang = overhang
        self.awall = awall
        self.bwall = bwall
        self.cwall = cwall
        self.panel_thickness = panel_thickness
        self.tabwidget = 1
        self.endcut = endcut
        self.post_width = 3.25
        self.wall_length = max(awall, cwall)

    def wall_height_pitch(self, a_pitch, c_pitch, a_wall_height, c_wall_height):
        """
        This method is designed for Scenario 1: Wall Height and Pitch. Wall Height must be in inches, pitch must be in
        radians. It returns a tuple with common calculations for each side of a studio roof. The length is in inches and
        pitch in radians.
        :param a_pitch: float
        :param c_pitch: float
        :param a_wall_height: float
        :param c_wall_height: float
        :return: list[class <CommonCalcs.CommonCalcs>, class <CommonCalcs.CommonCalcs>]
        """
        common = [None, None]
        a_soffit = a_wall_height - self.overhang * tan(a_pitch)
        c_soffit = c_wall_height - self.overhang * tan(c_pitch)
        soffit = max(a_soffit, c_soffit)
        peak = (self.bwall * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch) + \
               max(a_wall_height, c_wall_height)
        a_side_wall = (peak - max(a_wall_height, c_wall_height)) / tan(a_pitch)
        c_side_wall = (peak - max(a_wall_height, c_wall_height)) / tan(c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        f_peak = peak - (self.post_width * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch -
                                                                              c_pitch)
        max_h = f_peak + max(angled(a_pitch, self.panel_thickness), angled(c_pitch, self.panel_thickness)) + \
                (self.post_width * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch)
        common[0] = CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                wall_height=a_wall_height)
        common[1] = CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                wall_height=c_wall_height)
        return common

    def wall_height_peak_height(self, a_wall_height, c_wall_height, peak):
        """
        This method is designed for Scenario 2: Wall Height and Peak Height. The heights must be in inches. It returns a
        tuple with common calculations for each side of a studio roof. The length is in inches and pitch in radians.
        :param a_wall_height: float
        :param c_wall_height: float
        :param peak: float
        :return: list[class <CommonCalcs.CommonCalcs>, class <CommonCalcs.CommonCalcs>]
        """
        common = [None, None]
        a_side_wall = self.bwall / 2
        c_side_wall = self.bwall / 2
        a_pitch = atan2(float(peak - a_wall_height), float(a_side_wall - self.post_width / 2))
        c_pitch = atan2(float(peak - c_wall_height), float(c_side_wall - self.post_width / 2))
        a_soffit = a_wall_height - self.overhang * tan(a_pitch)
        c_soffit = c_wall_height - self.overhang * tan(c_pitch)
        soffit = max(a_soffit, c_soffit)
        a_max_h = peak + angled(a_pitch, self.panel_thickness) + \
                  (self.post_width * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch)
        c_max_h = peak + angled(c_pitch, self.panel_thickness) + \
                  (self.post_width * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch)
        max_h = max(a_max_h, c_max_h)
        common[0] = CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=peak, max_h=max_h,
                                wall_height=a_wall_height)
        common[1] = CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=peak, max_h=max_h,
                                wall_height=c_wall_height)
        return common

    def max_height_pitch(self, max_h, a_pitch, c_pitch):
        """
        This method is designed for Scenario 3: Max Height and Pitch. Max height has to be in inches and pitch in
        radians. It returns a tuple with common calculations for each side of a studio roof. The length is in inches and
        pitch in radians.
        :param max_h: float
        :param a_pitch: float
        :param c_pitch: float
        :return: list[class <CommonCalcs.CommonCalcs>, class <CommonCalcs.CommonCalcs>]
        """
        common = [None, None]
        peak = (self.bwall * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        f_peak = max_h - max(angled(a_pitch, self.panel_thickness), angled(c_pitch, self.panel_thickness)) - \
                 (self.post_width * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch)
        a_side_wall = peak / tan(a_pitch)
        c_side_wall = peak / tan(c_pitch)
        # a_wall_height = f_peak - peak
        a_wall_height = max_h - max(angled(a_pitch, self.panel_thickness), angled(c_pitch, self.panel_thickness)) \
                        - (self.bwall * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch)
        c_wall_height = a_wall_height
        a_soffit = a_wall_height - self.overhang * tan(a_pitch)
        c_soffit = c_wall_height - self.overhang * tan(c_pitch)
        soffit = max(a_soffit, c_soffit)
        common[0] = CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                wall_height=a_wall_height)
        common[1] = CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                wall_height=c_wall_height)
        return common

    def soffit_height_peak_height(self, a_soffit, c_soffit, peak):
        """
        This method is designed for Scenario 4: Soffit Height and Peak Height. The heights must be in inches. It returns
        a tuple with common calculations for each side of a studio roof. The length is in inches and pitch in radians.
        This assumes the peak height given is the Fenevision peak height.
        :param a_soffit: float
        :param c_soffit: float
        :param peak: float
        :return: list[class <CommonCalcs.CommonCalcs>, class <CommonCalcs.CommonCalcs>]
        """
        common = [None, None]
        soffit = max(a_soffit, c_soffit)
        a_side_wall = self.bwall / 2
        c_side_wall = self.bwall / 2
        a_pitch = atan((peak - soffit) / (a_side_wall + self.overhang - self.post_width / 2))
        c_pitch = atan((peak - soffit) / (c_side_wall + self.overhang - self.post_width / 2))
        a_wall_height = soffit + self.overhang * tan(a_pitch)
        c_wall_height = soffit + self.overhang * tan(c_pitch)
        h = (self.post_width * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch)
        a_max_h = peak + angled(a_pitch, self.panel_thickness) + h
        c_max_h = peak + angled(c_pitch, self.panel_thickness) + h
        max_h = max(a_max_h, c_max_h)
        common[0] = CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=peak, max_h=max_h,
                                wall_height=a_wall_height)
        common[1] = CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=peak, max_h=max_h,
                                wall_height=c_wall_height)
        return common

    def soffit_height_pitch(self, a_pitch, c_pitch, a_soffit, c_soffit):
        """
        This method is designed for Scenario 5: Soffit Height and Pitch. Soffit height has to be in inches and pitch in
        radians. It returns a tuple with common calculations for each side of a studio roof. The length is in inches and
        pitch in radians.
        :param a_pitch: float
        :param c_pitch: float
        :param a_soffit: float
        :param c_soffit: float
        :return: list[class <CommonCalcs.CommonCalcs>, class <CommonCalcs.CommonCalcs>]
        """
        common = [None, None]
        soffit = max(a_soffit, c_soffit)
        a_wall_height = soffit + self.overhang * tan(a_pitch)
        c_wall_height = soffit + self.overhang * tan(c_pitch)
        peak = (self.bwall * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch) + \
               max(a_wall_height, c_wall_height)
        a_side_wall = (peak - max(a_wall_height, c_wall_height)) / tan(a_pitch)
        c_side_wall = (peak - max(a_wall_height, c_wall_height)) / tan(c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        f_peak = peak - (self.post_width * sin(a_pitch) * sin(c_pitch)) / \
                 sin(pi - a_pitch - c_pitch)
        max_h = f_peak + max(angled(a_pitch, self.panel_thickness), angled(c_pitch, self.panel_thickness)) + \
                (self.post_width * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch)
        common[0] = CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                wall_height=a_wall_height)
        common[1] = CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                wall_height=c_wall_height)
        return common

    def drip_edge_peak_height(self, drip_edge, peak):
        """
        This method is designed for Scenario 6: Drip Edge and Peak Height. Drip edge and peak height must be in inches.
        It cycles through a number of pitches and passes them into CommonCalcs.py to determine the estimated drip edge.
        Once it gets an estimated drip edge close to the given one it uses that pitch for all calculations.
        :param drip_edge: float
        :param peak: float
        :return: class <CommonCalcs.CommonCalcs>
        """
        common = [None, None]
        tol = 0.01
        diff = 100
        incr = 0.1
        ratio_pitch = 0.0
        while diff > tol:
            old_ratio_pitch = ratio_pitch
            ratio_pitch += incr
            pitch = atan2(ratio_pitch, 12)
            drip_est = estimate_drip_from_peak(peak=peak, estimate_pitch=pitch, wall_length=self.wall_length,
                                               side_wall_length=self.bwall / 2 - self.post_width / 2,
                                               overhang=self.overhang,
                                               thickness=self.panel_thickness, tab=self.tabwidget,
                                               endcut=self.endcut)
            diff = abs(drip_edge - drip_est)
            if ratio_pitch > 12:
                break
            if drip_est < drip_edge:
                ratio_pitch = old_ratio_pitch
                incr /= 2
        # Now take the estimated pitch and set it as a ratio then convert back to radians. Its more accurate for some
        # reason
        a_wall_height = peak - (self.bwall / 2 - self.post_width / 2) * tan(pitch)
        c_wall_height = a_wall_height
        a_side_wall = self.bwall / 2
        c_side_wall = a_side_wall
        soffit = a_wall_height - self.overhang * tan(pitch)

        max_h = peak + angled(pitch, self.panel_thickness) + (self.post_width * sin(pitch) *
                                                              sin(pitch)) / sin(pi - pitch - pitch)
        common[0] = CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=peak, max_h=max_h,
                                wall_height=a_wall_height)
        common[1] = CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=peak, max_h=max_h,
                                wall_height=c_wall_height)
        return common

    def drip_edge_pitch(self, drip_edge, a_pitch, c_pitch):
        """
        This method is designed for Scenario 7: Drip Edge and Pitch. Drip Edge must be in inches while pitch must be in
        radians. It returns the results where the length is in inches and pitch in radians.
        :param drip_edge: float
        :param a_pitch: float
        :param c_pitch: float
        :return: class <CommonCalcs.CommonCalcs>
        """
        common = [None, None]
        a_soffit = drip_edge - angled(a_pitch, self.panel_thickness)
        c_soffit = drip_edge - angled(c_pitch, self.panel_thickness)
        soffit = max(a_soffit, c_soffit)
        a_wall_height = soffit + self.overhang * tan(a_pitch)
        c_wall_height = soffit + self.overhang * tan(c_pitch)
        peak = (self.bwall * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch) + \
               max(a_wall_height, c_wall_height)
        a_side_wall = (peak - max(a_wall_height, c_wall_height)) / tan(a_pitch)
        c_side_wall = (peak - max(a_wall_height, c_wall_height)) / tan(c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        f_peak = peak - (self.post_width * sin(a_pitch) * sin(c_pitch)) / \
                 sin(pi - a_pitch - c_pitch)
        max_h = f_peak + max(angled(a_pitch, self.panel_thickness), angled(c_pitch, self.panel_thickness)) + \
                (self.post_width * sin(a_pitch) * sin(c_pitch)) / sin(pi - a_pitch - c_pitch)
        common[0] = CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                wall_height=a_wall_height)
        common[1] = CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
                                soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                wall_height=c_wall_height)
        return common


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
    wall_height = peak - side_wall_length * tan(estimate_pitch)
    soffit = wall_height - overhang * tan(estimate_pitch)
    max_h = peak + angled(estimate_pitch, thickness)
    estimate_drip = CommonCalcs(wall_length, side_wall_length, estimate_pitch, soffit, overhang, tab, thickness, endcut,
                                peak, max_h, wall_height)
    return estimate_drip.drip_edge()
