#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CommonCalcs as Cc
import math


# noinspection SpellCheckingInspection
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
        a_soffit = a_wall_height - self.overhang * math.tan(a_pitch)
        c_soffit = c_wall_height - self.overhang * math.tan(c_pitch)
        soffit = max(a_soffit, c_soffit)
        peak = (self.bwall * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch) + \
               max(a_wall_height, c_wall_height)
        a_side_wall = (peak - max(a_wall_height, c_wall_height)) / math.tan(a_pitch)
        c_side_wall = (peak - max(a_wall_height, c_wall_height)) / math.tan(c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        f_peak = peak - (self.post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch -
                                                                                             c_pitch)
        max_h = f_peak + max(Cc.angled(a_pitch, self.panel_thickness), Cc.angled(c_pitch, self.panel_thickness)) + \
                (self.post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
        common[0] = Cc.CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                   soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                   thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                   wall_height=a_wall_height)
        common[1] = Cc.CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
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
        a_pitch = math.atan2(float(peak - a_wall_height), float(a_side_wall - self.post_width / 2))
        c_pitch = math.atan2(float(peak - c_wall_height), float(c_side_wall - self.post_width / 2))
        a_soffit = a_wall_height - self.overhang * math.tan(a_pitch)
        c_soffit = c_wall_height - self.overhang * math.tan(c_pitch)
        soffit = max(a_soffit, c_soffit)
        a_max_h = peak + Cc.angled(a_pitch, self.panel_thickness) + \
                  (self.post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
        c_max_h = peak + Cc.angled(c_pitch, self.panel_thickness) + \
                  (self.post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
        max_h = max(a_max_h, c_max_h)
        common[0] = Cc.CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                   soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                   thickness=self.panel_thickness, endcut=self.endcut, peak=peak, max_h=max_h,
                                   wall_height=a_wall_height)
        common[1] = Cc.CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
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
        peak = (self.bwall * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        f_peak = max_h - max(Cc.angled(a_pitch, self.panel_thickness), Cc.angled(c_pitch, self.panel_thickness)) -\
                 (self.post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
        a_side_wall = peak / math.tan(a_pitch)
        c_side_wall = peak / math.tan(c_pitch)
        # a_wall_height = f_peak - peak
        a_wall_height = max_h - max(Cc.angled(a_pitch, self.panel_thickness), Cc.angled(c_pitch, self.panel_thickness))\
            - (self.bwall*math.sin(a_pitch)*math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
        c_wall_height = a_wall_height
        a_soffit = a_wall_height - self.overhang * math.tan(a_pitch)
        c_soffit = c_wall_height - self.overhang * math.tan(c_pitch)
        soffit = max(a_soffit, c_soffit)
        common[0] = Cc.CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                   soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                   thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                   wall_height=a_wall_height)
        common[1] = Cc.CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
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
        a_pitch = math.atan((peak - soffit) / (a_side_wall + self.overhang - self.post_width/2))
        c_pitch = math.atan((peak - soffit) / (c_side_wall + self.overhang - self.post_width/2))
        a_wall_height = soffit + self.overhang * math.tan(a_pitch)
        c_wall_height = soffit + self.overhang * math.tan(c_pitch)
        h = (self.post_width * math.sin(a_pitch)*math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
        a_max_h = peak + Cc.angled(a_pitch, self.panel_thickness) + h
        c_max_h = peak + Cc.angled(c_pitch, self.panel_thickness) + h
        max_h = max(a_max_h, c_max_h)
        common[0] = Cc.CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                   soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                   thickness=self.panel_thickness, endcut=self.endcut, peak=peak, max_h=max_h,
                                   wall_height=a_wall_height)
        common[1] = Cc.CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
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
        a_wall_height = soffit + self.overhang * math.tan(a_pitch)
        c_wall_height = soffit + self.overhang * math.tan(c_pitch)
        peak = (self.bwall * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch) + \
               max(a_wall_height, c_wall_height)
        a_side_wall = (peak - max(a_wall_height, c_wall_height)) / math.tan(a_pitch)
        c_side_wall = (peak - max(a_wall_height, c_wall_height)) / math.tan(c_pitch)
        # Fenevision sets the peak height for cathedrals at the base of the post that sits in the center.
        f_peak = peak - (self.post_width * math.sin(a_pitch) * math.sin(c_pitch)) / \
                 math.sin(math.pi - a_pitch - c_pitch)
        max_h = f_peak + max(Cc.angled(a_pitch, self.panel_thickness), Cc.angled(c_pitch, self.panel_thickness)) + \
                (self.post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
        common[0] = Cc.CommonCalcs(wall_length=self.wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                   soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                   thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                   wall_height=a_wall_height)
        common[1] = Cc.CommonCalcs(wall_length=self.wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
                                   soffit=soffit, overhang=self.overhang, tabwidget=self.tabwidget,
                                   thickness=self.panel_thickness, endcut=self.endcut, peak=f_peak, max_h=max_h,
                                   wall_height=c_wall_height)
        return common

    def drip_edge_peak_height(self):
        pass

    def drip_edge_pitch(self):
        pass
