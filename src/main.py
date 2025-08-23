import os
import sys
import logging
import shutil

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Statics
# You can change according to your needs:
FAMILY = "MyEmojiFamily"
RANGES_FILE_PATH = "../local/hex_ranges.txt"
SOURCE_SVGS_DIR_PATH = "../local/source_svgs/"
SVGS_DIR_PATH = "../local/svgs/"

def _hex_to_int(hex):
    return int(hex, 16) 

def _int_to_hex(_int):
    return hex(_int)[2:]    

def _get_ranges_file_content():
    ranges = ""
    # Read file with ranges
    with open(RANGES_FILE_PATH) as f:
        ranges = f.read()
    return ranges

# Get hexes and hex ranges converted into tuple
def _parse_hex_ranges(ranges_content):
    ranges = ranges_content.split("\n")

    hex_ranges = []
    hex = ""
    for _range in ranges:
        if (_range):
            # Parse hex range format: 0057-0EAE
            # into tuple (0057, 0EAE)
            if ("-" in _range):
                rs = _range.split("-")
                hex = (rs[0], rs[1])
            else:
                hex = _range

            hex_ranges.append(hex)
    return hex_ranges

# Convert every hex to int for convenient manipulation of ranges 
def _hex_ranges_to_int_ranges(hex_ranges):
    int_ranges = []
    number = -1
    for hr in hex_ranges:
        if (type(hr) == str):
            number = _hex_to_int(hr)
        elif (type(hr) == tuple):
            number = (_hex_to_int(hr[0]), _hex_to_int(hr[1]))

        int_ranges.append(number)
    return int_ranges

# Replace each tuple in the list with a range of integers 
# between the first and second number in the tuple
def _int_ranges_to_int_list(int_ranges):
    int_list = []
    numbers = [] 
    for ir in int_ranges:
        if (type(ir) == int):
            numbers = [ir] 
        elif (type(ir) == tuple):
            numbers = list(range(ir[0], ir[1]))

        int_list.extend(numbers)
    return int_list

# Hexadecimal number cannot exceed 10FFFF in Unicode
def _check_int_list(int_list):
    for i in int_list:
        if (i > 1114111):
            raise Exception("Number must be less than 1114111 (hex: 10FFFF).")

# Convert every int to hex in list
def _int_list_to_hex_list(int_list):
    hex_list = []
    for i in int_list:
        hex_list.append(_int_to_hex(i))
    return hex_list

def _get_hex_list():
    content = _get_ranges_file_content()
    hex_ranges = _parse_hex_ranges(content)
    int_ranges = _hex_ranges_to_int_ranges(hex_ranges)
    int_list = _int_ranges_to_int_list(int_ranges)
    _check_int_list(int_list)
    return _int_list_to_hex_list(int_list)

# Copy svgs to the new location with the new hex names
def rename_svgs():
    os.makedirs(SVGS_DIR_PATH, exist_ok=True)

    hex_list = _get_hex_list()
    source_svgs = os.listdir(SOURCE_SVGS_DIR_PATH)

    if (len(source_svgs) > len(hex_list)):
        raise Exception(f"Too many svgs ({len(source_svgs)}) relative to the quantity hexs ({len(hex_list)}).")

    for filename in source_svgs :
        source_path = os.path.join(SOURCE_SVGS_DIR_PATH, filename)
        new_filename = f"{hex_list.pop(0)}.svg"
        destination_path = os.path.join(SVGS_DIR_PATH, new_filename)

        # Copy the file to the new location with the new name
        shutil.copy(source_path, destination_path)

if (__name__ == "__main__"):
    rename_svgs() 
    logger.info("The images have been successfully copied and renamed!")

    print("Run this command to build your own emoji font with the provided svgs (run in same dir):")
    print(f"nanoemoji --color_format glyf_colr_1 --family {FAMILY} {SVGS_DIR_PATH}*.svg")
