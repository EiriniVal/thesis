import unittest
from profiler import has_old_char, is_roman_numeral, has_scribal_abbrev, is_number, get_vocab_counts


class MyTestCase(unittest.TestCase):

    def test_has_old_char(self):
        old_char = ["hat3", "3ewyth", "no3t", "a3en", "ha3t", "þe", "þis", "þanne", "oþer", "beþ", "Sublimatæ",
                    "æmatitis", "Fœnigræci", "œconomy", "ʒiss", "ʒj", "℥ss", "℞"]
        not_old_char = ["3", "1345"]
        for word in old_char:
            self.assertTrue(has_old_char(word))
        for word in not_old_char:
            self.assertFalse(has_old_char(word))

    def test_is_roman_numeral(self):
        roman_numerals = ["iiij", "viij", "xxii", "XXIII", "LXXVII", "XXXVII", "DCC", "M", "CCCC", "VIII.", "IX", "X.",
                          "XIII."]
        for n in roman_numerals:
            self.assertTrue(is_roman_numeral(n))

    def test_has_scribal_abbrev(self):
        abbrev = ["y=e=", "wrety~", "w=t=", "N=o=", "vnguentu=m=", "son~e", "i~", "co~me~dable", "Co~me~tarie",
                  "e~treth"]
        for a in abbrev:
            self.assertTrue(has_scribal_abbrev(a))  # add assertion here

    def test_is_number(self):
        numbers = ["34", "5.6", ".9", "1/2", "1/14877708919520606993173874072000th", "1st", "62nd", "2d", "63rd", "4th"]
        for n in numbers:
            self.assertTrue(is_number(n))  # add assertion here

if __name__ == '__main__':
    unittest.main()
