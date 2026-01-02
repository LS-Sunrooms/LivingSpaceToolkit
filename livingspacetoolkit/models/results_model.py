from math import tan
from livingspacetoolkit.config.log_config import logger
from livingspacetoolkit.lib.toolkit_enums import SunroomType, Scenario, SunroomSide, LengthType
from livingspacetoolkit.models import ToolkitStateModel, SunroomModel
from livingspacetoolkit.utils.helpers import to_nice_number



def generate_results(toolkit_state: ToolkitStateModel, sunroom_model: SunroomModel) -> str:
    """This function is used to generate the results display text."""
    results_text = 'Now listing results.\n'
    results_text += '*===================*\n'
    match toolkit_state.scenario:
        case Scenario.WALL_HEIGHT_PITCH:
            results_text += 'Given wall height and pitch...\n'
        case Scenario.WALL_HEIGHT_PEAK_HEIGHT:
            results_text += 'Given wall height and peak height...\n'
        case Scenario.MAX_HEIGHT_PITCH:
            results_text += 'Given max height and pitch...\n'
        case Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT:
            results_text += 'Given soffit heights and peak height...\n'
        case Scenario.SOFFIT_HEIGHT_PITCH:
            results_text += 'Given soffit heights and pitch...\n'
        case Scenario.DRIP_EDGE_PEAK_HEIGHT:
            results_text += 'Given drip edge and peak height...\n'
        case Scenario.DRIP_EDGE_PITCH:
            results_text += 'Given drip edge and pitch...\n'
    match toolkit_state.sunroom_type:
        case SunroomType.STUDIO:
            pitch = 12 * tan(toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value)
            peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
            max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
            soffit = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length
            drip_edge = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
            b_wall_height = toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length
            gable_wall = sunroom_model.gable_wall[SunroomSide.B_SIDE].length
            roof_panels_b_side = sunroom_model.roof_panels[SunroomSide.B_SIDE]
            panel_length_b_side = sunroom_model.panel_length[SunroomSide.B_SIDE].length
            roof_area = sunroom_model.roof_area[SunroomSide.B_SIDE]
            armstrong = sunroom_model.armstrong_panels
            overhang_b_side = toolkit_state.overhang.length
            overhang_a_side = sunroom_model.roof_overhang[SunroomSide.A_SIDE]['value'].length
            hang_rails_b_side = sunroom_model.hang_rails[SunroomSide.B_SIDE]['value'].length
            fascia_a_side = sunroom_model.fascia[SunroomSide.A_SIDE]['value'][0].length
            fascia_b_side = sunroom_model.fascia[SunroomSide.B_SIDE]['value'][0].length
            fascia_c_side = sunroom_model.fascia[SunroomSide.C_SIDE]['value'][0].length
            results_text += 'The pitch is: {}/12.\n'.format(to_nice_number(pitch, 2))
            results_text += 'The peak height is {} in.\n'.format(to_nice_number(peak, 16))
            results_text += 'The soffit height is {} in.\n'.format(to_nice_number(soffit, 16))
            results_text += 'The drip edge is at {} in.\n'.format(to_nice_number(drip_edge, 16))
            results_text += 'The maximum height is {} in.\n'.format(to_nice_number(max_height, 16))
            results_text += 'The A and C Wall heights are {} in.\n'.format(to_nice_number(gable_wall, 16))
            results_text += 'The B Wall height is {} in.\n'.format(to_nice_number(b_wall_height, 16))
            results_text += 'This configuration will need {} roof panels.\n'.format(roof_panels_b_side)
            results_text += 'The length of each panel should be {:.0f} in.\n'.format(panel_length_b_side)
            if sunroom_model.max_panel_length[SunroomSide.B_SIDE]:
                results_text += 'These panels were divided in half because they were more than 24ft.\n'
            results_text += 'The roof sq. ft. is {:.0f} ft^2.\n'.format(roof_area)
            results_text += 'You will need {:.0f} boxes of Armstrong Ceiling Panels.\n'.format(armstrong)
            results_text += 'The overhang on B Wall is {:.0f} in.\n'.format(overhang_b_side)
            results_text += 'The overhang on A and C Walls are {:.0f} in.\n'.format(overhang_a_side)
            if sunroom_model.roof_overhang[SunroomSide.A_SIDE]['short_check']:
                results_text += 'The overhang on the sides are TOO SHORT!\n'
            if sunroom_model.hang_rails[SunroomSide.B_SIDE]['max_length']:
                results_text += 'There are 2 pairs of hang rails at {} in. each.\n'.format(hang_rails_b_side)
                results_text += 'They were divided in half because the original length was longer than 216 in.\n'
            else:
                results_text += 'There is 1 pair of hang rails at {:.0f} in. each.\n'.format(hang_rails_b_side)
            if toolkit_state.fascia:
                if sunroom_model.fascia[SunroomSide.B_SIDE]['max_length']:
                    results_text += 'There are 2 pieces of Fascia at {} in. each for the B wall\n'.format(fascia_b_side)
                    results_text += 'Their original length was more than 216 in. so they were cut in half.\n'
                else:
                    results_text += 'There is 1 piece of Fascia at {:.0f} in. for the B wall.\n'.format(fascia_b_side)
                if sunroom_model.fascia[SunroomSide.A_SIDE]['max_length']:
                    results_text += ('There are 2 pieces of Fascia for the A and C walls. Both are at {} in. for each '
                                     'wall').format(fascia_a_side)
                    results_text += 'Their original length was more than 216 in.\n'
                else:
                    results_text += ('There is one piece of Fascia at {:.0f} in. for the A Wall and one piece at {:.0f} '
                                     'for the C wall.').format(fascia_a_side,
                                                               fascia_c_side)
        case SunroomType.CATHEDRAL:
            pitch_a_side = 12 * tan(toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value)
            pitch_c_side = 12 * tan(toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value)
            peak = toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length
            max_height = toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length
            soffit_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length
            soffit_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length
            drip_edge_a_side = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
            drip_edge_c_side = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length
            a_wall_height = toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length
            c_wall_height = toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length
            roof_panels_a_side = sunroom_model.roof_panels[SunroomSide.A_SIDE]
            roof_panels_c_side = sunroom_model.roof_panels[SunroomSide.C_SIDE]
            panel_length_a_side = sunroom_model.panel_length[SunroomSide.A_SIDE].length
            panel_length_c_side = sunroom_model.panel_length[SunroomSide.C_SIDE].length
            roof_area = sunroom_model.roof_area[SunroomSide.A_SIDE] + sunroom_model.roof_area[SunroomSide.C_SIDE]
            armstrong = sunroom_model.armstrong_panels
            overhang_a_side = toolkit_state.overhang.length
            overhang_b_side = sunroom_model.roof_overhang[SunroomSide.B_SIDE]['value'].length
            overhang_c_side = toolkit_state.overhang.length
            hang_rails_a_side = sunroom_model.hang_rails[SunroomSide.A_SIDE]['value'].length
            hang_rails_c_side = sunroom_model.hang_rails[SunroomSide.C_SIDE]['value'].length
            fascia_a_side = sunroom_model.fascia[SunroomSide.A_SIDE]['value'][0].length
            fascia_ab_side = sunroom_model.fascia[SunroomSide.B_SIDE]['value'][0].length
            fascia_cb_side = sunroom_model.fascia[SunroomSide.B_SIDE]['value'][1].length
            fascia_c_side = sunroom_model.fascia[SunroomSide.C_SIDE]['value'][0].length
            results_text += 'The A side pitch is: {}/12.\n'.format(to_nice_number(pitch_a_side, 2))
            results_text += 'The C side pitch is: {}/12.\n'.format(to_nice_number(pitch_c_side, 2))
            results_text += 'The peak height is {} in.\n'.format(to_nice_number(peak, 16))
            results_text += 'The A Wall height is {} in.\n'.format(to_nice_number(a_wall_height, 16))
            results_text += 'The C Wall height is {} in.\n'.format(to_nice_number(c_wall_height, 16))
            results_text += 'The A side soffit height is {} in.\n'.format(to_nice_number(soffit_a_side, 16))
            results_text += 'The C side soffit height is {} in.\n'.format(to_nice_number(soffit_c_side, 16))
            results_text += 'The A side drip edge is at {} in.\n'.format(to_nice_number(drip_edge_a_side, 16))
            results_text += 'The C side drip edge is at {} in.\n'.format(to_nice_number(drip_edge_c_side, 16))
            results_text += 'The maximum height is {} in.\n'.format(to_nice_number(max_height, 16))
            results_text += 'This configuration will need {} A side roof panels.\n'.format(roof_panels_a_side)
            results_text += 'The length of each A side panel should be {:.0f} in.\n'.format(panel_length_a_side)
            if sunroom_model.max_panel_length[SunroomSide.A_SIDE]:
                results_text += 'The A side panels were divided in half because they were more than 24ft.\n'
            results_text += 'This configuration will need {} C side roof panels.\n'.format(roof_panels_c_side)
            results_text += 'The length of each C side panel should be {:.0f} in.\n'.format(panel_length_c_side)
            if sunroom_model.max_panel_length[SunroomSide.C_SIDE]:
                results_text += 'The A side panels were divided in half because they were more than 24ft.\n'
            results_text += 'The total number of roof panels is {:.0f}.\n'.format(roof_panels_a_side + roof_panels_c_side)
            results_text += 'The total roof sq. ft. is {:.0f} ft^2.\n'.format(roof_area)
            results_text += 'You will need {} boxes of Armstrong Ceiling Panels.\n'.format(armstrong)
            results_text += 'The overhang on A Wall is {:.0f} in.\n'.format(overhang_a_side)
            results_text += 'The overhang on C Wall is {:.0f} in.\n'.format(overhang_c_side)
            results_text += 'The overhang on B Wall is {:.0f} in.\n'.format(overhang_b_side)
            if sunroom_model.roof_overhang[SunroomSide.B_SIDE]['short_check']:
                results_text += 'The overhang on the sides are TOO SHORT!\n'
            if sunroom_model.hang_rails[SunroomSide.A_SIDE]['max_length']:
                results_text += 'There are 2 pairs of hang rails at {} in. each on the A wall.\n'.format(hang_rails_a_side)
                results_text += 'They were divided in half because the original length was longer than 216".\n'
            else:
                results_text += 'There is 1 pair of hang rails at {:.0f} in. on the A wall\n'.format(hang_rails_a_side)
            if sunroom_model.hang_rails[SunroomSide.C_SIDE]['max_length']:
                results_text += 'There are 2 pairs of hang rails at {} in. each on the C wall.\n'.format(hang_rails_c_side)
                results_text += 'They were divided in half because the original length was longer than 216".\n'
            else:
                results_text += 'There is 1 pair of hang rails at {:.0f} in. on the C wall\n'.format(hang_rails_c_side)
            if toolkit_state.fascia:
                if sunroom_model.fascia[SunroomSide.A_SIDE]['max_length']:
                    results_text += 'There are 2 pieces of Fascia at {} in. each for the A wall\n'.format(fascia_a_side)
                    results_text += 'Their original length was more than 216 in. so they were cut in half.\n'
                else:
                    results_text += 'There is 1 pieces of Fascia at {:.0f} in. for the A wall\n'.format(fascia_a_side)
                if sunroom_model.fascia[SunroomSide.C_SIDE]['max_length']:
                    results_text += 'There are 2 pieces of Fascia at {} in. each for the C wall\n'.format(fascia_c_side)
                    results_text += 'Their original length was more than 216 in. so they were cut in half.\n'
                else:
                    results_text += 'There is 1 pieces of Fascia at {:.0f} in. for the C wall\n'.format(fascia_c_side)
                if sunroom_model.fascia[SunroomSide.B_SIDE]['max_length']:
                    results_text += 'There are 2 pieces of Fascia for the A side B Wall. Both are at {} in. each\n'.format(fascia_ab_side)
                    results_text += 'Their original length was more than 216 in.\n'
                else:
                    results_text += 'There is 1 pieces of Fascia for the A side B Wall at {:.0f} in.\n'.format(fascia_ab_side)
                if sunroom_model.fascia[SunroomSide.B_SIDE]['max_length']:
                    results_text += 'There are 2 pieces of Fascia for the C side B Wall. Both are at {} in. each\n'.format(fascia_cb_side)
                    results_text += 'Their original length was more than 216 in.'
                else:
                    results_text += 'There is 1 pieces of Fascia for the C side B Wall at {:.0f} in.'.format(fascia_cb_side)
    return results_text