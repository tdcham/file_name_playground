#Code by Trinity Chamblin

import pandas as pd
import numpy as np
import re
import os

#read the new CSV file
file_path = '/Users/trinityc/Documents/BII-Work/filename_test_cases.csv'
df_new = pd.read_csv(file_path)

# Applying validation function to each filename in the dataframe and appending the results
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


# Applying the validation function to the dataframe
df_new['Valid_Trin'] = df_new['filename'].apply(lambda x: is_valid_filename(x)[0])
df_new['Notes_Trin'] = df_new['filename'].apply(lambda x: is_valid_filename(x)[1])

# Displaying the results
print(df_new[[ 'Valid_Trin', 'Notes_Trin']])

#Saving csv
output_file_path = '/Users/trinityc/Documents/BII-Work/filename_test_cases.csv'
df_new.to_csv(output_file_path, index=False)
