import json
import pandas as pd

# === Input path ===
filepath = r"C:\Users\14805\Documents\Charges Research\Raw Data\106010776_ucsf-medical-center_standardcharges.json"

# === Load JSON ===
with open(filepath, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

for item in data.get("standard_charge_information", []):
    description = item.get("description", "")

    # Build code map from code_information
    code_map = {code.get("type"): code.get("code") for code in item.get("code_information", [])}

    for charge in item.get("standard_charges", []):
        row = {
            "description": description,
            "CDM": code_map.get("CDM"),
            "HCPCS": code_map.get("HCPCS"),
            "RC": code_map.get("RC"),
            "setting": charge.get("setting"),
            "billing_class": charge.get("billing_class"),
            "gross_charge": charge.get("gross_charge"),
            "discounted_cash": charge.get("discounted_cash"),
            "additional_generic_notes": charge.get("additional_generic_notes")
        }
        rows.append(row)

# === Convert to DataFrame and save ===
df = pd.DataFrame(rows)

# Save CSV
output_path = filepath.replace(".json", "_flattened.csv")
df.to_csv(output_path, index=False)

print(f"✅ Flattened UCSF file saved to:\n{output_path}")
