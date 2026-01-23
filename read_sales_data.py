def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)

    Expected Output Format:
    ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]

    Requirements:
    - Use 'with' statement
    - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    - Handle FileNotFoundError with appropriate error message
    - Skip the header row
    - Remove empty lines
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    data_lines = []
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                
                # Skip header row and remove empty lines
                for i, line in enumerate(lines):
                    # Skip first line (header)
                    if i == 0:
                        continue
                    
                    # Strip whitespace and skip empty lines
                    stripped_line = line.strip()
                    if stripped_line:
                        data_lines.append(stripped_line)
                
                return data_lines
        
        except UnicodeDecodeError:
            # Try next encoding
            continue
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: File '{filename}' not found.")
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
    
    # If all encodings fail
    raise UnicodeDecodeError('utf-8', b'', 0, 1, f"Could not decode file '{filename}' with any supported encoding (utf-8, latin-1, cp1252)")


# Test the function
if __name__ == "__main__":
    try:
        filename = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
        sales_data = read_sales_data(filename)
        
        print(f"Successfully read {len(sales_data)} records\n")
        print("First 5 records:")
        for i, line in enumerate(sales_data[:5], 1):
            print(f"  {i}. {line}")
        
        print(f"\nLast record:")
        print(f"  {sales_data[-1]}")
    
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError: {e}")
    except Exception as e:
        print(f"Error: {e}")
