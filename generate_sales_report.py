"""
Generate comprehensive sales analytics report
"""

import os
from datetime import datetime
from collections import defaultdict, Counter
from read_sales_data import read_sales_data
from parse_transactions import parse_transactions
from validate_and_filter import validate_and_filter
from enrich_sales_data_raw import (
    parse_sales_data_raw, 
    validate_sales_transactions, 
    enrich_with_api_mapping
)
from fetch_all_products import fetch_all_products
from create_product_mapping import create_product_mapping


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report

    Report Must Include (in this order):

    1. HEADER
       - Report title
       - Generation date and time
       - Total records processed

    2. OVERALL SUMMARY
       - Total Revenue (formatted with commas)
       - Total Transactions
       - Average Order Value
       - Date Range of data

    3. REGION-WISE PERFORMANCE
       - Table showing each region with:
         * Total Sales Amount
         * Percentage of Total
         * Transaction Count
       - Sorted by sales amount descending

    4. TOP 5 PRODUCTS
       - Table with columns: Rank, Product Name, Quantity Sold, Revenue

    5. TOP 5 CUSTOMERS
       - Table with columns: Rank, Customer ID, Total Spent, Order Count

    6. DAILY SALES TREND
       - Table showing: Date, Revenue, Transactions, Unique Customers

    7. PRODUCT PERFORMANCE ANALYSIS
       - Best selling day
       - Low performing products (if any)
       - Average transaction value per region

    8. API ENRICHMENT SUMMARY
       - Total products enriched
       - Success rate percentage
       - List of products that couldn't be enriched
    """
    
    if not transactions or not enriched_transactions:
        print("✗ Error: Missing transaction data")
        return False
    
    try:
        # Create output directory if needed
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Calculate report metrics
        report_data = calculate_report_metrics(transactions, enriched_transactions)
        
        # Generate report content
        report_lines = []
        
        # 1. HEADER
        report_lines.extend(generate_header(len(transactions)))
        
        # 2. OVERALL SUMMARY
        report_lines.extend(generate_overall_summary(report_data))
        
        # 3. REGION-WISE PERFORMANCE
        report_lines.extend(generate_region_performance(report_data))
        
        # 4. TOP 5 PRODUCTS
        report_lines.extend(generate_top_products(report_data))
        
        # 5. TOP 5 CUSTOMERS
        report_lines.extend(generate_top_customers(report_data))
        
        # 6. DAILY SALES TREND
        report_lines.extend(generate_daily_trend(report_data))
        
        # 7. PRODUCT PERFORMANCE ANALYSIS
        report_lines.extend(generate_performance_analysis(report_data))
        
        # 8. API ENRICHMENT SUMMARY
        report_lines.extend(generate_enrichment_summary(enriched_transactions))
        
        # Write report to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        file_size = os.path.getsize(output_file)
        print(f"[OK] Sales report generated: {output_file}")
        print(f"  File size: {file_size:,} bytes")
        print(f"  Records analyzed: {len(transactions)}\n")
        
        # Also print to console
        print('\n'.join(report_lines))
        
        return True
    
    except Exception as e:
        print(f"[ERROR] Error generating report: {e}")
        import traceback
        traceback.print_exc()
        return False


def calculate_report_metrics(transactions, enriched_transactions):
    """
    Calculates all metrics needed for the report
    """
    metrics = {
        'total_revenue': 0,
        'total_transactions': len(transactions),
        'transactions': transactions,
        'enriched_transactions': enriched_transactions,
        'regions': defaultdict(lambda: {'revenue': 0, 'count': 0, 'transactions': []}),
        'products': defaultdict(lambda: {'quantity': 0, 'revenue': 0, 'name': ''}),
        'customers': defaultdict(lambda: {'spent': 0, 'count': 0}),
        'daily_sales': defaultdict(lambda: {'revenue': 0, 'count': 0, 'customers': set()}),
        'dates': [],
    }
    
    for tx in transactions:
        try:
            qty = float(tx.get('Quantity', 0))
            price = float(tx.get('UnitPrice', 0))
            revenue = qty * price
            
            # Overall metrics
            metrics['total_revenue'] += revenue
            
            # Region metrics
            region = tx.get('Region', 'Unknown')
            if region is None or region == '':
                region = 'Unknown'
            metrics['regions'][region]['revenue'] += revenue
            metrics['regions'][region]['count'] += 1
            metrics['regions'][region]['transactions'].append(revenue)
            
            # Product metrics
            product_id = tx.get('ProductID', 'Unknown')
            product_name = tx.get('ProductName', 'Unknown')
            metrics['products'][product_id]['quantity'] += qty
            metrics['products'][product_id]['revenue'] += revenue
            metrics['products'][product_id]['name'] = product_name
            
            # Customer metrics
            customer_id = tx.get('CustomerID', 'Unknown')
            if customer_id is None or customer_id == '':
                customer_id = 'Unknown'
            metrics['customers'][customer_id]['spent'] += revenue
            metrics['customers'][customer_id]['count'] += 1
            
            # Daily metrics
            date = tx.get('Date', 'Unknown')
            if date is None or date == '':
                date = 'Unknown'
            metrics['daily_sales'][date]['revenue'] += revenue
            metrics['daily_sales'][date]['count'] += 1
            metrics['daily_sales'][date]['customers'].add(customer_id)
            metrics['dates'].append(date)
        
        except Exception as e:
            print(f"⚠ Warning: Error processing transaction: {e}")
            continue
    
    metrics['dates'] = sorted(set(metrics['dates']))
    
    return metrics


def generate_header(total_records):
    """
    Generates report header
    """
    lines = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    lines.append("=" * 80)
    lines.append("SALES ANALYTICS REPORT".center(80))
    lines.append("=" * 80)
    lines.append(f"Generated: {timestamp}")
    lines.append(f"Records Processed: {total_records}")
    lines.append("=" * 80)
    lines.append("")
    
    return lines


def generate_overall_summary(metrics):
    """
    Generates overall summary section
    """
    lines = []
    
    total_revenue = metrics['total_revenue']
    total_transactions = metrics['total_transactions']
    avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0
    dates = sorted(metrics['dates'])
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"
    
    lines.append("OVERALL SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Total Revenue:          ${total_revenue:,.2f}")
    lines.append(f"Total Transactions:     {total_transactions:,}")
    lines.append(f"Average Order Value:    ${avg_order_value:,.2f}")
    lines.append(f"Date Range:             {date_range}")
    lines.append("")
    
    return lines


def generate_region_performance(metrics):
    """
    Generates region-wise performance section
    """
    lines = []
    total_revenue = metrics['total_revenue']
    
    lines.append("REGION-WISE PERFORMANCE")
    lines.append("-" * 80)
    lines.append(f"{'Region':<15} {'Sales':<20} {'% of Total':<15} {'Transactions':<15}")
    lines.append("-" * 80)
    
    # Sort regions by revenue descending
    sorted_regions = sorted(
        metrics['regions'].items(),
        key=lambda x: x[1]['revenue'],
        reverse=True
    )
    
    for region, data in sorted_regions:
        revenue = data['revenue']
        count = data['count']
        percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
        
        lines.append(f"{region:<15} ${revenue:>18,.2f} {percentage:>13.2f}% {count:>14,}")
    
    lines.append("")
    
    return lines


def generate_top_products(metrics):
    """
    Generates top 5 products section
    """
    lines = []
    
    lines.append("TOP 5 PRODUCTS")
    lines.append("-" * 80)
    lines.append(f"{'Rank':<8} {'Product Name':<35} {'Qty Sold':<15} {'Revenue':<20}")
    lines.append("-" * 80)
    
    # Sort products by revenue descending
    sorted_products = sorted(
        metrics['products'].items(),
        key=lambda x: x[1]['revenue'],
        reverse=True
    )[:5]
    
    for rank, (product_id, data) in enumerate(sorted_products, 1):
        name = data['name'][:32]
        qty = data['quantity']
        revenue = data['revenue']
        
        lines.append(f"{rank:<8} {name:<35} {qty:>14,.0f} ${revenue:>18,.2f}")
    
    lines.append("")
    
    return lines


def generate_top_customers(metrics):
    """
    Generates top 5 customers section
    """
    lines = []
    
    lines.append("TOP 5 CUSTOMERS")
    lines.append("-" * 80)
    lines.append(f"{'Rank':<8} {'Customer ID':<20} {'Total Spent':<20} {'Order Count':<15}")
    lines.append("-" * 80)
    
    # Sort customers by spending descending
    sorted_customers = sorted(
        metrics['customers'].items(),
        key=lambda x: x[1]['spent'],
        reverse=True
    )[:5]
    
    for rank, (customer_id, data) in enumerate(sorted_customers, 1):
        spent = data['spent']
        count = data['count']
        
        lines.append(f"{rank:<8} {customer_id:<20} ${spent:>18,.2f} {count:>14,}")
    
    lines.append("")
    
    return lines


def generate_daily_trend(metrics):
    """
    Generates daily sales trend section
    """
    lines = []
    
    lines.append("DAILY SALES TREND")
    lines.append("-" * 80)
    lines.append(f"{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Unique Customers':<20}")
    lines.append("-" * 80)
    
    for date in sorted(metrics['daily_sales'].keys()):
        data = metrics['daily_sales'][date]
        revenue = data['revenue']
        count = data['count']
        customers = len(data['customers'])
        
        lines.append(f"{date:<15} ${revenue:>18,.2f} {count:>14,} {customers:>19,}")
    
    lines.append("")
    
    return lines


def generate_performance_analysis(metrics):
    """
    Generates product performance analysis section
    """
    lines = []
    
    lines.append("PRODUCT PERFORMANCE ANALYSIS")
    lines.append("-" * 80)
    
    # Best selling day
    if metrics['daily_sales']:
        best_day = max(
            metrics['daily_sales'].items(),
            key=lambda x: x[1]['revenue']
        )
        lines.append(f"Best Selling Day:       {best_day[0]} (${best_day[1]['revenue']:,.2f})")
    
    # Average transaction value per region
    lines.append("")
    lines.append("Average Transaction Value by Region:")
    lines.append("-" * 80)
    
    for region, data in sorted(metrics['regions'].items()):
        if data['count'] > 0:
            avg_value = sum(data['transactions']) / data['count']
            lines.append(f"  {region:<15} ${avg_value:,.2f}")
    
    # Low performing products (less than average)
    if metrics['products']:
        avg_qty = sum(p['quantity'] for p in metrics['products'].values()) / len(metrics['products'])
        low_performers = [
            (pid, data) for pid, data in metrics['products'].items()
            if data['quantity'] < avg_qty * 0.5
        ]
        
        if low_performers:
            lines.append("")
            lines.append("Low Performing Products (< 50% of avg):")
            lines.append("-" * 80)
            
            for product_id, data in sorted(low_performers, key=lambda x: x[1]['quantity']):
                lines.append(f"  {product_id}: {data['name']} - {data['quantity']:.0f} units (${data['revenue']:,.2f})")
    
    lines.append("")
    
    return lines


def generate_enrichment_summary(enriched_transactions):
    """
    Generates API enrichment summary section
    """
    lines = []
    
    total = len(enriched_transactions)
    matched = sum(1 for t in enriched_transactions if t.get('API_Match', False))
    unmatched = total - matched
    success_rate = (matched / total * 100) if total > 0 else 0
    
    lines.append("API ENRICHMENT SUMMARY")
    lines.append("-" * 80)
    lines.append(f"Total Products Enriched:  {total}")
    lines.append(f"Successfully Matched:     {matched} ({success_rate:.1f}%)")
    lines.append(f"Not Matched:              {unmatched} ({100 - success_rate:.1f}%)")
    
    if unmatched > 0:
        # List unmatched products
        unmatched_products = set()
        for t in enriched_transactions:
            if not t.get('API_Match', False):
                product_name = t.get('ProductName', 'Unknown')
                unmatched_products.add(product_name)
        
        if unmatched_products:
            lines.append("")
            lines.append("Products Not Matched with API:")
            lines.append("-" * 80)
            
            for product_name in sorted(unmatched_products):
                count = sum(
                    1 for t in enriched_transactions
                    if not t.get('API_Match', False) and t.get('ProductName') == product_name
                )
                lines.append(f"  • {product_name} ({count} transactions)")
    
    lines.append("")
    lines.append("=" * 80)
    
    return lines


def save_report_to_file(report_content, output_file):
    """
    Saves report to file
    """
    try:
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✓ Report saved to: {output_file}")
        return True
    
    except Exception as e:
        print(f"✗ Error saving report: {e}")
        return False


# Main execution
if __name__ == "__main__":
    try:
        print(f"\n{'='*120}")
        print("GENERATE SALES ANALYTICS REPORT")
        print(f"{'='*120}\n")
        
        # Step 1: Load raw sales data
        print("Step 1: Loading sales data...")
        print("-" * 120 + "\n")
        
        sales_file = r'c:\Users\ADMIN\Downloads\sales_data.txt'
        raw_transactions = parse_sales_data_raw(sales_file)
        
        if not raw_transactions:
            print("✗ Failed to load sales data")
            exit(1)
        
        # Step 2: Validate
        print("Step 2: Validating transactions...")
        print("-" * 120 + "\n")
        
        valid_transactions, _ = validate_sales_transactions(raw_transactions)
        
        if not valid_transactions:
            print("✗ No valid transactions")
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
        
        # Step 5: Enrich data
        print("Step 5: Enriching sales data...")
        print("-" * 120 + "\n")
        
        enriched_transactions = enrich_with_api_mapping(valid_transactions, product_mapping)
        
        if not enriched_transactions:
            print("✗ Failed to enrich data")
            exit(1)
        
        # Step 6: Generate report
        print("Step 6: Generating comprehensive sales report...")
        print("-" * 120 + "\n")
        
        output_file = r'c:\Users\ADMIN\Downloads\sales_report.txt'
        generate_sales_report(valid_transactions, enriched_transactions, output_file)
        
        print(f"\n{'='*120}")
        print("REPORT GENERATION COMPLETE")
        print(f"{'='*120}\n")
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
