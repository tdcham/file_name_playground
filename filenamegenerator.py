import random
import re
import pandas as pd
#this program is for generating test cases

def is_valid_filename(filename):
    """
    Validates the filename against the established convention:
    [coverage_area]_[resolution]_[data_source]_[year]_[description].csv
    """

    # List of valid state abbreviations
    state_abbreviations = [
        'al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga',
        'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md',
        'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj',
        'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc',
        'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy',
        'dc', 'us', 'ncr', 'usa'
    ]

    state_pattern = "|".join(state_abbreviations)

    # These are the regex patterns for each segment of the filename
    coverage_pattern = f"({state_pattern})" #Does it contain a valid coverage area?
    resolution_pattern = "(bl|bg|tr|nb|ct|hd|co|pl|pr|bz)" #Does it contain a valid resolution? Are the resolutions sorted in order?
    data_source_pattern = "(acs5|lodes|pseo|qwi|mcig|hifld|ookla|webmd|sdad|abc)" # Does it contain the data source?
    year_pattern = r"(\d{4})" #Does it contain the time period of the data captured in the file?

    description_pattern = r"([\w_]+)"   # Does it contain the variable name that is captured in the data file?
    #this could possibly be tweaked so that we ensure that the description is relevant to the content of the file
    #this would take some work

    # Full regex pattern
    pattern = f"^{coverage_pattern}_{resolution_pattern}_{data_source_pattern}_{year_pattern}_{description_pattern}\.csv$"

    return bool(re.match(pattern, filename))


# # Test
# print(is_valid_filename("al_bg_acs5_2015_adults_health_insured_by_sex.csv"))  # Should print True
# print(is_valid_filename("2461567277782.csv"))  # Should print False


# these are the components for generating valid filenames
state_abbreviations = [
    'al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga',
    'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md',
    'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj',
    'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc',
    'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy',
    'dc', 'us', 'ncr', 'usa'
]
resolutions = ["bl", "bg", "tr", "nb", "ct", "hd", "co", "pl", "pr", "bz"]
data_sources = ["acs5", "lodes", "pseo", "qwi", "mcig", "hifld", "ookla", "webmd", "sdad", "abc"]
#function to produce valid names
def generate_valid_filename():
    state = random.choice(state_abbreviations)# coverage area
    resolution = random.choice(resolutions)
    data_source = random.choice(data_sources)
    year = str(random.randint(1900, 2099))
    description = '_'.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(1, 10))])

    return f"{state}_{resolution}_{data_source}_{year}_{description}.csv"


def generate_invalid_filename():
    choices = [
        lambda: str(random.randint(1000, 9999999)) + ".csv",
        lambda: str(random.randint(1000, 9999)) + ''.join(
            [random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(1, 4))]) + ".csv",
        lambda: "a_" + ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(50)]) + ".csv",
        generate_almost_valid_filename
    ]
    return random.choice(choices)()


def generate_almost_valid_filename():
    # Base it on a valid filename but introduce small irregularities
    filename = generate_valid_filename()
    components = filename.split('_')

    # Chance to change one of the components
    if random.choice([True, False]):
        index = random.randint(0, len(components) - 2)  # -2 to avoid the last component (description)
        components[index] = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(1, 4))])

    # Chance to omit one of the components
    if random.choice([True, False]):
        components.pop(random.randint(0, len(components) - 1))

    return '_'.join(components)


# Testing
for _ in range(100):
    valid_filename = generate_valid_filename()
    print(f"Generated filename: {valid_filename}, Validation: {is_valid_filename(valid_filename)}")
    invalid_filename = generate_invalid_filename()
    print(f"Generated filename: {invalid_filename}, Validation: {is_valid_filename(invalid_filename)}")

