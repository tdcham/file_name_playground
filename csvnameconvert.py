import pandas as pd
from collections import Counter
import re

#Function #1

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

    # Patterns for each segment of the filename
    coverage_pattern = f"({state_pattern})"
    resolution_pattern = "(bl|bg|tr|nb|ct|hd|co|pl|pr|bz)"
    data_source_pattern = "(acs5|lodes|pseo|qwi|mcig|hifld|ookla|webmd|sdad|abc)"
    year_pattern = r"(\d{4})"
    description_pattern = r"([\w_]+)"

    # Full pattern
    pattern = f"^{coverage_pattern}_{resolution_pattern}_{data_source_pattern}_{year_pattern}_{description_pattern}\.csv$"

    return bool(re.match(pattern, filename))


# Test
print(is_valid_filename("al_bg_acs5_2015_adults_health_insured_by_sex.csv"))  # Should print True
print(is_valid_filename("2461567277782.csv"))  # Should print False


#Function #2

def generate_filename_from_csv(csv_path):
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

    df = pd.read_csv(csv_path, dtype={'geoid': 'object'})

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


# Example
csv_path = "/Users/trinityc/PycharmProject/sdc.valid_file_names_playground/ncr_broadbandnow_acs_sdad_2021_perc_income_on_internet.csv"
new_path = generate_filename_from_csv(csv_path)
print(new_path)
#print ("the file" + csv_path + "is now" new_path)



