"""
Fetch products with pagination and filtering from DummyJSON API
"""

import requests
import json
from datetime import datetime


def fetch_products_with_limit(limit=100, skip=0):
    """
    Fetches products with limit and skip parameters
    
    Args:
        limit (int): Number of products to fetch (max 100)
        skip (int): Number of products to skip
    
    Returns: dictionary with products and metadata
    """
    try:
        print(f"Fetching products with limit={limit}, skip={skip}...")
        response = requests.get(f'https://dummyjson.com/products?limit={limit}&skip={skip}')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Successfully fetched {len(data.get('products', []))} products")
            print(f"  Total available: {data.get('total', 0)}")
            print(f"  Current skip: {data.get('skip', 0)}\n")
            return data
        else:
            print(f"✗ Error: Status code {response.status_code}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching products: {e}")
        return None


def fetch_products_by_category(category):
    """
    Fetches products filtered by category
    
    Args:
        category (str): Category name
    
    Returns: dictionary with filtered products
    """
    try:
        print(f"Fetching products from category: {category}...")
        response = requests.get(f'https://dummyjson.com/products/category/{category}')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Found {len(data.get('products', []))} products in '{category}'\n")
            return data
        else:
            print(f"✗ Category not found: {category}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching category: {e}")
        return None


def fetch_products_by_search(search_term):
    """
    Searches for products by keyword
    
    Args:
        search_term (str): Search keyword
    
    Returns: dictionary with search results
    """
    try:
        print(f"Searching for products: '{search_term}'...")
        response = requests.get(f'https://dummyjson.com/products/search?q={search_term}')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Found {len(data.get('products', []))} products matching '{search_term}'\n")
            return data
        else:
            print(f"✗ Search failed")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error searching products: {e}")
        return None


def analyze_products_batch(products_data):
    """
    Analyzes a batch of products
    """
    if not products_data or 'products' not in products_data:
        return None
    
    products = products_data['products']
    
    analysis = {
        'total_fetched': len(products),
        'total_available': products_data.get('total', 0),
        'categories': {},
        'brands': {},
        'price_stats': {
            'min': float('inf'),
            'max': 0,
            'total': 0,
            'avg': 0
        },
        'rating_stats': {
            'min': 5,
            'max': 0,
            'total': 0,
            'avg': 0
        },
        'stock_stats': {
            'total_units': 0,
            'avg_per_product': 0
        },
        'discount_stats': {
            'max_discount': 0,
            'avg_discount': 0
        }
    }
    
    for product in products:
        # Categories
        category = product.get('category', 'Unknown')
        if category not in analysis['categories']:
            analysis['categories'][category] = 0
        analysis['categories'][category] += 1
        
        # Brands
        brand = product.get('brand', 'Unknown')
        if brand not in analysis['brands']:
            analysis['brands'][brand] = 0
        analysis['brands'][brand] += 1
        
        # Price stats
        price = product.get('price', 0)
        analysis['price_stats']['min'] = min(analysis['price_stats']['min'], price)
        analysis['price_stats']['max'] = max(analysis['price_stats']['max'], price)
        analysis['price_stats']['total'] += price
        
        # Rating stats
        rating = product.get('rating', 0)
        analysis['rating_stats']['min'] = min(analysis['rating_stats']['min'], rating)
        analysis['rating_stats']['max'] = max(analysis['rating_stats']['max'], rating)
        analysis['rating_stats']['total'] += rating
        
        # Stock stats
        stock = product.get('stock', 0)
        analysis['stock_stats']['total_units'] += stock
        
        # Discount stats
        discount = product.get('discountPercentage', 0)
        analysis['discount_stats']['max_discount'] = max(analysis['discount_stats']['max_discount'], discount)
        analysis['discount_stats']['avg_discount'] += discount
    
    # Calculate averages
    if len(products) > 0:
        analysis['price_stats']['avg'] = analysis['price_stats']['total'] / len(products)
        analysis['rating_stats']['avg'] = analysis['rating_stats']['total'] / len(products)
        analysis['stock_stats']['avg_per_product'] = analysis['stock_stats']['total_units'] / len(products)
        analysis['discount_stats']['avg_discount'] = analysis['discount_stats']['avg_discount'] / len(products)
    
    return analysis


def display_analysis(analysis, title):
    """
    Displays analysis results
    """
    if not analysis:
        return
    
    print("="*100)
    print(title)
    print("="*100)
    
    print(f"""
PRODUCT SUMMARY:
  Total Fetched:         {analysis['total_fetched']}
  Total Available:       {analysis['total_available']}
  
PRICE STATISTICS:
  Minimum:               ${analysis['price_stats']['min']:,.2f}
  Maximum:               ${analysis['price_stats']['max']:,.2f}
  Average:               ${analysis['price_stats']['avg']:,.2f}
  Total Value:           ${analysis['price_stats']['total']:,.2f}

RATING STATISTICS:
  Highest Rating:        {analysis['rating_stats']['max']:.1f}/5.0
  Lowest Rating:         {analysis['rating_stats']['min']:.1f}/5.0
  Average Rating:        {analysis['rating_stats']['avg']:.2f}/5.0

STOCK INFORMATION:
  Total Units in Stock:  {analysis['stock_stats']['total_units']:,}
  Avg Units/Product:     {analysis['stock_stats']['avg_per_product']:.1f}

DISCOUNT ANALYSIS:
  Maximum Discount:      {analysis['discount_stats']['max_discount']:.1f}%
  Average Discount:      {analysis['discount_stats']['avg_discount']:.2f}%

CATEGORIES ({len(analysis['categories'])}):
""")
    
    sorted_categories = sorted(analysis['categories'].items(), key=lambda x: x[1], reverse=True)
    for category, count in sorted_categories[:10]:
        percentage = (count / analysis['total_fetched']) * 100
        print(f"  {category:<25} {count:<10} ({percentage:>5.1f}%)")
    
    print(f"\nTOP BRANDS ({min(10, len(analysis['brands']))}):")
    sorted_brands = sorted(analysis['brands'].items(), key=lambda x: x[1], reverse=True)
    for brand, count in sorted_brands[:10]:
        percentage = (count / analysis['total_fetched']) * 100
        print(f"  {brand:<25} {count:<10} ({percentage:>5.1f}%)")


def display_product_list(products, limit=10):
    """
    Displays product list
    """
    print(f"\nTOP {min(limit, len(products))} PRODUCTS:")
    print(f"\n{'ID':<6} {'Title':<35} {'Price':<12} {'Rating':<10} {'Discount':<12} {'Stock':<8}")
    print("-"*100)
    
    for product in products[:limit]:
        product_id = product.get('id', 'N/A')
        title = product.get('title', 'Unknown')[:32]
        price = product.get('price', 0)
        rating = product.get('rating', 0)
        discount = product.get('discountPercentage', 0)
        stock = product.get('stock', 0)
        
        print(f"{product_id:<6} {title:<35} ${price:<11,.2f} {rating:<10.1f} {discount:<11.1f}% {stock:<8}")


# Main execution
if __name__ == "__main__":
    try:
        print("="*100)
        print("PRODUCT PAGINATION & FILTERING ANALYSIS")
        print("="*100 + "\n")
        
        # 1. Fetch with limit
        print("[1/4] FETCHING WITH LIMIT\n")
        products_limit = fetch_products_with_limit(limit=100)
        
        if products_limit:
            analysis_limit = analyze_products_batch(products_limit)
            display_analysis(analysis_limit, "ANALYSIS: PRODUCTS WITH LIMIT=100")
            display_product_list(products_limit['products'], limit=10)
        
        # 2. Fetch by category
        print("\n\n[2/4] FETCHING BY CATEGORY\n")
        products_category = fetch_products_by_category('beauty')
        
        if products_category:
            analysis_category = analyze_products_batch(products_category)
            display_analysis(analysis_category, "ANALYSIS: BEAUTY CATEGORY PRODUCTS")
            display_product_list(products_category['products'], limit=5)
        
        # 3. Search for products
        print("\n\n[3/4] SEARCHING FOR PRODUCTS\n")
        products_search = fetch_products_by_search('laptop')
        
        if products_search:
            analysis_search = analyze_products_batch(products_search)
            display_analysis(analysis_search, "ANALYSIS: SEARCH RESULTS FOR 'LAPTOP'")
            display_product_list(products_search['products'], limit=5)
        
        # 4. Comparison across different fetches
        print("\n\n[4/4] COMPARATIVE ANALYSIS\n")
        print("="*100)
        print("COMPARATIVE METRICS ACROSS DIFFERENT FETCH METHODS")
        print("="*100)
        
        if analysis_limit and analysis_category and analysis_search:
            print(f"\n{'Metric':<30} {'Limit=100':<25} {'Category=Beauty':<25} {'Search=Laptop':<25}")
            print("-"*100)
            print(f"{'Products Fetched':<30} {analysis_limit['total_fetched']:<25} {analysis_category['total_fetched']:<25} {analysis_search['total_fetched']:<25}")
            print(f"{'Avg Price':<30} ${analysis_limit['price_stats']['avg']:<24,.2f} ${analysis_category['price_stats']['avg']:<24,.2f} ${analysis_search['price_stats']['avg']:<24,.2f}")
            print(f"{'Avg Rating':<30} {analysis_limit['rating_stats']['avg']:<25.2f} {analysis_category['rating_stats']['avg']:<25.2f} {analysis_search['rating_stats']['avg']:<25.2f}")
            print(f"{'Avg Discount':<30} {analysis_limit['discount_stats']['avg_discount']:<24.2f}% {analysis_category['discount_stats']['avg_discount']:<24.2f}% {analysis_search['discount_stats']['avg_discount']:<24.2f}%")
            print(f"{'Total Stock Units':<30} {analysis_limit['stock_stats']['total_units']:<25,} {analysis_category['stock_stats']['total_units']:<25,} {analysis_search['stock_stats']['total_units']:<25,}")
        
        # Export data
        print("\n\n" + "="*100)
        print("EXPORTING DATA")
        print("="*100 + "\n")
        
        export_data = {
            'fetch_timestamp': datetime.now().isoformat(),
            'limit_100': products_limit,
            'category_beauty': products_category,
            'search_laptop': products_search
        }
        
        output_file = r'c:\Users\ADMIN\Downloads\products_pagination_analysis.json'
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✓ Data exported to: {output_file}")
        
        print("\n✓ Analysis complete!")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
