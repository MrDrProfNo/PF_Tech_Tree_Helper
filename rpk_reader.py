"""
@author MrDrProfNo

Set of utilities built to parse an AoW:P .rpk file. The file's contents
are never read in as a whole; instead, functions grab the information that they
need.
"""

from sys import argv
from re import findall
import struct


def add_to_dict(generic_dict, key_value_tuple):
    """
    Dictionary of text replacement. Same key can map to multiple values;
    the values will be stored in list at the end. Duplicate key/value pairs
    will not be inserted; duplicate keys with different values will be inserted.
    :param generic_dict: dict to update
    :param key_value_tuple: (key, value) pair to attempt to insert
    :return:
    """
    key = key_value_tuple[0]
    value = key_value_tuple[1]

    if generic_dict.get(key):
        for existing_value in generic_dict[key]:
            if value == existing_value:
                return

        generic_dict[key].append(value)
    else:
        generic_dict[key] = [value]


def rip_text_replacement(rpk_filename):
    """
    Given an RPK file, removes all of the text-replacement stuff referenced in
    it and returns a dict mapping replacement markers to their text. Duplicate
    markers will be written as a list.
    :param rpk_filename: filename of rpk file to work with
    :return:
    """
    rpk_file = open(rpk_filename, encoding="latin_1")

    replacement_dict = {}

    line = rpk_file.read()
    results = findall("\{.*?\}.......+?", line)
    for result in results:
        # these 3 bytes always follow the replacement marker
        split_result = result.split("\x01\x00\x00", 1)
        replacement_marker = split_result[0]

        # Mostly, I'm just trying to bypass crashes. The regex catches
        # almost all of the text replacement markers; the rest can be
        # entered manually.
        if len(split_result) != 2:
            continue
        elif len(split_result[1]) < 4:
            continue

        # the length of the replacement text is stored as a 4-byte int,
        # starting immediately at the beginning of split_result[1]
        text_length_bytes = bytes(split_result[1][0:4], encoding="latin_1")
        text_length = struct.unpack("<I", text_length_bytes)[0]

        # first 4 bytes were the length; [4, 4+text_length) is the end of
        # the string.
        replacement_text = split_result[1][4:4 + text_length]

        # print the result in a more usable format
        print(replacement_marker + ": " + replacement_text)

        add_to_dict(replacement_dict,
                    (replacement_marker, replacement_text))

    return replacement_dict

def main():
    if len(argv) != 2:
        print("usage: rpk_read_test.py <rpk file>")
        return -1

    rip_text_replacement(argv[1])


if __name__ == '__main__':
    main()
