"""
Comprehensive Sales Data Analysis
Applies all analysis functions to the cleaned sales data
"""

from read_sales_data import read_sales_data
from parse_transactions import parse_transactions
from validate_and_filter import validate_and_filter
from calculate_total_revenue import calculate_total_revenue
from region_wise_sales import region_wise_sales
from top_selling_products import top_selling_products
from customer_analysis import customer_analysis


def main():
    try:
        filename = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
        
        print("\n" + "="*100)
        print("COMPREHENSIVE SALES DATA ANALYSIS")
        print("="*100)
        
        # Step 1: Read and Parse Data
        print("\n[1/6] Reading and parsing data...")
        raw_lines = read_sales_data(filename)
        transactions = parse_transactions(raw_lines)
        print(f"✓ Successfully loaded {len(transactions)} transactions")
        
        # Step 2: Validate and Filter
        print("\n[2/6] Validating transactions...")
        valid_trans, invalid_count, validation_summary = validate_and_filter(transactions)
        print(f"✓ Validation complete: {validation_summary['valid']} valid, {invalid_count} invalid")
        
        # Step 3: Calculate Total Revenue
        print("\n[3/6] Calculating total revenue...")
        total_revenue = calculate_total_revenue(valid_trans)
        print(f"✓ Total Revenue: ${total_revenue:,.2f}")
        
        # Step 4: Region-wise Analysis
        print("\n[4/6] Analyzing region-wise sales...")
        region_stats = region_wise_sales(valid_trans)
        print(f"✓ Found {len(region_stats)} regions")
        
        # Step 5: Top Selling Products
        print("\n[5/6] Identifying top selling products...")
        top_products = top_selling_products(valid_trans, n=10)
        print(f"✓ Found {len(top_products)} top products")
        
        # Step 6: Customer Analysis
        print("\n[6/6] Analyzing customer patterns...")
        customers = customer_analysis(valid_trans)
        print(f"✓ Found {len(customers)} unique customers")
        
        # ===== COMPREHENSIVE REPORT =====
        print("\n\n" + "="*100)
        print("EXECUTIVE SUMMARY")
        print("="*100)
        
        print(f"""
Total Transactions:     {len(valid_trans)}
Total Revenue:          ${total_revenue:,.2f}
Unique Customers:       {len(customers)}
Unique Regions:         {len(region_stats)}
Unique Products:        {len(top_selling_products(valid_trans, n=1000))}
        """)
        
        # ===== REGION-WISE BREAKDOWN =====
        print("\n" + "="*100)
        print("REGION-WISE SALES BREAKDOWN")
        print("="*100)
        
        print(f"\n{'Region':<15} {'Total Sales':<20} {'Transactions':<15} {'Percentage':<12}")
        print("-"*100)
        
        for region, stats in region_stats.items():
            print(f"{region:<15} ${stats['total_sales']:>17,.2f} {stats['transaction_count']:>14} {stats['percentage']:>10.2f}%")
        
        # ===== TOP PRODUCTS =====
        print("\n" + "="*100)
        print("TOP 10 SELLING PRODUCTS (BY QUANTITY)")
        print("="*100)
        
        print(f"\n{'Rank':<6} {'Product Name':<30} {'Quantity':<12} {'Revenue':<20} {'Avg Price':<15}")
        print("-"*100)
        
        for i, (product_name, quantity, revenue) in enumerate(top_products, 1):
            avg_price = revenue / quantity if quantity > 0 else 0
            print(f"{i:<6} {product_name:<30} {quantity:<12} ${revenue:>17,.2f} ${avg_price:>12,.2f}")
        
        # ===== TOP CUSTOMERS =====
        print("\n" + "="*100)
        print("TOP 10 CUSTOMERS BY TOTAL SPENDING")
        print("="*100)
        
        print(f"\n{'Rank':<6} {'Customer ID':<15} {'Total Spent':<20} {'Purchases':<15} {'Avg Order Value':<20}")
        print("-"*100)
        
        top_customers = list(customers.items())[:10]
        for i, (customer_id, stats) in enumerate(top_customers, 1):
            print(f"{i:<6} {customer_id:<15} ${stats['total_spent']:>17,.2f} {stats['purchase_count']:<15} ${stats['avg_order_value']:>17,.2f}")
        
        # ===== KEY METRICS =====
        print("\n" + "="*100)
        print("KEY PERFORMANCE INDICATORS")
        print("="*100)
        
        avg_order_value = total_revenue / len(valid_trans)
        avg_customer_value = total_revenue / len(customers)
        
        # Get top region and customer
        top_region = list(region_stats.items())[0]
        top_customer = list(customers.items())[0]
        
        print(f"""
Average Transaction Value:  ${avg_order_value:,.2f}
Average Customer Spend:      ${avg_customer_value:,.2f}
Purchases per Customer:      {len(valid_trans) / len(customers):.2f}

Top Performing Region:       {top_region[0]} (${top_region[1]['total_sales']:,.2f})
Top Spending Customer:       {top_customer[0]} (${top_customer[1]['total_spent']:,.2f})

Total Units Sold:            {sum(qty for _, qty, _ in top_selling_products(valid_trans, n=1000)):,}
        """)
        
        # ===== INSIGHTS =====
        print("\n" + "="*100)
        print("KEY INSIGHTS")
        print("="*100)
        
        # Product insights
        top_product = top_products[0]
        bottom_region = list(region_stats.items())[-1]
        
        print(f"""
1. PRODUCT PERFORMANCE
   - Best-selling product: {top_product[0]} ({top_product[1]} units)
   - Product contributes to ${top_product[2]:,.2f} in revenue

2. REGIONAL ANALYSIS
   - Strongest region: {top_region[0]} ({top_region[1]['percentage']:.1f}% of revenue)
   - Weakest region: {bottom_region[0]} ({bottom_region[1]['percentage']:.1f}% of revenue)
   - Gap: {top_region[1]['percentage'] - bottom_region[1]['percentage']:.1f} percentage points

3. CUSTOMER INSIGHTS
   - Top customer ({top_customer[0]}) represents {(top_customer[1]['total_spent']/total_revenue)*100:.1f}% of revenue
   - Average customer makes {len(valid_trans) / len(customers):.1f} purchases
   - Customer concentration: High (top 10% contribute significantly)

4. SALES DISTRIBUTION
   - Revenue range: ${min(qty*price for trans in valid_trans for qty in [trans['Quantity']] for price in [trans['UnitPrice']]):,.2f} to ${max(qty*price for trans in valid_trans for qty in [trans['Quantity']] for price in [trans['UnitPrice']]):,.2f}
   - Most transactions are in {list(region_stats.keys())[0]} region
        """)
        
        print("\n" + "="*100)
        print("END OF REPORT")
        print("="*100 + "\n")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
