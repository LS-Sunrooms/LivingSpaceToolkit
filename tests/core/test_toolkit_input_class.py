import pytest

from livingspacetoolkit.lib import ToolkitLength, ToolkitPitch
from livingspacetoolkit.lib.toolkit_enums import LengthType, PitchType, RoofSide


class TestToolkitLength:

    length_equality_list = [
                                 (["12'", LengthType.THICKNESS], True),
                                 (["11'", LengthType.THICKNESS], False),
                                 (["12'", LengthType.OVERHANG], False)
                             ]

    @staticmethod
    def length_input_id(param: list):
        return f"length: {param[0][0]}, length_type: {param[0][1].name}"

    @pytest.mark.unit
    def test_getter_setter(self):
        # Arrange
        length = ToolkitLength(LengthType.OVERHANG)
        length.length = '15"'
        # Assert
        assert length.length_type == LengthType.OVERHANG
        assert length.length == 15

    @pytest.mark.unit
    @pytest.mark.parametrize("class_input", length_equality_list, ids=length_input_id)
    def test_equality(self, class_input: tuple[list, bool]):
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = "12'"

        length_2 = ToolkitLength(class_input[0][1])
        length_2.length = class_input[0][0]

        assert length_1 == class_input[1]