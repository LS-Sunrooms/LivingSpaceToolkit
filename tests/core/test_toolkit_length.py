import pytest

from livingspacetoolkit.lib import ToolkitLength
from livingspacetoolkit.lib.toolkit_enums import LengthType


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
        assert length.modified == True

    @pytest.mark.unit
    @pytest.mark.parametrize("class_input", length_equality_list, ids=length_input_id)
    def test_equality(self, class_input: tuple[list, bool]):
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = "12'"

        length_2 = ToolkitLength(class_input[0][1])
        length_2.length = class_input[0][0]

        assert (length_1 == length_2) == class_input[1]

    @pytest.mark.unit
    def test_less_than(self):
        # Arrange
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = "1ft"

        length_2 = ToolkitLength(LengthType.THICKNESS)
        length_2.length = "2ft"

        assert length_1 < length_2

    @pytest.mark.unit
    def test_greater_than(self):
        # Arrange
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = "1ft"

        length_2 = ToolkitLength(LengthType.THICKNESS)
        length_2.length = "2ft"

        assert length_2 > length_1

    @pytest.mark.unit
    def test_add(self):
        # Arrange
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = "1ft"

        length_2 = ToolkitLength(LengthType.THICKNESS)
        length_2.length = "2ft"

        assert (length_1 + length_2) == 36

    @pytest.mark.unit
    def test_subtract(self):
        # Arrange
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = "1ft"

        length_2 = ToolkitLength(LengthType.THICKNESS)
        length_2.length = "2ft"

        assert (length_2 - length_1) == 12

    @pytest.mark.unit
    @pytest.mark.parametrize("actual, expected",
                             [
                                 ("10'", 120),
                                 ("10ft", 120),
                                 ("10feet", 120),
                                 ("10 ft", 120),
                                 ("10 feet", 120),
                             ])
    def test_feet(self, actual, expected):
        # Arrange
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = actual

        assert length_1.length == expected

    @pytest.mark.unit
    @pytest.mark.parametrize("actual, expected",
                             [
                                 ('15', 15),
                                 ('15"', 15),
                                 ('15in.', 15),
                                 ('15 inches', 15),
                                 ('15.75', 15.75),
                                 ('15.75"', 15.75),
                                 ('15.75in.', 15.75),
                                 ('15.75 inches', 15.75),
                             ])
    def test_inches(self, actual, expected):
        # Arrange
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = actual

        assert length_1.length == expected

    @pytest.mark.unit
    @pytest.mark.parametrize("actual, expected",
                             [
                                 ('1/2"', 0.5),
                                 ('1/2in', 0.5),
                                 ('1/2inch', 0.5),
                                 ('1/2 in.', 0.5),
                                 ('1/2 inch', 0.5),
                                 ('1 1/2 inch', 1.5)
                             ])
    def test_fract_in(self, actual, expected):
        # Arrange
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = actual

        assert length_1.length == expected

    @pytest.mark.unit
    @pytest.mark.parametrize("actual, expected",
                             [
                                 ("1/2'", 6),
                                 ('1/2ft.', 6),
                                 ('1/2feet', 6),
                                 ('1/2 ft.', 6),
                                 ('1/2 feet', 6),
                                 ('1 1/2 feet', 18)
                             ])
    def test_fract_ft(self, actual, expected):
        # Arrange
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = actual

        assert length_1.length == expected

    @pytest.mark.unit
    @pytest.mark.parametrize("actual, expected",
                             [
                                 ("1' - 1\"", 13),
                                 ('1ft - 1in.', 13),
                                 ('1 1/2ft - 1 1/2in', 19.5),
                                 ('1/2ft - 1 1/2in', 7.5),
                                 ('1ft - 1/2in', 12.5),
                                 ('1 ft 1 in', 13)
                             ])
    def test_combo(self, actual, expected):
        # Arrange
        length_1 = ToolkitLength(LengthType.THICKNESS)
        length_1.length = actual

        assert length_1.length == expected

    @pytest.mark.unit
    @pytest.mark.parametrize("variable",
                             [
                                 '-10ft',
                                 '-10 1/2ft',
                                 '-10 ft',
                                 '-10 1/2 ft',
                                 "-10'",
                                 "-10 1/2'",
                                 '-10 feet',
                                 '-10 1/2 feet',
                                 '-10in',
                                 '-10 in',
                                 '-10"',
                                 '-10 1/2in',
                                 '-10 1/2 in',
                                 '-10 1/2"',
                                 '-10 feet - 10 inches',
                                 '-10 ft. - -10 in.',
                             ])
    def test_negative_input(self, variable):
        # Arrange
        length_1 = ToolkitLength(LengthType.THICKNESS)
        with pytest.raises(ValueError):
            length_1.length = variable
