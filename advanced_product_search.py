"""
Advanced product search with filtering and competitive analysis
"""

import requests
import json
from datetime import datetime


def search_products(query):
    """
    Searches for products by keyword
    
    Args:
        query (str): Search keyword
    
    Returns: dictionary with search results
    """
    try:
        print(f"Searching for: '{query}'...")
        response = requests.get(f'https://dummyjson.com/products/search?q={query}')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Found {len(data.get('products', []))} products\n")
            return data
        else:
            print(f"✗ Error: Status code {response.status_code}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error searching products: {e}")
        return None


def analyze_search_results(search_results):
    """
    Performs detailed analysis of search results
    """
    if not search_results or 'products' not in search_results:
        return None
    
    products = search_results['products']
    
    analysis = {
        'total_results': len(products),
        'categories': {},
        'brands': {},
        'price_tiers': {
            'budget': [],      # < $50
            'mid_range': [],   # $50-$500
            'premium': [],     # $500-$2000
            'luxury': []       # > $2000
        },
        'rating_segments': {
            'excellent': [],   # >= 4.5
            'good': [],        # 4.0-4.5
            'average': [],     # 3.0-4.0
            'poor': []         # < 3.0
        },
        'price_stats': {
            'min': float('inf'),
            'max': 0,
            'total': 0,
            'avg': 0,
            'median': 0
        },
        'rating_stats': {
            'min': 5,
            'max': 0,
            'total': 0,
            'avg': 0
        },
        'discount_stats': {
            'max': 0,
            'avg': 0,
            'total': 0
        },
        'stock_stats': {
            'total': 0,
            'avg': 0,
            'out_of_stock': 0
        }
    }
    
    prices = []
    ratings = []
    
    for product in products:
        # Category
        category = product.get('category', 'Unknown')
        if category not in analysis['categories']:
            analysis['categories'][category] = {'count': 0, 'products': []}
        analysis['categories'][category]['count'] += 1
        analysis['categories'][category]['products'].append(product.get('title', ''))
        
        # Brand
        brand = product.get('brand', 'Unknown')
        if brand not in analysis['brands']:
            analysis['brands'][brand] = 0
        analysis['brands'][brand] += 1
        
        # Price
        price = product.get('price', 0)
        prices.append(price)
        analysis['price_stats']['min'] = min(analysis['price_stats']['min'], price)
        analysis['price_stats']['max'] = max(analysis['price_stats']['max'], price)
        analysis['price_stats']['total'] += price
        
        # Price tier classification
        if price < 50:
            analysis['price_tiers']['budget'].append(product)
        elif price < 500:
            analysis['price_tiers']['mid_range'].append(product)
        elif price < 2000:
            analysis['price_tiers']['premium'].append(product)
        else:
            analysis['price_tiers']['luxury'].append(product)
        
        # Rating
        rating = product.get('rating', 0)
        ratings.append(rating)
        analysis['rating_stats']['min'] = min(analysis['rating_stats']['min'], rating)
        analysis['rating_stats']['max'] = max(analysis['rating_stats']['max'], rating)
        analysis['rating_stats']['total'] += rating
        
        # Rating segment classification
        if rating >= 4.5:
            analysis['rating_segments']['excellent'].append(product)
        elif rating >= 4.0:
            analysis['rating_segments']['good'].append(product)
        elif rating >= 3.0:
            analysis['rating_segments']['average'].append(product)
        else:
            analysis['rating_segments']['poor'].append(product)
        
        # Discount
        discount = product.get('discountPercentage', 0)
        analysis['discount_stats']['max'] = max(analysis['discount_stats']['max'], discount)
        analysis['discount_stats']['total'] += discount
        
        # Stock
        stock = product.get('stock', 0)
        analysis['stock_stats']['total'] += stock
        if stock == 0:
            analysis['stock_stats']['out_of_stock'] += 1
    
    # Calculate averages
    if len(products) > 0:
        analysis['price_stats']['avg'] = analysis['price_stats']['total'] / len(products)
        analysis['rating_stats']['avg'] = analysis['rating_stats']['total'] / len(products)
        analysis['discount_stats']['avg'] = analysis['discount_stats']['total'] / len(products)
        analysis['stock_stats']['avg'] = analysis['stock_stats']['total'] / len(products)
    
    # Calculate median
    if prices:
        prices.sort()
        if len(prices) % 2 == 0:
            analysis['price_stats']['median'] = (prices[len(prices)//2 - 1] + prices[len(prices)//2]) / 2
        else:
            analysis['price_stats']['median'] = prices[len(prices)//2]
    
    return analysis, products


def display_search_results(search_term, analysis, products):
    """
    Displays detailed search results
    """
    if not analysis:
        return
    
    print("="*100)
    print(f"SEARCH RESULTS FOR: '{search_term.upper()}'")
    print("="*100)
    
    print(f"""
SUMMARY:
  Total Products Found:  {analysis['total_results']}
  Categories:            {len(analysis['categories'])}
  Brands:                {len(analysis['brands'])}

PRICE ANALYSIS:
  Minimum:               ${analysis['price_stats']['min']:,.2f}
  Maximum:               ${analysis['price_stats']['max']:,.2f}
  Average:               ${analysis['price_stats']['avg']:,.2f}
  Median:                ${analysis['price_stats']['median']:,.2f}

RATING ANALYSIS:
  Highest:               {analysis['rating_stats']['max']:.1f}/5.0
  Lowest:                {analysis['rating_stats']['min']:.1f}/5.0
  Average:               {analysis['rating_stats']['avg']:.2f}/5.0

DISCOUNT ANALYSIS:
  Maximum Discount:      {analysis['discount_stats']['max']:.1f}%
  Average Discount:      {analysis['discount_stats']['avg']:.2f}%

STOCK INFORMATION:
  Total Units:           {analysis['stock_stats']['total']:,}
  Average per Product:   {analysis['stock_stats']['avg']:.1f}
  Out of Stock:          {analysis['stock_stats']['out_of_stock']}
    """)
    
    # Price tiers
    print("\nPRICE TIER DISTRIBUTION:")
    print("-" * 100)
    tiers = [
        ('Budget (<$50)', analysis['price_tiers']['budget']),
        ('Mid-Range ($50-$500)', analysis['price_tiers']['mid_range']),
        ('Premium ($500-$2000)', analysis['price_tiers']['premium']),
        ('Luxury (>$2000)', analysis['price_tiers']['luxury'])
    ]
    
    for tier_name, tier_products in tiers:
        percentage = (len(tier_products) / len(products)) * 100 if len(products) > 0 else 0
        print(f"{tier_name:<25} {len(tier_products):<10} ({percentage:>5.1f}%)")
    
    # Rating segments
    print("\nRATING DISTRIBUTION:")
    print("-" * 100)
    segments = [
        ('Excellent (4.5+ ⭐)', analysis['rating_segments']['excellent']),
        ('Good (4.0-4.5 ⭐)', analysis['rating_segments']['good']),
        ('Average (3.0-4.0 ⭐)', analysis['rating_segments']['average']),
        ('Poor (< 3.0 ⭐)', analysis['rating_segments']['poor'])
    ]
    
    for segment_name, segment_products in segments:
        percentage = (len(segment_products) / len(products)) * 100 if len(products) > 0 else 0
        print(f"{segment_name:<25} {len(segment_products):<10} ({percentage:>5.1f}%)")
    
    # Categories
    print("\nCATEGORIES:")
    print("-" * 100)
    sorted_categories = sorted(analysis['categories'].items(), key=lambda x: x[1]['count'], reverse=True)
    
    for category, data in sorted_categories[:10]:
        percentage = (data['count'] / len(products)) * 100
        print(f"{category:<30} {data['count']:<10} ({percentage:>5.1f}%)")
    
    # Top brands
    print("\nTOP BRANDS:")
    print("-" * 100)
    sorted_brands = sorted(analysis['brands'].items(), key=lambda x: x[1], reverse=True)
    
    for brand, count in sorted_brands[:10]:
        percentage = (count / len(products)) * 100
        print(f"{brand:<30} {count:<10} ({percentage:>5.1f}%)")
    
    # Top products
    print("\n" + "="*100)
    print("TOP 10 PRODUCTS BY RATING")
    print("="*100)
    
    sorted_by_rating = sorted(products, key=lambda x: x.get('rating', 0), reverse=True)
    
    print(f"\n{'Rank':<6} {'Title':<35} {'Price':<12} {'Rating':<10} {'Discount':<12} {'Stock':<8}")
    print("-"*100)
    
    for i, product in enumerate(sorted_by_rating[:10], 1):
        title = product.get('title', 'Unknown')[:32]
        price = product.get('price', 0)
        rating = product.get('rating', 0)
        discount = product.get('discountPercentage', 0)
        stock = product.get('stock', 0)
        
        print(f"{i:<6} {title:<35} ${price:<11,.2f} {rating:<10.1f} {discount:<11.1f}% {stock:<8}")
    
    # Best value products
    print("\n" + "="*100)
    print("BEST VALUE PRODUCTS (High Rating + High Discount)")
    print("="*100)
    
    # Calculate value score: rating * discount
    value_scores = [
        (p, p.get('rating', 0) * p.get('discountPercentage', 0))
        for p in products
    ]
    
    sorted_by_value = sorted(value_scores, key=lambda x: x[1], reverse=True)
    
    print(f"\n{'Rank':<6} {'Title':<35} {'Price':<12} {'Rating':<10} {'Discount':<12} {'Value Score':<12}")
    print("-"*100)
    
    for i, (product, value_score) in enumerate(sorted_by_value[:10], 1):
        title = product.get('title', 'Unknown')[:32]
        price = product.get('price', 0)
        rating = product.get('rating', 0)
        discount = product.get('discountPercentage', 0)
        
        print(f"{i:<6} {title:<35} ${price:<11,.2f} {rating:<10.1f} {discount:<11.1f}% {value_score:<12.2f}")


def competitive_comparison(search_terms):
    """
    Compares multiple product searches
    """
    print("\n" + "="*100)
    print("COMPETITIVE COMPARISON ACROSS SEARCH TERMS")
    print("="*100)
    
    comparison_data = {}
    
    for term in search_terms:
        results = search_products(term)
        if results and 'products' in results:
            products = results['products']
            
            avg_price = sum(p.get('price', 0) for p in products) / len(products) if products else 0
            avg_rating = sum(p.get('rating', 0) for p in products) / len(products) if products else 0
            avg_discount = sum(p.get('discountPercentage', 0) for p in products) / len(products) if products else 0
            
            comparison_data[term] = {
                'count': len(products),
                'avg_price': avg_price,
                'avg_rating': avg_rating,
                'avg_discount': avg_discount
            }
    
    if comparison_data:
        print(f"\n{'Search Term':<20} {'Products Found':<20} {'Avg Price':<15} {'Avg Rating':<15} {'Avg Discount':<15}")
        print("-"*100)
        
        for term, data in comparison_data.items():
            print(f"{term:<20} {data['count']:<20} ${data['avg_price']:<14,.2f} {data['avg_rating']:<15.2f} {data['avg_discount']:<14.2f}%")


# Main execution
if __name__ == "__main__":
    try:
        print("="*100)
        print("ADVANCED PRODUCT SEARCH & ANALYSIS")
        print("="*100 + "\n")
        
        # Single search
        search_term = 'phone'
        search_results = search_products(search_term)
        
        if search_results:
            analysis, products = analyze_search_results(search_results)
            display_search_results(search_term, analysis, products)
        
        # Comparative analysis
        print("\n\n" + "="*100)
        print("COMPARATIVE SEARCH ANALYSIS")
        print("="*100 + "\n")
        
        search_terms = ['phone', 'laptop', 'watch', 'camera']
        competitive_comparison(search_terms)
        
        # Export results
        print("\n\n" + "="*100)
        print("EXPORTING RESULTS")
        print("="*100 + "\n")
        
        if search_results:
            output_file = r'c:\Users\ADMIN\Downloads\product_search_analysis.json'
            
            export_data = {
                'search_timestamp': datetime.now().isoformat(),
                'search_term': search_term,
                'results_count': len(products),
                'products': products,
                'analysis_summary': {
                    'total_results': analysis['total_results'],
                    'price_stats': analysis['price_stats'],
                    'rating_stats': analysis['rating_stats'],
                    'discount_stats': analysis['discount_stats'],
                    'stock_stats': analysis['stock_stats'],
                    'categories_count': len(analysis['categories']),
                    'brands_count': len(analysis['brands'])
                }
            }
            
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            print(f"✓ Search results exported to: {output_file}")
        
        print("\n✓ Analysis complete!")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
