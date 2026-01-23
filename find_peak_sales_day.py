def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)

    Expected Output Format:
    ('2024-12-15', 185000.0, 12)
    """
    
    daily_stats = {}
    
    # Aggregate data by date
    for transaction in transactions:
        date = transaction['Date']
        revenue = transaction['Quantity'] * transaction['UnitPrice']
        
        if date not in daily_stats:
            daily_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0
            }
        
        daily_stats[date]['revenue'] += revenue
        daily_stats[date]['transaction_count'] += 1
    
    # Find the date with highest revenue
    if not daily_stats:
        return None
    
    peak_date = max(daily_stats.items(), key=lambda x: x[1]['revenue'])
    
    return (peak_date[0], peak_date[1]['revenue'], peak_date[1]['transaction_count'])


# Test the function
if __name__ == "__main__":
    from read_sales_data import read_sales_data
    from parse_transactions import parse_transactions
    from daily_sales_trend import daily_sales_trend
    from calculate_total_revenue import calculate_total_revenue
    
    try:
        filename = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
        
        # Read and parse
        raw_lines = read_sales_data(filename)
        transactions = parse_transactions(raw_lines)
        
        print(f"Total transactions: {len(transactions)}\n")
        
        # Find peak sales day
        peak_date, peak_revenue, peak_count = find_peak_sales_day(transactions)
        
        print("="*80)
        print("PEAK SALES DAY ANALYSIS")
        print("="*80)
        
        print(f"\nPeak Sales Date:        {peak_date}")
        print(f"Peak Day Revenue:       ${peak_revenue:,.2f}")
        print(f"Peak Day Transactions:  {peak_count}")
        
        # Compare with averages
        total_revenue = calculate_total_revenue(transactions)
        daily_trends = daily_sales_trend(transactions)
        avg_daily_revenue = total_revenue / len(daily_trends)
        avg_transactions = len(transactions) / len(daily_trends)
        
        print(f"\nComparison with Averages:")
        print(f"Average Daily Revenue:  ${avg_daily_revenue:,.2f}")
        print(f"Peak vs Average:        {(peak_revenue / avg_daily_revenue):.2f}x")
        print(f"Average Transactions:   {avg_transactions:.2f}")
        print(f"Peak vs Average Trans:  {(peak_count / avg_transactions):.2f}x")
        
        # Calculate percentage of total
        percentage = (peak_revenue / total_revenue) * 100
        print(f"\nPeak Day Impact:        {percentage:.2f}% of total revenue")
        
        # Find transactions on peak day
        print("\n" + "="*80)
        print(f"TRANSACTIONS ON PEAK DAY ({peak_date})")
        print("="*80)
        
        peak_day_transactions = [t for t in transactions if t['Date'] == peak_date]
        peak_day_transactions.sort(key=lambda x: x['Quantity'] * x['UnitPrice'], reverse=True)
        
        print(f"\n{'TransID':<12} {'Product':<25} {'Quantity':<12} {'Unit Price':<15} {'Revenue':<20}")
        print("-"*80)
        
        for trans in peak_day_transactions:
            revenue = trans['Quantity'] * trans['UnitPrice']
            print(f"{trans['TransactionID']:<12} {trans['ProductName']:<25} {trans['Quantity']:<12} ${trans['UnitPrice']:>13,.2f} ${revenue:>17,.2f}")
        
        # Top 5 peak days
        print("\n" + "="*80)
        print("TOP 5 PEAK SALES DAYS")
        print("="*80)
        
        sorted_days = sorted(daily_trends.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]
        
        print(f"\n{'Rank':<6} {'Date':<15} {'Revenue':<20} {'Transactions':<15} {'% of Total':<15}")
        print("-"*80)
        
        for i, (date, stats) in enumerate(sorted_days, 1):
            percentage = (stats['revenue'] / total_revenue) * 100
            print(f"{i:<6} {date:<15} ${stats['revenue']:>17,.2f} {stats['transaction_count']:<15} {percentage:>13.2f}%")
        
        # Day of week analysis for peak day
        print("\n" + "="*80)
        print("DAY OF WEEK ANALYSIS")
        print("="*80)
        
        from datetime import datetime
        
        peak_datetime = datetime.strptime(peak_date, '%Y-%m-%d')
        day_of_week = peak_datetime.strftime('%A')
        
        print(f"\nPeak sales day falls on: {day_of_week}")
        
        # Analyze all dates by day of week
        day_of_week_stats = {}
        for date, stats in daily_trends.items():
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            dow = date_obj.strftime('%A')
            
            if dow not in day_of_week_stats:
                day_of_week_stats[dow] = {
                    'revenue': 0.0,
                    'days': 0,
                    'transactions': 0
                }
            
            day_of_week_stats[dow]['revenue'] += stats['revenue']
            day_of_week_stats[dow]['days'] += 1
            day_of_week_stats[dow]['transactions'] += stats['transaction_count']
        
        # Sort by revenue
        sorted_dow = sorted(day_of_week_stats.items(), key=lambda x: x[1]['revenue'], reverse=True)
        
        print(f"\n{'Day of Week':<15} {'Total Revenue':<20} {'Avg Revenue/Day':<20} {'Avg Trans/Day':<15}")
        print("-"*80)
        
        for dow, stats in sorted_dow:
            avg_revenue = stats['revenue'] / stats['days'] if stats['days'] > 0 else 0
            avg_trans = stats['transactions'] / stats['days'] if stats['days'] > 0 else 0
            print(f"{dow:<15} ${stats['revenue']:>17,.2f} ${avg_revenue:>17,.2f} {avg_trans:>13.2f}")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
