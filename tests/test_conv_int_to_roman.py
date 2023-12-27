from Practice_4.converter_integer_to_roman import printRoman


def test_print_3549():
    assert printRoman(3549) == "MMMDXLIX"

def test_print_2023():
    assert printRoman(2023) == "MMXXIII"

def test_print_99():
    assert printRoman(99) == "XCIX"
