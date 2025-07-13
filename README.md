# Melanoma-Cost-of-Care
Preprocessing
ReplaceSlashCSV_preprocess.py
RemoveCSV_preprocess.py
To troubleshoot CSV formatting issues
JSONto_CSV_UCSF05012025
For UCSF data due to formatting issues
JSONto_CSV_final05012025
For large data files (>2 GB)

Order of operations
CMS_Extract
For MAC medicare reimbursement Data
Read_CSV
Read CSV → XLSX
4_26_JSON to excel
Flattens JSON data, extracts CPT codes of interest into csv file
5_2_Pivot to Spreadsheet
Puts pivot table information (all 58) into Payer Neg sheet for data collection
5_2_Pivot to Cash
Puts pivot table information (all 58) into Discount Cash sheet for data collection
5_5_Pivot to Methodology
Puts pivot table information (all 58) into methodology sheet for data collection
Normalize_MAC
Normalizes payer neg and discount cash sheet info to MAC cost

