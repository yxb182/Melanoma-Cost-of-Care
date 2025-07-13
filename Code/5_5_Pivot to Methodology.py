# -*- coding: utf-8 -*-
"""
Created on Mon May  5 23:21:45 2025

@author: 14805
"""

import pandas as pd
import os

# Define folder
folder_path = r"C:\Users\14805\Documents\Charges Research\Processed Data\Pivot Tables"
payer_neg_path = os.path.join(folder_path, "5_5_25_Methodology.xlsx")
output_path = os.path.join(folder_path, "Updated_5_5_25_Methodology.xlsx")

# Load payer_neg (header=None so we preserve structure)
payer_neg_df = pd.read_excel(payer_neg_path, header=None)

# Map header names to column indices (row 0 = column names)
header_row = payer_neg_df.iloc[0]
header_map = {str(h).strip(): i for i, h in enumerate(header_row)}

# Loop over cancer center names in column A, skipping the first row (header)
for idx in range(1, payer_neg_df.shape[0]):
    file_base = payer_neg_df.iat[idx, 0]
    if not isinstance(file_base, str) or not file_base.endswith("Pivot"):
        continue  # skip if not a valid file name

    case_pivot_file = os.path.join(folder_path, f"{file_base}.xlsx")
    if not os.path.exists(case_pivot_file):
        print(f"❌ Missing file for: {file_base}")
        continue

    # Load case pivot file
    case_pivot_df = pd.read_excel(case_pivot_file)

    # Fill in CPT values for this row
    for _, row in case_pivot_df.iterrows():
        try:
            cpt_code = str(int(row[0]))  # Ensure '10021.0' → '10021'
        except ValueError:
            continue  # Skip invalid CPT code rows

        values = row.iloc[7:10].values  # max, min, avg, median
        col_names = [f"{cpt_code} fee schedule", f"{cpt_code} total billed charges", f"{cpt_code} case rate"]

        for col_name, value in zip(col_names, values):
            col_index = header_map.get(col_name.strip())
            if col_index is not None:
                payer_neg_df.iat[idx, col_index] = value

# Save updated payer_neg
payer_neg_df.to_excel(output_path, index=False, header=False)
print(f"✅ Updated file saved to: {output_path}")
