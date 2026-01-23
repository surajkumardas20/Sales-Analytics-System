def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics

    Expected Output Format:
    {
        'C001': {
            'total_spent': 95000.0,
            'purchase_count': 3,
            'avg_order_value': 31666.67,
            'products_bought': ['Laptop', 'Mouse', 'Keyboard']
        },
        'C002': {...},
        ...
    }

    Requirements:
    - Calculate total amount spent per customer
    - Count number of purchases
    - Calculate average order value
    - List unique products bought
    - Sort by total_spent descending
    """
    
    customer_stats = {}
    
    # Aggregate customer data
    for transaction in transactions:
        customer_id = transaction['CustomerID']
        product_name = transaction['ProductName']
        amount_spent = transaction['Quantity'] * transaction['UnitPrice']
        
        if customer_id not in customer_stats:
            customer_stats[customer_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }
        
        customer_stats[customer_id]['total_spent'] += amount_spent
        customer_stats[customer_id]['purchase_count'] += 1
        customer_stats[customer_id]['products_bought'].add(product_name)
    
    # Calculate average order value and convert set to list
    for customer_id in customer_stats:
        stats = customer_stats[customer_id]
        stats['avg_order_value'] = round(stats['total_spent'] / stats['purchase_count'], 2)
        stats['products_bought'] = sorted(list(stats['products_bought']))
    
    # Sort by total_spent descending
    sorted_customers = dict(sorted(customer_stats.items(),
                                    key=lambda x: x[1]['total_spent'],
                                    reverse=True))
    
    return sorted_customers


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
        
        # Get customer analysis
        customers = customer_analysis(transactions)
        
        print("="*100)
        print("CUSTOMER ANALYSIS - TOP 10 CUSTOMERS BY TOTAL SPENDING")
        print("="*100)
        
        print(f"\n{'Rank':<6} {'Customer ID':<15} {'Total Spent':<20} {'Purchases':<15} {'Avg Order Value':<20}")
        print("-"*100)
        
        top_10_customers = list(customers.items())[:10]
        for i, (customer_id, stats) in enumerate(top_10_customers, 1):
            print(f"{i:<6} {customer_id:<15} ${stats['total_spent']:>17,.2f} {stats['purchase_count']:<15} ${stats['avg_order_value']:>17,.2f}")
        
        # Overall customer statistics
        total_customers = len(customers)
        total_spent = sum(stats['total_spent'] for stats in customers.values())
        total_purchases = sum(stats['purchase_count'] for stats in customers.values())
        avg_customer_value = total_spent / total_customers if total_customers > 0 else 0
        
        print("\n" + "="*100)
        print("OVERALL CUSTOMER STATISTICS")
        print("="*100)
        
        print(f"\nTotal Customers: {total_customers}")
        print(f"Total Revenue: ${total_spent:,.2f}")
        print(f"Total Purchases: {total_purchases}")
        print(f"Average Revenue per Customer: ${avg_customer_value:,.2f}")
        print(f"Average Purchases per Customer: {total_purchases / total_customers:.2f}")
        
        # Customer segmentation
        print("\n" + "="*100)
        print("CUSTOMER SEGMENTATION")
        print("="*100)
        
        # Find top spenders, frequent buyers, etc.
        top_spender = list(customers.items())[0]
        most_frequent = max(customers.items(), key=lambda x: x[1]['purchase_count'])
        most_diverse = max(customers.items(), key=lambda x: len(x[1]['products_bought']))
        
        print(f"\nTop Spender: {top_spender[0]}")
        print(f"  - Total Spent: ${top_spender[1]['total_spent']:,.2f}")
        print(f"  - Purchases: {top_spender[1]['purchase_count']}")
        print(f"  - Average Order Value: ${top_spender[1]['avg_order_value']:,.2f}")
        
        print(f"\nMost Frequent Buyer: {most_frequent[0]}")
        print(f"  - Total Purchases: {most_frequent[1]['purchase_count']}")
        print(f"  - Total Spent: ${most_frequent[1]['total_spent']:,.2f}")
        print(f"  - Average Order Value: ${most_frequent[1]['avg_order_value']:,.2f}")
        
        print(f"\nMost Diverse Buyer (Most Different Products): {most_diverse[0]}")
        print(f"  - Products Bought: {len(most_diverse[1]['products_bought'])}")
        print(f"  - Products: {', '.join(most_diverse[1]['products_bought'])}")
        print(f"  - Total Spent: ${most_diverse[1]['total_spent']:,.2f}")
        
        # Spending distribution
        print("\n" + "="*100)
        print("SPENDING DISTRIBUTION")
        print("="*100)
        
        spending_ranges = {
            'High Spenders (>$100K)': 0,
            'Medium Spenders ($50K-$100K)': 0,
            'Regular Spenders ($10K-$50K)': 0,
            'Low Spenders (<$10K)': 0
        }
        
        for customer_id, stats in customers.items():
            total_spent = stats['total_spent']
            if total_spent > 100000:
                spending_ranges['High Spenders (>$100K)'] += 1
            elif total_spent >= 50000:
                spending_ranges['Medium Spenders ($50K-$100K)'] += 1
            elif total_spent >= 10000:
                spending_ranges['Regular Spenders ($10K-$50K)'] += 1
            else:
                spending_ranges['Low Spenders (<$10K)'] += 1
        
        print("\nCustomers by Spending Category:")
        for category, count in spending_ranges.items():
            percentage = (count / total_customers) * 100
            print(f"  {category}: {count} customers ({percentage:.1f}%)")
        
        # Detailed view - all customers
        print("\n" + "="*100)
        print("ALL CUSTOMERS (SORTED BY TOTAL SPENDING)")
        print("="*100)
        
        print(f"\n{'Rank':<6} {'Customer ID':<15} {'Total Spent':<20} {'Purchases':<15} {'Avg Order':<18} {'Products':<30}")
        print("-"*100)
        
        for i, (customer_id, stats) in enumerate(customers.items(), 1):
            products_str = ', '.join(stats['products_bought'][:2])
            if len(stats['products_bought']) > 2:
                products_str += f", +{len(stats['products_bought']) - 2} more"
            print(f"{i:<6} {customer_id:<15} ${stats['total_spent']:>17,.2f} {stats['purchase_count']:<15} ${stats['avg_order_value']:>16,.2f} {products_str:<30}")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
