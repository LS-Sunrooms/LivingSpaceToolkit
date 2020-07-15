#!/usr/bin/env python3

import re
import math
from fractions import Fraction
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:[%(name)s]:[%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
file_handler = logging.FileHandler('LS Toolkit_{}.log'.format(datetime.now().strftime("%Y-%m-%d")))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

unit_type = ['angle', 'length']


def feet_search(text):
    if 'ft' in text or "'" in text or 'feet' in text:
        return True
    else:
        return False


def inch_search(text):
    if 'in' in text or '"' in text:
        return True
    else:
        return False


class EngineeringUnits:
    def __init__(self, measurement, u_type):
        self.measurement = measurement
        if u_type not in unit_type:
            raise LookupError("The unit type selected is not available.")
        else:
            self.u_type = u_type
        degrees = re.compile(r'(\d*\.?\d*)deg')
        feet = re.compile(r'(\d*\s*)[\'|ft|fe+t]')
        inches = re.compile(r'\"|in')
        fract = re.compile(r'(\d+\/\d+)[\"|in|\'|ft|fe+t]')
        ft_or_in = re.compile(r'(\d*\.\d+|\d+)\s?[\"|in|\'|ft|feet]')
        in_fract = re.compile(r'(\d+)[\s*](\d+\/\d+)[\"|in]')
        # ft_and_in = re.compile(r'(\d+\.?\d*)\s?[\'|ft|feet](\s?\-?\s?)(\d+\.?\d*)[\"|in]')
        ft_and_in = re.compile(r'(\d+\.?\d*)(\D+)(\d+\.?\d*)')
        ft_and_in_fract = re.compile(r'(\d+\.?\d*)\s?[\'|ft|feet](\s?\-?\s?)(\d*\s?)(\d+\/\d+)[\"|in]')
        """ Refer to pg. 152 of 'Automate the Boring Stuff with Python' to understand regular expression groups"""
        try:
            if self.u_type == 'angle':
                if degrees.search(self.measurement):
                    c = degrees.search(self.measurement)
                    self.base = math.radians(float(c.group(1)))
                    self.base_unit = 'deg'
                else:
                    self.base = math.radians(float(self.measurement))
                    self.base_unit = 'deg'
        except AttributeError as err:
            logger.exception(err)
        except TypeError as err:
            logger.exception(err)
        try:
            if self.u_type == 'length':
                if feet_search(self.measurement) and inch_search(self.measurement):
                    if fract.search(self.measurement) is None:
                        c = ft_and_in.search(self.measurement)
                        self.base = eval(c.group(1)) * 12 + eval(c.group(3))
                        self.base_unit = 'in.'
                    else:
                        c = ft_and_in_fract.search(self.measurement)
                        if c.group(3) == '':
                            self.base = eval(c.group(1)) * 12 + eval(c.group(4))
                            self.base_unit = 'in.'
                        else:
                            self.base = eval(c.group(1)) * 12 + eval(c.group(3)) + eval(c.group(4))
                            self.base_unit = 'in.'
                elif feet_search(self.measurement) or inch_search(self.measurement):
                    if feet_search(self.measurement):
                        if fract.search(self.measurement) is None:
                            c = ft_or_in.search(self.measurement)
                            self.base = eval(c.group(1)) * 12
                            self.base_unit = 'in.'
                        else:
                            c = in_fract.search(self.measurement)
                            if c.group(1) == '':
                                self.base = eval(c.group(2))
                                self.base_unit = 'in.'
                            else:
                                self.base = eval(c.group(1)) + eval(c.group(2))
                                self.base_unit = 'in.'
                    if inch_search(self.measurement):
                        c = ft_or_in.search(self.measurement)
                        self.base = eval(c.group(1))
                        self.base_unit = 'in.'
                else:
                    if fract.search(self.measurement) is None:
                        c = ft_and_in.search(self.measurement)
                        self.base = eval(c.group(1)) * 12 + eval(c.group(3))
                        self.base_unit = 'in.'
                    else:
                        c = ft_and_in_fract.search(self.measurement)
                        if c.group(3) == '':
                            self.base = eval(c.group(1)) * 12 + eval(c.group(4))
                            self.base_unit = 'in.'
                        else:
                            self.base = eval(c.group(1)) * 12 + eval(c.group(3)) + eval(c.group(4))
                            self.base_unit = 'in.'
                self.base = float(self.base)
        except AttributeError as err:
            logger.exception(err)
        except TypeError as err:
            logger.exception(err)

    def simplified(self, desired_unit):
        if desired_unit == "ft-in":
            if self.base_unit == 'in.':
                number = math.modf(self.base)
                feet = number[1] / 12
                inches = number[1] % 12
                fract = Fraction(math.ceil(number[0]*16)/16).limit_denominator(16)
                if inches == 0.0 and fract.numerator == 0:
                    simple = str(int(feet)) + "'"
                elif fract == 0:
                    simple = str(int(feet)) + "' - " + str(int(inches)) + "\""
                elif inches == 0.0:
                    simple = str(int(feet)) + "' - " + str(fract) + "\""
                elif fract.numerator == fract.denominator:
                    simple = str(int(feet)) + "' - " + str(int(inches)+1) + "\""
                else:
                    simple = str(int(feet)) + "' - " + str(int(inches)) + ' ' + str(fract) + "\""
            elif self.base_unit == 'deg':
                simple = str(round(math.degrees(self.base))) + ' deg.'
        elif desired_unit == "in":
            number = math.modf(self.base)
            inches = number[1]
            fract = Fraction(math.ceil(number[0] * 16) / 16).limit_denominator(16)
            if fract.numerator == 0:
                simple = str(int(inches)) + " in"
            else:
                simple = str(float(inches + fract.numerator/fract.denominator)) + " in"
        return simple

    def __str__(self):
        return str(round(self.base, 3))
