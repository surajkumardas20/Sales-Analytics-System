import csv

input_file = r'c:\Users\ADMIN\Downloads\sales_data_pipe_delimited.txt'

# Define different encodings to convert to
encodings = ['utf-8', 'ascii', 'latin-1', 'cp1252', 'iso-8859-1']

for encoding in encodings:
    try:
        output_file = rf'c:\Users\ADMIN\Downloads\sales_data_{encoding.replace("-", "_")}.txt'
        
        with open(input_file, 'r', encoding='utf-8') as infile:
            content = infile.read()
        
        with open(output_file, 'w', encoding=encoding) as outfile:
            outfile.write(content)
        
        print(f"✓ Converted to {encoding}: {output_file}")
    except Exception as e:
        print(f"✗ Failed to convert to {encoding}: {e}")

print("\nDone! Files created with different encodings.")
