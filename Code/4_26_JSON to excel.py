import pandas as pd
import os
import ast
import datetime

def convert_city_of_hope_format(input_path, output_folder):

    df = pd.read_csv(input_path)
    rows = []

    for idx, row in df.iterrows():
        description = row.iloc[0]
        codes_raw = row.iloc[1]
        pricing_raw = row.iloc[2]

        try:
            codes_list = ast.literal_eval(codes_raw)
            pricing_list = ast.literal_eval(pricing_raw)
        except (ValueError, SyntaxError):
            continue

        code_map = {entry['type']: entry['code'] for entry in codes_list if 'type' in entry and 'code' in entry}

        cdm_code = code_map.get('CDM')
        rc_code = code_map.get('RC')
        cpt_code = code_map.get('CPT')
        hcpcs_code = code_map.get('HCPCS')

        for price_entry in pricing_list:
            setting = price_entry.get('setting')
            gross_charge = price_entry.get('gross_charge')
            discounted_cash = price_entry.get('discounted_cash')
            payers_info = price_entry.get('payers_information', [{}])  # Default to [{}] if empty

            for payer in payers_info:
                payer_name = payer.get('payer_name')
                plan_name = payer.get('plan_name')
                methodology = payer.get('methodology')
                additional_notes = payer.get('additional_payer_notes')

                minimum = payer.get('minimum')
                maximum = payer.get('maximum')
                standard_charge_dollar = payer.get('standard_charge_dollar')
                estimated_amount = payer.get('estimated_amount')
                modifiers = payer.get('modifiers')

                new_row = {
                    'description': description,
                    'code|1': cdm_code,
                    'code|1|type': 'CDM',
                    'code|2': rc_code,
                    'code|2|type': 'RC',
                    'code|3': cpt_code,
                    'code|3|type': 'CPT' if cpt_code else None,
                    'code|4': hcpcs_code,
                    'code|4|type': 'HCPCS' if hcpcs_code else None,
                    'setting': setting,
                    'standard_charge|gross': gross_charge,
                    'standard_charge|discounted_cash': discounted_cash,
                    'payer_name': payer_name,
                    'plan_name': plan_name,
                    'standard_charge|methodology': methodology,
                    'additional_generic_notes': additional_notes,
                    'standard_charge|min': minimum,
                    'standard_charge|max': maximum,
                    'standard_charge|negotiated_dollar': standard_charge_dollar,
                    'estimated_amount': estimated_amount,
                    'modifiers': modifiers
                }

                rows.append(new_row)

    final_df = pd.DataFrame(rows)

    os.makedirs(output_folder, exist_ok=True)
    output_filename = "converted_" + os.path.basename(input_path)
    output_path = os.path.join(output_folder, output_filename)
    final_df.to_csv(output_path, index=False)

    return output_path, len(final_df)


def convert_generic_format(input_path, output_folder):
    df = pd.read_csv(input_path)
    selected_columns = [col for col in df.columns if 'code' in col.lower() or 'description' in col.lower()]
    if not selected_columns:
        selected_columns = df.columns
    final_df = df[selected_columns]

    os.makedirs(output_folder, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"converted_generic_{timestamp}_" + os.path.basename(input_path)
    output_path = os.path.join(output_folder, output_filename)
    final_df.to_csv(output_path, index=False)

    return output_path, len(final_df)

def batch_convert_from_excel(excel_path, folder_path):
    files_to_convert = pd.read_excel(excel_path)

    converted_folder = os.path.join(folder_path, 'Converted')
    os.makedirs(converted_folder, exist_ok=True)

    summary = []

    for file in files_to_convert.iloc[:, 0]:
        input_file_path = os.path.join(folder_path, file)
        if os.path.exists(input_file_path):
            print(f"Converting: {file}")
            try:
                df_sample = pd.read_csv(input_file_path, nrows=5)
                second_column = df_sample.columns[1]
                first_row_second_col = str(df_sample.iloc[0, 1])

                use_city_of_hope_parser = False
                try:
                    codes_sample = ast.literal_eval(first_row_second_col)
                    if isinstance(codes_sample, list) and isinstance(codes_sample[0], dict) and 'type' in codes_sample[0]:
                        use_city_of_hope_parser = True
                except (ValueError, SyntaxError):
                    use_city_of_hope_parser = False

                if use_city_of_hope_parser:
                    output_path, num_rows = convert_city_of_hope_format(input_file_path, converted_folder)
                else:
                    output_path, num_rows = convert_generic_format(input_file_path, converted_folder)

                print(f"✅ Saved to {output_path} ({num_rows} rows)")
                summary.append({"file": file, "status": "Success", "rows": num_rows})
            except Exception as e:
                print(f"❌ Failed to process {file}: {e}")
                summary.append({"file": file, "status": f"Failed: {e}", "rows": 0})
        else:
            print(f"❌ File not found: {file}")
            summary.append({"file": file, "status": "File not found", "rows": 0})

    summary_df = pd.DataFrame(summary)
    summary_path = os.path.join(converted_folder, "conversion_summary.xlsx")
    summary_df.to_excel(summary_path, index=False)
    print(f"\nSummary report saved to: {summary_path}")

# Example usage:
# batch_convert_from_excel(
#     r"C:\\Users\\14805\\Documents\\Charges Research\\Processed Data\\files_to_convert.xlsx",
#     r"C:\\Users\\14805\\Documents\\Charges Research\\Processed Data"
# )
