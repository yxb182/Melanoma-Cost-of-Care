# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 18:13:55 2025

@author: 14805
"""

import os
import pandas as pd
import chardet

folder_path = r"C:\Users\14805\Documents\Charges Research\Converted CSV"
excel_file = os.path.join(folder_path, "Missing JSON directory.xlsx")
CPT_codes = os.path.join(folder_path, "CPT Codes.xlsx")
output_folder = r"C:\Users\14805\Documents\Charges Research\Processed Data"

def process_files(folder_path, excel_file, CPT_codes, output_folder):
    """
    Processes CSV and JSON files listed in an Excel file by filtering rows that contain specified CPT codes.
    
    Parameters:
    folder_path (str): Path to the folder containing the raw data files.
    excel_file (str): Path to the Excel file listing the files to process.
    cpt_codes_file (str): Path to the Excel file containing CPT codes.
    output_folder (str): Path to save the processed data.
    """
    
    # Load the Excel sheets
    file_directory = pd.read_excel(excel_file)
    file_names = file_directory.iloc[:, 0]  # First column
    
    CPT_directory = pd.read_excel(CPT_codes)
    CPT_query = CPT_directory.iloc[:, 1]
    CPT_query_regex = "|".join(CPT_query.astype(str))
    
    encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']
    
    for file_name in file_names:
        file_path = os.path.join(folder_path, str(file_name))
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
        
        print(f"Processing: {file_path}")
        filtered_chunks = []
        
        try:
            # Detect encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read(100000)
                detected_encoding = chardet.detect(raw_data)['encoding']
        except Exception as e:
            print(f"Error detecting encoding for {file_name}: {e}")
            detected_encoding = 'utf-8'  # Default to UTF-8
        
        if file_name.endswith(".csv"):
            for enc in [detected_encoding] + encodings:
                try:
                    for chunk in pd.read_csv(file_path, chunksize=100000, encoding=enc, 
                                             header=2, on_bad_lines='skip', low_memory=False):
                        filtered_chunk = chunk[chunk.apply(lambda row: row.astype(str).str.contains(CPT_query_regex, case=False, na=False).any(), axis=1)]
                        filtered_chunks.append(filtered_chunk)
                    break  # Stop if successful
                except UnicodeDecodeError:
                    continue  # Try the next encoding
        
        elif file_name.endswith(".json"):
            try:
                df = pd.read_json(file_path, encoding=detected_encoding)
                filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(CPT_query_regex, case=False, na=False).any(), axis=1)]
                filtered_chunks.append(filtered_df)
            except Exception as e:
                print(f"Error processing JSON file {file_name}: {e}")
                continue
        
        if filtered_chunks:
            final_df = pd.concat(filtered_chunks)
            output_file = os.path.join(output_folder, file_name)
            final_df.to_csv(output_file, index=False)  # Always saving as CSV for consistency
            print(f"Saved processed file: {output_file}")
