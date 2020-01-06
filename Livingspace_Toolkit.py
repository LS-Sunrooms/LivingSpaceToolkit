#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# main.py
# noinspection SpellCheckingInspection
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
import StudioCalcs
import CatherdralCalcs
import CommonCalcs as Cc
import math
import re

list_ = re.compile(r'\'|ft|feet|\"|in')


# noinspection SpellCheckingInspection
class Form(QObject):

    def __init__(self, ui_file, parent=None):
        """
        Sets all the initial variables that will be used throughout the class.
        :param ui_file:
        :param parent:
        """
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
        self.ca_endcut1_radio.clicked.connect(self.ca_endcuts)
        self.ca_endcut2_radio.clicked.connect(self.ca_endcuts)
        self.ca_endcut3_radio.clicked.connect(self.ca_endcuts)

        self.studio_form_control()
        self.cathedral_form_control()
        self.window.show()

    def studio_form_control(self):
        """
        This method disables the form until an appropriate scenario is selected.
        :return:
        """
        self.st_pitch_gbox.setEnabled(False)
        self.st_endcuts()
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
        """
        This method disables the form until an appropriate scenario is selected.
        :return:
        """
        self.ca_a_pitch_gbox.setEnabled(False)
        self.ca_c_pitch_gbox.setEnabled(False)
        self.ca_endcuts()
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
        """
        This method toggles the edit boxes depending on the scenario selected.
        :return:
        """
        self.studio_form_control()
        self.st_awall_edit.setEnabled(True)
        self.st_bwall_edit.setEnabled(True)
        self.st_cwall_edit.setEnabled(True)
        self.st_overhang_edit.setEnabled(True)
        self.st_roof_gbox.setEnabled(True)
        self.st_thick_combo.setEnabled(True)
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
        """
        This method toggles the edit boxes depending on the scenario selected.
        :return:
        """
        self.cathedral_form_control()
        self.ca_awall_edit.setEnabled(True)
        self.ca_bwall_edit.setEnabled(True)
        self.ca_cwall_edit.setEnabled(True)
        self.ca_overhang_edit.setEnabled(True)
        self.ca_roof_gbox.setEnabled(True)
        self.ca_thick_combo.setEnabled(True)
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
        """
        This method toggles Fascia checkbox depending on the End Cuts selected.
        :return:
        """
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
        """
        This method toggles Fascia checkbox depending on the End Cuts selected.
        :return:
        """
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
        """
        This method toggles the Fascia checkbox depnding on the roofing type and thickness selected.
        :return:
        """
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
        """
        This method toggles the Fascia checkbox depnding on the roofing type and thickness selected.
        :return:
        """
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
        """
        This method changes the pitch label depending on the radio selected.
        :return:
        """
        self.st_pitch_label.clear()
        if self.st_ratio_radio.isChecked():
            self.st_pitch_label.setText('/12 in.')
        elif self.st_angle_radio.isChecked():
            self.st_pitch_label.setText('Angle in\nDegrees')

    def ca_pitch_label_change(self):
        """
        This method changes the pitch label depending on the radio selected.
        :return:
        """
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
        """
        This method is used to populate the Thickness combo box.
        :return:
        """
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
        """
        This method is used to populate the Thickness combo box.
        :return:
        """
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

    def common_results(self, common):
        """
        This method is used to organize the results into a dictionary.
        :param common: class
        :return: dict
        """
        peak = Eu(Cc.assume_units(str(Cc.sixteenth(common.peak)), '"'), u_type='length')
        panel_length = Eu(Cc.assume_units(str(common.panel_length()[0]), '"'), u_type='length')
        max_panel_length = common.panel_length()[1]
        soffit_height = Eu(Cc.assume_units(str(Cc.sixteenth(common.soffit)), '"'), u_type='length')
        drip_edge = Eu(Cc.assume_units(str(Cc.sixteenth(common.drip_edge())), '"'), u_type='length')
        roof_area = math.ceil(common.roof_panels()[0] / 144)
        hang_rail = Eu(Cc.assume_units(str(common.hang_rail()[0]), '"'), u_type='length')
        max_hang_rail_length = common.hang_rail()[1]
        fascia_b_wall = Eu(Cc.assume_units(str(common.fascia()[0]), '"'), u_type='length')
        fascia_sides = Eu(Cc.assume_units(str(common.fascia()[1]), '"'), u_type='length')
        max_fascia_length = common.fascia()[2]
        roof_panels = common.roof_panels()[1]
        max_height = Eu(Cc.assume_units(str(Cc.sixteenth(common.max_h)), '"'), u_type='length')
        overhang_ = Eu(Cc.assume_units(str(common.overhang), '"'), u_type='length')
        side_overhang = Eu(Cc.assume_units(str(common.roof_panels()[2]), '"'), u_type='length')
        armstrong = common.armstrong_panels()
        overhang_error = common.roof_panels()[3]
        wall_height_ = Eu(Cc.assume_units(str(Cc.sixteenth(common.wall_height)), '"'), u_type='length')
        split = common.roof_panels()[4]
        tol = common.panel_length()[2]
        common_results = {'pitch': common.pitch, 'peak': peak.simplified('in'), 'panel length':
            panel_length.simplified('in'), 'max panel length': max_panel_length,
                          'soffit height': soffit_height.simplified('in'), 'drip edge': drip_edge.simplified('in'),
                          'roof area': roof_area, 'hang rail': hang_rail.simplified('in'),
                          'max hang rail length': max_hang_rail_length, 'fascia wall': fascia_b_wall.simplified('in'),
                          'fascia sides': fascia_sides.simplified('in'), 'max fascia length': max_fascia_length,
                          'roof panels': roof_panels, 'max height': max_height.simplified('in'),
                          'overhang': overhang_.simplified('in'), 'side overhang': side_overhang.simplified('in'),
                          'armstrong': armstrong, 'wallheight': wall_height_.simplified('in'),
                          'sidewall': wall_height_.simplified('in'), 'overhang error': overhang_error,
                          'split panels': split, 'panel tolerance': tol}
        return common_results

    @property
    def st_scenario_calc(self):
        """
        This method is called when the "Calculate" button is pressed. It calls functions to perform the calculations and
        saves it to a dictionary.
        :return: dict
        """
        overhang = Eu(Cc.assume_units(self.st_overhang_edit.text(), '"'), u_type='length')
        awall = Eu(Cc.assume_units(self.st_awall_edit.text(), '"'), u_type='length')
        bwall = Eu(Cc.assume_units(self.st_bwall_edit.text(), '"'), u_type='length')
        cwall = Eu(Cc.assume_units(self.st_cwall_edit.text(), '"'), u_type='length')
        panel_thickness = Eu(self.st_thick_combo.itemData(self.st_thick_combo.currentIndex()), u_type='length')
        if self.st_endcut1_radio.isChecked():
            endcut = 'uncut'
        elif self.st_endcut2_radio.isChecked():
            endcut = 'plum_T_B'
        elif self.st_endcut3_radio.isChecked():
            endcut = 'plum_T'
        studio = StudioCalcs.StudioCalcs(overhang.base, awall.base, bwall.base, cwall.base, panel_thickness.base,
                                         endcut)
        if self.st_scenario1_radio.isChecked():
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(Cc.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(Cc.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            pitch = Cc.pitch_input(pitch_input)
            b_wall_height = Eu(Cc.assume_units(self.st_bwallheight_edit.text(), '"'), u_type='length')
            common = studio.wall_height_pitch(pitch, b_wall_height.base)
        elif self.st_scenario2_radio.isChecked():
            b_wall_height = Eu(Cc.assume_units(self.st_bwallheight_edit.text(), '"'), u_type='length')
            peak = Eu(Cc.assume_units(self.st_peak_edit.text(), '"'), u_type='length')
            common = studio.wall_height_peak_height(b_wall_height.base, peak.base)
        elif self.st_scenario3_radio.isChecked():
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(Cc.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(Cc.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            pitch = Cc.pitch_input(pitch_input)
            max_h = Eu(Cc.assume_units(self.st_max_edit.text(), '"'), u_type='length')
            common = studio.max_height_pitch(pitch, max_h.base)
        elif self.st_scenario4_radio.isChecked():
            peak = Eu(Cc.assume_units(self.st_peak_edit.text(), '"'), u_type='length')
            soffit = Eu(Cc.assume_units(self.st_soffit_edit.text(), '"'), u_type='length')
            common = studio.soffit_height_peak_height(peak.base, soffit.base)
        elif self.st_scenario5_radio.isChecked():
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(Cc.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(Cc.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            pitch = Cc.pitch_input(pitch_input)
            soffit = Eu(Cc.assume_units(self.st_soffit_edit.text(), '"'), u_type='length')
            common = studio.soffit_height_pitch(pitch, soffit.base)
        elif self.st_scenario6_radio.isChecked():
            peak = Eu(Cc.assume_units(self.st_peak_edit.text(), '"'), u_type='length')
            drip_edge = Eu(Cc.assume_units(self.st_drip_edit.text(), '"'), u_type='length')
            common = studio.drip_edge_peak_height(drip_edge.base, peak.base)
        elif self.st_scenario7_radio.isChecked():
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(Cc.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(Cc.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            pitch = Cc.pitch_input(pitch_input)
            drip_edge = Eu(Cc.assume_units(self.st_drip_edit.text(), '"'), u_type='length')
            common = studio.drip_edge_pitch(drip_edge.base, pitch)
        return self.common_results(common)

    @property
    def ca_scenario_calc(self):
        """
        This method is called when the "Calculate" button is pressed. It calls functions to perform the calculations and
        saves it to a dictionary.
        :return: dict
        """
        overhang = Eu(Cc.assume_units(self.ca_overhang_edit.text(), '"'), u_type='length')
        awall = Eu(Cc.assume_units(self.ca_awall_edit.text(), '"'), u_type='length')
        bwall = Eu(Cc.assume_units(self.ca_bwall_edit.text(), '"'), u_type='length')
        cwall = Eu(Cc.assume_units(self.ca_cwall_edit.text(), '"'), u_type='length')
        panel_thickness = Eu(self.ca_thick_combo.itemData(self.ca_thick_combo.currentIndex()), u_type='length')
        if self.ca_endcut1_radio.isChecked():
            endcut = 'uncut'
        elif self.ca_endcut2_radio.isChecked():
            endcut = 'plum_T_B'
        elif self.ca_endcut3_radio.isChecked():
            endcut = 'plum_T'
        catherdral = CatherdralCalcs.CathedralCalcs(overhang.base, awall.base, bwall.base, cwall.base,
                                                    panel_thickness.base, endcut)
        if self.ca_scenario1_radio.isChecked():
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(Cc.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(Cc.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(Cc.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                c_pitch_input = Eu(Cc.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            a_pitch = Cc.pitch_input(a_pitch_input)
            c_pitch = Cc.pitch_input(c_pitch_input)
            a_wall_height = Eu(Cc.assume_units(self.ca_awallheight_edit.text(), '"'), u_type='length')
            c_wall_height = Eu(Cc.assume_units(self.ca_cwallheight_edit.text(), '"'), u_type='length')
            common = catherdral.wall_height_pitch(a_pitch=a_pitch, c_pitch=c_pitch, a_wall_height=a_wall_height.base,
                                                  c_wall_height=c_wall_height.base)
        elif self.ca_scenario2_radio.isChecked():
            a_wall_height = Eu(Cc.assume_units(self.ca_awallheight_edit.text(), '"'), u_type='length')
            c_wall_height = Eu(Cc.assume_units(self.ca_cwallheight_edit.text(), '"'), u_type='length')
            peak = Eu(Cc.assume_units(self.ca_peak_edit.text(), '"'), u_type='length')
            common = catherdral.wall_height_peak_height(a_wall_height=a_wall_height.base,
                                                        c_wall_height=c_wall_height.base, peak=peak.base)
        elif self.ca_scenario3_radio.isChecked():
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(Cc.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(Cc.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(Cc.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                c_pitch_input = Eu(Cc.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            a_pitch = Cc.pitch_input(a_pitch_input)
            c_pitch = Cc.pitch_input(c_pitch_input)
            max_h = Eu(Cc.assume_units(self.ca_max_edit.text(), '"'), u_type='length')
            common = catherdral.max_height_pitch(max_h=max_h.base, a_pitch=a_pitch, c_pitch=c_pitch)
        elif self.ca_scenario4_radio.isChecked():
            a_soffit = Eu(Cc.assume_units(self.ca_a_soffit_edit.text(), '"'), u_type='length')
            c_soffit = Eu(Cc.assume_units(self.ca_c_soffit_edit.text(), '"'), u_type='length')
            peak = Eu(Cc.assume_units(self.ca_peak_edit.text(), '"'), u_type='length')
            common = catherdral.soffit_height_peak_height(a_soffit=a_soffit.base, c_soffit=c_soffit.base,
                                                          peak=peak.base)
        elif self.ca_scenario5_radio.isChecked():
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(Cc.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(Cc.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(Cc.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                c_pitch_input = Eu(Cc.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            a_pitch = Cc.pitch_input(a_pitch_input)
            c_pitch = Cc.pitch_input(c_pitch_input)
            a_soffit = Eu(Cc.assume_units(self.ca_a_soffit_edit.text(), '"'), u_type='length')
            c_soffit = Eu(Cc.assume_units(self.ca_c_soffit_edit.text(), '"'), u_type='length')
            common = catherdral.soffit_height_pitch(a_pitch=a_pitch, c_pitch=c_pitch, a_soffit=a_soffit.base,
                                                    c_soffit=c_soffit.base)
        elif self.ca_scenario6_radio.isChecked():
            peak = Eu(Cc.assume_units(self.ca_peak_edit.text(), '"'), u_type='length')
            drip_edge = Eu(Cc.assume_units(self.ca_drip_edit.text(), '"'), u_type='length')
            common = catherdral.drip_edge_peak_height(drip_edge=drip_edge.base, peak=peak.base)
        elif self.ca_scenario7_radio.isChecked():
            drip_edge = Eu(Cc.assume_units(self.ca_drip_edit.text(), '"'), u_type='length')
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(Cc.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(Cc.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(Cc.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                c_pitch_input = Eu(Cc.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            a_pitch = Cc.pitch_input(a_pitch_input)
            c_pitch = Cc.pitch_input(c_pitch_input)
            common = catherdral.drip_edge_pitch(drip_edge=drip_edge.base, a_pitch=a_pitch, c_pitch=c_pitch)
        a_results = self.common_results(common[0])
        c_results = self.common_results(common[1])
        results = {'a pitch': a_results['pitch'], 'c pitch': c_results['pitch'], 'peak': a_results['peak'],
                   'a panel length': c_results['panel length'], 'c panel length': c_results['panel length'],
                   'a max panel length': a_results['max panel length'], 'c max panel length':
                       c_results['max panel length'], 'a soffit height': a_results['soffit height'],
                   'c soffit height': c_results['soffit height'], 'a drip edge': a_results['drip edge'],
                   'c drip edge': c_results['drip edge'], 'a roof area': a_results['roof area'], 'c roof area':
                       c_results['roof area'], 'a hang rail': a_results['hang rail'], 'c hang rail':
                       c_results['hang rail'], 'max hang rail length a': a_results['max hang rail length'],
                   'max hang rail length c': c_results['max hang rail length'], 'fascia a wall':
                       a_results['fascia wall'], 'fascia c wall': c_results['fascia wall'], 'fascia a side':
                       a_results['fascia sides'], 'fascia c side': c_results['fascia sides'], 'max fascia length a':
                   a_results['max fascia length'], 'max fascia length c': c_results['max fascia length'],
                   'a roof panels': a_results['roof panels'], 'c roof panels': c_results['roof panels'], 'max height':
                       a_results['max height'], 'a overhang': a_results['overhang'], 'c overhang':
                       c_results['overhang'], 'a side overhang': a_results['side overhang'], 'c side overhang':
                       c_results['side overhang'], 'a armstrong': a_results['armstrong'], 'c armstrong':
                       c_results['armstrong'], 'awallheight': a_results['wallheight'], 'cwallheight':
                       c_results['wallheight'], 'sidewall': a_results['sidewall'], 'a overhang error':
                       a_results['overhang error'], 'c overhang error': c_results['overhang error'], 'a split panels':
                   a_results['split panels'], 'c split panels': c_results['split panels'], 'a panel tolerance':
                       a_results['panel tolerance'], 'c panel tolerance': c_results['panel tolerance']}
        return results

    def st_results_message(self, results):
        """
        This method displays all the results to the st_text_browser object.
        :param results: dict
        :return:
        """
        roof_total = results['roof area']
        self.st_results.append('The pitch is: {}/12.'.format(Cc.pitch_estimate(12 * math.tan(results['pitch']))))
        self.st_results.append('The peak height is {}.'.format(results['peak']))
        self.st_results.append('The soffit height is {}.'.format(results['soffit height']))
        self.st_results.append('The drip edge is at {}.'.format(results['drip edge']))
        self.st_results.append('The maximum height is {}.'.format(results['max height']))
        self.st_results.append('The A and C Wall heights are {}.'.format(results['sidewall']))
        self.st_results.append('The B Wall height is {}.'.format(results['wallheight']))
        self.st_results.append('This configuration will need {} roof panels.'.format(results['roof panels']))
        self.st_results.append('The length of each panel should be {}.'.format(results['panel length']))
        if results['panel tolerance'] is True:
            self.st_results.append("These panels are 1 in. beyond the nearest foot! They should be within the "
                                   "manufacturer's tolerance.")
        if results['max panel length'] is True:
            self.st_results.append('These panels were divided in half because they were more than 24ft.')
        self.st_results.append('The roof sq. ft. is {} ft^2.'.format(roof_total))
        self.st_results.append('You will need {} boxes of Armstrong Ceiling Panels.'.format(results['armstrong']))
        self.st_results.append('The overhang on B Wall is {}.'.format(results['overhang']))
        self.st_results.append('The overhang on A and C Walls are {}.'.format(results['side overhang']))
        if results['overhang error'][0] is True:
            # self.st_results.clear()
            self.st_results.append('The overhang on the sides are TOO SHORT!')
        # elif results['overhang error'][1] is True:
        # self.st_results.clear()
        # self.st_results.append('The overhang on the sides are too long and need to be cut!')
        if results['max hang rail length'] is True:
            self.st_results.append('There are 2 pairs of hang rails at {}. each.'.format(results['hang rail']))
            self.st_results.append('They were divided in half because the original length was longer than 216 in.')
        else:
            self.st_results.append('There is 1 pair of hang rails at {}. each.'.format(results['hang rail']))
        if self.st_fascia.isChecked():
            if results['max fascia length'][0] is True:
                self.st_results.append('There are 2 pieces of Fascia at {}. each for the B wall'
                                       .format(results['fascia wall']))
                self.st_results.append('Their original length was more than 216 in. so they were cut in half.')
            else:
                self.st_results.append('There is 1 piece of Fascia at {}. for the B wall.'
                                       .format(results['fascia wall']))
            if results['max fascia length'][1] is True:
                self.st_results.append('There are 2 pieces of Fascia for the A and C walls. Both are at {}. for each'
                                       ' wall'.format(results['fascia sides']))
                self.st_results.append('Their original length was more than 216 in.')
            else:
                self.st_results.append('There is one piece of Fascia at {}. for the A Wall and one piece at {} '
                                       'for the C wall.'.format(results['fascia sides'], results['fascia sides']))

    def ca_results_message(self, results):
        """
        This method displays all the results to the ca_text_browser object.
        :param results: dict
        :return:
        """
        roof_total = (int(results['a roof area'] + results['c roof area']))
        self.ca_results.append('The A side pitch is: {}/12.'
                               .format(Cc.pitch_estimate(12 * math.tan(results['a pitch']))))
        self.ca_results.append('The C side pitch is: {}/12.'
                               .format(Cc.pitch_estimate(12 * math.tan(results['c pitch']))))
        self.ca_results.append('The peak height is {}.'.format(results['peak']))
        self.ca_results.append('The A Wall height is {}.'.format(results['awallheight']))
        # self.ca_results.append('The B Wall height is {}.'.format(results['sidewall']))
        self.ca_results.append('The C Wall height is {}.'.format(results['cwallheight']))
        self.ca_results.append('The A side soffit height is {}.'.format(results['a soffit height']))
        self.ca_results.append('The C side soffit height is {}.'.format(results['c soffit height']))
        self.ca_results.append('The A side drip edge is at {}.'.format(results['a drip edge']))
        self.ca_results.append('The C side drip edge is at {}.'.format(results['c drip edge']))
        self.ca_results.append('The maximum height is {}.'.format(results['max height']))
        self.ca_results.append('This configuration will need {} A side roof panels.'.format(results['a roof panels']))
        self.ca_results.append('The length of each A side panel should be {}.'.format(results['a panel length']))
        if results['a panel tolerance'] is True:
            self.ca_results.append("The A side panels are 1 in. beyond the nearest foot! They should be within the "
                                   "manufacturer's tolerance.")
        if results['a max panel length'] is True:
            self.ca_results.append('The A side panels were divided in half because they were more than 24ft.')
        self.ca_results.append('This configuration will need {} C side roof panels.'.format(results['c roof panels']))
        self.ca_results.append('The length of each C side panel should be {}.'.format(results['c panel length']))
        if results['c panel tolerance'] is True:
            self.ca_results.append("The C side panels are 1 in. beyond the nearest foot! They should be within the "
                                   "manufacturer's tolerance.")
        if results['c max panel length'] is True:
            self.ca_results.append('The C side panels were divided in half because they were more than 24ft.')
        self.ca_results.append('The total number of roof panels is {}.'.format(int(results['a roof panels'] +
                                                                               results['c roof panels'])))
        # if results['a split panels'] is True or results['c split panels'] is True:
        #     self.ca_results.append('One of the panels should be split in half on site!!!')
        self.ca_results.append('The Total roof sq. ft. is {} ft^2.'.format(roof_total))
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
            self.ca_results.append('There are 2 pairs of hang rails at {}. each on the A wall.'
                                   .format(results['a hang rail']))
            self.ca_results.append('They were divided in half because the original length was longer than 216".')
        else:
            self.ca_results.append('There is 1 pair of hang rails at {} on the A wall'
                                   .format(results['a hang rail']))
        if results['max hang rail length c'] is True:
            self.ca_results.append('There are 2 pairs of hang rails at {} each on the C wall.'
                                   .format(results['c hang rail']))
            self.ca_results.append('They were divided in half because the original length was longer than 216".')
        else:
            self.ca_results.append('There is 1 pair of hang rails at {} on the C wall'
                                   .format(results['c hang rail']))
        if self.ca_fascia.isChecked():
            if results['max fascia length a'][0] is True:
                self.ca_results.append('There are 2 pieces of Fascia at {} in. each for the A wall'
                                       .format(results['fascia a wall']))
                self.ca_results.append('Their original length was more than 216 in. so they were cut in half.')
            else:
                self.ca_results.append('There is 1 pieces of Fascia at {} for the A wall'
                                       .format(results['fascia a wall']))
            if results['max fascia length c'][0] is True:
                self.ca_results.append('There are 2 pieces of Fascia at {} each for the C wall'
                                       .format(results['fascia c wall']))
                self.ca_results.append('Their original length was more than 216 in. so they were cut in half.')
            else:
                self.ca_results.append('There is 1 pieces of Fascia at {} for the C wall'
                                       .format(results['fascia c wall']))
            if results['max fascia length a'][1] is True:
                self.ca_results.append('There are 2 pieces of Fascia for the A side B Wall. Both are at {} in. each'
                                       .format(results['fascia a side']))
                self.ca_results.append('Their original length was more than 216 in.')
            else:
                self.ca_results.append('There is 1 pieces of Fascia for the A side B Wall at {}'
                                       .format(results['fascia a side']))
            if results['max fascia length c'][1] is True:
                self.ca_results.append('There are 2 pieces of Fascia for the C side B Wall. Both are at {} each'
                                       .format(results['fascia c side']))
                self.ca_results.append('Their original length was more than 216 in.')
            else:
                self.ca_results.append('There is 1 pieces of Fascia for the C side B Wall at {}'
                                       .format(results['fascia c side']))

    def input_errors(self, box_name):
        """
        This method outputs a error message box. The input is the name of the edit box tied to the message.
        :param box_name: str
        :return: class
        """
        return QMessageBox.about(self.window, 'Input Error!', 'Missing input in {} box!'.format(box_name))

    def st_common_errors(self):
        """
        This method is displays error messages for the four common input boxes: Overhang, A Wall, B Wall, and C Wall.
        :return:
        """
        if self.st_overhang_edit.text() == '':
            QMessageBox.about(self.window, 'Input Error!', 'Missing input in overhang box!!')
        if self.st_awall_edit.text() == '':
            QMessageBox.about(self.window, 'Input Error!', 'Missing input in A Wall box!!')
        if self.st_bwall_edit.text() == '':
            QMessageBox.about(self.window, 'Input Error!', 'Missing input in B Wall box!!')
        if self.st_cwall_edit.text() == '':
            QMessageBox.about(self.window, 'Input Error!', 'Missing input in C Wall box!!')

    def ca_common_errors(self):
        """
        This method is displays error messages for the four common input boxes: Overhang, A Wall, B Wall, and C Wall.
        :return:
        """
        if self.ca_overhang_edit.text() == '':
            QMessageBox.about(self.window, 'Input Error!', 'Missing input in overhang box!!')
        if self.ca_awall_edit.text() == '':
            QMessageBox.about(self.window, 'Input Error!', 'Missing input in A Wall box!!')
        if self.ca_bwall_edit.text() == '':
            QMessageBox.about(self.window, 'Input Error!', 'Missing input in B Wall box!!')
        if self.ca_cwall_edit.text() == '':
            QMessageBox.about(self.window, 'Input Error!', 'Missing input in C Wall box!!')

    def st_calcbutton(self):
        """
        This method checks for missing input upon pressing the "Calculate" button. It then calls st_scenario_calc to
        calculate the quatities based on scenario selected.
        :return: dict
        """
        self.st_results.clear()
        self.st_common_errors()
        self.st_results.setText('Now listing results.')
        if self.st_scenario1_radio.isChecked():
            if self.st_pitch_edit.text() == '':
                self.input_errors('Pitch')
            elif self.st_bwallheight_edit.text() == '':
                self.input_errors('B Wall Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given B wall height and pitch...')
                results = self.st_scenario_calc
                self.st_results_message(results)
        elif self.st_scenario2_radio.isChecked():
            if self.st_peak_edit.text() == '':
                self.input_errors('Peak Height')
            elif self.st_bwallheight_edit.text() == '':
                self.input_errors('B Wall Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given wall height and peak height...')
                results = self.st_scenario_calc
                self.st_results_message(results)
        elif self.st_scenario3_radio.isChecked():
            if self.st_pitch_edit.text() == '':
                self.input_errors('pitch')
            elif self.st_max_edit.text() == '':
                self.input_errors('Max Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given max height and pitch...')
                results = self.st_scenario_calc
                self.st_results_message(results)
        elif self.st_scenario4_radio.isChecked():
            if self.st_soffit_edit.text() == '':
                self.input_errors('Soffit Height')
            elif self.st_peak_edit.text() == '':
                self.input_errors('Peak Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given soffit heights and peak height...')
                results = self.st_scenario_calc
                self.st_results_message(results)
        elif self.st_scenario5_radio.isChecked():
            if self.st_pitch_edit.text() == '':
                self.input_errors('pitch')
            elif self.st_soffit_edit.text() == '':
                self.input_errors('Soffit Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given soffit heights and pitch...')
                results = self.st_scenario_calc
                self.st_results_message(results)
        elif self.st_scenario6_radio.isChecked():
            if self.st_drip_edit.text() == '':
                self.input_errors('Drip Edge Height')
            elif self.st_peak_edit.text() == '':
                self.input_errors('Peak Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given drip edge and peak height...')
                results = self.st_scenario_calc
                self.st_results_message(results)
        elif self.st_scenario7_radio.isChecked():
            if self.st_pitch_edit.text() == '':
                self.input_errors('pitch')
            elif self.st_drip_edit.text() == '':
                self.input_errors('Drip Edge Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given drip edge and pitch...')
                results = self.st_scenario_calc
                self.st_results_message(results)
        else:
            QMessageBox.about(self.window, 'Select a Scenario!', 'No scenarios selected!')

    def ca_calcbutton(self):
        """
        This method checks for missing input upon pressing the "Calculate" button. It then calls ca_scenario_calc to
        calculate the quatities based on scenario selected.
        :return: dict
        """
        self.ca_results.clear()
        self.ca_common_errors()
        self.ca_results.setText('Now listing results.')
        if self.ca_scenario1_radio.isChecked():
            if self.ca_a_pitch_edit.text() == '':
                self.input_errors('A Side Pitch')
            elif self.ca_c_pitch_edit.text() == '':
                self.input_errors('C Side Pitch')
            elif self.ca_awallheight_edit.text() == '':
                self.input_errors('A Wall Height')
            elif self.ca_cwallheight_edit.text() == '':
                self.input_errors('C Wall Height')
            else:
                self.ca_results.append('*===================*')
                self.ca_results.append('Given wall height and pitch...')
                results = self.ca_scenario_calc
                self.ca_results_message(results)
        elif self.ca_scenario2_radio.isChecked():
            if self.ca_peak_edit.text() == '':
                self.input_errors('Peak Height')
            elif self.ca_awallheight_edit.text() == '':
                self.input_errors('A Wall Height')
            elif self.ca_cwallheight_edit.text() == '':
                self.input_errors('C Wall Height')
            else:
                self.ca_results.append('*===================*')
                self.ca_results.append('Given wall height and peak height...')
                results = self.ca_scenario_calc
                self.ca_results_message(results)
        elif self.ca_scenario3_radio.isChecked():
            if self.ca_a_pitch_edit.text() == '':
                self.input_errors('A Side Pitch')
            elif self.ca_c_pitch_edit.text() == '':
                self.input_errors('C Side Pitch')
            elif self.ca_max_edit.text() == '':
                self.input_errors('Max Height')
            else:
                self.ca_results.append('*===================*')
                self.ca_results.append('Given max height and pitch...')
                results = self.ca_scenario_calc
                self.ca_results_message(results)
        elif self.ca_scenario4_radio.isChecked():
            if self.ca_peak_edit.text() == '':
                self.input_errors('Peak Height')
            elif self.ca_a_soffit_edit.text() == '':
                self.input_errors('Soffit Height A Wall')
            elif self.ca_c_soffit_edit.text() == '':
                self.input_errors('Soffit Height C Wall')
            else:
                self.ca_results.append('*===================*')
                self.ca_results.append('Given soffit heights and peak height...')
                results = self.ca_scenario_calc
                self.ca_results_message(results)
        elif self.ca_scenario5_radio.isChecked():
            if self.ca_a_pitch_edit.text() == '':
                self.input_errors('A Side Pitch')
            elif self.ca_c_pitch_edit.text() == '':
                self.input_errors('C Side Pitch')
            elif self.ca_a_soffit_edit.text() == '':
                self.input_errors('Soffit Height A Wall')
            elif self.ca_c_soffit_edit.text() == '':
                self.input_errors('Soffit Height C Wall')
            else:
                self.ca_results.append('*===================*')
                self.ca_results.append('Given soffit heights and pitch...')
                results = self.ca_scenario_calc
                self.ca_results_message(results)
        elif self.ca_scenario6_radio.isChecked():
            if self.ca_peak_edit.text() == '':
                self.input_errors('Peak Height')
            elif self.ca_drip_edit.text() == '':
                self.input_errors('Drip Edge Height')
            else:
                self.ca_results.append('*===================*')
                self.ca_results.append('Given drip edge and peak height...')
                results = self.ca_scenario_calc
                self.ca_results_message(results)
        elif self.ca_scenario7_radio.isChecked():
            if self.ca_a_pitch_edit.text() == '':
                self.input_errors('A Side Pitch')
            elif self.ca_c_pitch_edit.text() == '':
                self.input_errors('C Side Pitch')
            elif self.ca_drip_edit.text() == '':
                self.input_errors('Drip Edge Height')
            else:
                self.ca_results.append('*===================*')
                self.ca_results.append('Given drip edge and pitch...')
                results = self.ca_scenario_calc
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
