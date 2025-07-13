# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 20:17:42 2025

@author: 14805
"""

import os
import pandas as pd
import chardet

# Define the folder path and Excel file name
folder_path = r"C:\Users\14805\Documents\Charges Research\Raw Data"
excel_file = os.path.join(folder_path, "standard charges file directory.xlsx")
CPT_codes = os.path.join(folder_path, "CPT Codes.xlsx")
output_folder = r"C:\Users\14805\Documents\Charges Research\Processed Data"

# Load the Excel sheet and get the first column containing file names
file_directory = pd.read_excel(excel_file)
file_names = file_directory.iloc[:, 0]  # First column
CPT_directory = pd.read_excel(CPT_codes)
CPT_query = CPT_directory.iloc[:, 1]
CPT_query_regex = "|".join(CPT_query.astype(str))

# Iterate through the filenames and process only CSV files
for file_name in file_names:
    if str(file_name).endswith(".csv"):  # Check if the file ends with .csv
        file_path = os.path.join(folder_path, file_name)
        
        # Check if the file exists to avoid errors
        if os.path.exists(file_path):
            print(f"Opening: {file_path}")
            
            # Initialize an empty list to store results
            filtered_chunks = []
            
            try:
                # Detect encoding
                with open(file_path, 'rb') as f:
                    raw_data = f.read(100000)  # Read a portion of the file
                    detected_encoding = chardet.detect(raw_data)['encoding']

                # Try reading with detected encoding
                for chunk in pd.read_csv(file_path, chunksize=100000, encoding=detected_encoding, 
                                         header=2, on_bad_lines='skip', low_memory=False):
                    filtered_chunk = chunk[chunk.apply(lambda row: row.astype(str).str.contains(CPT_query_regex, case=False, na=False).any(), axis=1)]
                    filtered_chunks.append(filtered_chunk)

            except UnicodeDecodeError as e:
                # Print the error message and default to 'utf-8' encoding
                print(f"UnicodeDecodeError for {file_name}: {e}. Defaulting to 'utf-8' encoding.")
           
            encodings = ['utf-8','latin1','ISO-8859-1','cp1252']
            for enc in encodings:
                try:
                    # Retry with 'utf-8' encoding
                    for chunk in pd.read_csv(file_path, chunksize=100000, encoding=enc, 
                                             header=2, on_bad_lines='skip', low_memory=False):
                        filtered_chunk = chunk[chunk.apply(lambda row: row.astype(str).str.contains(CPT_query_regex, case=False, na=False).any(), axis=1)]
                        filtered_chunks.append(filtered_chunk)
                        break

                except UnicodeDecodeError as e:
                    # If the utf-8 also fails, print the error and continue to the next file
                    print(f"UnicodeDecodeError for {file_name} (enc): {e}. Skipping this file.")
                    continue  # Skip the current file and move to the next file

            # Concatenate and save the filtered results if there was no error
            if filtered_chunks:
                filtered_df = pd.concat(filtered_chunks)
                output_path = os.path.join(output_folder, file_name)
                filtered_df.to_csv(output_path, index=False)
                filtered_df = None

        else:
            print(f"File not found: {file_path}")

