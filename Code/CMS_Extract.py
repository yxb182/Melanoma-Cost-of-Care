# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 20:44:26 2025
@author: 14805
"""

import os
import pandas as pd

# Define folder paths
folder_path = r"C:\Users\14805\Documents\Charges Research\CMS Data Raw"
excel_file = os.path.join(folder_path, "MAC Centers.xlsx")
output_folder = r"C:\Users\14805\Documents\Charges Research\CMS Data Extracted"

# Load MAC Centers file and extract relevant codes
mac_df = pd.read_excel(excel_file, dtype=str)  # Load entire sheet
mac_codes = set(mac_df.iloc[:, 0].dropna().astype(str).str.zfill(7))  # Extract unique MAC codes from first column

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process all relevant Excel files in folder_path
for file_name in os.listdir(folder_path):
    if file_name.startswith("2025-pricing_information-") and file_name.endswith("-all_macs.csv"):
        file_path = os.path.join(folder_path, file_name)
        
        # Load the file
        df = pd.read_csv(file_path, dtype=str)
        
        # Filter rows where Column D (index 3) contains a MAC code from MAC Centers
        filtered_df = df[df.iloc[:, 3].isin(mac_codes)]
        
        # Save filtered data
        if not filtered_df.empty:
            output_file = os.path.join(output_folder, f"filtered_{file_name}")
            filtered_df.to_csv(output_file, index=False)
            print(f"Processed and saved: {output_file}")

print("Processing complete.")
