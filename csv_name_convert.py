import pandas as pd
import numpy as np
import re
import os


#the file path of the filename here
file_path = "/Users/trinityc/PycharmProject/sdc.valid_file_names_playground/ncr_broadbandnow_acs_sdad_2021_perc_income_on_internet.csv"

def is_valid_filename(file_path):
    """
    Validates the filename against a specific naming convention:
    [coverage_area]_[resolution]_[data_source]_[year]_[description].csv.
    The function checks for valid file extensions, coverage areas, resolutions,
    data sources, time periods, variable names, and case sensitivity.
    """
    global filename
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

if lambda x: is_valid_filename(x) == False:

    def generate_filename_from_csv(file_path):
        """
        Generates a filename based on the established naming convention:
        [coverage_area]_[resolution]_[data_source]_[year]_[description].csv
        using data extracted from a provided CSV.

        Args:
        - csv_path (str): Path to the input CSV file.

        Returns:
        - str: A valid filename based on the provided data.

        Example:
        The CSV at '01007.csv.xz' contains data for the state of VA, block group resolution,
        from the 'sdad' data source, and for the year 2022:
        #>>> generate_filename_from_csv('01007.csv.xz')
        'va_bg_sdad_2022_data_description.csv'
        """

        df = pd.read_csv(file_path, dtype={'geoid': 'object'})

        # List of all state GEOID prefixes
        all_states = [
            '01', '02', '04', '05', '06', '08', '09', '10', '12', '13',
            '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
            '25', '26', '27', '28', '29', '30', '31', '32', '33', '34',
            '35', '36', '37', '38', '39', '40', '41', '42', '44', '45',
            '46', '47', '48', '49', '50', '51', '53', '54', '55', '56'
        ]

        ncr_states = ['24', '51', '11']  # Maryland, Virginia, DC

        unique_geoids = df['geoid'].apply(lambda x: x[:2]).unique()

        # Determine the coverage area based on the unique GEOIDs present
        if set(ncr_states).issubset(set(unique_geoids)):
            coverage_area = 'ncr'
        elif set(all_states).issubset(set(unique_geoids)):
            coverage_area = 'usa'
        elif len(unique_geoids) == 1:
            # Assuming a mapping of GEOID to state abbreviation exists. This is a placeholder.
            coverage_area = unique_geoids[0]
        else:
            coverage_area = 'multiple'

        # Extracting the resolution from the 'region_type' column
        resolution_mapping = {
            'census block': 'bl',
            'block group': 'bg',
            'census tract': 'tr',
            # we can add more mappings as needed
        }
        resolution = resolution_mapping[df['region_type'].iloc[0]]

        # Extracting the year
        year = str(df['year'].iloc[0])

        # Data source: Assuming 'sdad' for now
        data_source = 'sdad'  # Replace this as necessary

        # Description: this is a placeholder for now. Can be customized based on requirements
        global count
        count = 0
        for c in df:
            if count == 0:
                if c == "measure":
                    count += 1
                    description = df[c][0]
                else:
                    description = "enter_the_description"

        filename = f"{coverage_area}_{resolution}_{data_source}_{year}_{description}.csv"
        return filename
else:
    print(is_valid_filename(file_path))


# Example
new_filename = generate_filename_from_csv(file_path)
new_path = file_path.strip(os.path.basename(file_path)) + new_filename
print("New File Path: " + new_path)
#print ("the file" + file_path + "is now" + new_path)



