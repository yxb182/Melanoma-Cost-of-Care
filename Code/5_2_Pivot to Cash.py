import pandas as pd
import os

# Define folder path
folder_path = r"C:\Users\14805\Documents\Charges Research\Processed Data\Pivot Tables"

# Input/output files
payer_neg_path = os.path.join(folder_path, "5_2_25_Discount Cash.xlsx")
output_path = os.path.join(folder_path, "Updated_5_2_25_Discount Cash.xlsx")

# Load payer_neg sheet
payer_neg_df = pd.read_excel(payer_neg_path, header=None)

# Create map of headers
header_row = payer_neg_df.iloc[0]
header_map = {str(h).strip(): i for i, h in enumerate(header_row)}

# Loop through each cancer center row
for idx in range(1, payer_neg_df.shape[0]):
    file_base = payer_neg_df.iat[idx, 0]
    if not isinstance(file_base, str) or not file_base.endswith("Pivot"):
        continue  # Skip non-pivot rows

    case_pivot_file = os.path.join(folder_path, f"{file_base}.xlsx")
    if not os.path.exists(case_pivot_file):
        print(f"❌ File not found for: {file_base}")
        continue

    # Load case pivot file
    case_pivot_df = pd.read_excel(case_pivot_file)

    # Extract median & countunique values
    for _, row in case_pivot_df.iterrows():
        try:
            cpt_code = str(int(row[0]))  # Convert 10021.0 → '10021'
        except ValueError:
            continue

        values = row.iloc[1:3].values  # Columns B & C = median & countunique
        col_names = [f"{cpt_code} median", f"{cpt_code} count unique"]

        for col_name, value in zip(col_names, values):
            col_index = header_map.get(col_name.strip())
            if col_index is not None:
                payer_neg_df.iat[idx, col_index] = value

# Save updated file
payer_neg_df.to_excel(output_path, index=False, header=False)
print(f"✅ Updated file saved to: {output_path}")
