import pandas as pd
import ijson

# === Load CPT/HCPCS codes from Excel ===
excel_path = r"C:\Users\14805\Documents\Charges Research\Raw Data\CPT Codes.xlsx"
cpt_df = pd.read_excel(excel_path, usecols=["CPT Search Term"])
cpt_set = set(cpt_df["CPT Search Term"].dropna().astype(str))

# === Path to large JSON file ===
json_path = r"C:\Users\14805\Documents\Charges Research\Raw Data\541848065_vcu-health_standardcharges.json"

# === Initialize result container ===
filtered_rows = []

with open(json_path, 'r', encoding='utf-8') as f:
    entries = ijson.items(f, 'standard_charge_information.item')

    for item in entries:
        code_map = {code.get("type"): code.get("code") for code in item.get("code_information", [])}
        cpt_code = code_map.get("CPT")
        hcpcs_code = code_map.get("HCPCS")

        # Skip rows not in CPT/HCPCS list
        if (cpt_code not in cpt_set) and (hcpcs_code not in cpt_set):
            continue

        description = item.get("description", "")

        for charge in item.get("standard_charges", []):
            setting = charge.get("setting")
            gross = charge.get("gross_charge")
            cash = charge.get("discounted_cash")
            min_val = charge.get("minimum")
            max_val = charge.get("maximum")

            for payer in charge.get("payers_information", []):
                row = {
                    "description": description,
                    "CPT": cpt_code,
                    "HCPCS": hcpcs_code,
                    "CDM": code_map.get("CDM"),
                    "RC": code_map.get("RC"),
                    "setting": setting,
                    "gross_charge": gross,
                    "discounted_cash": cash,
                    "minimum": min_val,
                    "maximum": max_val,
                    "payer_name": payer.get("payer_name"),
                    "plan_name": payer.get("plan_name"),
                    "estimated_amount": payer.get("estimated_amount"),
                    "standard_charge_percentage": payer.get("standard_charge_percentage"),
                    "standard_charge_dollar": payer.get("standard_charge_dollar"),
                    "methodology": payer.get("methodology"),
                    "additional_payer_notes": payer.get("additional_payer_notes")
                }
                filtered_rows.append(row)

# === Convert to DataFrame and Save ===
df_filtered = pd.DataFrame(filtered_rows)

# Choose one format below:

# Save as CSV
output_path = json_path.replace(".json", "_flattened.csv")
df_filtered.to_csv(output_path, index=False)

# OR save as Parquet (recommended for performance)
# output_path = json_path.replace(".json", "_flattened.parquet")
# df_filtered.to_parquet(output_path, index=False)

print(f"✅ Flattened file saved to:\n{output_path}")
print(f"🧾 Rows extracted: {len(df_filtered)}")
