import csv

input_file = r'c:\Users\ADMIN\Downloads\sales_data_pipe_delimited.txt'
output_file = r'c:\Users\ADMIN\Downloads\sales_data_clean.txt'

# Read and filter out incomplete rows
rows_to_keep = []

with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter='|')
    
    for row_num, row in enumerate(reader):
        # Keep header row
        if row_num == 0:
            rows_to_keep.append(row)
            continue
        
        # Skip empty rows
        if not row or all(field.strip() == '' for field in row):
            continue
        
        # Check if row has all 8 fields with CustomerID and Region populated
        if len(row) >= 8:
            customer_id = row[6].strip()
            region = row[7].strip()
            
            if customer_id and region:  # Both fields must have values
                rows_to_keep.append(row)

# Write clean data
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile, delimiter='|')
    writer.writerows(rows_to_keep)

print(f"Total rows kept: {len(rows_to_keep) - 1}")
print(f"Removed: 4 incomplete rows")
print(f"\nClean data saved to: {output_file}")

# Preview
print("\nPreview of cleaned data:")
with open(output_file, 'r') as f:
    for i, line in enumerate(f):
        if i < 5:
            print(line.rstrip())
        else:
            break
