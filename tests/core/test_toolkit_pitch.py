import pytest
from math import atan, radians

from livingspacetoolkit.lib import ToolkitPitch
from livingspacetoolkit.lib.toolkit_enums import PitchType, SunroomSide


class TestToolkitPitch:

    pitch_equality_list = [
        (['30 deg', PitchType.ANGLE, SunroomSide.A_SIDE], True),
        (['30 deg', PitchType.ANGLE, SunroomSide.B_SIDE], False),
        (['45 deg', PitchType.ANGLE, SunroomSide.A_SIDE], False),
        (['5', PitchType.RATIO, SunroomSide.A_SIDE], False)
    ]

    @staticmethod
    def pitch_input_ids(param: list):
        return f"pitch: {param[0][0]}, pitch_type: {param[0][1].name}, roof_side: {param[0][2].name}"

    @pytest.mark.unit
    def test_getter_setter(self):
        # Arrange
        pitch = ToolkitPitch(PitchType.RATIO, SunroomSide.A_SIDE)
        # Act
        pitch.pitch_type = PitchType.ANGLE
        pitch.pitch_value = '30 deg'
        # Assert
        assert pitch.pitch_type == PitchType.ANGLE
        assert pitch.pitch_value == radians(30)
        assert pitch.modified == True

    @pytest.mark.unit
    @pytest.mark.parametrize("class_input", pitch_equality_list, ids=pitch_input_ids)
    def test_equality(self, class_input: tuple[list, bool]):
        # Arrange
        pitch_1 = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        pitch_1.pitch_value = '30 deg'
        # Act
        pitch_2 = ToolkitPitch(class_input[0][1], class_input[0][2])
        pitch_2.pitch_value = class_input[0][0]
        # Assert
        assert (pitch_1 == pitch_2) == class_input[1]

    @pytest.mark.unit
    def test_less_than(self):
        # Arrange
        pitch_1 = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        pitch_1.pitch_value = '45 deg'

        pitch_2 = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        pitch_2.pitch_value = '40 deg'

        assert pitch_2 < pitch_1

    @pytest.mark.unit
    def test_greater_than(self):
        # Arrange
        pitch_1 = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        pitch_1.pitch_value = '45 deg'

        pitch_2 = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        pitch_2.pitch_value = '40 deg'

        assert pitch_1 > pitch_2

    @pytest.mark.unit
    def test_add(self):
        # Arrange
        pitch_1 = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        pitch_1.pitch_value = '15 deg'

        pitch_2 = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        pitch_2.pitch_value = '10 deg'

        assert (pitch_1 + pitch_2) == (radians(15) + radians(10))

    @pytest.mark.unit
    def test_subtract(self):
        # Arrange
        pitch_1 = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        pitch_1.pitch_value = '15 deg'

        pitch_2 = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        pitch_2.pitch_value = '10 deg'

        assert (pitch_1 - pitch_2) == (radians(15) - radians(10))

    @pytest.mark.unit
    @pytest.mark.parametrize("actual, expected",
                             [
                                 ('30 deg', 30),
                                 ('30deg', 30),
                                 ('30', 30),
                                 (15, 15)
                             ])
    def test_angle_input(self, actual, expected):
        # Arrange
        pitch = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        # Act
        pitch.pitch_value = actual
        # Assert
        assert pitch.pitch_value == radians(expected)

    @pytest.mark.unit
    @pytest.mark.parametrize("actual, expected",
                             [
                                 ('5', 5),
                                 ('5.5', 5.5),
                                 ('5 1/2', 5.5),
                                 ('1/2', 0.5),
                                 (1/2, 0.5)
                             ])
    def test_ratio_input(self, actual, expected):
        # Arrange
        pitch = ToolkitPitch(PitchType.RATIO, SunroomSide.A_SIDE)
        # Act
        pitch.pitch_value = actual
        # Assert
        assert pitch.pitch_value == atan(expected/12)

    @pytest.mark.unit
    @pytest.mark.parametrize("variable",
                             [
                                 '-30deg',
                                 '-30 deg',
                                 '-30',
                                 -30
                             ])
    def test_negative_angle(self, variable):
        pitch = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        with pytest.raises(ValueError):
            pitch.pitch_value = variable

    @pytest.mark.unit
    def test_negative_ratio(self):
        pitch = ToolkitPitch(PitchType.RATIO, SunroomSide.A_SIDE)
        with pytest.raises(ValueError):
            pitch.pitch_value = '-5'

    @pytest.mark.unit
    def test_max_allowed_angle(self):
        pitch = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        with pytest.raises(ValueError):
            pitch.pitch_value = '60'

    @pytest.mark.unit
    def test_max_allowed_ratio(self):
        pitch = ToolkitPitch(PitchType.RATIO, SunroomSide.A_SIDE)
        with pytest.raises(ValueError):
            pitch.pitch_value = '21'

    @pytest.mark.unit
    @pytest.mark.parametrize("variable",
                             [
                                 'abc',
                                 '30d'
                             ])
    def test_invalid_angle(self, variable):
        pitch = ToolkitPitch(PitchType.ANGLE, SunroomSide.A_SIDE)
        with pytest.raises(ValueError):
            pitch.pitch_value = variable

    @pytest.mark.unit
    def test_invalid_ratio(self):
        pitch = ToolkitPitch(PitchType.RATIO, SunroomSide.A_SIDE)
        with pytest.raises(ValueError):
            pitch.pitch_value = 'abc'
