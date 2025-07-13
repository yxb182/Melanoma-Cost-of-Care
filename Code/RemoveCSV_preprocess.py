# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 15:41:58 2025

@author: 14805
"""

import csv

# Define file path
input_file_path = r"C:\Users\14805\Documents\Charges Research\Raw Data\876000525_UNIVERSITY-OF-UTAH-HOSPITAL-AND-CLINICS_standardcharges2024-06-27 15-32-27-nh.csv"
output_file_path =r"C:\Users\14805\Documents\Charges Research\Raw Data\876000525_UNIVERSITY-OF-UTAH-HOSPITAL-AND-CLINICS_standardcharges2024-06-27 15-32-27-nh_new.csv"

# Define the row number to delete (1-based index)
row_to_delete = 2

# Open the input file for reading and output file for writing
with open(input_file_path, 'r', newline='', encoding='utf-8') as infile, \
     open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Iterate through each row in the CSV file
    for row_number, row in enumerate(reader, start=1):
        # Skip the row to delete
        if row_number == row_to_delete:
            continue
        # Write the row to the new file if it's not the one to delete
        writer.writerow(row)

print(f"Row {row_to_delete} has been deleted. The cleaned file is saved as {output_file_path}")