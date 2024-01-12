#Code by Trinity Chamblin

import pandas as pd
import numpy as np
import re
import os

# #read the data frame of filenames
# file_path = '/Users/trinityc/Documents/BII-Work/filename_test_cases.csv'
# df_new = pd.read_csv(file_path)

#Check validation for a file name here
def is_valid_filename(file_path):
    """
    Validates the filename against a specific naming convention:
    [coverage_area]_[resolution]_[data_source]_[year]_[description].csv.
    The function checks for valid file extensions, coverage areas, resolutions,
    data sources, time periods, variable names, and case sensitivity.
    """

    # Extract filename from the file path
    filename = os.path.basename(file_path)


    # List of valid state abbreviations
    state_abbreviations = [
        'al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'de', 'fl', 'ga',
        'hi', 'id', 'il', 'in', 'ia', 'ks', 'ky', 'la', 'me', 'md',
        'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj',
        'nm', 'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc',
        'sd', 'tn', 'tx', 'ut', 'vt', 'va', 'wa', 'wv', 'wi', 'wy',
        'dc', 'us', 'ncr', 'usa', 'va013'
    ]

    state_pattern = "|".join(state_abbreviations)

    # Regex patterns for each segment of the filename
    coverage_pattern = f"({state_pattern})"
    resolution_pattern = "(bl|bg|tr|nb|ct|hd|co|pl|pr|bz)"
    data_source_pattern = "(acs5|lodes|pseo|qwi|mcig|hifld|ookla|webmd|sdad|abc)"
    year_pattern = r"(\d{4})"
    description_pattern = r"([\w_]+)"
    extension = ".csv"

    parts = filename.split('_')

    # Check if parts are in the correct order and validate each part
    for c in ['%', '^', '&', '*', '#', '@', '!', '?']:
        if c in filename:
            return False, "Filename contains Special characters"
    if len(parts) < 5:
        return False, "Filename has no Structure"

    if filename != filename.lower():
        return False, "Capitalized Character in Filename"

    if " " in filename:
        return False, "Space in Filename"
    # coverage area
    if not re.fullmatch(coverage_pattern, parts[0].lower()):
        for s in state_abbreviations:
            if s in filename:
                if len(parts[0]) < 4:
                    if parts[0] not in state_abbreviations:
                        return False, "Coverage Area Does Not Exist"
                    else:
                        return False, "Coverage Area is Incorrectly Formatted, Replace " + parts[
                            0] + " with Coverage Area"
            if s not in filename:
                return False, "Invalid or missing coverage area"
    # resolution
    if not re.fullmatch(resolution_pattern, parts[1].lower()):
        rp = ['bl', 'bg', 'tr', 'nb', 'ct', 'hd', 'co', 'pl', 'pr', 'bz']
        for r in rp:
            if r not in filename:
                return False, "Invalid or missing resolution"
            if r in filename:
                return False, "Resolution is Incorrectly Formatted, Replace " + parts[1] + " with Resolution"
    # data source
    if not re.fullmatch(data_source_pattern, parts[2].lower()):
        sources = ["acs5", 'lodes', 'pseo', 'qwi', 'mcig', 'hifld', 'ookla', 'webmd', 'sdad', 'abc']
        for n in sources:
            if n not in filename:
                return False, "Invalid or missing data source"
            if n in filename:
                return False, "Data Source is Incorrectly Formatted, Replace " + parts[2] + " with Source"
    # year
    if not re.fullmatch(year_pattern, parts[3]):
        if '-' not in parts[3]:
            return False, "Invalid or missing year"

    # Description is everything after the year part
    description = '_'.join(parts[4:]).rstrip('.csv')
    if not re.fullmatch(description_pattern, description):
        return False, "Invalid or missing description"

    else:
        return True, "Filename is Valid"

# Example of a single filename validation for is_valid_filename
file_path1 = "/Users/trinityc/PycharmProject/sdc.valid_file_names_playground/ncr_broadbandnow_acs_sdad_2021_perc_income_on_internet.csv"
print(is_valid_filename(file_path1))

#Example of applying the validation function to a dataframe of many filenames
# df_new['Valid'] = df_new['filename'].apply(lambda x: is_valid_filename(x)[0])
# df_new['Notes'] = df_new['filename'].apply(lambda x: is_valid_filename(x)[1])
#
# # Displaying the results
# print(df_new[[ 'Valid', 'Notes']])
#
# #Saving csv
# df_new.to_csv(output_file_path, index=False)



#Check Validation for the contents of a csv file here:

def is_valid_csv(file_path):
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
        df = pd.read_csv(file_path, dtype={'geoid': str})
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

# Example usage for is_valid_csv
is_valid_csv(file_path1)



