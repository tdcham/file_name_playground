import pandas as pd
import random
import csv
import string

# Constants for column names
VALID_COLUMN_NAMES = ['geoid', 'measure', 'moe', 'value', 'year', 'region_type']

# Helper function to generate a random string
def random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

# Generate a valid CSV structure
def generate_valid_csv(filename):
    df = pd.DataFrame(columns=VALID_COLUMN_NAMES)
    # Populate DataFrame with sample data if needed
    # df.to_csv(filename, index=False)

# Generate an invalid CSV structure
def generate_invalid_csv(filename):
    # Choose a random set of column names, either by shuffling, adding, or removing columns
    columns = VALID_COLUMN_NAMES.copy()
    if random.choice([True, False]):
        random.shuffle(columns)  # Shuffle the column order
    else:
        if random.choice([True, False]):
            columns.append(random_string(5))  # Add a random column
        else:
            columns.pop(random.randint(0, len(columns) - 1))  # Remove a random column

    df = pd.DataFrame(columns=columns)
    # Populate DataFrame with sample data if needed
    # df.to_csv(filename, index=False)

# Usage
generate_valid_csv('valid_structure.csv')
generate_invalid_csv('invalid_structure.csv')