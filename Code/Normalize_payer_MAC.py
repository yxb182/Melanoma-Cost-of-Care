# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 11:33:37 2025

@author: 14805
"""
import os
import pandas as pd

# Load the spreadsheet
file_path = r"C:\Users\14805\Documents\Charges Research\Completed Spreadsheets"
file_name = "Payer Negotiated Normalized.xlsx"
file = os.path.join(file_path, file_name)
excel_file = pd.ExcelFile(file)

new_file_name = file_name.replace(".xlsx", "_norm.xlsx")
new_file_path = os.path.join(file_path, new_file_name)

# Loop through each sheet in the Excel file
with pd.ExcelWriter(new_file_path, engine="openpyxl") as writer:
    for sheet_name in excel_file.sheet_names:
        print(f"Processing sheet: {sheet_name}")

        # Load the current sheet into a DataFrame
        df = excel_file.parse(sheet_name)
        
        # Convert numeric columns to proper types
        df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

        # Identify rows containing 6 or 7-digit MAC codes in Column A
        code_rows = df.iloc[:, 0].astype(str).str.match(r"^\d{6,7}$", na=False)

        # Get indices of MAC code rows
        mac_indices = df[code_rows].index.tolist()

        # Process the normalization for rows between MAC codes
        for i in range(1, len(mac_indices)):
            start_idx = mac_indices[i - 1] + 1
            end_idx = mac_indices[i]

            for idx in range(start_idx, end_idx):
                mac_values = df.iloc[mac_indices[i], 1:]
                df.iloc[idx, 1:] = df.iloc[idx, 1:].div(mac_values).replace([float('inf'), -float('inf')], None)

        # Handle the rows before the first MAC code (if any)
        if mac_indices:
            for idx in range(0, mac_indices[0]):
                mac_values = df.iloc[mac_indices[0], 1:]
                df.iloc[idx, 1:] = df.iloc[idx, 1:].div(mac_values).replace([float('inf'), -float('inf')], None)

        # Drop rows containing 6 or 7-digit MAC codes
        df = df[~code_rows]

        # Save the modified sheet to the new file
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Normalization complete! All sheets processed and saved as '{new_file_name}'.")
