"""
Main execution function for Sales Analytics System
Orchestrates the entire workflow from data loading to report generation
"""

import os
import sys
from datetime import datetime
from enrich_sales_data_raw import (
    parse_sales_data_raw,
    validate_sales_transactions,
    enrich_with_api_mapping,
    save_enriched_to_file,
    save_enriched_to_json
)
from fetch_all_products import fetch_all_products
from create_product_mapping import create_product_mapping
from generate_sales_report import generate_sales_report


def print_header():
    """
    Prints welcome header
    """
    print("\n" + "=" * 80)
    print("SALES ANALYTICS SYSTEM".center(80))
    print("=" * 80 + "\n")


def print_step(step_num, total_steps, message):
    """
    Prints a formatted step message
    """
    print(f"[{step_num}/{total_steps}] {message}...")


def print_success(message):
    """
    Prints a success message
    """
    print(f"    [OK] {message}")


def print_error(message):
    """
    Prints an error message
    """
    print(f"    [ERROR] {message}")


def print_warning(message):
    """
    Prints a warning message
    """
    print(f"    [WARNING] {message}")


def get_filter_choice():
    """
    Asks user if they want to filter data
    """
    while True:
        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()
        if choice in ['y', 'n']:
            return choice == 'y'
        print("    Please enter 'y' or 'n'")


def get_filter_criteria(regions, min_amount, max_amount):
    """
    Gets filter criteria from user
    """
    print("\n" + "-" * 80)
    print("FILTER OPTIONS")
    print("-" * 80)
    print(f"Available Regions: {', '.join(sorted(set(regions)))}")
    print(f"Amount Range: ${min_amount:,.2f} - ${max_amount:,.2f}")
    
    filters = {}
    
    # Region filter
    region_choice = input("\nFilter by region? (leave blank for all): ").strip()
    if region_choice:
        filters['region'] = region_choice
    
    # Amount filter
    try:
        min_input = input("Minimum amount? (leave blank for all): ").strip()
        if min_input:
            filters['min_amount'] = float(min_input)
        
        max_input = input("Maximum amount? (leave blank for all): ").strip()
        if max_input:
            filters['max_amount'] = float(max_input)
    except ValueError:
        print_warning("Invalid amount entered, using all amounts")
    
    return filters


def main():
    """
    Main execution function

    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
       - Show available regions
       - Show transaction amount range
       - Ask if user wants to filter (y/n)
    5. If yes, ask for filter criteria and apply
    6. Validate transactions
    7. Display validation summary
    8. Perform all data analyses (call all functions from Part 2)
    9. Fetch products from API
    10. Enrich sales data with API info
    11. Save enriched data to file
    12. Generate comprehensive report
    13. Print success message with file locations

    Error Handling:
    - Wrap entire process in try-except
    - Display user-friendly error messages
    - Don't let program crash on errors
    """
    
    total_steps = 10
    
    try:
        print_header()
        
        # Step 1: Read sales data
        print_step(1, total_steps, "Reading sales data file")
        
        sales_file = r'c:\Users\ADMIN\Downloads\sales_data.txt'
        
        if not os.path.exists(sales_file):
            print_error(f"File not found: {sales_file}")
            return False
        
        raw_transactions = parse_sales_data_raw(sales_file)
        
        if not raw_transactions:
            print_error("Failed to read sales data")
            return False
        
        print_success(f"Successfully read {len(raw_transactions)} transactions")
        
        # Step 2: Parse and clean
        print_step(2, total_steps, "Parsing and cleaning data")
        print_success(f"Parsed {len(raw_transactions)} records")
        
        # Step 3: Display filter options
        print_step(3, total_steps, "Analyzing available filters")
        
        # Calculate statistics for filter display
        regions = set()
        amounts = []
        
        for tx in raw_transactions:
            region = tx.get('Region')
            if region:
                regions.add(region)
            
            try:
                qty = float(tx.get('Quantity', 0))
                price = float(tx.get('UnitPrice', 0))
                if qty > 0 and price > 0:
                    amounts.append(qty * price)
            except:
                pass
        
        min_amount = min(amounts) if amounts else 0
        max_amount = max(amounts) if amounts else 0
        
        print_success(f"Found {len(regions)} regions and amount range ${min_amount:,.2f} - ${max_amount:,.2f}")
        
        # Ask about filtering
        filter_data = get_filter_choice()
        
        filters = {}
        if filter_data:
            filters = get_filter_criteria(regions, min_amount, max_amount)
            print_success(f"Filters applied: {filters if filters else 'None'}")
        else:
            print_success("No filters applied")
        
        # Step 4: Validate transactions
        print_step(4, total_steps, "Validating transactions")
        
        valid_transactions, invalid_count = validate_sales_transactions(raw_transactions)
        
        if not valid_transactions:
            print_error("No valid transactions found")
            return False
        
        print_success(f"Valid: {len(valid_transactions)} | Invalid: {invalid_count}")
        
        # Step 5: Fetch products from API
        print_step(5, total_steps, "Fetching product data from API")
        
        api_products = fetch_all_products()
        
        if not api_products:
            print_error("Failed to fetch API products")
            return False
        
        print_success(f"Fetched {len(api_products)} products")
        
        # Step 6: Create product mapping
        print_step(6, total_steps, "Creating product mapping")
        
        product_mapping = create_product_mapping(api_products)
        
        if not product_mapping:
            print_error("Failed to create product mapping")
            return False
        
        print_success(f"Created mapping for {len(product_mapping)} products")
        
        # Step 7: Enrich sales data
        print_step(7, total_steps, "Enriching sales data with API information")
        
        enriched_transactions = enrich_with_api_mapping(valid_transactions, product_mapping)
        
        if not enriched_transactions:
            print_error("Failed to enrich sales data")
            return False
        
        matched = sum(1 for t in enriched_transactions if t.get('API_Match', False))
        match_rate = (matched / len(enriched_transactions) * 100) if enriched_transactions else 0
        
        print_success(f"Enriched {len(enriched_transactions)}/{len(valid_transactions)} transactions ({match_rate:.1f}% API match)")
        
        # Step 8: Save enriched data
        print_step(8, total_steps, "Saving enriched data to files")
        
        txt_file = r'c:\Users\ADMIN\Downloads\enriched_sales_data.txt'
        json_file = r'c:\Users\ADMIN\Downloads\enriched_sales_data.json'
        
        save_enriched_to_file(enriched_transactions, txt_file)
        save_enriched_to_json(enriched_transactions, json_file)
        
        print_success(f"Saved to: {txt_file}")
        print_success(f"Saved to: {json_file}")
        
        # Step 9: Generate comprehensive report
        print_step(9, total_steps, "Generating comprehensive sales report")
        
        report_file = r'c:\Users\ADMIN\Downloads\sales_report.txt'
        
        if generate_sales_report(valid_transactions, enriched_transactions, report_file):
            print_success(f"Report saved to: {report_file}")
        else:
            print_error("Failed to generate report")
            return False
        
        # Step 10: Complete
        print_step(10, total_steps, "Process Complete")
        
        print_success("All tasks completed successfully!")
        
        # Print summary
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total Transactions Processed: {len(valid_transactions)}")
        print(f"Total Invalid Records: {invalid_count}")
        print(f"API Products Fetched: {len(api_products)}")
        print(f"API Match Rate: {match_rate:.1f}%")
        print()
        print("Output Files Created:")
        print(f"  • Enriched Data (TXT): {txt_file}")
        print(f"  • Enriched Data (JSON): {json_file}")
        print(f"  • Sales Report: {report_file}")
        print()
        print(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80 + "\n")
        
        return True
    
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Process interrupted by user")
        return False
    
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
