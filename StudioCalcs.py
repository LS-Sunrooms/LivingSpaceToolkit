#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import CommonCalcs as Cc
import math


class StudioCalcs:
    """
    This class performs the calculations for a studio style sunroom. It works in conjunction with CommonCalcs.py and
    Units.py. Pitch of the roof is needed but calculated separately and needs to be in radians.
    """
    def __init__(self, overhang, awall, bwall, cwall, panel_thickness, tabwidget, endcut):
        """
        Initiallizes common variables used in methods. Floats are in inches.
        :param overhang: float
        :param awall: float
        :param bwall: float
        :param cwall: float
        :param panel_thickness: float
        :param tabwidget: int
        :param endcut: str
        """
        self.awall = awall
        self.bwall = bwall
        self.cwall = cwall
        self.panel_thickness = panel_thickness
        self.tabwidget = tabwidget
        self.endcut = endcut
        self.overhang = overhang
        self.side_wall = max(self.awall, self.cwall)

    def wall_height_pitch_soffit(self, pitch, b_wall_height):
        """
        This method returns the soffit height given the  pitch and B Wall Height. Pitch has to be in radians. B Wall
        Height is in inches.
        :param pitch: float
        :param b_wall_height: float
        :return: float
        """
        soffit = b_wall_height - self.overhang * math.tan(pitch)
        return soffit

    def wall_height_peak_height_pitch_soffit(self, b_wall_height, peak_height):
        """
        Calculates pitch and soffit given wall height and peak height.
        :param b_wall_height: float
        :param peak_height: float
        :return: float, float
        """
        pitch = math.atan((peak_height - b_wall_height) / max(self.awall, self.cwall))
        soffit = b_wall_height - self.overhang * math.tan(pitch)
        return pitch, soffit

    def max_height_pitch(self, pitch, max_height):
        """
        Calculates B wall height and soffit height based on pitch and max height. Needs panel thickness. Pitch is in
        radians.
        :param pitch: float
        :param max_height: float
        :return: float, float
        """
        angled_thickness = Cc.angled_thickness(pitch=pitch, thickness=self.panel_thickness)
        b_wall_height = max_height - max(self.awall, self.cwall) * math.tan(pitch) - angled_thickness
        soffit = b_wall_height - self.overhang * math.tan(pitch)
        return b_wall_height, soffit

    def soffit_height_peak_height(self, peak_height, soffit):
        """
        Calculates pitch and B wall height using peak height and soffit height. Pitch is in radians.
        :param peak_height: float
        :param soffit: float
        :return: float, float
        """
        pitch = math.atan((peak_height - soffit) / (max(self.awall, self.cwall)+self.overhang))
        b_wall_height = soffit + self.overhang * math.tan(pitch)
        return pitch, b_wall_height

    def soffit_height_pitch(self, pitch, soffit):
        b_wall_height = soffit + self.overhang * math.tan(pitch)
        return b_wall_height

    def drip_edge_peak_height(self):
        pass

    def drip_edge_pitch(self):
        pass
