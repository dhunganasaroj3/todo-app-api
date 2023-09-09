"""
Sample tests
"""
from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """Test the calc module."""
    def test_add_numbers(self):
        """Test adding numbers"""
        res = calc.add(5, 6)

        self.assertEquals(res, 11)

    def test_subtract_numbers(self):
        """Test subtract number"""
        res = calc.subtract(5, 2)

        self.assertEquals(res, 3)
