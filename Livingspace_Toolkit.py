#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# main.py
# noinspection SpellCheckingInspection
"""
This is the main program file for the Livingspace Toolkit. This program generates the GUI for the representatives to
help their sales reps on meeting the needs of their customers.
"""

import sys
from os import path as os_path
from datetime import datetime
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QPushButton, QLineEdit, QRadioButton, QComboBox, QTextBrowser
from PySide6.QtWidgets import QGroupBox, QLabel, QMessageBox, QCheckBox, QTabWidget
from PySide6.QtCore import QFile, QObject
import UI_rc
from Units import EngineeringUnits as Eu
import LivingspaceToolkitClass as LSTKC
from math import tan
import logging
import yaml
from pathlib import Path


# noinspection SpellCheckingInspection
class Form(QObject):

    def __init__(self, ui_file, parent=None):
        """
        Sets all the initial variables that will be used throughout the class.
        :param ui_file:
        :param parent:
        """
        logger.info('The current date and time is: {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")))
        version = '1.9.5'
        logger.info(f"Current version is {version}.")
        version_path = \
            r'\\192.168.1.13\Conwed\Interior Systems\Engineering\Custom_Software\Livingspace_Toolkit\version.yaml'
        super(Form, self).__init__(parent)
        ui_file = QFile(ui_file)
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        # self.max_panel_length = 24 * 12
        self.tabWidget = self.window.findChild(QTabWidget, 'tabWidget')
        self.studio = None
        self.cathedral = None
        self.version_label = self.window.findChild(QLabel, 'lbl_version')
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
        self.version_label.setText(f"Version: {version}")
        self.window.show()
        remote_version = version
        try:
            with open(version_path) as file:
                remote_version = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError as err:
            logger.exception(err)
        else:
            if remote_version > version:
                QMessageBox.warning(self.window, 'Please Update!',
                                    f"You are using version {version}. Please update to version {remote_version}!")

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

    def st_scenario_calc(self):
        """
        This method is called when the "Calculate" button is pressed. It calls functions to perform the calculations and
        saves it to a dictionary.
        """
        pitch_input = None
        endcut = None
        overhang = Eu(LSTKC.assume_units(self.st_overhang_edit.text(), '"'), u_type='length')
        awall = Eu(LSTKC.assume_units(self.st_awall_edit.text(), '"'), u_type='length')
        bwall = Eu(LSTKC.assume_units(self.st_bwall_edit.text(), '"'), u_type='length')
        cwall = Eu(LSTKC.assume_units(self.st_cwall_edit.text(), '"'), u_type='length')
        panel_thickness = Eu(self.st_thick_combo.itemData(self.st_thick_combo.currentIndex()), u_type='length')
        if self.st_endcut1_radio.isChecked():
            endcut = 'uncut'
        elif self.st_endcut2_radio.isChecked():
            endcut = 'plum_T_B'
        elif self.st_endcut3_radio.isChecked():
            endcut = 'plum_T'
        self.studio = LSTKC.Studio(overhang.base, awall.base, bwall.base, cwall.base, panel_thickness.base, endcut)
        if self.st_scenario1_radio.isChecked():
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(LSTKC.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(LSTKC.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            pitch = LSTKC.pitch_input(pitch_input)
            b_wall_height = Eu(LSTKC.assume_units(self.st_bwallheight_edit.text(), '"'), u_type='length')
            self.studio.wall_height_pitch(pitch, b_wall_height.base)
        elif self.st_scenario2_radio.isChecked():
            b_wall_height = Eu(LSTKC.assume_units(self.st_bwallheight_edit.text(), '"'), u_type='length')
            peak = Eu(LSTKC.assume_units(self.st_peak_edit.text(), '"'), u_type='length')
            self.studio.wall_height_peak_height(b_wall_height.base, peak.base)
        elif self.st_scenario3_radio.isChecked():
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(LSTKC.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(LSTKC.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            pitch = LSTKC.pitch_input(pitch_input)
            max_h = Eu(LSTKC.assume_units(self.st_max_edit.text(), '"'), u_type='length')
            self.studio.max_height_pitch(pitch, max_h.base)
        elif self.st_scenario4_radio.isChecked():
            peak = Eu(LSTKC.assume_units(self.st_peak_edit.text(), '"'), u_type='length')
            soffit = Eu(LSTKC.assume_units(self.st_soffit_edit.text(), '"'), u_type='length')
            self.studio.soffit_height_peak_height(peak.base, soffit.base)
        elif self.st_scenario5_radio.isChecked():
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(LSTKC.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(LSTKC.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            pitch = LSTKC.pitch_input(pitch_input)
            soffit = Eu(LSTKC.assume_units(self.st_soffit_edit.text(), '"'), u_type='length')
            self.studio.soffit_height_pitch(pitch, soffit.base)
        elif self.st_scenario6_radio.isChecked():
            peak = Eu(LSTKC.assume_units(self.st_peak_edit.text(), '"'), u_type='length')
            drip_edge = Eu(LSTKC.assume_units(self.st_drip_edit.text(), '"'), u_type='length')
            self.studio.drip_edge_peak_height(drip_edge.base, peak.base)
        elif self.st_scenario7_radio.isChecked():
            if self.st_ratio_radio.isChecked():
                pitch_input = Eu(LSTKC.assume_units(self.st_pitch_edit.text(), '"'), u_type='length')
            elif self.st_angle_radio.isChecked():
                pitch_input = Eu(LSTKC.assume_units(self.st_pitch_edit.text(), 'deg'), u_type='angle')
            pitch = LSTKC.pitch_input(pitch_input)
            drip_edge = Eu(LSTKC.assume_units(self.st_drip_edit.text(), '"'), u_type='length')
            self.studio.drip_edge_pitch(drip_edge.base, pitch)
        self.studio.calculate_sunroom()

    def ca_scenario_calc(self):
        """
        This method is called when the "Calculate" button is pressed. It calls functions to perform the calculations and
        saves it to a dictionary.
        """
        a_pitch_input = None
        c_pitch_input = None
        endcut = None
        overhang = Eu(LSTKC.assume_units(self.ca_overhang_edit.text(), '"'), u_type='length')
        awall = Eu(LSTKC.assume_units(self.ca_awall_edit.text(), '"'), u_type='length')
        bwall = Eu(LSTKC.assume_units(self.ca_bwall_edit.text(), '"'), u_type='length')
        cwall = Eu(LSTKC.assume_units(self.ca_cwall_edit.text(), '"'), u_type='length')
        panel_thickness = Eu(self.ca_thick_combo.itemData(self.ca_thick_combo.currentIndex()), u_type='length')
        if self.ca_endcut1_radio.isChecked():
            endcut = 'uncut'
        elif self.ca_endcut2_radio.isChecked():
            endcut = 'plum_T_B'
        elif self.ca_endcut3_radio.isChecked():
            endcut = 'plum_T'
        self.cathedral = LSTKC.Cathedral(overhang.base, awall.base, bwall.base, cwall.base, panel_thickness.base,
                                         endcut)
        if self.ca_scenario1_radio.isChecked():
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(LSTKC.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(LSTKC.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(LSTKC.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                c_pitch_input = Eu(LSTKC.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            a_pitch = LSTKC.pitch_input(a_pitch_input)
            c_pitch = LSTKC.pitch_input(c_pitch_input)
            a_wall_height = Eu(LSTKC.assume_units(self.ca_awallheight_edit.text(), '"'), u_type='length')
            c_wall_height = Eu(LSTKC.assume_units(self.ca_cwallheight_edit.text(), '"'), u_type='length')
            self.cathedral.wall_height_pitch([a_pitch, c_pitch], [a_wall_height.base, c_wall_height.base])
        elif self.ca_scenario2_radio.isChecked():
            a_wall_height = Eu(LSTKC.assume_units(self.ca_awallheight_edit.text(), '"'), u_type='length')
            c_wall_height = Eu(LSTKC.assume_units(self.ca_cwallheight_edit.text(), '"'), u_type='length')
            peak = Eu(LSTKC.assume_units(self.ca_peak_edit.text(), '"'), u_type='length')
            self.cathedral.wall_height_peak_height([a_wall_height.base, c_wall_height.base], peak.base)
        elif self.ca_scenario3_radio.isChecked():
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(LSTKC.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(LSTKC.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(LSTKC.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                c_pitch_input = Eu(LSTKC.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            a_pitch = LSTKC.pitch_input(a_pitch_input)
            c_pitch = LSTKC.pitch_input(c_pitch_input)
            max_h = Eu(LSTKC.assume_units(self.ca_max_edit.text(), '"'), u_type='length')
            self.cathedral.max_height_pitch([a_pitch, c_pitch], max_h.base)
        elif self.ca_scenario4_radio.isChecked():
            a_soffit = Eu(LSTKC.assume_units(self.ca_a_soffit_edit.text(), '"'), u_type='length')
            c_soffit = Eu(LSTKC.assume_units(self.ca_c_soffit_edit.text(), '"'), u_type='length')
            peak = Eu(LSTKC.assume_units(self.ca_peak_edit.text(), '"'), u_type='length')
            self.cathedral.soffit_height_peak_height(peak.base, [a_soffit.base, c_soffit.base])
        elif self.ca_scenario5_radio.isChecked():
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(LSTKC.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(LSTKC.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(LSTKC.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                c_pitch_input = Eu(LSTKC.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            a_pitch = LSTKC.pitch_input(a_pitch_input)
            c_pitch = LSTKC.pitch_input(c_pitch_input)
            a_soffit = Eu(LSTKC.assume_units(self.ca_a_soffit_edit.text(), '"'), u_type='length')
            c_soffit = Eu(LSTKC.assume_units(self.ca_c_soffit_edit.text(), '"'), u_type='length')
            self.cathedral.soffit_height_pitch([a_pitch, c_pitch], [a_soffit.base, c_soffit.base])
        elif self.ca_scenario6_radio.isChecked():
            peak = Eu(LSTKC.assume_units(self.ca_peak_edit.text(), '"'), u_type='length')
            drip_edge = Eu(LSTKC.assume_units(self.ca_drip_edit.text(), '"'), u_type='length')
            self.cathedral.drip_edge_peak_height(drip_edge.base, peak.base)
        elif self.ca_scenario7_radio.isChecked():
            drip_edge = Eu(LSTKC.assume_units(self.ca_drip_edit.text(), '"'), u_type='length')
            if self.ca_a_ratio_radio.isChecked():
                a_pitch_input = Eu(LSTKC.assume_units(self.ca_a_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                a_pitch_input = Eu(LSTKC.assume_units(self.ca_a_pitch_edit.text(), 'deg'), u_type='angle')
            if self.ca_c_ratio_radio.isChecked():
                c_pitch_input = Eu(LSTKC.assume_units(self.ca_c_pitch_edit.text(), '"'), u_type='length')
            elif self.ca_a_angle_radio.isChecked():
                c_pitch_input = Eu(LSTKC.assume_units(self.ca_c_pitch_edit.text(), 'deg'), u_type='angle')
            a_pitch = LSTKC.pitch_input(a_pitch_input)
            c_pitch = LSTKC.pitch_input(c_pitch_input)
            self.cathedral.drip_edge_pitch(drip_edge.base, [a_pitch, c_pitch])
        self.cathedral.calculate_sunroom()

    def st_results_message(self):
        """
        This method displays all the results to the st_text_browser object.
        :return:
        """
        self.st_results.append('The pitch is: {}/12.'
                               .format(LSTKC.pitch_estimate(12 * tan(self.studio.pitch))))
        self.st_results.append('The peak height is {} in.'.format(LSTKC.sixteenth(self.studio.peak)))
        self.st_results.append('The soffit height is {} in.'.format(LSTKC.sixteenth(self.studio.soffit)))
        self.st_results.append('The drip edge is at {} in.'.format(LSTKC.sixteenth(self.studio.drip_edge)))
        self.st_results.append('The maximum height is {} in.'.format(LSTKC.sixteenth(self.studio.max_h)))
        self.st_results.append(
            'The A and C Wall heights are {} in.'.format(LSTKC.sixteenth(self.studio.unpitched_wall)))
        self.st_results.append('The B Wall height is {} in.'.format(LSTKC.sixteenth(self.studio.unpitched_wall)))
        self.st_results.append('This configuration will need {} roof panels.'
                               .format(self.studio.roof_panel_dict['Roof Panels']))
        self.st_results.append('The length of each panel should be {:.0f} in.'
                               .format(self.studio.panel_length_dict['Panel Length']))
        if self.studio.panel_length_dict['Max Length Check'] is True:
            self.st_results.append('These panels were divided in half because they were more than 24ft.')
        self.st_results.append(
            'The roof sq. ft. is {:.0f} ft^2.'.format(self.studio.roof_panel_dict['Roof Area'] / 144))
        self.st_results.append('You will need {:.0f} boxes of Armstrong Ceiling Panels.'
                               .format(self.studio.armstrong_panels))
        self.st_results.append('The overhang on B Wall is {:.0f} in.'.format(self.studio.overhang))
        self.st_results.append('The overhang on A and C Walls are {:.0f} in.'
                               .format(self.studio.roof_panel_dict['Side Overhang']))
        if self.studio.roof_panel_dict['Overhang Short Check'] is True:
            self.st_results.append('The overhang on the sides are TOO SHORT!')
        if self.studio.hang_rail_dict['Hang Rail Check'] is True:
            self.st_results.append('There are 2 pairs of hang rails at {} in. each.'
                                   .format(self.studio.hang_rail_dict['Hang Rail']))
            self.st_results.append('They were divided in half because the original length was longer than 216 in.')
        else:
            self.st_results.append('There is 1 pair of hang rails at {:.0f} in. each.'
                                   .format(self.studio.hang_rail_dict['Hang Rail']))
        if self.st_fascia.isChecked():
            if self.studio.fascia_dict['Fascia Check'][0] is True:
                self.st_results.append('There are 2 pieces of Fascia at {} in. each for the B wall'
                                       .format(self.studio.fascia_dict['Wall Fascia']))
                self.st_results.append('Their original length was more than 216 in. so they were cut in half.')
            else:
                self.st_results.append('There is 1 piece of Fascia at {:.0f} in. for the B wall.'
                                       .format(self.studio.fascia_dict['Wall Fascia']))
            if self.studio.fascia_dict['Fascia Check'][1] is True:
                self.st_results.append('There are 2 pieces of Fascia for the A and C walls. Both are at {} in. for each'
                                       ' wall'.format(self.studio.fascia_dict['Side Fascia']))
                self.st_results.append('Their original length was more than 216 in.')
            else:
                self.st_results.append('There is one piece of Fascia at {:.0f} in. for the A Wall and one piece at '
                                       '{:.0f} for the C wall.'.format(self.studio.fascia_dict['Side Fascia'],
                                                                       self.studio.fascia_dict['Side Fascia']))

    def ca_results_message(self):
        """
        This method displays all the results to the ca_text_browser object.
        :return:
        """
        self.ca_results.append('The A side pitch is: {}/12.'
                               .format(LSTKC.pitch_estimate(12 * tan(self.cathedral.a_pitch))))
        self.ca_results.append('The C side pitch is: {}/12.'
                               .format(LSTKC.pitch_estimate(12 * tan(self.cathedral.c_pitch))))
        self.ca_results.append('The peak height is {} in.'.format(LSTKC.sixteenth(self.cathedral.f_peak)))
        self.ca_results.append('The A Wall height is {} in.'.format(LSTKC.sixteenth(self.cathedral.a_unpitched_wall_h)))
        self.ca_results.append('The C Wall height is {} in.'.format(LSTKC.sixteenth(self.cathedral.c_unpitched_wall_h)))
        self.ca_results.append('The A side soffit height is {} in.'.format(LSTKC.sixteenth(self.cathedral.a_soffit)))
        self.ca_results.append('The C side soffit height is {} in.'.format(LSTKC.sixteenth(self.cathedral.c_soffit)))
        self.ca_results.append('The A side drip edge is at {} in.'.format(LSTKC.sixteenth(self.cathedral.a_drip_edge)))
        self.ca_results.append('The C side drip edge is at {} in.'.format(LSTKC.sixteenth(self.cathedral.c_drip_edge)))
        self.ca_results.append('The maximum height is {} in.'.format(LSTKC.sixteenth(self.cathedral.max_h)))
        self.ca_results.append('This configuration will need {} A side roof panels.'
                               .format(self.cathedral.a_roof_panel_dict['Roof Panels']))
        self.ca_results.append('The length of each A side panel should be {:.0f} in.'
                               .format(self.cathedral.a_panel_length_dict['Panel Length']))
        if self.cathedral.a_panel_length_dict['Max Length Check'] is True:
            self.ca_results.append('The A side panels were divided in half because they were more than 24ft.')
        self.ca_results.append('This configuration will need {} C side roof panels.'
                               .format(self.cathedral.c_roof_panel_dict['Roof Panels']))
        self.ca_results.append('The length of each C side panel should be {:.0f} in.'
                               .format(self.cathedral.c_panel_length_dict['Panel Length']))
        if self.cathedral.c_panel_length_dict['Max Length Check'] is True:
            self.ca_results.append('The C side panels were divided in half because they were more than 24ft.')
        self.ca_results.append('The total number of roof panels is {:.0f}.'
                               .format(self.cathedral.a_roof_panel_dict['Roof Panels'] +
                                       self.cathedral.c_roof_panel_dict['Roof Panels']))
        self.ca_results.append('The total roof sq. ft. is {:.0f} ft^2.'
                               .format((self.cathedral.a_roof_panel_dict['Roof Area'] +
                                        self.cathedral.c_roof_panel_dict['Roof Area']) / 144))
        self.ca_results.append('You will need {} boxes of Armstrong Ceiling Panels.'
                               .format(self.cathedral.a_armstrong_panels + self.cathedral.c_armstrong_panels))
        self.ca_results.append('The overhang on A Wall is {:.0f} in.'.format(self.cathedral.overhang))
        self.ca_results.append('The overhang on C Wall is {:.0f} in.'.format(self.cathedral.overhang))
        self.ca_results.append('The overhang on B Wall is {:.0f} in.'
                               .format(self.cathedral.a_roof_panel_dict['Side Overhang']))
        if self.cathedral.a_roof_panel_dict['Overhang Short Check'] is True:
            self.ca_results.append('The overhang on the sides are TOO SHORT!')
        if self.cathedral.a_hang_rail_dict['Hang Rail Check'] is True:
            self.ca_results.append('There are 2 pairs of hang rails at {} in. each on the A wall.'
                                   .format(self.cathedral.a_hang_rail_dict['Hang Rail']))
            self.ca_results.append('They were divided in half because the original length was longer than 216".')
        else:
            self.ca_results.append('There is 1 pair of hang rails at {:.0f} in. on the A wall'
                                   .format(self.cathedral.a_hang_rail_dict['Hang Rail']))
        if self.cathedral.c_hang_rail_dict['Hang Rail Check'] is True:
            self.ca_results.append('There are 2 pairs of hang rails at {} in. each on the C wall.'
                                   .format(self.cathedral.a_hang_rail_dict['Hang Rail']))
            self.ca_results.append('They were divided in half because the original length was longer than 216".')
        else:
            self.ca_results.append('There is 1 pair of hang rails at {:.0f} in. on the C wall'
                                   .format(self.cathedral.a_hang_rail_dict['Hang Rail']))
        if self.ca_fascia.isChecked():
            if self.cathedral.a_fascia_dict['Fascia Check'][0] is True:
                self.ca_results.append('There are 2 pieces of Fascia at {} in. each for the A wall'
                                       .format(self.cathedral.a_fascia_dict['Wall Fascia']))
                self.ca_results.append('Their original length was more than 216 in. so they were cut in half.')
            else:
                self.ca_results.append('There is 1 pieces of Fascia at {:.0f} in. for the A wall'
                                       .format(self.cathedral.a_fascia_dict['Wall Fascia']))
            if self.cathedral.c_fascia_dict['Fascia Check'][0] is True:
                self.ca_results.append('There are 2 pieces of Fascia at {} in. each for the C wall'
                                       .format(self.cathedral.c_fascia_dict['Wall Fascia']))
                self.ca_results.append('Their original length was more than 216 in. so they were cut in half.')
            else:
                self.ca_results.append('There is 1 pieces of Fascia at {:.0f} in. for the C wall'
                                       .format(self.cathedral.c_fascia_dict['Wall Fascia']))
            if self.cathedral.a_fascia_dict['Fascia Check'][1] is True:
                self.ca_results.append('There are 2 pieces of Fascia for the A side B Wall. Both are at {} in. each'
                                       .format(self.cathedral.a_fascia_dict['Side Fascia']))
                self.ca_results.append('Their original length was more than 216 in.')
            else:
                self.ca_results.append('There is 1 pieces of Fascia for the A side B Wall at {:.0f} in.'
                                       .format(self.cathedral.a_fascia_dict['Side Fascia']))
            if self.cathedral.c_fascia_dict['Fascia Check'][1] is True:
                self.ca_results.append('There are 2 pieces of Fascia for the C side B Wall. Both are at {} in. each'
                                       .format(self.cathedral.c_fascia_dict['Side Fascia']))
                self.ca_results.append('Their original length was more than 216 in.')
            else:
                self.ca_results.append('There is 1 pieces of Fascia for the C side B Wall at {:.0f} in.'
                                       .format(self.cathedral.c_fascia_dict['Side Fascia']))

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
            self.input_errors('Overhang')
        if self.st_awall_edit.text() == '':
            self.input_errors('A Wall')
        if self.st_bwall_edit.text() == '':
            self.input_errors('B Wall')
        if self.st_cwall_edit.text() == '':
            self.input_errors('C Wall')

    def ca_common_errors(self):
        """
        This method is displays error messages for the four common input boxes: Overhang, A Wall, B Wall, and C Wall.
        :return:
        """
        if self.ca_overhang_edit.text() == '':
            self.input_errors('Overhang')
        if self.ca_awall_edit.text() == '':
            self.input_errors('A Wall')
        if self.ca_bwall_edit.text() == '':
            self.input_errors('B Wall')
        if self.ca_cwall_edit.text() == '':
            self.input_errors('C Wall')

    def st_calcbutton(self):
        """
        This method checks for missing input upon pressing the "Calculate" button. It then calls st_scenario_calc to
        calculate the quatities based on scenario selected.
        :return: dict
        """
        self.st_results.clear()
        self.st_common_errors()
        self.st_results.setText('Now listing results.')
        # self.st_results.setText('This is a bug!')
        self.st_scenario_calc()
        if self.st_scenario1_radio.isChecked():
            if self.st_pitch_edit.text() == '':
                self.input_errors('Pitch')
            elif self.st_bwallheight_edit.text() == '':
                self.input_errors('B Wall Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given B wall height and pitch...')
                self.st_results_message()
        elif self.st_scenario2_radio.isChecked():
            if self.st_peak_edit.text() == '':
                self.input_errors('Peak Height')
            elif self.st_bwallheight_edit.text() == '':
                self.input_errors('B Wall Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given wall height and peak height...')
                self.st_results_message()
        elif self.st_scenario3_radio.isChecked():
            if self.st_pitch_edit.text() == '':
                self.input_errors('pitch')
            elif self.st_max_edit.text() == '':
                self.input_errors('Max Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given max height and pitch...')
                self.st_results_message()
        elif self.st_scenario4_radio.isChecked():
            if self.st_soffit_edit.text() == '':
                self.input_errors('Soffit Height')
            elif self.st_peak_edit.text() == '':
                self.input_errors('Peak Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given soffit heights and peak height...')
                self.st_results_message()
        elif self.st_scenario5_radio.isChecked():
            if self.st_pitch_edit.text() == '':
                self.input_errors('pitch')
            elif self.st_soffit_edit.text() == '':
                self.input_errors('Soffit Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given soffit heights and pitch...')
                self.st_results_message()
        elif self.st_scenario6_radio.isChecked():
            if self.st_drip_edit.text() == '':
                self.input_errors('Drip Edge Height')
            elif self.st_peak_edit.text() == '':
                self.input_errors('Peak Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given drip edge and peak height...')
                self.st_results_message()
        elif self.st_scenario7_radio.isChecked():
            if self.st_pitch_edit.text() == '':
                self.input_errors('pitch')
            elif self.st_drip_edit.text() == '':
                self.input_errors('Drip Edge Height')
            else:
                self.st_results.append('*===================*')
                self.st_results.append('Given drip edge and pitch...')
                self.st_results_message()
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
        self.ca_scenario_calc()
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
                self.ca_results_message()
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
                self.ca_results_message()
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
                self.ca_results_message()
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
                self.ca_results_message()
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
                self.ca_results_message()
        elif self.ca_scenario6_radio.isChecked():
            if self.ca_peak_edit.text() == '':
                self.input_errors('Peak Height')
            elif self.ca_drip_edit.text() == '':
                self.input_errors('Drip Edge Height')
            else:
                self.ca_results.append('*===================*')
                self.ca_results.append('Given drip edge and peak height...')
                self.ca_results_message()
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
                self.ca_results_message()
        else:
            QMessageBox.about(self.window, 'Select a Scenario!', 'No scenarios selected!')


if __name__ == '__main__':
    current_dir = Path.cwd()
    # Set up logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:[%(name)s:%(lineno)s - %(funcName)10s() ]:[%(levelname)s]: '
                                  '%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    file_handler = logging.FileHandler('LS Toolkit.log', mode='w')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Define function to import external files when using PyInstaller.
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os_path.abspath(".")

        return os_path.join(base_path, relative_path)


    mainwindow = resource_path('LivingspaceToolkitMain.ui')
    app = QApplication(sys.argv)
    form = Form(resource_path('LivingspaceToolkitMain.ui'))
    sys.exit(app.exec())
