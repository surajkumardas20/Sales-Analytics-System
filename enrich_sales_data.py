"""
Enrich sales transaction data with API product information
"""

import json
import os
from pathlib import Path
from read_sales_data import read_sales_data
from parse_transactions import parse_transactions
from validate_and_filter import validate_and_filter
from create_product_mapping import create_product_mapping
from fetch_all_products import fetch_all_products


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information

    Parameters:
    - transactions: list of transaction dictionaries
    - product_mapping: dictionary from create_product_mapping()

    Returns: list of enriched transaction dictionaries

    Expected Output Format (each transaction):
    {
        'TransactionID': 'T001',
        'Date': '2024-12-01',
        'ProductID': 'P101',
        'ProductName': 'Laptop',
        'Quantity': 2,
        'UnitPrice': 45000.0,
        'CustomerID': 'C001',
        'Region': 'North',
        # NEW FIELDS ADDED FROM API:
        'API_Category': 'laptops',
        'API_Brand': 'Apple',
        'API_Rating': 4.7,
        'API_Match': True  # True if enrichment successful, False otherwise
    }

    Enrichment Logic:
    - Extract numeric ID from ProductID (P101 → 101, P5 → 5)
    - If ID exists in product_mapping, add API fields
    - If ID doesn't exist, set API_Match to False and other fields to None
    - Handle all errors gracefully
    """
    
    enriched_transactions = []
    matched_count = 0
    unmatched_count = 0
    error_count = 0
    
    if not transactions:
        print("✗ Error: No transactions provided")
        return enriched_transactions
    
    if not product_mapping:
        print("✗ Error: No product mapping provided")
        return enriched_transactions
    
    print(f"Enriching {len(transactions)} transactions with API product data...\n")
    
    for idx, transaction in enumerate(transactions, 1):
        try:
            # Create enriched transaction (copy of original)
            enriched = dict(transaction)
            
            # Extract numeric ID from ProductID (e.g., "P101" → 101)
            product_id_str = transaction.get('ProductID', '')
            
            # Remove 'P' prefix and convert to int
            numeric_id = None
            if product_id_str.startswith('P'):
                try:
                    numeric_id = int(product_id_str[1:])
                except ValueError:
                    numeric_id = None
            
            # Look up in product mapping
            if numeric_id and numeric_id in product_mapping:
                product_info = product_mapping[numeric_id]
                
                # Add API fields
                enriched['API_Category'] = product_info.get('category', 'N/A')
                enriched['API_Brand'] = product_info.get('brand', 'Unknown')
                enriched['API_Rating'] = product_info.get('rating', 0)
                enriched['API_Price'] = product_info.get('price', 0)
                enriched['API_Stock'] = product_info.get('stock', 0)
                enriched['API_Discount'] = product_info.get('discount', 0)
                enriched['API_Match'] = True
                
                matched_count += 1
            else:
                # No match found in API
                enriched['API_Category'] = None
                enriched['API_Brand'] = None
                enriched['API_Rating'] = None
                enriched['API_Price'] = None
                enriched['API_Stock'] = None
                enriched['API_Discount'] = None
                enriched['API_Match'] = False
                
                unmatched_count += 1
            
            enriched_transactions.append(enriched)
        
        except Exception as e:
            print(f"⚠ Error processing transaction {idx}: {e}")
            error_count += 1
            continue
    
    print(f"✓ Enrichment complete:")
    print(f"  Matched: {matched_count} ({matched_count/len(transactions)*100:.1f}%)")
    print(f"  Unmatched: {unmatched_count} ({unmatched_count/len(transactions)*100:.1f}%)")
    print(f"  Errors: {error_count}\n")
    
    return enriched_transactions


def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file

    Expected File Format:
    TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    ...

    Requirements:
    - Create output file with all original + new fields
    - Use pipe delimiter
    - Handle None values appropriately
    """
    if not enriched_transactions:
        print("✗ Error: No enriched transactions to save")
        return False
    
    try:
        # Create directories if they don't exist
        output_dir = os.path.dirname(filename)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Define column order - essential fields only
        columns = [
            'TransactionID', 'Date', 'ProductID', 'ProductName', 'Quantity',
            'UnitPrice', 'CustomerID', 'Region',
            'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
        ]
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Write header
            f.write('|'.join(columns) + '\n')
            
            # Write data rows
            for transaction in enriched_transactions:
                row_values = []
                for col in columns:
                    value = transaction.get(col, '')
                    
                    # Handle None values
                    if value is None or value == '':
                        value = ''
                    else:
                        value = str(value)
                    
                    row_values.append(value)
                
                f.write('|'.join(row_values) + '\n')
        
        print(f"✓ Enriched data saved to: {filename}")
        print(f"  Records: {len(enriched_transactions)}")
        print(f"  Columns: {len(columns)}")
        print(f"  File size: {os.path.getsize(filename):,} bytes\n")
        
        return True
    
    except Exception as e:
        print(f"✗ Error saving enriched data: {e}")
        return False


def save_enriched_data_to_file(enriched_transactions, output_path):
    """
    Alias for save_enriched_data() - maintains backward compatibility
    """
    return save_enriched_data(enriched_transactions, output_path)


def display_enrichment_summary(enriched_transactions):
    """
    Displays summary of enriched data
    """
    if not enriched_transactions:
        print("No enriched transactions to display")
        return
    
    print(f"\n{'='*120}")
    print("ENRICHED SALES DATA SUMMARY")
    print(f"{'='*120}\n")
    
    # Count matches
    matched = sum(1 for t in enriched_transactions if t.get('API_Match', False))
    unmatched = len(enriched_transactions) - matched
    
    print(f"Total Transactions: {len(enriched_transactions)}")
    print(f"API Matches: {matched} ({matched/len(enriched_transactions)*100:.1f}%)")
    print(f"No API Match: {unmatched} ({unmatched/len(enriched_transactions)*100:.1f}%)\n")
    
    # Categories matched
    if matched > 0:
        matched_categories = set()
        for t in enriched_transactions:
            if t.get('API_Match', False):
                cat = t.get('API_Category')
                if cat:
                    matched_categories.add(cat)
        
        print(f"API Categories Found: {len(matched_categories)}")
        for cat in sorted(matched_categories):
            count = sum(1 for t in enriched_transactions if t.get('API_Category') == cat)
            print(f"  {cat}: {count} transactions")
    
    print()


def display_enriched_sample(enriched_transactions, limit=10):
    """
    Displays sample of enriched transactions
    """
    if not enriched_transactions:
        return
    
    print(f"\n{'='*120}")
    print(f"SAMPLE ENRICHED TRANSACTIONS (First {min(limit, len(enriched_transactions))})")
    print(f"{'='*120}\n")
    
    print(f"{'TID':<8} {'Date':<12} {'PID':<8} {'Qty':<5} {'Price':<12} {'Customer':<10} {'Region':<10} {'API_Match':<12} {'Category':<20} {'Brand':<15} {'Rating':<10}")
    print(f"{'-'*120}")
    
    for transaction in enriched_transactions[:limit]:
        tid = transaction.get('TransactionID', 'N/A')
        date = transaction.get('Date', 'N/A')
        pid = transaction.get('ProductID', 'N/A')
        qty = transaction.get('Quantity', 0)
        price = transaction.get('UnitPrice', 0)
        customer = transaction.get('CustomerID', 'N/A')
        region = transaction.get('Region', 'N/A')
        api_match = transaction.get('API_Match', False)
        category = transaction.get('API_Category', 'N/A') or 'N/A'
        brand = transaction.get('API_Brand', 'Unknown') or 'Unknown'
        rating = transaction.get('API_Rating', 'N/A')
        
        if rating and rating != 'N/A':
            rating = f"{rating:.1f}"
        
        match_str = "✓" if api_match else "✗"
        
        print(f"{tid:<8} {date:<12} {pid:<8} {qty:<5} ${price:<11.2f} {customer:<10} {region:<10} {match_str:<12} {str(category)[:19]:<20} {str(brand)[:14]:<15} {str(rating):<10}")


def export_enriched_to_json(enriched_transactions, output_file):
    """
    Exports enriched transactions to JSON
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(enriched_transactions, f, indent=2)
        
        print(f"✓ Enriched data exported to: {output_file}")
        print(f"  Records: {len(enriched_transactions)}")
        return True
    
    except Exception as e:
        print(f"✗ Error exporting to JSON: {e}")
        return False


def compare_original_vs_enriched(transactions, enriched_transactions):
    """
    Compares original and enriched transaction structures
    """
    print(f"\n{'='*120}")
    print("ORIGINAL VS ENRICHED STRUCTURE COMPARISON")
    print(f"{'='*120}\n")
    
    if transactions and enriched_transactions:
        original_keys = set(transactions[0].keys())
        enriched_keys = set(enriched_transactions[0].keys())
        
        new_keys = enriched_keys - original_keys
        
        print(f"Original Columns: {len(original_keys)}")
        for key in sorted(original_keys):
            print(f"  • {key}")
        
        print(f"\nNew Columns Added: {len(new_keys)}")
        for key in sorted(new_keys):
            print(f"  • {key}")
        
        print(f"\nTotal Columns: {len(enriched_keys)}")


# Main execution
if __name__ == "__main__":
    try:
        print(f"\n{'='*120}")
        print("ENRICH SALES DATA WITH API PRODUCT INFORMATION")
        print(f"{'='*120}\n")
        
        # Step 1: Load sales data
        print("Step 1: Loading sales data...")
        print("-" * 120)
        
        sales_file = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
        raw_lines = read_sales_data(sales_file)
        
        if not raw_lines:
            print("✗ Failed to load sales data")
            exit(1)
        
        print(f"✓ Loaded {len(raw_lines)} raw transaction lines\n")
        
        # Step 2: Parse transactions
        print("Step 2: Parsing transactions...")
        print("-" * 120)
        
        transactions = parse_transactions(raw_lines)
        
        if not transactions:
            print("✗ Failed to parse transactions")
            exit(1)
        
        print(f"✓ Parsed {len(transactions)} transactions\n")
        
        # Step 3: Validate transactions
        print("Step 3: Validating transactions...")
        print("-" * 120)
        
        valid_transactions, invalid_count, summary = validate_and_filter(transactions)
        
        if not valid_transactions:
            print("✗ No valid transactions found")
            exit(1)
        
        print(f"✓ Validation complete")
        print(f"  Valid: {len(valid_transactions)}")
        print(f"  Invalid: {invalid_count}\n")
        
        # Step 4: Fetch API products
        print("Step 4: Fetching API products...")
        print("-" * 120)
        
        api_products = fetch_all_products()
        
        if not api_products:
            print("✗ Failed to fetch API products")
            exit(1)
        
        print(f"✓ Fetched {len(api_products)} products\n")
        
        # Step 5: Create product mapping
        print("Step 5: Creating product mapping...")
        print("-" * 120)
        
        product_mapping = create_product_mapping(api_products)
        
        if not product_mapping:
            print("✗ Failed to create product mapping")
            exit(1)
        
        print(f"✓ Created mapping for {len(product_mapping)} products\n")
        
        # Step 6: Enrich sales data
        print("Step 6: Enriching sales data...")
        print("-" * 120 + "\n")
        
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)
        
        if not enriched_transactions:
            print("✗ Failed to enrich sales data")
            exit(1)
        
        # Display comparison
        compare_original_vs_enriched(valid_transactions, enriched_transactions)
        
        # Display enrichment summary
        display_enrichment_summary(enriched_transactions)
        
        # Display sample
        display_enriched_sample(enriched_transactions, limit=10)
        
        # Step 7: Save enriched data to file
        print(f"\n{'='*120}")
        print("Step 7: Saving enriched data to file...")
        print(f"{'='*120}\n")
        
        output_file = r'c:\Users\ADMIN\Downloads\enriched_sales_data.txt'
        save_enriched_data_to_file(enriched_transactions, output_file)
        
        # Step 8: Export to JSON
        print("Step 8: Exporting to JSON...")
        print("-" * 120 + "\n")
        
        json_file = r'c:\Users\ADMIN\Downloads\enriched_sales_data.json'
        export_enriched_to_json(enriched_transactions, json_file)
        
        # Final summary
        print(f"\n{'='*120}")
        print("ENRICHMENT COMPLETE")
        print(f"{'='*120}")
        
        matched = sum(1 for t in enriched_transactions if t.get('API_Match', False))
        print(f"\n✓ Successfully enriched {len(enriched_transactions)} transactions")
        print(f"✓ API matches: {matched} ({matched/len(enriched_transactions)*100:.1f}%)")
        print(f"✓ Files saved:")
        print(f"  • {output_file}")
        print(f"  • {json_file}")
        print(f"\n✓ Enriched data ready for analysis and comparison")
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
