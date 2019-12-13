#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CommonCalcs as Cc
import math


# noinspection SpellCheckingInspection
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
        soffit = b_wall_height - self.overhang * math.tan(pitch)
        peak = b_wall_height + self.side_wall * math.tan(pitch)
        max_h = peak + Cc.angled(pitch=pitch, thickness=self.panel_thickness)
        common = Cc.CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
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
        pitch = math.atan((peak - b_wall_height) / max(self.awall, self.cwall))
        soffit = b_wall_height - self.overhang * math.tan(pitch)
        max_h = peak + Cc.angled(pitch=pitch, thickness=self.panel_thickness)
        common = Cc.CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
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
        b_wall_height = max_h - max(self.awall, self.cwall) * math.tan(pitch) - \
                        Cc.angled(pitch=pitch, thickness=self.panel_thickness)
        soffit = b_wall_height - self.overhang * math.tan(pitch)
        peak = max_h - Cc.angled(pitch=pitch, thickness=self.panel_thickness)
        common = Cc.CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
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
        pitch = math.atan((peak - soffit) / (max(self.awall, self.cwall) + self.overhang))
        b_wall_height = soffit + self.overhang * math.tan(pitch)
        max_h = peak + Cc.angled(pitch=pitch, thickness=self.panel_thickness)
        common = Cc.CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
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
        b_wall_height = soffit + self.overhang * math.tan(pitch)
        peak = b_wall_height + self.side_wall * math.tan(pitch)
        max_h = peak + Cc.angled(pitch=pitch, thickness=self.panel_thickness)
        common = Cc.CommonCalcs(wall_length=self.bwall, side_wall_length=self.side_wall, pitch=pitch, soffit=soffit,
                                overhang=self.overhang, tabwidget=self.tabwidget, thickness=self.panel_thickness,
                                endcut=self.endcut, peak=peak, max_h=max_h, wall_height=b_wall_height)
        return common

    def drip_edge_peak_height(self):
        pass

    def drip_edge_pitch(self):
        pass
