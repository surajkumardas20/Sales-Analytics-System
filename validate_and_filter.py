def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns: tuple (valid_transactions, invalid_count, filter_summary)

    Expected Output Format:
    (
        [list of valid filtered transactions],
        5,  # count of invalid transactions
        {
            'total_input': 100,
            'invalid': 5,
            'filtered_by_region': 20,
            'filtered_by_amount': 10,
            'final_count': 65
        }
    )

    Validation Rules:
    - Quantity must be > 0
    - UnitPrice must be > 0
    - All required fields must be present
    - TransactionID must start with 'T'
    - ProductID must start with 'P'
    - CustomerID must start with 'C'

    Filter Display:
    - Print available regions to user before filtering
    - Print transaction amount range (min/max) to user
    - Show count of records after each filter applied
    """
    
    required_fields = ['TransactionID', 'Date', 'ProductID', 'ProductName',
                       'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    
    valid_transactions = []
    invalid_count = 0
    regions_found = set()
    amounts = []
    
    # First pass: validate all transactions
    for trans in transactions:
        is_valid = True
        
        # Check all required fields present
        if not all(field in trans for field in required_fields):
            is_valid = False
        
        # Validate TransactionID starts with 'T'
        elif not trans['TransactionID'].startswith('T'):
            is_valid = False
        
        # Validate ProductID starts with 'P'
        elif not trans['ProductID'].startswith('P'):
            is_valid = False
        
        # Validate CustomerID starts with 'C'
        elif not trans['CustomerID'].startswith('C'):
            is_valid = False
        
        # Validate Quantity > 0
        elif trans['Quantity'] <= 0:
            is_valid = False
        
        # Validate UnitPrice > 0
        elif trans['UnitPrice'] <= 0:
            is_valid = False
        
        if is_valid:
            valid_transactions.append(trans)
            regions_found.add(trans['Region'])
            amount = trans['Quantity'] * trans['UnitPrice']
            amounts.append(amount)
        else:
            invalid_count += 1
    
    # Print available regions and amount range
    print("=" * 60)
    print("AVAILABLE REGIONS:")
    for r in sorted(regions_found):
        print(f"  - {r}")
    
    if amounts:
        min_trans_amount = min(amounts)
        max_trans_amount = max(amounts)
        print(f"\nTRANSACTION AMOUNT RANGE:")
        print(f"  Minimum: ${min_trans_amount:,.2f}")
        print(f"  Maximum: ${max_trans_amount:,.2f}")
    print("=" * 60)
    
    # Apply filters
    filtered_transactions = valid_transactions[:]
    filtered_by_region = 0
    filtered_by_amount = 0
    
    # Filter by region
    if region is not None:
        region = region.strip()
        before_region = len(filtered_transactions)
        filtered_transactions = [t for t in filtered_transactions if t['Region'] == region]
        filtered_by_region = before_region - len(filtered_transactions)
        print(f"\nAfter region filter ('{region}'): {len(filtered_transactions)} records")
    
    # Filter by amount range
    if min_amount is not None or max_amount is not None:
        before_amount = len(filtered_transactions)
        
        filtered_transactions = [
            t for t in filtered_transactions
            if (min_amount is None or t['Quantity'] * t['UnitPrice'] >= min_amount) and
               (max_amount is None or t['Quantity'] * t['UnitPrice'] <= max_amount)
        ]
        
        filtered_by_amount = before_amount - len(filtered_transactions)
        
        if min_amount is not None and max_amount is not None:
            print(f"After amount filter (${min_amount:,.2f} - ${max_amount:,.2f}): {len(filtered_transactions)} records")
        elif min_amount is not None:
            print(f"After amount filter (min: ${min_amount:,.2f}): {len(filtered_transactions)} records")
        else:
            print(f"After amount filter (max: ${max_amount:,.2f}): {len(filtered_transactions)} records")
    
    # Build summary
    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'valid': len(valid_transactions),
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(filtered_transactions)
    }
    
    return filtered_transactions, invalid_count, filter_summary


# Test the function
if __name__ == "__main__":
    from read_sales_data import read_sales_data
    from parse_transactions import parse_transactions
    
    try:
        filename = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
        
        # Read and parse
        raw_lines = read_sales_data(filename)
        transactions = parse_transactions(raw_lines)
        
        print(f"Total transactions loaded: {len(transactions)}\n")
        
        # Test 1: Validate without filters
        print("\n" + "="*60)
        print("TEST 1: Validation only (no filters)")
        print("="*60)
        valid, invalid, summary = validate_and_filter(transactions)
        
        print(f"\nValidation Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        # Test 2: Filter by region
        print("\n\n" + "="*60)
        print("TEST 2: Filter by region 'North'")
        print("="*60)
        valid, invalid, summary = validate_and_filter(transactions, region='North')
        
        print(f"\nFilter Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        print(f"\nNorth region transactions:")
        for trans in valid[:3]:
            amount = trans['Quantity'] * trans['UnitPrice']
            print(f"  {trans['TransactionID']}: {trans['ProductName']} - Qty: {trans['Quantity']}, Price: ${trans['UnitPrice']:,.2f}, Amount: ${amount:,.2f}")
        
        # Test 3: Filter by amount range
        print("\n\n" + "="*60)
        print("TEST 3: Filter by amount range ($5000 - $50000)")
        print("="*60)
        valid, invalid, summary = validate_and_filter(transactions, min_amount=5000, max_amount=50000)
        
        print(f"\nFilter Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
