import pandas as pd
import numpy as np
import re


filename = "ncr_broadbandnow_acs_sdad_2021_perc_income_on_internet.csv"
csv_path = "/Users/trinityc/PycharmProject/sdc.valid_file_names_playground/ncr_broadbandnow_acs_sdad_2021_perc_income_on_internet.csv"
#Check validation for a file name here
def is_valid_filename(filename):
    """
    Validates the filename against the established convention:
    [coverage_area]_[resolution]_[data_source]_[year]_[description].csv

    These are the checks that need to be fufilled in order for a filename to be considered
    "valid" and up to standards:

•   Does it contain a valid file extension? Possible extensions:
•	Does it contain a valid coverage area?
•	Does it contain a valid resolution? Are the resolutions sorted in order?
•	Does it contain the data source?
•	Does it contain the time period of the data captured in the file?
•	Does it contain the variable name that is captured in the data file?
•	Case sensitivity

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


#Check Validation for the contents of a csv file here:

def is_valid_csv(csv_path):
    """
    Validates a csv's structure against the established conventions:

    Required columns:
    geoid, measure, margin of error, value, year, region_type

    These are the checks that need to be fufilled in order for a csv to be considered
    "valid" and up to standards:

•	Does it contain the correct number of attributes?
•	For each attribute, is all the data contained in the file of the same data type?
•	Is the file cleaned? Does it have missing values, Nan or Null values?
•	Does it have a header?
•	For each attribute, is all the data within the specified range for that attribute?
•	Check if the file naming convention adheres to the actual data in the file.

"""
    required_columns = {'geoid', 'year', 'moe', 'measure', 'value', 'region_type'}
    data_types = {
        'geoid': [str, int],
        'year': int,
        'moe': [int, float],
        'measure': str,
        'value': [int, float],
        'region_type': str
    }
    # Specify appropriate ranges
    ranges = {
        'year': range(1900, 2100),
    }

    # Read the CSV file
    try:
        df = pd.read_csv(csv_path, dtype={'geoid': str})
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return False

    # Check for header
    if df.empty or df.columns.to_list() == list(range(len(df.columns))):
        print("CSV file does not have a header.")
        return False

    # Check for required columns
    if not required_columns.issubset(df.columns):
        print("CSV file is missing one or more required columns.")
        return False

    # Check for correct data types
    for col in required_columns:
            # Ensure data_types[col] is a list for the 'in' operator to work correctly
            valid_types = data_types[col] if isinstance(data_types[col], list) else [data_types[col]]
            if df[col].dtype not in (np.dtype(t) for t in valid_types):
                print(f"Data type for {col} is incorrect. Found {df[col].dtype}, expected {valid_types}.")
                return False
            if df[col].isnull().any():
                print(f"Column {col} contains missing values.")
                return False

    # Check for data within specified ranges
    for col, rng in ranges.items():
        if not df[col].apply(lambda x: x in rng).all():
            print(f"Data in column {col} is out of the specified range.")
            return False

    # If file naming is also to be validated, this should be incorporated into the function
    # This part depends on the details of how the file name correlates to the data

    print("CSV file is valid.")
    return True

    # Example usage
print(is_valid_filename(filename))
is_valid_csv(csv_path)



