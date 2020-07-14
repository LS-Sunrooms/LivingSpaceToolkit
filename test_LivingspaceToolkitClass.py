#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from math import atan, radians, tan
import LivingspaceToolkitClass
from LivingspaceToolkitClass import sixteenth, pitch_estimate
import Units as EU


@pytest.fixture
def studio_setup():
    studio = []
    for i in LivingspaceToolkitClass.end_cuts:
        studio.append(LivingspaceToolkitClass.Studio(12, 168, 162, 168, 10.25, i))
    return studio


@pytest.fixture
def cathedral_setup():
    cathedral = []
    for i in LivingspaceToolkitClass.end_cuts:
        cathedral.append(LivingspaceToolkitClass.Cathedral(12, 168, 162, 168, 10.25, i))
    return cathedral


def test_angled():
    pitch = atan(5 / 12)
    thickness = 10.25
    assert LivingspaceToolkitClass.angled(pitch, thickness) == 11.104166666666668


def test_pitch_input():
    ratio = EU.EngineeringUnits('5"', u_type='length')
    angle = EU.EngineeringUnits('24deg', u_type='angle')
    assert LivingspaceToolkitClass.pitch_input(ratio) == atan(5 / 12)
    assert LivingspaceToolkitClass.pitch_input(angle) == radians(24)


def test_pitch_estimate():
    assert pitch_estimate(5.0) == 5.0
    assert pitch_estimate(5.1) == 5.0
    assert pitch_estimate(5.4) == 5.5
    assert pitch_estimate(5.5) == 5.5
    assert pitch_estimate(5.6) == 5.5
    assert pitch_estimate(5.9) == 6.0
    assert pitch_estimate(6.0) == 6.0


def test_sixteenth():
    assert sixteenth(9 / 32) == 4 / 16
    assert sixteenth(10 / 32) == 5 / 16
    assert sixteenth(11 / 32) == 6 / 16
    assert sixteenth(0.37) == 6 / 16


def test_studio_calculate_sunroom(studio_setup):
    pitch = atan(5 / 12)
    studio_setup[0].pitch = pitch
    studio_setup[0].unpitched_wall = 95
    studio_setup[0].pitched_wall = 168
    studio_setup[0].calculate_sunroom()
    assert studio_setup[0].panel_length_dict['Panel Length'] == 204
    assert studio_setup[0].panel_length_dict['Max Length Check'] is False
    assert studio_setup[0].panel_length_dict['Panel Tolerance'] is False
    assert studio_setup[0].roof_panel_dict['Roof Area'] == 39168
    assert studio_setup[0].roof_panel_dict['Roof Panels'] == 6
    assert studio_setup[0].roof_panel_dict['Side Overhang'] == 12
    assert studio_setup[0].roof_panel_dict['Overhang Short Check'] is False
    assert studio_setup[0].roof_panel_dict['Overhang Long Check'] is False
    assert studio_setup[0].hang_rail_dict['Hang Rail'] == 192.0
    assert studio_setup[0].hang_rail_dict['Hang Rail Check'] is False
    assert studio_setup[0].fascia_dict['Wall Fascia'] == 204
    assert studio_setup[0].fascia_dict['Side Fascia'] == 210
    assert studio_setup[0].fascia_dict['Fascia Check'] == [False, False]
    assert studio_setup[0].armstrong_panels == 8


def test_studio_scenario1(studio_setup):
    pitch = atan(5 / 12)
    studio_setup[0].wall_height_pitch(pitch, 95)
    studio_setup[1].wall_height_pitch(pitch, 95)
    assert pitch_estimate(tan(studio_setup[0].pitch) * 12) == 5.0
    assert sixteenth(studio_setup[0].peak) == 165.0
    assert sixteenth(studio_setup[0].drip_edge) == 99.4375
    assert sixteenth(studio_setup[1].drip_edge) == 101.125
    assert sixteenth(studio_setup[0].max_h) == 176.125
    assert sixteenth(studio_setup[0].soffit_wall) == 162.0
    assert sixteenth(studio_setup[0].soffit) == 90.0
    assert sixteenth(studio_setup[0].unpitched_wall) == 95.0


def test_studio_scenario2(studio_setup):
    studio_setup[0].wall_height_peak_height(95, 165)
    studio_setup[1].wall_height_peak_height(95, 165)
    assert pitch_estimate(tan(studio_setup[0].pitch)*12) == 5.0
    assert sixteenth(studio_setup[0].peak) == 165.0
    assert sixteenth(studio_setup[0].drip_edge) == 99.4375
    assert sixteenth(studio_setup[1].drip_edge) == 101.125
    assert sixteenth(studio_setup[0].max_h) == 176.125
    assert sixteenth(studio_setup[0].soffit_wall) == 162.0
    assert sixteenth(studio_setup[0].soffit) == 90.0
    assert sixteenth(studio_setup[0].unpitched_wall) == 95.0


def test_studio_scenario3(studio_setup):
    pitch = atan(5 / 12)
    studio_setup[0].max_height_pitch(pitch, 176.125)
    studio_setup[1].max_height_pitch(pitch, 176.125)
    assert pitch_estimate(tan(studio_setup[0].pitch) * 12) == 5.0
    assert sixteenth(studio_setup[0].peak) == 165.0
    assert sixteenth(studio_setup[0].drip_edge) == 99.5
    assert sixteenth(studio_setup[1].drip_edge) == 101.125
    assert sixteenth(studio_setup[0].max_h) == 176.125
    assert sixteenth(studio_setup[0].soffit_wall) == 162.0
    assert sixteenth(studio_setup[0].soffit) == 90.0
    assert sixteenth(studio_setup[0].unpitched_wall) == 95.0


def test_studio_scenario4(studio_setup):
    studio_setup[0].soffit_height_peak_height(165, 90)
    studio_setup[1].soffit_height_peak_height(165, 90)
    assert pitch_estimate(tan(studio_setup[0].pitch) * 12) == 5.0
    assert sixteenth(studio_setup[0].peak) == 165.0
    assert sixteenth(studio_setup[0].drip_edge) == 99.4375
    assert sixteenth(studio_setup[1].drip_edge) == 101.125
    assert sixteenth(studio_setup[0].max_h) == 176.125
    assert sixteenth(studio_setup[0].soffit_wall) == 162.0
    assert sixteenth(studio_setup[0].soffit) == 90.0
    assert sixteenth(studio_setup[0].unpitched_wall) == 95.0


def test_studio_scenario5(studio_setup):
    pitch = atan(5 / 12)
    studio_setup[0].soffit_height_pitch(pitch, 90)
    studio_setup[1].soffit_height_pitch(pitch, 90)
    assert pitch_estimate(tan(studio_setup[0].pitch) * 12) == 5.0
    assert sixteenth(studio_setup[0].peak) == 165.0
    assert sixteenth(studio_setup[0].drip_edge) == 99.4375
    assert sixteenth(studio_setup[1].drip_edge) == 101.125
    assert sixteenth(studio_setup[0].max_h) == 176.125
    assert sixteenth(studio_setup[0].soffit_wall) == 162.0
    assert sixteenth(studio_setup[0].soffit) == 90.0
    assert sixteenth(studio_setup[0].unpitched_wall) == 95.0


def test_studio_scenario6(studio_setup):
    studio_setup[0].drip_edge_peak_height(101.125, 165)
    studio_setup[1].drip_edge_peak_height(101.125, 165)
    assert pitch_estimate(tan(studio_setup[0].pitch) * 12) == 5.0
    assert sixteenth(studio_setup[0].peak) == 165.0
    assert sixteenth(studio_setup[0].drip_edge) == 101.125
    assert sixteenth(studio_setup[1].drip_edge) == 101.125
    assert sixteenth(studio_setup[0].max_h) == 176.0625
    assert sixteenth(studio_setup[1].max_h) == 176.125
    assert sixteenth(studio_setup[0].soffit_wall) == 162.0
    assert sixteenth(studio_setup[0].soffit) == 91.625
    assert sixteenth(studio_setup[1].soffit) == 90
    assert sixteenth(studio_setup[0].unpitched_wall) == 96.5625
    assert sixteenth(studio_setup[1].unpitched_wall) == 95


def test_studio_scenario7(studio_setup):
    pitch = atan(5 / 12)
    studio_setup[0].drip_edge_pitch(101.125, pitch)
    studio_setup[1].drip_edge_pitch(101.125, pitch)
    assert pitch_estimate(tan(studio_setup[0].pitch) * 12) == 5.0
    assert sixteenth(studio_setup[0].peak) == 165.0
    assert sixteenth(studio_setup[0].drip_edge) == 99.5
    assert sixteenth(studio_setup[1].drip_edge) == 101.125
    assert sixteenth(studio_setup[0].max_h) == 176.125
    assert sixteenth(studio_setup[1].max_h) == 176.125
    assert sixteenth(studio_setup[0].soffit_wall) == 162.0
    assert sixteenth(studio_setup[0].soffit) == 90
    assert sixteenth(studio_setup[1].soffit) == 90
    assert sixteenth(studio_setup[0].unpitched_wall) == 95
    assert sixteenth(studio_setup[1].unpitched_wall) == 95


def test_cathedral_calculate_sunroom(cathedral_setup):
    a_pitch = atan(5 / 12)
    c_pitch = atan(5 / 12)
    cathedral_setup[0].a_pitch = a_pitch
    cathedral_setup[0].c_pitch = c_pitch
    cathedral_setup[0].a_pitched_wall = 81
    cathedral_setup[0].c_pitched_wall = 81
    cathedral_setup[0].calculate_sunroom()
    assert cathedral_setup[0].a_panel_length_dict['Panel Length'] == 108
    assert cathedral_setup[0].a_panel_length_dict['Max Length Check'] is False
    assert cathedral_setup[0].a_panel_length_dict['Panel Tolerance'] is False
    assert cathedral_setup[0].c_panel_length_dict['Panel Length'] == 108
    assert cathedral_setup[0].c_panel_length_dict['Max Length Check'] is False
    assert cathedral_setup[0].c_panel_length_dict['Panel Tolerance'] is False
    assert cathedral_setup[0].a_roof_panel_dict['Roof Area'] == 20736
    assert cathedral_setup[0].a_roof_panel_dict['Roof Panels'] == 6
    assert cathedral_setup[0].a_roof_panel_dict['Side Overhang'] == 24
    assert cathedral_setup[0].a_roof_panel_dict['Overhang Short Check'] is False
    assert cathedral_setup[0].a_roof_panel_dict['Overhang Long Check'] is True
    assert cathedral_setup[0].c_roof_panel_dict['Roof Area'] == 20736
    assert cathedral_setup[0].c_roof_panel_dict['Roof Panels'] == 6
    assert cathedral_setup[0].c_roof_panel_dict['Side Overhang'] == 24
    assert cathedral_setup[0].c_roof_panel_dict['Overhang Short Check'] is False
    assert cathedral_setup[0].c_roof_panel_dict['Overhang Long Check'] is True
    assert cathedral_setup[0].a_hang_rail_dict['Hang Rail'] == 108
    assert cathedral_setup[0].a_hang_rail_dict['Hang Rail Check'] is False
    assert cathedral_setup[0].c_hang_rail_dict['Hang Rail'] == 108
    assert cathedral_setup[0].c_hang_rail_dict['Hang Rail Check'] is False
    assert cathedral_setup[0].a_fascia_dict['Wall Fascia'] == 198
    assert cathedral_setup[0].a_fascia_dict['Side Fascia'] == 114
    assert cathedral_setup[0].a_fascia_dict['Fascia Check'] == [False, False]
    assert cathedral_setup[0].c_fascia_dict['Wall Fascia'] == 198
    assert cathedral_setup[0].c_fascia_dict['Side Fascia'] == 114
    assert cathedral_setup[0].c_fascia_dict['Fascia Check'] == [False, False]
    assert cathedral_setup[0].a_armstrong_panels == 4
    assert cathedral_setup[0].c_armstrong_panels == 4


def test_cathedral_scenario1(cathedral_setup):
    a_pitch = atan(5 / 12)
    c_pitch = atan(5 / 12)
    cathedral_setup[0].wall_height_pitch([a_pitch, c_pitch], [95, 95])
    cathedral_setup[1].wall_height_pitch([a_pitch, c_pitch], [95, 95])
    assert pitch_estimate(tan(cathedral_setup[0].a_pitch) * 12) == 5.0
    assert pitch_estimate(tan(cathedral_setup[0].c_pitch) * 12) == 5.0
    assert sixteenth(cathedral_setup[0].f_peak) == 128.0625
    assert sixteenth(cathedral_setup[0].max_h) == 139.875
    assert sixteenth(cathedral_setup[0].a_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[0].c_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[1].a_drip_edge) == 101.125
    assert sixteenth(cathedral_setup[1].c_drip_edge) == 101.125
    assert sixteenth(cathedral_setup[0].a_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].c_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].a_unpitched_wall_h) == 95.0
    assert sixteenth(cathedral_setup[0].c_unpitched_wall_h) == 95.0


def test_cathedral_scenario2(cathedral_setup):
    cathedral_setup[0].wall_height_peak_height([95, 95], 128.0625)
    cathedral_setup[1].wall_height_peak_height([95, 95], 128.0625)
    assert pitch_estimate(tan(cathedral_setup[0].a_pitch) * 12) == 5.0
    assert pitch_estimate(tan(cathedral_setup[0].c_pitch) * 12) == 5.0
    assert sixteenth(cathedral_setup[0].f_peak) == 128.0625
    assert sixteenth(cathedral_setup[0].max_h) == 139.8125
    assert sixteenth(cathedral_setup[0].a_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[0].c_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[1].a_drip_edge) == 101.125
    assert sixteenth(cathedral_setup[1].c_drip_edge) == 101.125
    assert sixteenth(cathedral_setup[0].a_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].c_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].a_unpitched_wall_h) == 95.0
    assert sixteenth(cathedral_setup[0].c_unpitched_wall_h) == 95.0


def test_cathedral_scenario3(cathedral_setup):
    a_pitch = atan(5 / 12)
    c_pitch = atan(5 / 12)
    cathedral_setup[0].max_height_pitch([a_pitch, c_pitch], 139.875)
    cathedral_setup[1].max_height_pitch([a_pitch, c_pitch], 139.875)
    assert pitch_estimate(tan(cathedral_setup[0].a_pitch) * 12) == 5.0
    assert pitch_estimate(tan(cathedral_setup[0].c_pitch) * 12) == 5.0
    assert sixteenth(cathedral_setup[0].f_peak) == 128.125
    assert sixteenth(cathedral_setup[0].max_h) == 139.875
    assert sixteenth(cathedral_setup[0].a_drip_edge) == 99.5
    assert sixteenth(cathedral_setup[0].c_drip_edge) == 99.5
    assert sixteenth(cathedral_setup[1].a_drip_edge) == 101.125
    assert sixteenth(cathedral_setup[1].c_drip_edge) == 101.125
    assert sixteenth(cathedral_setup[0].a_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].c_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].a_unpitched_wall_h) == 95.0
    assert sixteenth(cathedral_setup[0].c_unpitched_wall_h) == 95.0


def test_cathedral_scenario4(cathedral_setup):
    cathedral_setup[0].soffit_height_peak_height(128.0625, [90, 90])
    cathedral_setup[1].soffit_height_peak_height(128.0625, [90, 90])
    assert pitch_estimate(tan(cathedral_setup[0].a_pitch) * 12) == 5.0
    assert pitch_estimate(tan(cathedral_setup[0].c_pitch) * 12) == 5.0
    assert sixteenth(cathedral_setup[0].f_peak) == 128.0625
    assert sixteenth(cathedral_setup[0].max_h) == 139.8125
    assert sixteenth(cathedral_setup[0].a_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[0].c_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[1].a_drip_edge) == 101.125
    assert sixteenth(cathedral_setup[1].c_drip_edge) == 101.125
    assert sixteenth(cathedral_setup[0].a_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].c_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].a_unpitched_wall_h) == 95.0
    assert sixteenth(cathedral_setup[0].c_unpitched_wall_h) == 95.0


def test_cathedral_scenario5(cathedral_setup):
    a_pitch = atan(5 / 12)
    c_pitch = atan(5 / 12)
    cathedral_setup[0].soffit_height_pitch([a_pitch, c_pitch], [90, 90])
    cathedral_setup[1].soffit_height_pitch([a_pitch, c_pitch], [90, 90])
    assert pitch_estimate(tan(cathedral_setup[0].a_pitch) * 12) == 5.0
    assert pitch_estimate(tan(cathedral_setup[0].c_pitch) * 12) == 5.0
    assert sixteenth(cathedral_setup[0].f_peak) == 128.0625
    assert sixteenth(cathedral_setup[0].max_h) == 139.875
    assert sixteenth(cathedral_setup[0].a_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[0].c_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[1].a_drip_edge) == 101.125
    assert sixteenth(cathedral_setup[1].c_drip_edge) == 101.125
    assert sixteenth(cathedral_setup[0].a_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].c_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].a_unpitched_wall_h) == 95.0
    assert sixteenth(cathedral_setup[0].c_unpitched_wall_h) == 95.0


def test_cathedral_scenario6(cathedral_setup):
    cathedral_setup[0].drip_edge_peak_height(99.4375, 128.0625)
    cathedral_setup[1].drip_edge_peak_height(99.4375, 128.0625)
    assert pitch_estimate(tan(cathedral_setup[0].a_pitch) * 12) == 5.0
    assert pitch_estimate(tan(cathedral_setup[0].c_pitch) * 12) == 5.0
    assert sixteenth(cathedral_setup[0].f_peak) == 128.0625
    assert sixteenth(cathedral_setup[0].max_h) == 139.875
    assert sixteenth(cathedral_setup[1].max_h) == 139.9375
    assert sixteenth(cathedral_setup[0].a_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[0].c_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[0].a_soffit) == 90.0
    assert sixteenth(cathedral_setup[0].c_soffit) == 90.0
    assert sixteenth(cathedral_setup[1].a_soffit) == 88.25
    assert sixteenth(cathedral_setup[1].c_soffit) == 88.25
    assert sixteenth(cathedral_setup[0].a_unpitched_wall_h) == 95
    assert sixteenth(cathedral_setup[0].c_unpitched_wall_h) == 95
    assert sixteenth(cathedral_setup[1].a_unpitched_wall_h) == 93.5
    assert sixteenth(cathedral_setup[1].c_unpitched_wall_h) == 93.5


def test_cathedral_scenario7(cathedral_setup):
    a_pitch = atan(5 / 12)
    c_pitch = atan(5 / 12)
    cathedral_setup[0].drip_edge_pitch(99.4375, [a_pitch, c_pitch])
    cathedral_setup[1].drip_edge_pitch(99.4375, [a_pitch, c_pitch])
    assert pitch_estimate(tan(cathedral_setup[0].a_pitch) * 12) == 5.0
    assert pitch_estimate(tan(cathedral_setup[0].c_pitch) * 12) == 5.0
    assert sixteenth(cathedral_setup[0].f_peak) == 126.375
    assert sixteenth(cathedral_setup[0].max_h) == 138.1875
    assert sixteenth(cathedral_setup[0].a_drip_edge) == 97.8125
    assert sixteenth(cathedral_setup[0].c_drip_edge) == 97.8125
    assert sixteenth(cathedral_setup[1].a_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[1].c_drip_edge) == 99.4375
    assert sixteenth(cathedral_setup[0].a_soffit) == 88.3125
    assert sixteenth(cathedral_setup[0].c_soffit) == 88.3125
    assert sixteenth(cathedral_setup[0].a_unpitched_wall_h) == 93.3125
    assert sixteenth(cathedral_setup[0].c_unpitched_wall_h) == 93.3125
