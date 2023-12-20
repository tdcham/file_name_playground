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
