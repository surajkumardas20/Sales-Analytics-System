import csv

# Read original file and convert to pipe-delimited format
input_file = r'c:\Users\ADMIN\Downloads\sales_data.txt'
output_file = r'c:\Users\ADMIN\Downloads\sales_data_pipe_delimited.txt'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile, delimiter='|')
    
    for row in reader:
        # Strip whitespace from each field
        cleaned_row = [field.strip() for field in row]
        # Write back as pipe-delimited
        outfile.write('|'.join(cleaned_row) + '\n')

print(f"Pipe-delimited file saved to: {output_file}")

# Display first few rows
print("\nPreview:")
with open(output_file, 'r') as f:
    for i, line in enumerate(f):
        if i < 4:
            print(line.rstrip())
        else:
            break
