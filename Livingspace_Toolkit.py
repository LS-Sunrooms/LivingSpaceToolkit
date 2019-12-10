#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# main.py

"""
This is the main program file for the Livingspace Toolkit. This program generates the GUI for the representatives to
help their sales reps on meeting the needs of their customers.
"""

import sys
import os
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QRadioButton, QComboBox, QTextBrowser
from PySide2.QtWidgets import QGroupBox, QLabel, QMessageBox, QCheckBox, QTabWidget
from PySide2.QtCore import QFile, QObject
import UI_rc
from Units import EngineeringUnits as Eu
import math
import re

list_ = re.compile(r'\'|ft|feet|\"|in')


class Form(QObject):

    def __init__(self, ui_file, parent=None):
        super(Form, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        self.max_panel_length = 24 * 12
        self.tabWidget = self.window.findChild(QTabWidget, 'tabWidget')
        # Studio objects
        self.st_scenario1_radio = self.window.findChild(QRadioButton, 'st_scenario1_radio')
        self.st_scenario2_radio = self.window.findChild(QRadioButton, 'st_scenario2_radio')
        self.st_scenario3_radio = self.window.findChild(QRadioButton, 'st_scenario3_radio')
        self.st_scenario4_radio = self.window.findChild(QRadioButton, 'st_scenario4_radio')
        self.st_scenario5_radio = self.window.findChild(QRadioButton, 'st_scenario5_radio')
        self.st_scenario6_radio = self.window.findChild(QRadioButton, 'st_scenario6_radio')
        self.st_scenario7_radio = self.window.findChild(QRadioButton, 'st_scenario7_radio')
        self.st_calc_btn = self.window.findChild(QPushButton, 'st_calculate_btn')
        self.st_results = self.window.findChild(QTextBrowser, 'st_text_browser')
        self.st_pitch_label = self.window.findChild(QLabel, 'st_pitch_label')
        self.st_pitch_gbox = self.window.findChild(QGroupBox, 'st_pitch_gbox')
        self.st_pitch_edit = self.window.findChild(QLineEdit, 'st_pitch_editbox')
        self.st_overhang_edit = self.window.findChild(QLineEdit, 'st_overhang_editbox')
        self.st_roof_gbox = self.window.findChild(QGroupBox, 'st_roof_gbox')
        self.st_thick_combo = self.window.findChild(QComboBox, 'st_thick_combo')
        self.st_panel_gbox = self.window.findChild(QGroupBox, 'st_panel_gbox')
        self.st_width_combo = self.window.findChild(QComboBox, 'st_width_combo')
        self.st_endcut_gbox = self.window.findChild(QGroupBox, 'st_endcut_gbox')
        self.st_fascia = self.window.findChild(QCheckBox, 'st_fascia_checkbox')
        self.st_al_radio = self.window.findChild(QRadioButton, 'st_al_radio')
        self.st_eco_radio = self.window.findChild(QRadioButton, 'st_eco_radio')
        self.st_endcut1_radio = self.window.findChild(QRadioButton, 'st_endcut1_radio')
        self.st_endcut2_radio = self.window.findChild(QRadioButton, 'st_endcut2_radio')
        self.st_endcut3_radio = self.window.findChild(QRadioButton, 'st_endcut3_radio')
        self.st_ratio_radio = self.window.findChild(QRadioButton, 'st_ratio_radio')
        self.st_angle_radio = self.window.findChild(QRadioButton, 'st_angle_radio')
        # self.st_3ply_radio = self.window.findChild(QRadioButton, 'st_3ply_radio')
        # self.st_4ply_radio = self.window.findChild(QRadioButton, 'st_4ply_radio')
        self.st_peak_edit = self.window.findChild(QLineEdit, 'st_peak_editbox')
        self.st_max_edit = self.window.findChild(QLineEdit, 'st_max_editbox')
        self.st_bwallheight_edit = self.window.findChild(QLineEdit, 'st_bwallheight_editbox')
        self.st_soffit_edit = self.window.findChild(QLineEdit, 'st_soffit_editbox')
        self.st_drip_edit = self.window.findChild(QLineEdit, 'st_drip_editbox')
        self.st_awall_edit = self.window.findChild(QLineEdit, 'st_awall_editbox')
        self.st_bwall_edit = self.window.findChild(QLineEdit, 'st_bwall_editbox')
        self.st_cwall_edit = self.window.findChild(QLineEdit, 'st_cwall_editbox')
        # Cathedral object
        self.ca_scenario1_radio = self.window.findChild(QRadioButton, 'ca_scenario1_radio')
        self.ca_scenario2_radio = self.window.findChild(QRadioButton, 'ca_scenario2_radio')
        self.ca_scenario3_radio = self.window.findChild(QRadioButton, 'ca_scenario3_radio')
        self.ca_scenario4_radio = self.window.findChild(QRadioButton, 'ca_scenario4_radio')
        self.ca_scenario5_radio = self.window.findChild(QRadioButton, 'ca_scenario5_radio')
        self.ca_scenario6_radio = self.window.findChild(QRadioButton, 'ca_scenario6_radio')
        self.ca_scenario7_radio = self.window.findChild(QRadioButton, 'ca_scenario7_radio')
        self.ca_calc_btn = self.window.findChild(QPushButton, 'ca_calculate_btn')
        self.ca_results = self.window.findChild(QTextBrowser, 'ca_text_browser')
        self.ca_a_pitch_label = self.window.findChild(QLabel, 'ca_a_pitch_label')
        self.ca_a_pitch_gbox = self.window.findChild(QGroupBox, 'ca_a_pitch_gbox')
        self.ca_a_pitch_edit = self.window.findChild(QLineEdit, 'ca_a_pitch_editbox')
        self.ca_c_pitch_gbox = self.window.findChild(QGroupBox, 'ca_c_pitch_gbox')
        self.ca_c_pitch_edit = self.window.findChild(QLineEdit, 'ca_c_pitch_editbox')
        self.ca_c_pitch_label = self.window.findChild(QLabel, 'ca_c_pitch_label')
        self.ca_overhang_edit = self.window.findChild(QLineEdit, 'ca_overhang_editbox')
        self.ca_roof_gbox = self.window.findChild(QGroupBox, 'ca_roof_gbox')
        self.ca_thick_combo = self.window.findChild(QComboBox, 'ca_thick_combo')
        self.ca_panel_gbox = self.window.findChild(QGroupBox, 'ca_panel_gbox')
        self.ca_width_combo = self.window.findChild(QComboBox, 'ca_width_combo')
        self.ca_endcut_gbox = self.window.findChild(QGroupBox, 'ca_endcut_gbox')
        self.ca_fascia = self.window.findChild(QCheckBox, 'ca_fascia_checkbox')
        self.ca_al_radio = self.window.findChild(QRadioButton, 'ca_al_radio')
        self.ca_eco_radio = self.window.findChild(QRadioButton, 'ca_eco_radio')
        self.ca_endcut1_radio = self.window.findChild(QRadioButton, 'ca_endcut1_radio')
        self.ca_endcut2_radio = self.window.findChild(QRadioButton, 'ca_endcut2_radio')
        self.ca_endcut3_radio = self.window.findChild(QRadioButton, 'ca_endcut3_radio')
        self.ca_a_ratio_radio = self.window.findChild(QRadioButton, 'ca_a_ratio_radio')
        self.ca_c_ratio_radio = self.window.findChild(QRadioButton, 'ca_c_ratio_radio')
        self.ca_a_angle_radio = self.window.findChild(QRadioButton, 'ca_a_angle_radio')
        self.ca_c_angle_radio = self.window.findChild(QRadioButton, 'ca_c_angle_radio')
        # self.ca_3ply_radio = self.window.findChild(QRadioButton, 'ca_3ply_radio')
        # self.ca_4ply_radio = self.window.findChild(QRadioButton, 'ca_4ply_radio')
        self.ca_peak_edit = self.window.findChild(QLineEdit, 'ca_peak_editbox')
        self.ca_max_edit = self.window.findChild(QLineEdit, 'ca_max_editbox')
        self.ca_awallheight_edit = self.window.findChild(QLineEdit, 'ca_awallheight_editbox')
        self.ca_cwallheight_edit = self.window.findChild(QLineEdit, 'ca_cwallheight_editbox')
        self.ca_a_soffit_edit = self.window.findChild(QLineEdit, 'ca_a_soffit_editbox')
        self.ca_c_soffit_edit = self.window.findChild(QLineEdit, 'ca_c_soffit_editbox')
        self.ca_drip_edit = self.window.findChild(QLineEdit, 'ca_drip_editbox')
        self.ca_awall_edit = self.window.findChild(QLineEdit, 'ca_awall_editbox')
        self.ca_bwall_edit = self.window.findChild(QLineEdit, 'ca_bwall_editbox')
        self.ca_cwall_edit = self.window.findChild(QLineEdit, 'ca_cwall_editbox')
        # Studio click events
        self.st_scenario1_radio.clicked.connect(self.st_scenario)
        self.st_scenario2_radio.clicked.connect(self.st_scenario)
        self.st_scenario3_radio.clicked.connect(self.st_scenario)
        self.st_scenario4_radio.clicked.connect(self.st_scenario)
        self.st_scenario5_radio.clicked.connect(self.st_scenario)
        self.st_scenario6_radio.clicked.connect(self.st_scenario)
        self.st_scenario7_radio.clicked.connect(self.st_scenario)
        self.st_calc_btn.clicked.connect(self.st_calcbutton)
        self.st_al_radio.clicked.connect(self.st_thick_combo_populate)
        self.st_eco_radio.clicked.connect(self.st_thick_combo_populate)
        # self.st_3ply_radio.clicked.connect(self.st_width_comb_populate)
        # self.st_4ply_radio.clicked.connect(self.st_width_comb_populate)
        self.st_ratio_radio.clicked.connect(self.st_pitch_label_change)
        self.st_angle_radio.clicked.connect(self.st_pitch_label_change)
        self.st_thick_combo.currentIndexChanged.connect(self.st_thickcombo)
        self.st_endcut1_radio.clicked.connect(self.st_endcuts)
        self.st_endcut2_radio.clicked.connect(self.st_endcuts)
        self.st_endcut3_radio.clicked.connect(self.st_endcuts)
        # Cathedral click events
        self.ca_scenario1_radio.clicked.connect(self.ca_scenario)
        self.ca_scenario2_radio.clicked.connect(self.ca_scenario)
        self.ca_scenario3_radio.clicked.connect(self.ca_scenario)
        self.ca_scenario4_radio.clicked.connect(self.ca_scenario)
        self.ca_scenario5_radio.clicked.connect(self.ca_scenario)
        self.ca_scenario6_radio.clicked.connect(self.ca_scenario)
        self.ca_scenario7_radio.clicked.connect(self.ca_scenario)
        self.ca_calc_btn.clicked.connect(self.ca_calcbutton)
        self.ca_al_radio.clicked.connect(self.ca_thick_combo_populate)
        self.ca_eco_radio.clicked.connect(self.ca_thick_combo_populate)
        self.ca_a_ratio_radio.clicked.connect(self.ca_pitch_label_change)
        self.ca_a_angle_radio.clicked.connect(self.ca_pitch_label_change)
        self.ca_c_ratio_radio.clicked.connect(self.ca_pitch_label_change)
        self.ca_c_angle_radio.clicked.connect(self.ca_pitch_label_change)
        self.ca_thick_combo.currentIndexChanged.connect(self.ca_thickcombo)
        # self.ca_3ply_radio.clicked.connect(self.ca_width_comb_populate)
        # self.ca_4ply_radio.clicked.connect(self.ca_width_comb_populate)
        self.ca_endcut1_radio.clicked.connect(self.ca_endcuts)
        self.ca_endcut2_radio.clicked.connect(self.ca_endcuts)
        self.ca_endcut3_radio.clicked.connect(self.ca_endcuts)

        self.studio_form_control()
        self.cathedral_form_control()
        self.window.show()

    def studio_form_control(self):
        self.st_pitch_gbox.setEnabled(False)
        self.st_fascia.setEnabled(False)
        self.st_overhang_edit.setEnabled(False)
        self.st_roof_gbox.setEnabled(False)
        self.st_thick_combo.setEnabled(False)
        self.st_endcut_gbox.setEnabled(False)
        self.st_peak_edit.setEnabled(False)
        self.st_max_edit.setEnabled(False)
        self.st_bwallheight_edit.setEnabled(False)
        self.st_soffit_edit.setEnabled(False)
        self.st_drip_edit.setEnabled(False)
        self.st_awall_edit.setEnabled(False)
        self.st_bwall_edit.setEnabled(False)
        self.st_cwall_edit.setEnabled(False)

    def cathedral_form_control(self):
        self.ca_a_pitch_gbox.setEnabled(False)
        self.ca_c_pitch_gbox.setEnabled(False)
        self.ca_fascia.setEnabled(False)
        self.ca_overhang_edit.setEnabled(False)
        self.ca_roof_gbox.setEnabled(False)
        self.ca_thick_combo.setEnabled(False)
        self.ca_endcut_gbox.setEnabled(False)
        self.ca_peak_edit.setEnabled(False)
        self.ca_max_edit.setEnabled(False)
        self.ca_awallheight_edit.setEnabled(False)
        self.ca_cwallheight_edit.setEnabled(False)
        self.ca_a_soffit_edit.setEnabled(False)
        self.ca_c_soffit_edit.setEnabled(False)
        self.ca_drip_edit.setEnabled(False)
        self.ca_awall_edit.setEnabled(False)
        self.ca_bwall_edit.setEnabled(False)
        self.ca_cwall_edit.setEnabled(False)

    def st_scenario(self):
        self.studio_form_control()
        self.st_awall_edit.setEnabled(True)
        self.st_bwall_edit.setEnabled(True)
        self.st_cwall_edit.setEnabled(True)
        self.st_overhang_edit.setEnabled(True)
        self.st_roof_gbox.setEnabled(True)
        self.st_thick_combo.setEnabled(True)
        # self.st_panel_gbox.setEnabled(True)
        # self.st_width_combo.setEnabled(True)
        self.st_endcut_gbox.setEnabled(True)
        if self.st_scenario1_radio.isChecked():
            self.st_pitch_gbox.setEnabled(True)
            self.st_bwallheight_edit.setEnabled(True)
        elif self.st_scenario2_radio.isChecked():
            self.st_peak_edit.setEnabled(True)
            self.st_bwallheight_edit.setEnabled(True)
        elif self.st_scenario3_radio.isChecked():
            self.st_pitch_gbox.setEnabled(True)
            self.st_max_edit.setEnabled(True)
        elif self.st_scenario4_radio.isChecked():
            self.st_peak_edit.setEnabled(True)
            self.st_soffit_edit.setEnabled(True)
        elif self.st_scenario5_radio.isChecked():
            self.st_pitch_gbox.setEnabled(True)
            self.st_soffit_edit.setEnabled(True)
        elif self.st_scenario6_radio.isChecked():
            self.st_drip_edit.setEnabled(True)
            self.st_peak_edit.setEnabled(True)
        elif self.st_scenario7_radio.isChecked():
            self.st_drip_edit.setEnabled(True)
            self.st_pitch_gbox.setEnabled(True)

    def ca_scenario(self):
        self.cathedral_form_control()
        self.ca_awall_edit.setEnabled(True)
        self.ca_bwall_edit.setEnabled(True)
        self.ca_cwall_edit.setEnabled(True)
        self.ca_overhang_edit.setEnabled(True)
        self.ca_roof_gbox.setEnabled(True)
        self.ca_thick_combo.setEnabled(True)
        # self.ca_panel_gbox.setEnabled(True)
        # self.ca_width_combo.setEnabled(True)
        self.ca_endcut_gbox.setEnabled(True)
        if self.ca_scenario1_radio.isChecked():
            self.ca_a_pitch_gbox.setEnabled(True)
            self.ca_c_pitch_gbox.setEnabled(True)
            self.ca_awallheight_edit.setEnabled(True)
            self.ca_cwallheight_edit.setEnabled(True)
        elif self.ca_scenario2_radio.isChecked():
            self.ca_peak_edit.setEnabled(True)
            self.ca_awallheight_edit.setEnabled(True)
            self.ca_cwallheight_edit.setEnabled(True)
        elif self.ca_scenario3_radio.isChecked():
            self.ca_a_pitch_gbox.setEnabled(True)
            self.ca_c_pitch_gbox.setEnabled(True)
            self.ca_max_edit.setEnabled(True)
        elif self.ca_scenario4_radio.isChecked():
            self.ca_peak_edit.setEnabled(True)
            self.ca_a_soffit_edit.setEnabled(True)
            self.ca_c_soffit_edit.setEnabled(True)
        elif self.ca_scenario5_radio.isChecked():
            self.ca_a_pitch_gbox.setEnabled(True)
            self.ca_c_pitch_gbox.setEnabled(True)
            self.ca_a_soffit_edit.setEnabled(True)
            self.ca_c_soffit_edit.setEnabled(True)
        elif self.ca_scenario6_radio.isChecked():
            self.ca_drip_edit.setEnabled(True)
            self.ca_peak_edit.setEnabled(True)
        elif self.ca_scenario7_radio.isChecked():
            self.ca_drip_edit.setEnabled(True)
            self.ca_a_pitch_gbox.setEnabled(True)
            self.ca_c_pitch_gbox.setEnabled(True)

    def st_endcuts(self):
        if self.st_eco_radio.isChecked() and (self.st_endcut1_radio.isChecked() or self.st_endcut3_radio.isChecked()):
            if self.st_thick_combo.itemData(self.st_thick_combo.currentIndex()) == '6"':
                self.st_fascia.setEnabled(True)
                self.st_fascia.setChecked(True)
            else:
                self.st_fascia.setEnabled(False)
                self.st_fascia.setChecked(False)
        elif self.st_al_radio.isChecked():
            self.st_fascia.setEnabled(True)
            self.st_fascia.setChecked(True)
        else:
            self.st_fascia.setEnabled(False)
            self.st_fascia.setChecked(False)

    def ca_endcuts(self):
        if self.ca_eco_radio.isChecked() and (self.ca_endcut1_radio.isChecked() or self.ca_endcut3_radio.isChecked()):
            if self.ca_thick_combo.itemData(self.ca_thick_combo.currentIndex()) == '6"':
                self.ca_fascia.setEnabled(True)
                self.ca_fascia.setChecked(True)
            else:
                self.ca_fascia.setEnabled(False)
                self.ca_fascia.setChecked(False)
        elif self.ca_al_radio.isChecked():
            self.ca_fascia.setEnabled(True)
            self.ca_fascia.setChecked(True)
        else:
            self.ca_fascia.setEnabled(False)
            self.ca_fascia.setChecked(False)

    def st_thickcombo(self):
        if self.st_eco_radio.isChecked() and (self.st_endcut1_radio.isChecked() or self.st_endcut3_radio.isChecked()):
            if self.st_thick_combo.itemData(self.st_thick_combo.currentIndex()) == '6"':
                self.st_fascia.setEnabled(True)
                self.st_fascia.setChecked(True)
            else:
                self.st_fascia.setEnabled(False)
                self.st_fascia.setChecked(False)
        elif self.st_al_radio.isChecked():
            self.st_fascia.setEnabled(True)
            self.st_fascia.setChecked(True)
        else:
            self.st_fascia.setEnabled(False)
            self.st_fascia.setChecked(False)
        self.st_results.clear()

    def ca_thickcombo(self):
        if self.ca_eco_radio.isChecked() and (self.ca_endcut1_radio.isChecked() or self.ca_endcut3_radio.isChecked()):
            if self.ca_thick_combo.itemData(self.ca_thick_combo.currentIndex()) == '6"':
                self.ca_fascia.setEnabled(True)
                self.ca_fascia.setChecked(True)
            else:
                self.ca_fascia.setEnabled(False)
                self.ca_fascia.setChecked(False)
        elif self.ca_al_radio.isChecked():
            self.ca_fascia.setEnabled(True)
            self.ca_fascia.setChecked(True)
        else:
            self.ca_fascia.setEnabled(False)
            self.ca_fascia.setChecked(False)
        self.ca_results.clear()

    def st_pitch_label_change(self):
        self.st_pitch_label.clear()
        if self.st_ratio_radio.isChecked():
            self.st_pitch_label.setText('/12 in.')
        elif self.st_angle_radio.isChecked():
            self.st_pitch_label.setText('Angle in\nDegrees')

    def ca_pitch_label_change(self):
        if self.ca_a_ratio_radio.isChecked():
            self.ca_a_pitch_label.clear()
            self.ca_a_pitch_label.setText('/12 in.')
        elif self.ca_a_angle_radio.isChecked():
            self.ca_a_pitch_label.clear()
            self.ca_a_pitch_label.setText('Angle in\nDegrees')
        if self.ca_c_ratio_radio.isChecked():
            self.ca_c_pitch_label.clear()
            self.ca_c_pitch_label.setText('/12 in.')
        elif self.ca_c_angle_radio.isChecked():
            self.ca_c_pitch_label.clear()
            self.ca_c_pitch_label.setText('Angle in\nDegrees')

    def st_thick_combo_populate(self):
        self.st_thick_combo.clear()
        if self.st_eco_radio.isChecked():
            self.st_endcut1_radio.setChecked(True)
            self.st_endcut2_radio.setEnabled(True)
            self.st_endcut2_radio.setChecked(False)
            self.st_endcut3_radio.setEnabled(True)
            self.st_endcut3_radio.setChecked(False)
            self.st_thick_combo.addItem('6"', userData='6"')
            self.st_thick_combo.addItem('8"', userData='8.25"')
            self.st_thick_combo.addItem('10"', userData='10.25"')
            self.st_thick_combo.addItem('12"', userData='12.25"')
        elif self.st_al_radio.isChecked():
            self.st_endcut1_radio.setChecked(True)
            self.st_endcut2_radio.setEnabled(False)
            self.st_endcut3_radio.setEnabled(False)
            self.st_thick_combo.addItem('3"', userData='3"')
            self.st_thick_combo.addItem('6"', userData='6"')

    def ca_thick_combo_populate(self):
        self.ca_thick_combo.clear()
        if self.ca_eco_radio.isChecked():
            self.ca_endcut1_radio.setChecked(True)
            self.ca_endcut2_radio.setEnabled(True)
            self.ca_endcut2_radio.setChecked(False)
            self.ca_endcut3_radio.setEnabled(True)
            self.ca_endcut3_radio.setChecked(False)
            self.ca_thick_combo.addItem('6"', userData='6"')
            self.ca_thick_combo.addItem('8"', userData='8.25"')
            self.ca_thick_combo.addItem('10"', userData='10.25"')
            self.ca_thick_combo.addItem('12"', userData='12.25"')
        elif self.ca_al_radio.isChecked():
            self.ca_endcut1_radio.setChecked(True)
            self.ca_endcut2_radio.setEnabled(False)
            self.ca_endcut3_radio.setEnabled(False)
            self.ca_thick_combo.addItem('3"', userData='3"')
            self.ca_thick_combo.addItem('6"', userData='6"')

    def common_function(self, wall_length, side_wall_length, pitch, soffit, overhang):
        if self.tabWidget.currentIndex() == 0:  # Studio Tab
            panel_thickness = Eu(self.st_thick_combo.itemData(self.st_thick_combo.currentIndex()), u_type='length')
        elif self.tabWidget.currentIndex() == 1:  # Cathedral Tab
            panel_thickness = Eu(self.ca_thick_combo.itemData(self.ca_thick_combo.currentIndex()), u_type='length')
        max_panel_length = False
        max_hang_rail_length = False
        max_fascia_length = [False, False]
        minmax_overhang = [False, False]
        if overhang.base > 16:
            side_overhang = 16
        else:
            side_overhang = overhang.base
        angled_thickness = panel_thickness.base * (math.sin(math.pi / 2) / math.sin(math.pi / 2 - pitch))
        if self.tabWidget.currentIndex() == 0:  # Studio Tab
            if self.st_endcut2_radio.isChecked():
                drip = soffit.base + angled_thickness
                drip = Eu(str(drip) + '"', u_type='length')
            else:
                drip = soffit.base + panel_thickness.base * math.cos(pitch)
                drip = Eu(str(drip) + '"', u_type='length')
            if self.st_endcut3_radio.isChecked():
                p_bottom = (side_wall_length + overhang.base) / math.cos(pitch)
                p_top = (side_wall_length + overhang.base + panel_thickness.base * math.sin(pitch)) / math.cos(pitch)
                p_length = max(p_bottom, p_top)
            else:
                p_length = (side_wall_length + overhang.base) / math.cos(pitch)
        elif self.tabWidget.currentIndex() == 1:  # Cathedral Tab
            if self.ca_endcut2_radio.isChecked():
                drip = soffit.base + angled_thickness
                drip = Eu(str(drip) + '"', u_type='length')
            else:
                drip = soffit.base + panel_thickness.base * math.cos(pitch)
                drip = Eu(str(drip) + '"', u_type='length')
            if self.ca_endcut3_radio.isChecked():
                p_bottom = (side_wall_length + overhang.base) / math.cos(pitch)
                p_top = (side_wall_length + overhang.base + panel_thickness.base * math.sin(pitch)) / math.cos(pitch)
                p_length = max(p_bottom, p_top)
            else:
                p_length = (side_wall_length + overhang.base) / math.cos(pitch)
        panel_length = math.ceil(p_length / 12) * 12  # Panel length (in inches) rounded up to nearest foot
        if panel_length > 288:
            max_panel_length = True
            panel_length /= 2
        panel_length = Eu(str(panel_length) + '"', u_type='length')
        if self.tabWidget.currentIndex() == 0:  # Studio Tab
            roof_width = wall_length + side_overhang * 2
        elif self.tabWidget.currentIndex() == 1:  # Cathedral Tab
            roof_width = wall_length + side_overhang
        roof_panels = math.ceil(roof_width / 32)
        if self.tabWidget.currentIndex() == 0:  # Studio Tab
            if (roof_panels * 32 - wall_length) / 2 < side_overhang:
                # Overhang too short
                side_overhang2 = Eu(str((roof_panels * 32 - wall_length) / 2) + '"', u_type='length')
                minmax_overhang[0] = True
            elif (roof_panels * 32 - wall_length) / 2 > 16:
                # Overhang too long
                side_overhang2 = Eu(str((roof_panels * 32 - wall_length) / 2) + '"', u_type='length')
                minmax_overhang[1] = True
            else:
                side_overhang2 = Eu(str(side_overhang) + '"', u_type='length')
        elif self.tabWidget.currentIndex() == 1:  # Cathedral Tab
            if (roof_panels * 32 - wall_length) < side_overhang:
                # Overhang too short
                side_overhang2 = Eu(str(roof_panels * 32 - wall_length) + '"', u_type='length')
                minmax_overhang[0] = True
            elif (roof_panels * 32 - wall_length) > 16:
                # Overhang too long
                side_overhang2 = Eu(str(roof_panels * 32 - wall_length) + '"', u_type='length')
                minmax_overhang[1] = True
            else:
                side_overhang2 = Eu(str(side_overhang) + '"', u_type='length')
        if max_panel_length is True:
            roof_area = panel_length.base * 2 * roof_panels * 32
        else:
            roof_area = panel_length.base * roof_panels * 32
        # Hang Rail
        if self.tabWidget.currentIndex() == 0:  # Studio Tab
            hang_rail = roof_panels * 32
        elif self.tabWidget.currentIndex() == 1:  # Cathedral Tab
            hang_rail = panel_length.base
        if hang_rail > 216:
            max_hang_rail_length = True
            hang_rail /= 2
        # Fascia
        if self.tabWidget.currentIndex() == 0:  # Studio Tab
            if self.st_fascia.isChecked():
                fascia_wall = roof_panels * 32 + 12
                fascia_sides = panel_length.base + 6
                if fascia_wall > 216:
                    max_fascia_length[0] = True
                    fascia_wall /= 2
                if fascia_sides > 216:
                    max_fascia_length[1] = True
                    fascia_sides /= 2
            else:
                fascia_wall = None
                fascia_sides = None
        elif self.tabWidget.currentIndex() == 1:  # Cathedral Tab
            if self.ca_fascia.isChecked():
                fascia_wall = roof_panels * 32 + 6
                fascia_sides = panel_length.base + 6
                if fascia_wall > 216:
                    max_fascia_length[0] = True
                    fascia_wall /= 2
                if fascia_sides > 216:
                    max_fascia_length[1] = True
                    fascia_sides /= 2
            else:
                fascia_wall = None
                fascia_sides = None
        # Armstrong Ceiling Panels
        rake_length = side_wall_length/math.cos(pitch)
        armstrong_area = rake_length*wall_length/144  # get it in sq ft
        armstrong = math.ceil((armstrong_area/29)+(armstrong_area/29)*0.1)

        results = {'overhang': overhang.simplified("in"), 'side overhang': side_overhang2.simplified("in"),
                   'max hang rail': max_hang_rail_length, 'max panel length': max_panel_length,
                   'max fascia': max_fascia_length, 'drip edge': drip.simplified('in'),
                   'panel length': panel_length.simplified("in"), 'overhang error': minmax_overhang,
                   'roof area': roof_area, 'hang rail': hang_rail, 'side fascia': fascia_sides,
                   'wall fascia': fascia_wall, 'roof panels': roof_panels, 'angled thickness': angled_thickness,
                   'armstrong': armstrong}
        return results

    def pitch_input(self, pitch_input):
        if pitch_input.base_unit == 'in.':
            pitch = math.atan(pitch_input.base / 12)
        elif pitch_input.base_unit == 'deg':
            pitch = pitch_input.base
        return pitch

    def pitch_estimate(self, number):
        return round(number * 2) / 2

    def assume_units(self, string_in, assume_unit):
        if list_.search(str(string_in)) is None:
            string_out = string_in + assume_unit
        else:
            string_out = string_in
        return string_out

    def st_scenario_calc(self):
        overhang = Eu(self.assume_units(self.st_overhang_edit.text(), '"'), u_type='length')
        awall = Eu(self.assume_units(self.st_awall_edit.text(), '"'), u_type='length')
        bwall = Eu(self.assume_units(self.st_bwall_edit.text(), '"'), u_type='length')
        cwall = Eu(self.assume_units(self.st_cwall_edit.text(), '"'), u_type='length')
        side_wall = max(awall.base, cwall.base)
        # Getting scenario inputs
        if self.st_scenario1_radio.isChecked():
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(self.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(self.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            bwallheight = Eu(self.assume_units(self.st_bwallheight_edit.text(), '"'), u_type='length')
            pitch = self.pitch_input(pitch_input)
            soffit = bwallheight.base - overhang.base * math.tan(pitch)
            soffit_height = Eu(str(soffit) + '"', u_type='length')
        elif self.st_scenario2_radio.isChecked():
            bwallheight = Eu(self.assume_units(self.st_bwallheight_edit.text(), '"'), u_type='length')
            peak_height = Eu(self.assume_units(self.st_peak_edit.text(), '"'), u_type='length')
            pitch = math.atan((peak_height.base - bwallheight.base) / max(awall.base, cwall.base))
            soffit = bwallheight.base - overhang.base * math.tan(pitch)
            soffit_height = Eu(str(soffit) + '"', u_type='length')
        elif self.st_scenario3_radio.isChecked():
            panel_thickness = Eu(self.st_thick_combo.itemData(self.st_thick_combo.currentIndex()), u_type='length')
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(self.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(self.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            max_height = Eu(self.assume_units(self.st_max_edit.text(), '"'), u_type='length')
            pitch = self.pitch_input(pitch_input)
            angled_thickness = panel_thickness.base * (math.sin(math.pi / 2) / math.sin(math.pi / 2 - pitch))
            bwallh = max_height.base - max(awall.base, cwall.base) * math.tan(pitch) - angled_thickness
            bwallheight = Eu(str(bwallh) + '"', u_type='length')
            soffit = bwallheight.base - overhang.base * math.tan(pitch)
            soffit_height = Eu(str(soffit) + '"', u_type='length')
        elif self.st_scenario4_radio.isChecked():
            peak_height = Eu(self.assume_units(self.st_peak_edit.text(), '"'), u_type='length')
            soffit_height = Eu(self.assume_units(self.st_soffit_edit.text(), '"'), u_type='length')
            pitch = math.atan((peak_height.base - soffit_height.base) / (max(awall.base, cwall.base) + overhang.base))
            bwallh = soffit_height.base + overhang.base * math.tan(pitch)
            bwallheight = Eu(str(bwallh) + '"', u_type='length')
        elif self.st_scenario5_radio.isChecked():
            panel_thickness = Eu(self.st_thick_combo.itemData(self.st_thick_combo.currentIndex()), u_type='length')
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(self.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(self.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            pitch = self.pitch_input(pitch_input)
            soffit_height = Eu(self.assume_units(self.st_soffit_edit.text(), '"'), u_type='length')
            bwallh = soffit_height.base + overhang.base * math.tan(pitch)
            bwallheight = Eu(str(bwallh) + '"', u_type='length')
        # Common Calculations
        common = self.common_function(wall_length=bwall.base, side_wall_length=side_wall, pitch=pitch,
                                      soffit=soffit_height, overhang=overhang)
        if self.st_scenario1_radio.isChecked():
            peak = bwallheight.base + side_wall * math.tan(pitch)
            peak_height = Eu(str(peak) + '"', u_type='length')
            max_h = peak_height.base + common['angled thickness']
            max_height = Eu(str(max_h) + '"', u_type='length')
        elif self.st_scenario2_radio.isChecked():
            max_h = peak_height.base + common['angled thickness']
            max_height = Eu(str(max_h) + '"', u_type='length')
        elif self.st_scenario3_radio.isChecked():
            peak = max_height.base - common['angled thickness']
            peak_height = Eu(str(peak) + '"', u_type='length')
        elif self.st_scenario4_radio.isChecked():
            max_h = peak_height.base + common['angled thickness']
            max_height = Eu(str(max_h) + '"', u_type='length')
        elif self.st_scenario5_radio.isChecked():
            peak = bwallheight.base + side_wall * math.tan(pitch)
            peak_height = Eu(str(peak) + '"', u_type='length')
            max_h = peak_height.base + common['angled thickness']
            max_height = Eu(str(max_h) + '"', u_type='length')
        results = {'pitch': pitch, 'peak': peak_height.simplified("in"),
                   'panel length': common['panel length'], 'max panel length': common['max panel length'],
                   'soffit height': soffit_height.simplified("in"), 'drip edge': common['drip edge'],
                   'overhang error': common['overhang error'], 'roof area': math.ceil(common['roof area'] / 144),
                   'hang rail': common['hang rail'], 'fascia b wall': common['wall fascia'],
                   'fascia sides': common['side fascia'], 'max hang rail length': common['max hang rail'],
                   'max fascia length': common['max fascia'], 'roof panels': common['roof panels'],
                   'max height': max_height.simplified("in"), 'overhang': common['overhang'],
                   'side overhang': common['side overhang'], 'armstrong': common['armstrong'],
                   'bwallheight': bwallheight.simplified("in"), 'sidewall': side_wall}
        return results

    def ca_scenario_calc(self):
        overhang = Eu(self.assume_units(self.ca_overhang_edit.text(), '"'), u_type='length')
        awall = Eu(self.assume_units(self.ca_awall_edit.text(), '"'), u_type='length')
        bwall = Eu(self.assume_units(self.ca_bwall_edit.text(), '"'), u_type='length')
        cwall = Eu(self.assume_units(self.ca_cwall_edit.text(), '"'), u_type='length')
        wall_length = max(awall.base, cwall.base)
        post_width = 3.25  # inches
        # Getting scenario inputs
        if self.ca_scenario1_radio.isChecked():
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(self.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(self.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(self.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_c_angle_radio.isChecked():
                c_pitch_input = Eu(self.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            awallheight = Eu(self.assume_units(self.ca_awallheight_edit.text(), '"'), u_type='length')
            cwallheight = Eu(self.assume_units(self.ca_cwallheight_edit.text(), '"'), u_type='length')
            a_pitch = self.pitch_input(a_pitch_input)
            c_pitch = self.pitch_input(c_pitch_input)
            a_soffit = awallheight.base - overhang.base * math.tan(a_pitch)
            c_soffit = cwallheight.base - overhang.base * math.tan(c_pitch)
            soffit = max(a_soffit, c_soffit)
            soffit_height = Eu(str(soffit) + '"', u_type='length')
            # Calculate peak height to bottom of panel
            peak_h = (bwall.base * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch) + \
                     max(awallheight.base, cwallheight.base)
            a_side_wall = (peak_h - max(awallheight.base, cwallheight.base)) / math.tan(a_pitch)
            c_side_wall = (peak_h - max(awallheight.base, cwallheight.base)) / math.tan(c_pitch)
        elif self.ca_scenario2_radio.isChecked():
            awallheight = Eu(self.assume_units(self.ca_awallheight_edit.text(), '"'), u_type='length')
            cwallheight = Eu(self.assume_units(self.ca_cwallheight_edit.text(), '"'), u_type='length')
            peak_height = Eu(self.assume_units(self.ca_peak_edit.text(), '"'), u_type='length') # Fenevision Peak Height
            a_side_wall = bwall.base / 2
            c_side_wall = bwall.base / 2
            a_pitch = math.atan2((peak_height.base - awallheight.base), (a_side_wall - post_width / 2))
            c_pitch = math.atan((float(peak_height.base) - float(cwallheight.base)) / (c_side_wall - post_width / 2))
            # Convert the pitch to whole numbers then recalculate
            a_soffit = awallheight.base - overhang.base * math.tan(a_pitch)
            c_soffit = cwallheight.base - overhang.base * math.tan(c_pitch)
            soffit = max(a_soffit, c_soffit)
            soffit_height = Eu(str(soffit) + '"', u_type='length')
        elif self.ca_scenario3_radio.isChecked():
            panel_thickness = Eu(self.ca_thick_combo.itemData(self.ca_thick_combo.currentIndex()), u_type='length')
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(self.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(self.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(self.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_c_angle_radio.isChecked():
                c_pitch_input = Eu(self.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            max_height = Eu(self.assume_units(self.ca_max_edit.text(), '"'), u_type='length')
            a_pitch = self.pitch_input(a_pitch_input)
            c_pitch = self.pitch_input(c_pitch_input)
            a_angled_thickness = panel_thickness.base * (math.sin(math.pi / 2) / math.sin(math.pi / 2 - a_pitch))
            c_angled_thickness = panel_thickness.base * (math.sin(math.pi / 2) / math.sin(math.pi / 2 - c_pitch))
            # Calculate peak height to bottom of panel
            peak_dh = (bwall.base * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
            peak_h = max_height.base - max(a_angled_thickness, c_angled_thickness) + \
                     (post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
            a_side_wall = peak_dh / math.tan(a_pitch)
            c_side_wall = peak_dh / math.tan(c_pitch)
            awallh = peak_h - peak_dh
            cwallh = peak_h - peak_dh
            awallheight = Eu(str(awallh) + '"', u_type='length')
            cwallheight = Eu(str(cwallh) + '"', u_type='length')
            a_soffit = awallheight.base - overhang.base * math.tan(a_pitch)
            c_soffit = cwallheight.base - overhang.base * math.tan(c_pitch)
            soffit = max(a_soffit, c_soffit)
            soffit_height = Eu(str(soffit) + '"', u_type='length')
        elif self.ca_scenario4_radio.isChecked():
            peak_height = Eu(self.assume_units(self.ca_peak_edit.text(), '"'), u_type='length')
            a_soffit = Eu(self.assume_units(self.ca_a_soffit_edit.text(), '"'), u_type='length')
            c_soffit = Eu(self.assume_units(self.ca_c_soffit_edit.text(), '"'), u_type='length')
            soffit = max(a_soffit.base, c_soffit.base)
            soffit_height = Eu(str(soffit) + '"', u_type='length')
            a_side_wall = bwall.base / 2
            c_side_wall = bwall.base / 2
            a_pitch = math.atan((peak_height.base - soffit_height.base) / (a_side_wall + overhang.base))
            c_pitch = math.atan((peak_height.base - soffit_height.base) / (c_side_wall + overhang.base))
            awallh = soffit_height.base + overhang.base * math.tan(a_pitch)
            cwallh = soffit_height.base + overhang.base * math.tan(c_pitch)
            awallheight = Eu(str(awallh) + '"', u_type='length')
            cwallheight = Eu(str(cwallh) + '"', u_type='length')
        elif self.ca_scenario5_radio.isChecked():
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(self.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(self.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(self.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_c_angle_radio.isChecked():
                c_pitch_input = Eu(self.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            a_pitch = self.pitch_input(a_pitch_input)
            c_pitch = self.pitch_input(c_pitch_input)
            a_soffit = Eu(self.assume_units(self.ca_a_soffit_edit.text(), '"'), u_type='length')
            c_soffit = Eu(self.assume_units(self.ca_c_soffit_edit.text(), '"'), u_type='length')
            soffit = max(a_soffit.base, c_soffit.base)
            soffit_height = Eu(str(soffit) + '"', u_type='length')
            awallh = soffit_height.base + overhang.base * math.tan(a_pitch)
            cwallh = soffit_height.base + overhang.base * math.tan(c_pitch)
            awallheight = Eu(str(awallh) + '"', u_type='length')
            cwallheight = Eu(str(cwallh) + '"', u_type='length')
            # Calculate peak height to bottom of panel
            peak_h = (bwall.base * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch) + \
                     max(awallheight.base, cwallheight.base)
            a_side_wall = (peak_h - max(awallheight.base, cwallheight.base)) / math.tan(a_pitch)
            c_side_wall = (peak_h - max(awallheight.base, cwallheight.base)) / math.tan(c_pitch)

        # Common Calculations
        a_common = self.common_function(wall_length=wall_length, side_wall_length=a_side_wall, pitch=a_pitch,
                                        soffit=soffit_height, overhang=overhang)
        c_common = self.common_function(wall_length=wall_length, side_wall_length=c_side_wall, pitch=c_pitch,
                                        soffit=soffit_height, overhang=overhang)
        if self.ca_scenario1_radio.isChecked():
            # Fenevision Peak for Cathedral
            f_peak = peak_h - (post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(
                math.pi - a_pitch - c_pitch)
            peak_height = Eu(str(f_peak) + '"', u_type='length')
            max_h = peak_height.base + max(a_common['angled thickness'], c_common['angled thickness']) + \
                    (post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
            max_height = Eu(str(max_h) + '"', u_type='length')
        elif self.ca_scenario2_radio.isChecked():
            a_max_h = peak_height.base + a_common['angled thickness'] + \
                      (post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
            c_max_h = peak_height.base + c_common['angled thickness'] + \
                      (post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
            max_h = max(a_max_h, c_max_h)
            max_height = Eu(str(max_h) + '"', u_type='length')
        elif self.ca_scenario3_radio.isChecked():
            peak_height = Eu(str(peak_h - (post_width * math.sin(a_pitch) * math.sin(c_pitch)) /
                                 math.sin(math.pi - a_pitch - c_pitch)) + '"', u_type='length')
        elif self.ca_scenario4_radio.isChecked():
            a_max_h = peak_height.base + a_common['angled thickness'] + \
                      (post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
            c_max_h = peak_height.base + c_common['angled thickness'] + \
                      (post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
            max_h = max(a_max_h, c_max_h)
            max_height = Eu(str(max_h) + '"', u_type='length')
        elif self.ca_scenario5_radio.isChecked():
            f_peak = peak_h - (post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(
                math.pi - a_pitch - c_pitch)
            peak_height = Eu(str(f_peak) + '"', u_type='length')
            max_h = peak_height.base + max(a_common['angled thickness'], c_common['angled thickness']) + \
                    (post_width * math.sin(a_pitch) * math.sin(c_pitch)) / math.sin(math.pi - a_pitch - c_pitch)
            max_height = Eu(str(max_h) + '"', u_type='length')
        side_wall = Eu(self.assume_units(str(max(a_side_wall, c_side_wall)), '"'), u_type='length')
        results = {'a pitch': a_pitch, 'peak': peak_height.simplified("in"), 'a panel length': a_common['panel length'],
                   'c panel length': c_common['panel length'], 'a max panel length': a_common['max panel length'],
                   'c max panel length': c_common['max panel length'], 'a soffit height':soffit_height.simplified("in"),
                   'c soffit height': soffit_height.simplified("in"), 'a drip edge': a_common['drip edge'],
                   'c drip edge': c_common['drip edge'], 'a overhang error': a_common['overhang error'],
                   'c overhang error': c_common['overhang error'],
                   'a roof area': math.ceil(a_common['roof area'] / 144),
                   'c roof area': math.ceil(c_common['roof area'] / 144), 'a hang rail': a_common['hang rail'],
                   'c hang rail': c_common['hang rail'], 'fascia a wall': a_common['wall fascia'],
                   'fascia c wall': c_common['wall fascia'], 'fascia a side': a_common['side fascia'],
                   'fascia c side': c_common['side fascia'], 'max hang rail length a': a_common['max hang rail'],
                   'max hang rail length c': c_common['max hang rail'], 'max fascia length a': a_common['max fascia'],
                   'max fascia length c': c_common['max fascia'], 'a roof panels': a_common['roof panels'],
                   'c roof panels': c_common['roof panels'], 'max height': max_height.simplified("in"),
                   'a overhang': a_common['overhang'], 'c overhang': c_common['overhang'], 'c pitch': c_pitch,
                   'a side overhang': a_common['side overhang'], 'c side overhang': c_common['side overhang'],
                   'a armstrong': a_common['armstrong'], 'c armstrong': c_common['armstrong'],
                   'awallheight': awallheight.simplified("in"), 'cwallheight': cwallheight.simplified("in"),
                   'sidewall': side_wall.simplified('in')}
        return results

    def st_results_message(self, results):
        roof_total = results['roof area']
        self.st_results.append('The pitch is: {}/12.'.format(self.pitch_estimate(12 * math.tan(results['pitch']))))
        self.st_results.append('The peak height is {} in.'.format(results['peak']))
        self.st_results.append('The soffit height is {} in.'.format(results['soffit height']))
        self.st_results.append('The drip edge is at {} in.'.format(results['drip edge']))
        self.st_results.append('The maximum height is {} in.'.format(results['max height']))
        self.st_results.append('The A and C Wall heights are {} in.'.format(results['sidewall']))
        self.st_results.append('The B Wall height is {} in.'.format(results['bwallheight']))
        self.st_results.append('This configuration will need {} roof panels.'.format(results['roof panels']))
        self.st_results.append('The length of each panel should be {} in.'.format(results['panel length']))
        if results['max panel length'] is True:
            self.st_results.append('These panels were divided in half because they were more than 24ft.')
        self.st_results.append('The roof sq. ft. is {}ft^2.'.format(roof_total))
        self.st_results.append('You will need {} boxes of Armstrong Ceiling Panels.'.format(results['armstrong']))
        self.st_results.append('The overhang on B Wall is {} in.'.format(results['overhang']))
        self.st_results.append('The overhang on A and C Walls are {} in.'.format(results['side overhang']))
        if results['overhang error'][0] is True:
            # self.st_results.clear()
            self.st_results.append('The overhang on the sides are TOO SHORT!')
        # elif results['overhang error'][1] is True:
        # self.st_results.clear()
        # self.st_results.append('The overhang on the sides are too long and need to be cut!')
        if results['max hang rail length'] is True:
            self.st_results.append('There are 2 pairs of hang rails at {} in. each.'.format(results['hang rail']))
            self.st_results.append('They were divided in half because the original length was longer than 216".')
        else:
            self.st_results.append('There is 1 pair of hang rails at {} in. each.'.format(results['hang rail']))
        if self.st_fascia.isChecked():
            if results['max fascia length'][0] is True:
                self.st_results.append('There are 2 pieces of Fascia at {} in. each for the B wall'
                                       .format(results['fascia b wall']))
                self.st_results.append('Their original length was more than 216" so they were cut in half.')
            else:
                self.st_results.append('There is 1 piece of Fascia at {} in. for the B wall.'
                                       .format(results['fascia b wall']))
            if results['max fascia length'][1] is True:
                self.st_results.append('There are 2 pieces of Fascia for the A and C walls. Both are at {} in. for each'
                                       ' wall'.format(results['fascia sides']))
                self.st_results.append('Their original length was more than 216".')
            else:
                self.st_results.append('There is one piece of Fascia at {} in. for the A Wall and one piece at {} in. '
                                       'for the C wall.'.format(results['fascia sides'], results['fascia sides']))

    def ca_results_message(self, results):
        roof_total = (results['a roof area'] + results['c roof area'])
        self.ca_results.append('The A side pitch is: {}/12.'
                               .format(self.pitch_estimate(12 * math.tan(results['a pitch']))))
        self.ca_results.append('The C side pitch is: {}/12.'
                               .format(self.pitch_estimate(12 * math.tan(results['c pitch']))))
        self.ca_results.append('The peak height is {}.'.format(results['peak']))
        self.ca_results.append('The A Wall height is {}.'.format(results['awallheight']))
        self.ca_results.append('The C Wall height is {}.'.format(results['cwallheight']))
        self.ca_results.append('The B Wall height is {}.'.format(results['sidewall']))
        self.ca_results.append('The A side soffit height is {}.'.format(results['a soffit height']))
        self.ca_results.append('The C side soffit height is {}.'.format(results['c soffit height']))
        self.ca_results.append('The A side drip edge is at {}.'.format(results['a drip edge']))
        self.ca_results.append('The C side drip edge is at {}.'.format(results['c drip edge']))
        self.ca_results.append('The maximum height is {}.'.format(results['max height']))
        self.ca_results.append('This configuration will need {} A side roof panels.'.format(results['a roof panels']))
        self.ca_results.append('The length of each A side panel should be {}.'.format(results['a panel length']))
        if results['a max panel length'] is True:
            self.ca_results.append('The A side panels were divided in half because they were more than 24ft.')
        self.ca_results.append('This configuration will need {} C side roof panels.'.format(results['c roof panels']))
        self.ca_results.append('The length of each C side panel should be {}.'.format(results['c panel length']))
        if results['c max panel length'] is True:
            self.ca_results.append('The C side panels were divided in half because they were more than 24ft.')
        self.ca_results.append('The total number of roof panels is {}.'.format(results['a roof panels'] +
                                                                               results['c roof panels']))
        self.ca_results.append('The Total roof sq. ft. is {}ft^2.'.format(roof_total))
        self.ca_results.append('You will need {} boxes of Armstrong Ceiling Panels.'
                               .format(results['a armstrong'] + (results['c armstrong'])))
        self.ca_results.append('The overhang on A Wall is {}.'.format(results['a overhang']))
        self.ca_results.append('The overhang on C Wall is {}.'.format(results['c overhang']))
        self.ca_results.append('The overhang on B Wall is {}.'.format(results['a side overhang']))
        if results['a overhang error'][0] is True:
            # self.ca_results.clear()
            self.ca_results.append('The overhang on the sides are TOO SHORT!')
        # elif results['a overhang error'][1] is True:
        # self.ca_results.clear()
        # self.ca_results.append('The overhang on the sides are too long and need to be cut!')
        if results['max hang rail length a'] is True:
            self.ca_results.append('There are 2 pairs of hang rails at {} in. each on the A wall.'
                                   .format(results['a hang rail']))
            self.ca_results.append('They were divided in half because the original length was longer than 216".')
        else:
            self.ca_results.append('There is 1 pair of hang rails at {} in. on the A wall'
                                   .format(results['a hang rail']))
        if results['max hang rail length c'] is True:
            self.ca_results.append('There are 2 pairs of hang rails at {} in. each on the C wall.'
                                   .format(results['c hang rail']))
            self.ca_results.append('They were divided in half because the original length was longer than 216".')
        else:
            self.ca_results.append('There is 1 pair of hang rails at {} in. on the C wall'
                                   .format(results['c hang rail']))
        if self.ca_fascia.isChecked():
            if results['max fascia length a'][0] is True:
                self.ca_results.append('There are 2 pieces of Fascia at {} in. each for the A wall'
                                       .format(results['fascia a wall']))
                self.ca_results.append('Their original length was more than 216" so they were cut in half.')
            else:
                self.ca_results.append('There is 1 pieces of Fascia at {} in. for the A wall'
                                       .format(results['fascia a wall']))
            if results['max fascia length c'][0] is True:
                self.ca_results.append('There are 2 pieces of Fascia at {} in. each for the C wall'
                                       .format(results['fascia c wall']))
                self.ca_results.append('Their original length was more than 216" so they were cut in half.')
            else:
                self.ca_results.append('There is 1 pieces of Fascia at {} in. for the C wall'
                                       .format(results['fascia c wall']))
            if results['max fascia length a'][1] is True:
                self.ca_results.append('There are 2 pieces of Fascia for the A side B Wall. Both are at {} in. each'
                                       .format(results['fascia a side']))
                self.ca_results.append('Their original length was more than 216".')
            else:
                self.ca_results.append('There is 1 pieces of Fascia for the A side B Wall at {} in.'
                                       .format(results['fascia a side']))
            if results['max fascia length c'][1] is True:
                self.ca_results.append('There are 2 pieces of Fascia for the C side B Wall. Both are at {} in. each'
                                       .format(results['fascia c side']))
                self.ca_results.append('Their original length was more than 216".')
            else:
                self.ca_results.append('There is 1 pieces of Fascia for the C side B Wall at {} in.'
                                       .format(results['fascia c side']))

    def st_calcbutton(self):
        self.st_results.clear()
        self.st_results.setText('Now listing results.')
        if self.st_scenario1_radio.isChecked():
            self.st_results.append('*===================*')
            self.st_results.append('Given B wall height and pitch...')
            results = self.st_scenario_calc()
            self.st_results_message(results)
        elif self.st_scenario2_radio.isChecked():
            self.st_results.append('*===================*')
            self.st_results.append('Given wall height and peak height...')
            results = self.st_scenario_calc()
            self.st_results_message(results)
        elif self.st_scenario3_radio.isChecked():
            self.st_results.append('*===================*')
            self.st_results.append('Given max height and pitch...')
            results = self.st_scenario_calc()
            self.st_results_message(results)
        elif self.st_scenario4_radio.isChecked():
            self.st_results.append('*===================*')
            self.st_results.append('Given soffit heights and peak height...')
            results = self.st_scenario_calc()
            self.st_results_message(results)
        elif self.st_scenario5_radio.isChecked():
            self.st_results.append('*===================*')
            self.st_results.append('Given soffit heights and pitch...')
            results = self.st_scenario_calc()
            self.st_results_message(results)
        else:
            QMessageBox.about(self.window, 'Select a Scenario!', 'No scenarios selected!')

    def ca_calcbutton(self):
        self.ca_results.clear()
        self.ca_results.setText('Now listing results.')
        if self.ca_scenario1_radio.isChecked():
            self.ca_results.append('*===================*')
            self.ca_results.append('Given wall height and pitch...')
            results = self.ca_scenario_calc()
            self.ca_results_message(results)
        elif self.ca_scenario2_radio.isChecked():
            self.ca_results.append('*===================*')
            self.ca_results.append('Given wall height and peak height...')
            results = self.ca_scenario_calc()
            self.ca_results_message(results)
        elif self.ca_scenario3_radio.isChecked():
            self.ca_results.append('*===================*')
            self.ca_results.append('Given max height and pitch...')
            results = self.ca_scenario_calc()
            self.ca_results_message(results)
        elif self.ca_scenario4_radio.isChecked():
            self.ca_results.append('*===================*')
            self.ca_results.append('Given soffit heights and peak height...')
            results = self.ca_scenario_calc()
            self.ca_results_message(results)
        elif self.ca_scenario5_radio.isChecked():
            self.ca_results.append('*===================*')
            self.ca_results.append('Given soffit heights and pitch...')
            results = self.ca_scenario_calc()
            self.ca_results_message(results)
        else:
            QMessageBox.about(self.window, 'Select a Scenario!', 'No scenarios selected!')


if __name__ == '__main__':
    # Define function to import external files when using PyInstaller.
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


    mainwindow = resource_path('LivingspaceToolkitMain.ui')
    app = QApplication(sys.argv)
    form = Form(resource_path('LivingspaceToolkitMain.ui'))
    sys.exit(app.exec_())
