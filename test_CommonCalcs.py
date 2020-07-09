import unittest
import CommonCalcs as CommonCalcsClass


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.Common = CommonCalcsClass.CommonCalcs(162.0, 84.0, 0.3946833668851363, 90.00151745068285, 12.0, 1, 10.25,
                                                   'uncut', 129.3125, 141.09304605488887, 95.0)

    def test_panel_length(self):
        # Checks panel length
        self.assertEqual(self.Common.panel_length()[0], 108)


if __name__ == '__main__':
    unittest.main()
