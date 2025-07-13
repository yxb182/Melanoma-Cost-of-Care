# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 21:43:42 2025
Process after extract
just do it manually, ignore
@author: 14805
"""

import os
import pandas as pd

# Define folder paths
folder_path = r"C:\Users\14805\Documents\Charges Research\CMS Data Extracted"
excel_file = os.path.join(folder_path, "MAC Centers.xlsx")
output_folder = r"C:\Users\14805\Documents\Charges Research\CMS Data Processed"

# Load MAC Centers file to get MAC locality to HCPCS mapping
mac_df = pd.read_excel(excel_file, dtype=str)

# Extract MAC codes from the first column and the corresponding HCPCS codes from the first row (B to AK)
mac_codes = set(mac_df.iloc[:, 0].dropna().astype(str))  # Extract unique MAC codes from first column
hcpcs_codes = mac_df.columns[1:].to_list()  # HCPCS codes are from column B to AK (excluding the first column)

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process all relevant Excel files in folder_path
for file_name in os.listdir(folder_path):
    if file_name.startswith("filtered_2025-pricing_information-") and file_name.endswith("-all_macs.csv"):
        file_path = os.path.join(folder_path, file_name)
        
        # Load the file
        df = pd.read_csv(file_path, dtype=str)
        
        # Filter rows where Column D (index 3) contains a MAC code from MAC Centers
        filtered_df = df[df.iloc[:, 3].isin(mac_codes)]
        
        # Iterate through each row in filtered_df
        for _, row in filtered_df.iterrows():
            hcpcs_code = row.iloc[0]  # Column A: HCPCS code
            mac_locality = row.iloc[3]  # Column D: MAC locality
            facility_price = row.iloc[5]  # Column F: Facility price
            
            # Check if the MAC locality is in the list of MAC codes and the HCPCS code is in the list
            if mac_locality in mac_codes and hcpcs_code in hcpcs_codes:
                # Find the row for the MAC locality
                mac_row_index = mac_df[mac_df.iloc[:, 0] == mac_locality].index[0]
                # Find the column index for the HCPCS code
                hcpcs_col_index = mac_df.columns.get_loc(hcpcs_code)
                
                # Update the cell with the facility price
                mac_df.at[mac_row_index, hcpcs_col_index] = facility_price

# Save the updated MAC Centers file (this will override the existing file)
output_file = os.path.join(output_folder, "Updated_MAC_Centers.xlsx")
mac_df.to_excel(output_file, index=False)

print(f"Processing complete. Updated MAC Centers saved as: {output_file}")