def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']

    Expected Output Format:
    [
        {
            'TransactionID': 'T001',
            'Date': '2024-12-01',
            'ProductID': 'P101',
            'ProductName': 'Laptop',
            'Quantity': 2,           # int type
            'UnitPrice': 45000.0,    # float type
            'CustomerID': 'C001',
            'Region': 'North'
        },
        ...
    ]

    Requirements:
    - Split by pipe delimiter '|'
    - Handle commas within ProductName (remove or replace)
    - Remove commas from numeric fields and convert to proper types
    - Convert Quantity to int
    - Convert UnitPrice to float
    - Skip rows with incorrect number of fields
    """
    transactions = []
    field_names = ['TransactionID', 'Date', 'ProductID', 'ProductName', 
                   'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    for line in raw_lines:
        try:
            # Split by pipe delimiter
            fields = line.split('|')
            
            # Skip rows with incorrect number of fields
            if len(fields) != 8:
                continue
            
            # Create dictionary with stripped values
            transaction = {}
            
            transaction['TransactionID'] = fields[0].strip()
            transaction['Date'] = fields[1].strip()
            transaction['ProductID'] = fields[2].strip()
            # Handle commas in ProductName - just strip them
            transaction['ProductName'] = fields[3].strip().replace(',', '')
            
            # Convert Quantity to int (remove commas first)
            quantity_str = fields[4].strip().replace(',', '')
            transaction['Quantity'] = int(quantity_str)
            
            # Convert UnitPrice to float (remove commas first)
            price_str = fields[5].strip().replace(',', '')
            transaction['UnitPrice'] = float(price_str)
            
            transaction['CustomerID'] = fields[6].strip()
            transaction['Region'] = fields[7].strip()
            
            transactions.append(transaction)
        
        except (ValueError, IndexError):
            # Skip rows with conversion errors
            continue
    
    return transactions


# Test the function
if __name__ == "__main__":
    # First, import and use the read_sales_data function
    from read_sales_data import read_sales_data
    
    try:
        filename = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
        
        # Read raw lines
        raw_lines = read_sales_data(filename)
        print(f"Read {len(raw_lines)} raw lines\n")
        
        # Parse transactions
        transactions = parse_transactions(raw_lines)
        print(f"Parsed {len(transactions)} transactions\n")
        
        print("First 3 transactions:")
        for i, trans in enumerate(transactions[:3], 1):
            print(f"\n  Transaction {i}:")
            for key, value in trans.items():
                print(f"    {key}: {value} ({type(value).__name__})")
        
        print(f"\n\nLast transaction:")
        last = transactions[-1]
        for key, value in last.items():
            print(f"  {key}: {value} ({type(value).__name__})")
    
    except Exception as e:
        print(f"Error: {e}")
