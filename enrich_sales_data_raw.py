"""
Specialized enrichment script for raw sales data with smart product ID mapping
"""

import csv
import json
import os
from datetime import datetime
from fetch_all_products import fetch_all_products
from create_product_mapping import create_product_mapping


def parse_sales_data_raw(filename):
    """
    Parses raw sales data from pipe-delimited file
    Handles messy data with commas in numbers, missing values, etc.
    """
    transactions = []
    
    try:
        with open(filename, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        
        if not lines:
            print("[ERROR] File is empty")
            return transactions
        
        # Parse header
        header = lines[0].strip().split('|')
        
        print(f"Header columns: {header}\n")
        
        # Parse data rows
        for idx, line in enumerate(lines[1:], 1):
            try:
                line = line.strip()
                if not line:
                    continue
                
                values = line.split('|')
                
                # Skip if not enough columns
                if len(values) < len(header):
                    print(f"⚠ Row {idx}: Skipping - insufficient columns")
                    continue
                
                transaction = {}
                for i, col in enumerate(header):
                    value = values[i].strip() if i < len(values) else ''
                    
                    # Convert numeric fields
                    if col == 'Quantity':
                        try:
                            transaction[col] = int(value.replace(',', ''))
                        except:
                            transaction[col] = 0
                    elif col == 'UnitPrice':
                        try:
                            transaction[col] = float(value.replace(',', ''))
                        except:
                            transaction[col] = 0.0
                    else:
                        transaction[col] = value if value else None
                
                transactions.append(transaction)
            
            except Exception as e:
                print(f"⚠ Row {idx}: Error parsing - {e}")
                continue
        
        print(f"[OK] Parsed {len(transactions)} transactions from raw file\n")
        return transactions
    
    except Exception as e:
        print(f"[ERROR] Error reading file: {e}")
        return transactions


def validate_sales_transactions(transactions):
    """
    Validates sales transactions and filters out invalid ones
    """
    valid = []
    invalid_count = 0
    
    for transaction in transactions:
        try:
            # Check required fields
            if not transaction.get('TransactionID'):
                invalid_count += 1
                continue
            
            # Check TransactionID format (should start with T or X for now)
            tid = transaction.get('TransactionID', '')
            if not (tid.startswith('T') or tid.startswith('X')):
                print(f"[WARNING] Invalid TransactionID format: {tid}")
                invalid_count += 1
                continue
            
            # Check quantity > 0
            qty = transaction.get('Quantity', 0)
            if qty <= 0:
                print(f"[WARNING] Invalid quantity for {tid}: {qty}")
                invalid_count += 1
                continue
            
            # Check price > 0
            price = transaction.get('UnitPrice', 0)
            if price <= 0:
                print(f"[WARNING] Invalid price for {tid}: {price}")
                invalid_count += 1
                continue
            
            # Check required ID fields
            if not transaction.get('CustomerID'):
                print(f"[WARNING] Missing CustomerID for {tid}")
                invalid_count += 1
                continue
            
            valid.append(transaction)
        
        except Exception as e:
            print(f"[WARNING] Validation error: {e}")
            invalid_count += 1
            continue
    
    print(f"[OK] Validation complete: {len(valid)} valid, {invalid_count} invalid\n")
    return valid, invalid_count


def enrich_with_api_mapping(transactions, product_mapping):
    """
    Enriches transactions with API product data using product ID mapping
    """
    enriched = []
    matched = 0
    unmatched = 0
    
    print("Enriching transactions with API product data...\n")
    
    for transaction in transactions:
        try:
            enriched_tx = dict(transaction)
            
            # Extract numeric ID from ProductID
            product_id_str = transaction.get('ProductID', '')
            numeric_id = None
            
            if product_id_str.startswith('P'):
                try:
                    numeric_id = int(product_id_str[1:])
                except ValueError:
                    numeric_id = None
            
            # Look up in product mapping
            if numeric_id and numeric_id in product_mapping:
                product_info = product_mapping[numeric_id]
                
                enriched_tx['API_Category'] = product_info.get('category', 'N/A')
                enriched_tx['API_Brand'] = product_info.get('brand', 'Unknown')
                enriched_tx['API_Rating'] = product_info.get('rating', 0)
                enriched_tx['API_Price'] = product_info.get('price', 0)
                enriched_tx['API_Stock'] = product_info.get('stock', 0)
                enriched_tx['API_Discount'] = product_info.get('discount', 0)
                enriched_tx['API_Match'] = True
                
                matched += 1
            else:
                enriched_tx['API_Category'] = None
                enriched_tx['API_Brand'] = None
                enriched_tx['API_Rating'] = None
                enriched_tx['API_Price'] = None
                enriched_tx['API_Stock'] = None
                enriched_tx['API_Discount'] = None
                enriched_tx['API_Match'] = False
                
                unmatched += 1
            
            enriched.append(enriched_tx)
        
        except Exception as e:
            print(f"[WARNING] Error enriching transaction: {e}")
            continue
    
    print(f"[OK] Enrichment complete:")
    print(f"  Matched: {matched} ({matched/len(transactions)*100:.1f}% if len(transactions) > 0)")
    print(f"  Unmatched: {unmatched} ({unmatched/len(transactions)*100:.1f}% if len(transactions) > 0)\n")
    
    return enriched


def save_enriched_to_file(enriched_transactions, output_file):
    """
    Saves enriched transactions to pipe-delimited file
    """
    if not enriched_transactions:
        print("✗ No transactions to save")
        return False
    
    try:
        # Ensure directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Define columns
        columns = [
            'TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity',
            'UnitPrice', 'CustomerID', 'Region',
            'API_Category', 'API_Brand', 'API_Rating', 'API_Price', 'API_Stock', 'API_Discount', 'API_Match'
        ]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write header
            f.write('|'.join(columns) + '\n')
            
            # Write data
            for tx in enriched_transactions:
                row = []
                for col in columns:
                    value = tx.get(col, '')
                    if value is None or value == '':
                        value = ''
                    row.append(str(value))
                
                f.write('|'.join(row) + '\n')
        
        file_size = os.path.getsize(output_file)
        print(f"[OK] Enriched data saved to: {output_file}")
        print(f"  Records: {len(enriched_transactions)}")
        print(f"  Columns: {len(columns)}")
        print(f"  File size: {file_size:,} bytes\n")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Error saving file: {e}")
        return False


def save_enriched_to_json(enriched_transactions, output_file):
    """
    Saves enriched transactions to JSON
    """
    try:
        # Ensure directory exists
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w') as f:
            json.dump(enriched_transactions, f, indent=2)
        
        file_size = os.path.getsize(output_file)
        print(f"[OK] Enriched data exported to JSON: {output_file}")
        print(f"  File size: {file_size:,} bytes\n")
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Error saving JSON: {e}")
        return False


def display_enrichment_summary(enriched_transactions):
    """
    Displays summary of enrichment results
    """
    if not enriched_transactions:
        return
    
    print(f"\n{'='*120}")
    print("ENRICHMENT SUMMARY")
    print(f"{'='*120}\n")
    
    matched = sum(1 for t in enriched_transactions if t.get('API_Match', False))
    unmatched = len(enriched_transactions) - matched
    
    print(f"Total Transactions: {len(enriched_transactions)}")
    print(f"API Matches: {matched} ({matched/len(enriched_transactions)*100:.1f}%)")
    print(f"No API Match: {unmatched} ({unmatched/len(enriched_transactions)*100:.1f}%)\n")
    
    # Categories found
    categories = set()
    for t in enriched_transactions:
        if t.get('API_Match', False):
            cat = t.get('API_Category')
            if cat:
                categories.add(cat)
    
    print(f"API Categories Found: {len(categories)}")
    if categories:
        for cat in sorted(categories):
            count = sum(1 for t in enriched_transactions if t.get('API_Category') == cat)
            print(f"  • {cat}: {count} transactions")


def display_sample_enriched(enriched_transactions, limit=10):
    """
    Displays sample of enriched transactions
    """
    if not enriched_transactions:
        return
    
    print(f"\n{'='*130}")
    print(f"SAMPLE ENRICHED TRANSACTIONS (First {min(limit, len(enriched_transactions))})")
    print(f"{'='*130}\n")
    
    print(f"{'TID':<8} {'Date':<12} {'Product':<20} {'Qty':<5} {'Price':<12} {'Customer':<10} {'Region':<8} {'Match':<8} {'Category':<20} {'Brand':<12} {'Rating':<8}")
    print(f"{'-'*130}")
    
    for tx in enriched_transactions[:limit]:
        tid = str(tx.get('TransactionID', 'N/A'))[:7]
        date = str(tx.get('Date', 'N/A'))[:10]
        product = str(tx.get('ProductName', 'N/A'))[:19]
        qty = str(tx.get('Quantity', 0))
        price = f"${tx.get('UnitPrice', 0):.0f}"
        customer = str(tx.get('CustomerID', 'N/A'))[:9]
        region = str(tx.get('Region', 'N/A'))[:7]
        match = "✓" if tx.get('API_Match', False) else "✗"
        category = str(tx.get('API_Category', 'N/A'))[:19]
        brand = str(tx.get('API_Brand', 'Unknown'))[:11]
        rating = str(tx.get('API_Rating', 'N/A'))[:7]
        
        print(f"{tid:<8} {date:<12} {product:<20} {qty:<5} {price:<12} {customer:<10} {region:<8} {match:<8} {category:<20} {brand:<12} {rating:<8}")


# Main execution
if __name__ == "__main__":
    try:
        print(f"\n{'='*120}")
        print("ENRICH RAW SALES DATA WITH API PRODUCT INFORMATION")
        print(f"{'='*120}\n")
        
        # Step 1: Load raw sales data
        print("Step 1: Loading raw sales data...")
        print("-" * 120 + "\n")
        
        sales_file = r'c:\Users\ADMIN\Downloads\sales_data.txt'
        raw_transactions = parse_sales_data_raw(sales_file)
        
        if not raw_transactions:
            print("✗ Failed to load sales data")
            exit(1)
        
        # Step 2: Validate transactions
        print("Step 2: Validating transactions...")
        print("-" * 120 + "\n")
        
        valid_transactions, invalid_count = validate_sales_transactions(raw_transactions)
        
        if not valid_transactions:
            print("✗ No valid transactions found")
            exit(1)
        
        # Step 3: Fetch API products
        print("Step 3: Fetching API products...")
        print("-" * 120 + "\n")
        
        api_products = fetch_all_products()
        
        if not api_products:
            print("✗ Failed to fetch API products")
            exit(1)
        
        # Step 4: Create product mapping
        print("Step 4: Creating product mapping...")
        print("-" * 120 + "\n")
        
        product_mapping = create_product_mapping(api_products)
        
        if not product_mapping:
            print("✗ Failed to create product mapping")
            exit(1)
        
        # Step 5: Enrich with API data
        print("Step 5: Enriching sales data with API information...")
        print("-" * 120 + "\n")
        
        enriched_transactions = enrich_with_api_mapping(valid_transactions, product_mapping)
        
        if not enriched_transactions:
            print("✗ Failed to enrich sales data")
            exit(1)
        
        # Display summary
        display_enrichment_summary(enriched_transactions)
        
        # Display sample
        display_sample_enriched(enriched_transactions, limit=10)
        
        # Step 6: Save enriched data
        print(f"\n{'='*120}")
        print("Step 6: Saving enriched data...")
        print("-" * 120 + "\n")
        
        output_txt = r'c:\Users\ADMIN\Downloads\enriched_sales_data_raw.txt'
        save_enriched_to_file(enriched_transactions, output_txt)
        
        output_json = r'c:\Users\ADMIN\Downloads\enriched_sales_data_raw.json'
        save_enriched_to_json(enriched_transactions, output_json)
        
        # Final summary
        print(f"{'='*120}")
        print("ENRICHMENT COMPLETE")
        print(f"{'='*120}")
        
        matched = sum(1 for t in enriched_transactions if t.get('API_Match', False))
        print(f"\n✓ Successfully enriched {len(enriched_transactions)} transactions")
        print(f"✓ API matches: {matched} ({matched/len(enriched_transactions)*100:.1f}%)")
        print(f"✓ Files saved:")
        print(f"  • {output_txt}")
        print(f"  • {output_json}")
        print(f"\n✓ Ready for further analysis and comparison\n")
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
