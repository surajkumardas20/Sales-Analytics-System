def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples

    Expected Output Format:
    [
        ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)
        ('Headphones', 7, 10500.0),
        ...
    ]

    Requirements:
    - Find products with total quantity < threshold
    - Include total quantity and revenue
    - Sort by TotalQuantity ascending
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
                'total_revenue': 0.0
            }
        
        product_stats[product_name]['total_quantity'] += quantity
        product_stats[product_name]['total_revenue'] += revenue
    
    # Filter products below threshold
    low_products = [
        (product_name, stats['total_quantity'], stats['total_revenue'])
        for product_name, stats in product_stats.items()
        if stats['total_quantity'] < threshold
    ]
    
    # Sort by total quantity ascending
    low_products.sort(key=lambda x: x[1])
    
    return low_products


# Test the function
if __name__ == "__main__":
    from read_sales_data import read_sales_data
    from parse_transactions import parse_transactions
    from top_selling_products import top_selling_products
    from calculate_total_revenue import calculate_total_revenue
    
    try:
        filename = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
        
        # Read and parse
        raw_lines = read_sales_data(filename)
        transactions = parse_transactions(raw_lines)
        
        print(f"Total transactions: {len(transactions)}\n")
        
        # Test with different thresholds
        thresholds = [10, 20, 30]
        
        for threshold in thresholds:
            low_products = low_performing_products(transactions, threshold=threshold)
            
            print("="*90)
            print(f"LOW PERFORMING PRODUCTS (Quantity < {threshold} units)")
            print("="*90)
            
            if low_products:
                print(f"\n{'Rank':<6} {'Product Name':<30} {'Quantity':<15} {'Revenue':<20}")
                print("-"*90)
                
                for i, (product_name, quantity, revenue) in enumerate(low_products, 1):
                    print(f"{i:<6} {product_name:<30} {quantity:<15} ${revenue:>17,.2f}")
                
                print(f"\nTotal Low-Performing Products: {len(low_products)}")
                total_quantity = sum(qty for _, qty, _ in low_products)
                total_revenue = sum(rev for _, _, rev in low_products)
                print(f"Combined Quantity: {total_quantity} units")
                print(f"Combined Revenue: ${total_revenue:,.2f}")
            else:
                print(f"\nNo products found with quantity below {threshold} units")
            
            print()
        
        # Detailed analysis with threshold=10
        print("\n" + "="*90)
        print("DETAILED ANALYSIS - LOW PERFORMING PRODUCTS (< 10 units)")
        print("="*90)
        
        low_products_10 = low_performing_products(transactions, threshold=10)
        
        if low_products_10:
            all_products = top_selling_products(transactions, n=1000)
            total_revenue = calculate_total_revenue(transactions)
            
            print(f"\n{'Rank':<6} {'Product':<30} {'Qty':<10} {'Revenue':<20} {'% of Total':<15} {'Avg Price':<15}")
            print("-"*90)
            
            for i, (product_name, quantity, revenue) in enumerate(low_products_10, 1):
                percentage = (revenue / total_revenue) * 100
                avg_price = revenue / quantity if quantity > 0 else 0
                print(f"{i:<6} {product_name:<30} {quantity:<10} ${revenue:>17,.2f} {percentage:>13.2f}% ${avg_price:>12,.2f}")
            
            # Risk assessment
            print("\n" + "="*90)
            print("RISK ASSESSMENT FOR LOW PERFORMERS")
            print("="*90)
            
            for product_name, quantity, revenue in low_products_10:
                # Determine risk level
                if quantity <= 3:
                    risk = "🔴 CRITICAL - Consider discontinuing"
                elif quantity <= 6:
                    risk = "🟠 HIGH - Needs improvement plan"
                else:
                    risk = "🟡 MEDIUM - Monitor closely"
                
                print(f"\n{product_name}")
                print(f"  Quantity: {quantity} units")
                print(f"  Revenue: ${revenue:,.2f}")
                print(f"  Risk Level: {risk}")
            
            # Recommendations
            print("\n" + "="*90)
            print("RECOMMENDATIONS")
            print("="*90)
            
            critical_products = [p for p in low_products_10 if p[1] <= 3]
            high_risk_products = [p for p in low_products_10 if 3 < p[1] <= 6]
            medium_risk_products = [p for p in low_products_10 if 6 < p[1] < 10]
            
            print(f"""
CRITICAL PRODUCTS ({len(critical_products)}): 
  - Consider discontinuing or heavy promotion
  - Review pricing strategy
  - May indicate market mismatch

HIGH RISK PRODUCTS ({len(high_risk_products)}):
  - Launch targeted marketing campaigns
  - Bundle with popular products
  - Review product quality/features

MEDIUM RISK PRODUCTS ({len(medium_risk_products)}):
  - Monitor sales trends
  - Consider promotional pricing
  - Gather customer feedback
            """)
        else:
            print("\nAll products are performing well above the threshold!")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
