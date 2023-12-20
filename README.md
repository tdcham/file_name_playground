# Validating Filenames
By Nakshatra Yalagach and Trinity Chamblin 

The standardization of file naming conventions is vital for a strong workflow, especially in the data science niche. With this information, creating a program to validate data filenames contained within the Social Impact Data Commons was necessary. This allows collaborators to easily check for when their data file paths need tweaking. We also created a program that can be used to correct the filenames classified as invalid based on the contents of CSV files.  

The following are the elements that need to be satisfied to classify a filename and CSV as valid, if at least one of these isn’t met, it is classified as invalid: 
1. File Names
- Does it contain a valid file extension? Possible extensions:  
- Does it contain a valid coverage area? 
- Does it contain a valid resolution? Are the resolutions sorted in order? 
- Does it contain the data source? 
- Does it contain the time period of when the data was collected in the file? 
- Does it contain the variable name that is captured in the data file? 
- Case sensitivity
  
2. Data Files
- Does it contain the correct number of attributes? 
- For each attribute, is all the data contained in the file of the same data type? 
- Is the file cleaned? Does it have missing values, Nan or Null values? 
- Does it have a header? 
- For each attribute, is all the data within the specified range for that attribute? 
- Check if the file naming convention adheres to the actual data in the file.

Functions
1. csv_name_convert.py
Purpose: This program is designed to address errors in file naming conventions. It contains two primary functions:

  Function 1: is_valid_filename(file_path) 
  
    Input: A string representing a filename. 
    Output: Returns True if the filename adheres to the established naming convention [coverage_a​rea]_[resolution]_[data_s​ource]_[year]_[description].csv. 
    otherwise returns False. 
    
    Assumptions: Assumes that the filename to be validated is provided as a string. 
  
  Function 2: generate_filename_from_csv(csv_path) 
  
    Input: File path of the CSV file. 
    Output: Generates and returns a new filename based on the established naming convention, using data extracted from the provided CSV file. 
    
    Conditions: This function is triggered only if is_valid_filename returns False. 
    Limitations: The CSV file must be in the same directory as the program. 

2. file_validation.py
Purpose: The focus of this program is to validate data filenames and the structure of these files more rigorously.

Function 1: Filename Validation 

Description: Similar to the first function in csv_name_convert.py, it validates a filename against the established naming convention: [coverage_a​rea]_[resolution]_[data_s​ource]_[year]_[description].csv. 

Output: Returns True if the filename meets the standard naming convention; otherwise returns False. 

Function 2: Data File Structure Validation 

Input: File path of the filename’s CSV. 
Output: Validates the structure of the data file against established conventions. 

Limitations: Descriptions generated in generate_filename_from_csv in csv_name_convert.py are based solely on measure names. Custom descriptions need to be manually added to the filename. 
