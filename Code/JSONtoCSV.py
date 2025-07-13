import os
import pandas as pd
import json
import chardet  # Used for automatic character encoding detection

# Define the folder path and Excel file name
folder_path = r"C:\Users\14805\Documents\Charges Research\Raw Data"
excel_file = os.path.join(folder_path, "standard charges directory.xlsx")
output_folder = r"C:\Users\14805\Documents\Charges Research\Converted CSV"

# Load the Excel sheet and get the first column containing file names
file_directory = pd.read_excel(excel_file)
file_names = file_directory.iloc[:, 0]  # First column

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Function to automatically detect encoding and read the file
def get_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

# Function to flatten and save JSON to CSV
def json_to_flat_csv(json_filepath, file_name):
    try:
        encoding = get_file_encoding(json_filepath)
        print(f"Detected encoding for {json_filepath}: {encoding}")

        with open(json_filepath, 'r', encoding=encoding, errors='ignore') as file:
            data = json.load(file)

        # If the JSON contains a top-level key like a facility ID, get the first value
        if isinstance(data, dict):
            top_level_value = next(iter(data.values()))
        else:
            top_level_value = data

        # Flatten the JSON using pandas.json_normalize
        df = pd.json_normalize(top_level_value)

        # Create output path and save to CSV
        output_csv_filepath = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.csv")
        df.to_csv(output_csv_filepath, index=False, encoding='utf-8-sig')
        print(f"Saved: {output_csv_filepath}")

    except Exception as e:
        print(f"Error processing {json_filepath}: {e}")

# Iterate through the filenames and process only JSON files
for file_name in file_names:
    if str(file_name).endswith(".json"):
        json_filepath = os.path.join(folder_path, file_name)
        if os.path.exists(json_filepath):
            json_to_flat_csv(json_filepath, file_name)
