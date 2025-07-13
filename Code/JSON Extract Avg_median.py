# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 18:38:28 2025

@author: 14805
"""
data_str = ''.join(data)
import json
# Parse the JSON data
data_parsed = json.loads(data)

# Function to extract and print all "estimated_amount" values
def extract_estimated_amounts(data):
    estimated_amounts = []
    
    for entry in data:
        for standard_charge in entry.get('standard_charges', []):
            for payer_info in standard_charge.get('payers_information', []):
                estimated_amounts.append(payer_info.get('estimated_amount'))
    
    return estimated_amounts

# Call the function to extract "estimated_amount" values
estimated_amounts = extract_estimated_amounts(data_parsed)

# Print the extracted estimated amounts
print("Estimated Amounts:", estimated_amounts)