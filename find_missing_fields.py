import csv

input_file = r'c:\Users\ADMIN\Downloads\sales_data_pipe_delimited.txt'
output_file = r'c:\Users\ADMIN\Downloads\sales_data_complete.txt'
missing_file = r'c:\Users\ADMIN\Downloads\sales_data_missing_fields.txt'

# Read and process the file
complete_rows = []
missing_rows = []

with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter='|')
    header = next(reader)
    complete_rows.append(header)
    
    for row_num, row in enumerate(reader, 2):
        # Check if row has all fields and CustomerID/Region are not empty
        if len(row) >= 8:
            customer_id = row[6].strip()
            region = row[7].strip()
            
            if customer_id and region:  # Both fields have values
                complete_rows.append(row)
            else:
                missing_rows.append((row_num, row))
        else:
            missing_rows.append((row_num, row))

# Write complete rows
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile, delimiter='|')
    writer.writerows(complete_rows)

# Write rows with missing fields
with open(missing_file, 'w', encoding='utf-8', newline='') as outfile:
    outfile.write("RowNumber|TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region\n")
    for row_num, row in missing_rows:
        outfile.write(f"{row_num}|" + '|'.join(row) + '\n')

print(f"Complete rows: {len(complete_rows) - 1}")
print(f"Missing CustomerID/Region: {len(missing_rows)}")
print(f"\nComplete data saved to: {output_file}")
print(f"Missing fields saved to: {missing_file}")

# Show missing rows
if missing_rows:
    print("\nRows with missing CustomerID or Region:")
    for row_num, row in missing_rows:
        print(f"  Row {row_num}: {row}")
