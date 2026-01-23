"""
Fetch all products from DummyJSON API with error handling
"""

import requests
import json
from datetime import datetime


def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries

    Expected Output Format:
    [
        {
            'id': 1,
            'title': 'iPhone 9',
            'category': 'smartphones',
            'brand': 'Apple',
            'price': 549,
            'rating': 4.69
        },
        ...
    ]

    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """
    
    all_products = []
    
    try:
        print("Fetching all products from DummyJSON API...")
        print("Endpoint: https://dummyjson.com/products?limit=100")
        
        # Fetch with limit=100 (API max)
        response = requests.get('https://dummyjson.com/products?limit=100', timeout=10)
        
        # Check response status
        if response.status_code != 200:
            print(f"[ERROR] HTTP Status {response.status_code}")
            return []
        
        # Parse JSON
        data = response.json()
        
        # Extract products
        products = data.get('products', [])
        total_available = data.get('total', 0)
        
        if not products:
            print("[ERROR] No products found in API response")
            return []
        
        # Extract required fields for each product
        for product in products:
            simplified_product = {
                'id': product.get('id', None),
                'title': product.get('title', 'N/A'),
                'category': product.get('category', 'N/A'),
                'brand': product.get('brand', 'Unknown'),
                'price': product.get('price', 0),
                'rating': product.get('rating', 0),
                'stock': product.get('stock', 0),
                'discount': product.get('discountPercentage', 0),
                'sku': product.get('sku', 'N/A')
            }
            all_products.append(simplified_product)
        
        # Success message
        print(f"[OK] Successfully fetched {len(all_products)} products")
        print(f"  Total available in API: {total_available}")
        print(f"  Response size: {len(response.text)} bytes\n")
        
        return all_products
    
    except requests.exceptions.Timeout:
        print("✗ Error: Request timeout (took too long to respond)")
        return []
    
    except requests.exceptions.ConnectionError:
        print("✗ Error: Connection failed (cannot reach API)")
        return []
    
    except requests.exceptions.HTTPError as e:
        print(f"✗ Error: HTTP error occurred - {e}")
        return []
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: Request failed - {e}")
        return []
    
    except json.JSONDecodeError:
        print("✗ Error: Failed to parse JSON response")
        return []
    
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return []


def analyze_fetched_products(products):
    """
    Analyzes the fetched products
    """
    if not products:
        print("No products to analyze")
        return
    
    print("="*100)
    print("FETCHED PRODUCTS ANALYSIS")
    print("="*100)
    
    print(f"""
SUMMARY:
  Total Products: {len(products)}
  Categories: {len(set(p['category'] for p in products))}
  Brands: {len(set(p['brand'] for p in products))}

PRICING:
  Min Price: ${min(p['price'] for p in products):,.2f}
  Max Price: ${max(p['price'] for p in products):,.2f}
  Avg Price: ${sum(p['price'] for p in products) / len(products):,.2f}

RATINGS:
  Highest: {max(p['rating'] for p in products):.1f}/5.0
  Lowest: {min(p['rating'] for p in products):.1f}/5.0
  Average: {sum(p['rating'] for p in products) / len(products):.2f}/5.0

INVENTORY:
  Total Units: {sum(p['stock'] for p in products):,}
  Average per Product: {sum(p['stock'] for p in products) / len(products):.1f}

DISCOUNTS:
  Max Discount: {max(p['discount'] for p in products):.1f}%
  Avg Discount: {sum(p['discount'] for p in products) / len(products):.2f}%
    """)
    
    # Categories
    print("\nTOP CATEGORIES:")
    print("-"*100)
    category_counts = {}
    for product in products:
        cat = product['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    for category, count in sorted_categories[:10]:
        percentage = (count / len(products)) * 100
        print(f"  {category:<30} {count:<10} ({percentage:>5.1f}%)")
    
    # Brands
    print("\nTOP BRANDS:")
    print("-"*100)
    brand_counts = {}
    for product in products:
        brand = product['brand']
        brand_counts[brand] = brand_counts.get(brand, 0) + 1
    
    sorted_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)
    for brand, count in sorted_brands[:10]:
        percentage = (count / len(products)) * 100
        print(f"  {brand:<30} {count:<10} ({percentage:>5.1f}%)")
    
    # Top products
    print("\nTOP 10 PRODUCTS BY RATING:")
    print("-"*100)
    sorted_by_rating = sorted(products, key=lambda x: x['rating'], reverse=True)
    
    print(f"\n{'Rank':<6} {'Title':<40} {'Price':<12} {'Rating':<10} {'Category':<20}")
    print("-"*100)
    
    for i, product in enumerate(sorted_by_rating[:10], 1):
        title = product['title'][:37]
        price = product['price']
        rating = product['rating']
        category = product['category']
        
        print(f"{i:<6} {title:<40} ${price:<11,.2f} {rating:<10.1f} {category:<20}")
    
    # Price tiers
    print("\n\nPRICE TIER DISTRIBUTION:")
    print("-"*100)
    
    budget = sum(1 for p in products if p['price'] < 50)
    mid = sum(1 for p in products if 50 <= p['price'] < 500)
    premium = sum(1 for p in products if 500 <= p['price'] < 2000)
    luxury = sum(1 for p in products if p['price'] >= 2000)
    
    print(f"  Budget (<$50): {budget} ({budget/len(products)*100:.1f}%)")
    print(f"  Mid-Range ($50-$500): {mid} ({mid/len(products)*100:.1f}%)")
    print(f"  Premium ($500-$2000): {premium} ({premium/len(products)*100:.1f}%)")
    print(f"  Luxury (>$2000): {luxury} ({luxury/len(products)*100:.1f}%)")


def display_products_table(products, limit=20):
    """
    Displays products in a formatted table
    """
    if not products:
        return
    
    print("\n" + "="*100)
    print(f"PRODUCT TABLE (Showing first {min(limit, len(products))} of {len(products)} products)")
    print("="*100)
    
    print(f"\n{'ID':<6} {'Title':<40} {'Category':<20} {'Brand':<15} {'Price':<12} {'Rating':<10}")
    print("-"*100)
    
    for product in products[:limit]:
        product_id = product['id']
        title = product['title'][:37]
        category = product['category'][:17]
        brand = product['brand'][:12]
        price = product['price']
        rating = product['rating']
        
        print(f"{product_id:<6} {title:<40} {category:<20} {brand:<15} ${price:<11,.2f} {rating:<10.1f}")


def export_products(products, filename):
    """
    Exports products to JSON file
    """
    try:
        data = {
            'timestamp': datetime.now().isoformat(),
            'total_products': len(products),
            'products': products
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Products exported to: {filename}")
        print(f"  File size: {len(json.dumps(data))} bytes")
    
    except Exception as e:
        print(f"✗ Error exporting products: {e}")


# Main execution
if __name__ == "__main__":
    try:
        print("\n" + "="*100)
        print("FETCH ALL PRODUCTS FROM DUMMYJSON API")
        print("="*100 + "\n")
        
        # Fetch all products
        products = fetch_all_products()
        
        if products:
            # Analyze
            analyze_fetched_products(products)
            
            # Display table
            display_products_table(products, limit=20)
            
            # Export
            print("\n" + "="*100)
            print("EXPORTING PRODUCTS")
            print("="*100 + "\n")
            
            export_file = r'c:\Users\ADMIN\Downloads\all_products_fetched.json'
            export_products(products, export_file)
            
            # Summary
            print("\n" + "="*100)
            print("FETCH COMPLETE")
            print("="*100)
            print(f"\n✓ Successfully fetched and processed {len(products)} products")
            print(f"✓ Data ready for analysis and comparison with sales data")
        else:
            print("\n✗ Failed to fetch products from API")
            print("✗ Returning empty list as per requirements")
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
