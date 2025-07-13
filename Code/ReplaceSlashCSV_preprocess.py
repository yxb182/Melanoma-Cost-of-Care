# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 23:33:18 2025

@author: 14805
"""
import csv

# Function to replace '/' with '-'
def replace_slash_in_csv(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Iterate through each row, replace '/' with '-', and write immediately to output file
        for row in reader:
            new_row = [cell.replace('/', '-') for cell in row]
            writer.writerow(new_row)

    print(f"File processed successfully. Output saved to {output_file}")

# Input and Output file paths
input_path = input(r"C:\Users\14805\Documents\Charges Research\Raw Data\522218584_medstargeorgetownuniversityhospital_standardcharges.csv")
output_path = input(r"C:\Users\14805\Documents\Charges Research\Raw Data\522218584_medstargeorgetownuniversityhospital_standardcharges_new.csv")

replace_slash_in_csv(input_path, output_path)