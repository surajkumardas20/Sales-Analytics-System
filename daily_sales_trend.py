def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date

    Expected Output Format:
    {
        '2024-12-01': {
            'revenue': 125000.0,
            'transaction_count': 8,
            'unique_customers': 6
        },
        '2024-12-02': {...},
        ...
    }

    Requirements:
    - Group by date
    - Calculate daily revenue
    - Count daily transactions
    - Count unique customers per day
    - Sort chronologically
    """
    
    daily_stats = {}
    
    # Aggregate data by date
    for transaction in transactions:
        date = transaction['Date']
        customer_id = transaction['CustomerID']
        revenue = transaction['Quantity'] * transaction['UnitPrice']
        
        if date not in daily_stats:
            daily_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }
        
        daily_stats[date]['revenue'] += revenue
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['unique_customers'].add(customer_id)
    
    # Convert sets to counts and sort chronologically
    for date in daily_stats:
        daily_stats[date]['unique_customers'] = len(daily_stats[date]['unique_customers'])
    
    # Sort by date
    sorted_daily_stats = dict(sorted(daily_stats.items()))
    
    return sorted_daily_stats


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
        
        # Get daily sales trend
        daily_trends = daily_sales_trend(transactions)
        
        print("="*90)
        print("DAILY SALES TREND ANALYSIS")
        print("="*90)
        
        print(f"\n{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Unique Customers':<20}")
        print("-"*90)
        
        for date, stats in daily_trends.items():
            print(f"{date:<15} ${stats['revenue']:>17,.2f} {stats['transaction_count']:<15} {stats['unique_customers']:<20}")
        
        # Summary statistics
        print("\n" + "="*90)
        print("DAILY TREND STATISTICS")
        print("="*90)
        
        total_days = len(daily_trends)
        revenues = [stats['revenue'] for stats in daily_trends.values()]
        transactions_per_day = [stats['transaction_count'] for stats in daily_trends.values()]
        customers_per_day = [stats['unique_customers'] for stats in daily_trends.values()]
        
        total_revenue = sum(revenues)
        avg_daily_revenue = total_revenue / total_days if total_days > 0 else 0
        max_daily_revenue = max(revenues) if revenues else 0
        min_daily_revenue = min(revenues) if revenues else 0
        
        # Find dates with max/min
        max_date = max(daily_trends.items(), key=lambda x: x[1]['revenue'])[0]
        min_date = min(daily_trends.items(), key=lambda x: x[1]['revenue'])[0]
        
        print(f"""
Total Days with Sales:          {total_days}
Total Revenue:                  ${total_revenue:,.2f}
Average Daily Revenue:          ${avg_daily_revenue:,.2f}
Highest Daily Revenue:          ${max_daily_revenue:,.2f} (Date: {max_date})
Lowest Daily Revenue:           ${min_daily_revenue:,.2f} (Date: {min_date})

Average Transactions per Day:   {sum(transactions_per_day) / total_days:.2f}
Average Unique Customers/Day:   {sum(customers_per_day) / total_days:.2f}
Max Transactions in a Day:      {max(transactions_per_day)}
Min Transactions in a Day:      {min(transactions_per_day)}
        """)
        
        # Weekly analysis
        print("\n" + "="*90)
        print("WEEKLY SALES ANALYSIS")
        print("="*90)
        
        from datetime import datetime, timedelta
        
        weekly_stats = {}
        for date, stats in daily_trends.items():
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            week_start = date_obj - timedelta(days=date_obj.weekday())
            week_key = f"Week of {week_start.strftime('%Y-%m-%d')}"
            
            if week_key not in weekly_stats:
                weekly_stats[week_key] = {
                    'revenue': 0.0,
                    'days': 0,
                    'transactions': 0
                }
            
            weekly_stats[week_key]['revenue'] += stats['revenue']
            weekly_stats[week_key]['days'] += 1
            weekly_stats[week_key]['transactions'] += stats['transaction_count']
        
        print(f"\n{'Week':<25} {'Revenue':<20} {'Days Active':<15} {'Transactions':<15}")
        print("-"*90)
        
        for week, stats in weekly_stats.items():
            print(f"{week:<25} ${stats['revenue']:>17,.2f} {stats['days']:<15} {stats['transactions']:<15}")
        
        # Best and worst days
        print("\n" + "="*90)
        print("TOP 5 BEST AND WORST DAYS")
        print("="*90)
        
        sorted_by_revenue = sorted(daily_trends.items(), key=lambda x: x[1]['revenue'], reverse=True)
        
        print("\nTop 5 Best Days:")
        print(f"\n{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Customers':<15}")
        print("-"*90)
        
        for i, (date, stats) in enumerate(sorted_by_revenue[:5], 1):
            print(f"{date:<15} ${stats['revenue']:>17,.2f} {stats['transaction_count']:<15} {stats['unique_customers']:<15}")
        
        print("\nTop 5 Worst Days:")
        print(f"\n{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Customers':<15}")
        print("-"*90)
        
        for i, (date, stats) in enumerate(sorted_by_revenue[-5:], 1):
            print(f"{date:<15} ${stats['revenue']:>17,.2f} {stats['transaction_count']:<15} {stats['unique_customers']:<15}")
        
        # Trend direction
        print("\n" + "="*90)
        print("SALES TREND DIRECTION")
        print("="*90)
        
        first_week_revenue = sum([stats['revenue'] for date, stats in list(daily_trends.items())[:7]])
        last_week_revenue = sum([stats['revenue'] for date, stats in list(daily_trends.items())[-7:]])
        
        trend = "📈 UPWARD" if last_week_revenue > first_week_revenue else "📉 DOWNWARD" if last_week_revenue < first_week_revenue else "➡️  STABLE"
        change = ((last_week_revenue - first_week_revenue) / first_week_revenue * 100) if first_week_revenue > 0 else 0
        
        print(f"""
First Week Revenue:     ${first_week_revenue:,.2f}
Last Week Revenue:      ${last_week_revenue:,.2f}
Trend Direction:        {trend}
Change:                 {change:+.2f}%
        """)
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
