def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics

    Expected Output Format:
    {
        'North': {
            'total_sales': 450000.0,
            'transaction_count': 15,
            'percentage': 29.13
        },
        'South': {...},
        ...
    }

    Requirements:
    - Calculate total sales per region
    - Count transactions per region
    - Calculate percentage of total sales
    - Sort by total_sales in descending order
    """
    
    region_stats = {}
    total_revenue = 0.0
    
    # First pass: calculate total revenue and gather region data
    for transaction in transactions:
        region = transaction['Region']
        sales_amount = transaction['Quantity'] * transaction['UnitPrice']
        total_revenue += sales_amount
        
        if region not in region_stats:
            region_stats[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }
        
        region_stats[region]['total_sales'] += sales_amount
        region_stats[region]['transaction_count'] += 1
    
    # Second pass: calculate percentages and sort
    for region in region_stats:
        percentage = (region_stats[region]['total_sales'] / total_revenue) * 100
        region_stats[region]['percentage'] = round(percentage, 2)
    
    # Sort by total_sales in descending order
    sorted_regions = dict(sorted(region_stats.items(), 
                                 key=lambda x: x[1]['total_sales'], 
                                 reverse=True))
    
    return sorted_regions


# Test the function
if __name__ == "__main__":
    from read_sales_data import read_sales_data
    from parse_transactions import parse_transactions
    from calculate_total_revenue import calculate_total_revenue
    
    try:
        filename = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
        
        # Read and parse
        raw_lines = read_sales_data(filename)
        transactions = parse_transactions(raw_lines)
        
        print(f"Total transactions: {len(transactions)}\n")
        
        # Calculate region-wise sales
        region_stats = region_wise_sales(transactions)
        
        # Calculate total revenue for reference
        total_revenue = calculate_total_revenue(transactions)
        
        print("="*70)
        print("REGION-WISE SALES ANALYSIS")
        print("="*70)
        
        print(f"\n{'Region':<15} {'Total Sales':<20} {'Transactions':<15} {'Percentage':<12}")
        print("-"*70)
        
        for region, stats in region_stats.items():
            print(f"{region:<15} ${stats['total_sales']:>17,.2f} {stats['transaction_count']:>14} {stats['percentage']:>10.2f}%")
        
        print("-"*70)
        print(f"{'TOTAL':<15} ${total_revenue:>17,.2f} {len(transactions):>14} {100.0:>10.2f}%")
        
        # Additional insights
        print("\n" + "="*70)
        print("REGION INSIGHTS")
        print("="*70)
        
        top_region = list(region_stats.items())[0]
        print(f"\nTop Performing Region: {top_region[0]}")
        print(f"  - Total Sales: ${top_region[1]['total_sales']:,.2f}")
        print(f"  - Transaction Count: {top_region[1]['transaction_count']}")
        print(f"  - Average Transaction Value: ${top_region[1]['total_sales'] / top_region[1]['transaction_count']:,.2f}")
        
        bottom_region = list(region_stats.items())[-1]
        print(f"\nLowest Performing Region: {bottom_region[0]}")
        print(f"  - Total Sales: ${bottom_region[1]['total_sales']:,.2f}")
        print(f"  - Transaction Count: {bottom_region[1]['transaction_count']}")
        print(f"  - Average Transaction Value: ${bottom_region[1]['total_sales'] / bottom_region[1]['transaction_count']:,.2f}")
        
        # Calculate sales difference
        difference = top_region[1]['total_sales'] - bottom_region[1]['total_sales']
        percentage_diff = (difference / bottom_region[1]['total_sales']) * 100
        print(f"\nSales Difference: ${difference:,.2f} ({percentage_diff:.1f}% more than {bottom_region[0]})")
        
        # Transaction count analysis
        print("\n" + "="*70)
        print("TRANSACTION COUNT BY REGION")
        print("="*70)
        
        for region, stats in region_stats.items():
            avg_value = stats['total_sales'] / stats['transaction_count']
            print(f"{region}: {stats['transaction_count']} transactions (Avg: ${avg_value:,.2f}/transaction)")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
