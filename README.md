# Validating Filenames
By Nakshatra Yalagach and Trinity Chamblin 

The standardization of file naming conventions is vital for a strong workflow, especially in the data science niche. With this information, creating a program to validate data filenames contained within the Social Impact Data Commons was necessary. This allows collaborators to easily check for when their data file paths need tweaking. We also created a program that can be used to correct the filenames classified as invalid based on the contents of CSV files.  

The following bullet points are the elements that need to be satisfied to classify a filename and csv as valid, if at least one of these aren’t met, it is classified as invalid

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

Based on the above questions, we came up with a few guidelines that files need to follow to be validated in our filename playground:

Program Guidelines for Valid File Names

1.	The filename should have 5 parts I.e., coverage area, resolution, data source, year and title.
2.	A valid coverage area should be one among this list ['ncr', 'va', 'us', 'va013', 'va059']
3.	A valid resolution should be one among this list ['bl', 'bg', 'tr', 'nb', 'ct', 'hd', 'co', 'pl', 'pr', 'bz', 'ca', 'ahec']
4.	A valid data source should be one among this list ['acs5', 'lodes', 'pseo', 'qwi', 'mcig', 'hifld', 'ookla', 'webmd', 'sdad', 'abc', 'usda', 'fa',  'acs', 'vdh', 'nchs', 'samhsa', 'schev', 'gmap']
5.	Year should have only numeric characters (accounts for dashes within year values to account for files displaying data over time e.g “2019-2021”).
6.	The title should not have space or capital letters.
7.	If the filename adheres to all the above guidelines, then it is in the right format.

Program Guidelines for Valid Data Structure

1.	The data file is a CSV.
2.	The data file has the required column names among this list [ 'geoid', 'year', 'moe', 'measure', 'value', 'region_type']
3.	The data file contains a header.
4.	The data file contains the correct data types in each column respectively: 'geoid': [str, int], 'year': int, 'moe': [int, float], 'measure': str, 'value': [int, float], 'region_type': str
5.	The data file does not contain missing values in its columns.
6.	The data file contains data within its columns’  specified ranges (e.g year: range (1900, 2100))



Program Names and Descriptions:

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
    
Limitations: Current code in is_valid_filename only takes into account one filename at a time, however, curtain lines of code can be manipulated to test a CSV full of filenames.


2. file_validation.py
Purpose: The focus of this program is to validate data filenames and the structure of these files more rigorously.

  Function 1: Filename Validation 
  
    Description: Similar to the first function in csv_name_convert.py, it validates a filename against the established naming convention: [coverage_a​rea]_[resolution]_[data_s​ource]_[year]_[description].csv. 
    
    Output: Returns True if the filename meets the standard naming convention; otherwise returns False. 
  
  Function 2: Data File Structure Validation 
  
    Input: File path of the filename’s CSV. 
    Output: Validates the structure of the data file against established conventions. 
    
Limitations: Descriptions generated in generate_filename_from_csv are based solely on measure names. Custom descriptions need to be manually added to the filename.



3. test_filename.py
Purpose: This program will take the filenames as input and check if they adhere to the format of the filenames set by the division.

  Function 1: test_fnames(filename) 
  
    Input: Filename without the extension. 
    Output: Returns if the filename aligns with the format or not. If the filename does not align with the format it also provides information on which part of the filename has to be fixed.  

Our Workflow 
- Utilized the For Developers Documentation for the SDC to brainstorm a checklist for file validation. 
-  Used regular expression to create a standardized formula for a filename pattern to be considered “valid.” 
- Used the regex formula to create a classifier for file naming. 
- Used standards for data files to create a classifier for data files (.csv) 
- Randomly generated valid and invalid test cases (filenames and data files) for classifiers  
- Made edits to classifiers to improve their efficiency.

Methods 

When it comes to checking for errors, we consider the "miss by one” error to be very likely to occur, therefore we wrote precise regular expression checks that would report a misnamed error even if a single character is out of place. For example, for our tests, we had a test for extra characters in each expected substring even accounting for the very extreme cases such as very long filenames, many spaces, and special characters. 

We also anticipate that data preparers can accidentally update the data in the file without updating the file names. For example, a data preparer adds new geographies for Maryland into a dataset but has yet to update the file name to include Maryland. 


Future Evaluation Methods

We plan to run our code against files in sdc.all and find out the number of CSV data files that are properly named and calculate the percentages of the common ways that files are misnamed. For example: 
[%] Capitalized Names
[%] Misspelled Names      
[%] File Name Data Mismatches


If you have any questions or concerns about file_validation.py or csv_name_convert.py (file_path) 
 contact Trinity Chamblin (huz2ph@virginia.edu). If you have any questions or concerns about test_filename.py  contact Nakshatra Yalagach (jhj5dh@virginia.edu)



  
