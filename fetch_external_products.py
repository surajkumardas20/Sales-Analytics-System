"""
Fetch product data from DummyJSON API and integrate with sales analysis
"""

import requests
import json


def fetch_external_products():
    """
    Fetches product data from DummyJSON API
    
    Returns: dictionary with product information
    """
    try:
        print("Fetching products from DummyJSON API...")
        response = requests.get('https://dummyjson.com/products')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Successfully fetched {data['total']} products\n")
            return data
        else:
            print(f"✗ Error: Status code {response.status_code}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching data: {e}")
        return None


def analyze_external_products(api_data):
    """
    Analyzes external product data and compares with internal sales data
    """
    if not api_data or 'products' not in api_data:
        return None
    
    products = api_data['products']
    
    # Aggregate by category
    category_stats = {}
    price_ranges = {'0-50': 0, '50-100': 0, '100-500': 0, '500-1000': 0, '1000+': 0}
    brand_stats = {}
    
    for product in products:
        # Category analysis
        category = product.get('category', 'Unknown')
        if category not in category_stats:
            category_stats[category] = {
                'count': 0,
                'avg_price': 0,
                'total_price': 0,
                'products': []
            }
        
        category_stats[category]['count'] += 1
        category_stats[category]['total_price'] += product.get('price', 0)
        category_stats[category]['products'].append(product.get('title', 'Unknown'))
        
        # Price range analysis
        price = product.get('price', 0)
        if price <= 50:
            price_ranges['0-50'] += 1
        elif price <= 100:
            price_ranges['50-100'] += 1
        elif price <= 500:
            price_ranges['100-500'] += 1
        elif price <= 1000:
            price_ranges['500-1000'] += 1
        else:
            price_ranges['1000+'] += 1
        
        # Brand analysis
        brand = product.get('brand', 'Unknown')
        if brand not in brand_stats:
            brand_stats[brand] = {'count': 0, 'avg_price': 0}
        brand_stats[brand]['count'] += 1
    
    # Calculate averages
    for category in category_stats:
        category_stats[category]['avg_price'] = (
            category_stats[category]['total_price'] / category_stats[category]['count']
        )
    
    return {
        'total_products': api_data['total'],
        'categories': category_stats,
        'price_ranges': price_ranges,
        'brands': brand_stats
    }


def compare_with_sales_data(api_analysis, sales_products):
    """
    Compares external product data with internal sales data
    """
    print("="*90)
    print("EXTERNAL PRODUCT DATA ANALYSIS (DummyJSON API)")
    print("="*90)
    
    if not api_analysis:
        print("\n✗ Could not analyze external data")
        return
    
    print(f"\nTotal Products Available: {api_analysis['total_products']}")
    
    # Category breakdown
    print("\n" + "="*90)
    print("PRODUCT CATEGORIES")
    print("="*90)
    
    print(f"\n{'Category':<25} {'Count':<12} {'Avg Price':<20}")
    print("-"*90)
    
    sorted_categories = sorted(
        api_analysis['categories'].items(),
        key=lambda x: x[1]['count'],
        reverse=True
    )
    
    for category, stats in sorted_categories:
        print(f"{category:<25} {stats['count']:<12} ${stats['avg_price']:>17,.2f}")
    
    # Price range distribution
    print("\n" + "="*90)
    print("PRICE RANGE DISTRIBUTION")
    print("="*90)
    
    print(f"\n{'Price Range':<20} {'Count':<15} {'Percentage':<15}")
    print("-"*90)
    
    total = api_analysis['total_products']
    for price_range, count in api_analysis['price_ranges'].items():
        percentage = (count / total) * 100 if total > 0 else 0
        print(f"{price_range:<20} {count:<15} {percentage:>13.2f}%")
    
    # Top brands
    print("\n" + "="*90)
    print("TOP 10 BRANDS (by product count)")
    print("="*90)
    
    sorted_brands = sorted(
        api_analysis['brands'].items(),
        key=lambda x: x[1]['count'],
        reverse=True
    )[:10]
    
    print(f"\n{'Brand':<30} {'Product Count':<15}")
    print("-"*90)
    
    for brand, stats in sorted_brands:
        print(f"{brand:<30} {stats['count']:<15}")
    
    # Comparison with sales data
    print("\n" + "="*90)
    print("COMPARISON: API PRODUCTS vs SALES DATA")
    print("="*90)
    
    print(f"""
API Products:          {api_analysis['total_products']} products
Sales Products:        {len(sales_products)} products
Categories Found:      {len(api_analysis['categories'])}

Price Insights:
  - Most affordable range: $0-$50 ({api_analysis['price_ranges']['0-50']} products)
  - Premium range: $1000+ ({api_analysis['price_ranges']['1000+']} products)
  - Most common category: {sorted_categories[0][0]} ({sorted_categories[0][1]['count']} products)
  - Highest avg price category: {max(sorted_categories, key=lambda x: x[1]['avg_price'])[0]}
    """)
    
    # Recommendations
    print("\n" + "="*90)
    print("RECOMMENDATIONS FOR PRODUCT EXPANSION")
    print("="*90)
    
    api_categories = set(api_analysis['categories'].keys())
    sales_categories = set([p[0] for p in sales_products])
    
    missing_categories = api_categories - sales_categories
    
    if missing_categories:
        print(f"\nProduct Categories Available in Market but NOT in Current Sales:")
        for i, category in enumerate(sorted(missing_categories), 1):
            count = api_analysis['categories'][category]['count']
            avg_price = api_analysis['categories'][category]['avg_price']
            print(f"  {i}. {category}: {count} products available (Avg: ${avg_price:,.2f})")
    else:
        print("\nYour sales catalog covers most market categories!")


# Main execution
if __name__ == "__main__":
    from read_sales_data import read_sales_data
    from parse_transactions import parse_transactions
    from top_selling_products import top_selling_products
    
    try:
        # Fetch external data
        api_data = fetch_external_products()
        
        if api_data:
            # Analyze external products
            api_analysis = analyze_external_products(api_data)
            
            # Load sales data for comparison
            filename = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
            raw_lines = read_sales_data(filename)
            transactions = parse_transactions(raw_lines)
            sales_products = top_selling_products(transactions, n=1000)
            
            # Compare
            compare_with_sales_data(api_analysis, sales_products)
            
            # Save API data to file for reference
            output_file = r'c:\Users\ADMIN\Downloads\external_products_data.json'
            with open(output_file, 'w') as f:
                json.dump(api_data, f, indent=2)
            print(f"\n✓ API data saved to: {output_file}")
        else:
            print("✗ Failed to fetch and analyze external products")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
