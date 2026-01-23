def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)

    Expected Output: Single number representing sum of (Quantity * UnitPrice)
    Example: 1545000.50
    """
    total_revenue = 0.0
    
    for transaction in transactions:
        revenue = transaction['Quantity'] * transaction['UnitPrice']
        total_revenue += revenue
    
    return total_revenue


# Test the function
if __name__ == "__main__":
    from read_sales_data import read_sales_data
    from parse_transactions import parse_transactions
    
    try:
        filename = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
        
        # Read and parse
        raw_lines = read_sales_data(filename)
        transactions = parse_transactions(raw_lines)
        
        print(f"Total transactions: {len(transactions)}\n")
        
        # Calculate total revenue
        total_revenue = calculate_total_revenue(transactions)
        
        print(f"Total Revenue: ${total_revenue:,.2f}")
        
        # Additional statistics
        print("\n" + "="*60)
        print("REVENUE BREAKDOWN:")
        print("="*60)
        
        # Revenue by region
        revenue_by_region = {}
        for trans in transactions:
            region = trans['Region']
            revenue = trans['Quantity'] * trans['UnitPrice']
            if region not in revenue_by_region:
                revenue_by_region[region] = 0
            revenue_by_region[region] += revenue
        
        print("\nRevenue by Region:")
        for region in sorted(revenue_by_region.keys()):
            revenue = revenue_by_region[region]
            percentage = (revenue / total_revenue) * 100
            print(f"  {region}: ${revenue:,.2f} ({percentage:.1f}%)")
        
        # Revenue by product
        revenue_by_product = {}
        for trans in transactions:
            product = trans['ProductName']
            revenue = trans['Quantity'] * trans['UnitPrice']
            if product not in revenue_by_product:
                revenue_by_product[product] = 0
            revenue_by_product[product] += revenue
        
        print("\nTop 5 Products by Revenue:")
        top_products = sorted(revenue_by_product.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (product, revenue) in enumerate(top_products, 1):
            percentage = (revenue / total_revenue) * 100
            print(f"  {i}. {product}: ${revenue:,.2f} ({percentage:.1f}%)")
        
        # Average transaction value
        avg_transaction = total_revenue / len(transactions)
        print(f"\nAverage Transaction Value: ${avg_transaction:,.2f}")
        
        # Min and max transaction values
        transactions_with_amounts = [(t['TransactionID'], t['Quantity'] * t['UnitPrice']) 
                                     for t in transactions]
        min_trans = min(transactions_with_amounts, key=lambda x: x[1])
        max_trans = max(transactions_with_amounts, key=lambda x: x[1])
        
        print(f"Lowest Transaction: {min_trans[0]} = ${min_trans[1]:,.2f}")
        print(f"Highest Transaction: {max_trans[0]} = ${max_trans[1]:,.2f}")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
