import csv

input_file = r'c:\Users\ADMIN\Downloads\sales_data_clean.txt'
output_file = r'c:\Users\ADMIN\Downloads\sales_data_final.txt'
removed_file = r'c:\Users\ADMIN\Downloads\sales_data_zero_quantity.txt'

rows_to_keep = []
rows_removed = []

with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile, delimiter='|')
    header = next(reader)
    rows_to_keep.append(header)
    
    for row_num, row in enumerate(reader, 2):
        if len(row) >= 5:
            quantity_str = row[4].strip()
            try:
                quantity = int(quantity_str)
                if quantity > 0:
                    rows_to_keep.append(row)
                else:
                    rows_removed.append((row_num, row))
            except ValueError:
                rows_removed.append((row_num, row))

# Write valid data
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile, delimiter='|')
    writer.writerows(rows_to_keep)

# Write removed rows
with open(removed_file, 'w', encoding='utf-8', newline='') as outfile:
    outfile.write("RowNumber|TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region\n")
    for row_num, row in rows_removed:
        outfile.write(f"{row_num}|" + '|'.join(row) + '\n')

print(f"Valid rows kept: {len(rows_to_keep) - 1}")
print(f"Rows removed (Quantity ≤ 0): {len(rows_removed)}")
print(f"\nFinal data saved to: {output_file}")
print(f"Removed data saved to: {removed_file}")

if rows_removed:
    print("\nRemoved transactions:")
    for row_num, row in rows_removed:
        print(f"  Row {row_num}: {row[0]} - Quantity: {row[4]}")
