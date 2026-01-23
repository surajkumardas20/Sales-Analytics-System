def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples

    Expected Output Format:
    [
        ('Laptop', 45, 2250000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Mouse', 38, 19000.0),
        ...
    ]

    Requirements:
    - Aggregate by ProductName
    - Calculate total quantity sold
    - Calculate total revenue for each product
    - Sort by TotalQuantity descending
    - Return top n products
    """
    
    product_stats = {}
    
    # Aggregate product data
    for transaction in transactions:
        product_name = transaction['ProductName']
        quantity = transaction['Quantity']
        revenue = quantity * transaction['UnitPrice']
        
        if product_name not in product_stats:
            product_stats[product_name] = {
                'total_quantity': 0,
                'total_revenue': 0.0,
                'transaction_count': 0
            }
        
        product_stats[product_name]['total_quantity'] += quantity
        product_stats[product_name]['total_revenue'] += revenue
        product_stats[product_name]['transaction_count'] += 1
    
    # Convert to list of tuples and sort by total quantity descending
    product_list = [
        (product_name, stats['total_quantity'], stats['total_revenue'])
        for product_name, stats in product_stats.items()
    ]
    
    product_list.sort(key=lambda x: x[1], reverse=True)
    
    # Return top n products
    return product_list[:n]


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
        
        # Get top 5 selling products
        top_products = top_selling_products(transactions, n=5)
        
        print("="*80)
        print("TOP 5 SELLING PRODUCTS (BY QUANTITY)")
        print("="*80)
        
        print(f"\n{'Rank':<6} {'Product Name':<30} {'Quantity':<15} {'Revenue':<20}")
        print("-"*80)
        
        for i, (product_name, quantity, revenue) in enumerate(top_products, 1):
            print(f"{i:<6} {product_name:<30} {quantity:<15} ${revenue:>17,.2f}")
        
        # Get all products statistics
        all_products = top_selling_products(transactions, n=1000)
        
        print("\n" + "="*80)
        print("ALL PRODUCTS STATISTICS")
        print("="*80)
        
        total_quantity = sum(qty for _, qty, _ in all_products)
        total_revenue = sum(rev for _, _, rev in all_products)
        
        print(f"\nTotal unique products: {len(all_products)}")
        print(f"Total quantity sold: {total_quantity:,} units")
        print(f"Total revenue: ${total_revenue:,.2f}")
        
        # Detailed analysis
        print("\n" + "="*80)
        print("DETAILED ANALYSIS - TOP 10 PRODUCTS")
        print("="*80)
        
        top_10 = top_selling_products(transactions, n=10)
        
        print(f"\n{'Rank':<6} {'Product Name':<30} {'Qty':<10} {'Revenue':<20} {'Avg Price':<15}")
        print("-"*80)
        
        for i, (product_name, quantity, revenue) in enumerate(top_10, 1):
            avg_price = revenue / quantity if quantity > 0 else 0
            print(f"{i:<6} {product_name:<30} {quantity:<10} ${revenue:>17,.2f} ${avg_price:>12,.2f}")
        
        # Cumulative analysis
        print("\n" + "="*80)
        print("CUMULATIVE REVENUE ANALYSIS")
        print("="*80)
        
        cumulative_revenue = 0
        cumulative_quantity = 0
        
        print(f"\n{'Top N':<8} {'Products':<15} {'Quantity':<15} {'Revenue':<20} {'% of Total':<12}")
        print("-"*80)
        
        for n_products in [1, 3, 5, 10, len(all_products)]:
            top_n = top_selling_products(transactions, n=n_products)
            cumulative_qty = sum(qty for _, qty, _ in top_n)
            cumulative_rev = sum(rev for _, _, rev in top_n)
            percentage = (cumulative_rev / total_revenue) * 100
            
            print(f"{n_products:<8} {n_products:<15} {cumulative_qty:<15} ${cumulative_rev:>17,.2f} {percentage:>10.2f}%")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
