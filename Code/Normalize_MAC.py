# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 18:08:05 2025

@author: 14805
"""
import os
import pandas as pd

# Define the file path where the original file is located
file_path = r"C:\Users\14805\Documents\Charges Research\Completed Spreadsheets"
file_name = "Filtered_5_2_25_Discount_Cash.xlsx"
file = os.path.join(file_path, file_name)

# Define the new file name for saving the modified data
new_file_name = file_name.replace(".xlsx", "_norm.xlsx")
new_file_path = os.path.join(file_path, new_file_name)

# Load the spreadsheet
excel_file = pd.ExcelFile(file)

# Loop through each sheet in the Excel file
with pd.ExcelWriter(new_file_path, engine="openpyxl") as writer:
    for sheet_name in excel_file.sheet_names:
        print(f"Processing sheet: {sheet_name}")

        # Load the current sheet into a DataFrame
        df = excel_file.parse(sheet_name)

        # Identify rows containing 7-digit MAC codes in Column A
        mac_rows = df.iloc[:, 0].astype(str).str.match(r"^\d{6,7}$", na=False)

        # Get indices of MAC code rows
        mac_indices = df[mac_rows].index.tolist()
    

        # Process the normalization for rows between MAC codes
        for i in range(1, len(mac_indices)):
            # Get the current MAC code row and the previous MAC code row
            start_idx = mac_indices[i - 1] + 1  # Row after the previous MAC code
            end_idx = mac_indices[i]  # Row with the current MAC code

            # Normalize all rows between start_idx and end_idx (not including the MAC code row)
            for idx in range(start_idx, end_idx):
                mac_values = df.iloc[mac_indices[i], 1:]  # Get the MAC code row values (Columns B and C)
                df.iloc[idx, 1:] = df.iloc[idx, 1:] / mac_values  # Divide by the current MAC code

        # Handle the rows before the first MAC code (if any)
        if mac_indices:
            for idx in range(0, mac_indices[0]):
                mac_values = df.iloc[mac_indices[0], 1:]  # Get the first MAC code row values
                df.iloc[idx, 1:] = df.iloc[idx, 1:] / mac_values  # Divide by the first MAC code

        # Drop the MAC code rows as they're no longer needed in the final dataset
        df = df[~mac_rows]

        # Save the modified sheet to the new file
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Normalization complete! All sheets processed and saved as '{new_file_name}'.")


