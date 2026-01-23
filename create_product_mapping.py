"""
Create product mapping from API products for quick lookups
"""

import json
from fetch_all_products import fetch_all_products


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters: api_products from fetch_all_products()

    Returns: dictionary mapping product IDs to info

    Expected Output Format:
    {
        1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
        2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
        ...
    }
    """
    
    product_mapping = {}
    
    if not api_products:
        print("✗ Error: No products provided")
        return product_mapping
    
    for product in api_products:
        try:
            product_id = product.get('id')
            
            if product_id is None:
                print(f"⚠ Warning: Product has no ID, skipping")
                continue
            
            # Create simplified product info
            product_info = {
                'title': product.get('title', 'N/A'),
                'category': product.get('category', 'N/A'),
                'brand': product.get('brand', 'Unknown'),
                'price': product.get('price', 0),
                'rating': product.get('rating', 0),
                'stock': product.get('stock', 0),
                'discount': product.get('discount', 0),
                'sku': product.get('sku', 'N/A')
            }
            
            product_mapping[product_id] = product_info
        
        except Exception as e:
            print(f"⚠ Warning: Error processing product - {e}")
            continue
    
    return product_mapping


def display_mapping_summary(product_mapping):
    """
    Displays summary of the product mapping
    """
    if not product_mapping:
        print("No products in mapping")
        return
    
    print(f"\n{'='*100}")
    print("PRODUCT MAPPING SUMMARY")
    print(f"{'='*100}\n")
    
    print(f"Total Products Mapped: {len(product_mapping)}")
    print(f"Product IDs Range: {min(product_mapping.keys())} - {max(product_mapping.keys())}\n")
    
    # Categories in mapping
    categories = set()
    brands = set()
    
    for product_info in product_mapping.values():
        categories.add(product_info['category'])
        brands.add(product_info['brand'])
    
    print(f"Unique Categories: {len(categories)}")
    print(f"Unique Brands: {len(brands)}\n")
    
    # Sample entries
    print(f"{'='*100}")
    print("SAMPLE ENTRIES (First 10 Products)")
    print(f"{'='*100}\n")
    
    print(f"{'ID':<6} {'Title':<40} {'Category':<20} {'Brand':<15} {'Price':<10} {'Rating':<10}")
    print(f"{'-'*100}")
    
    for product_id in sorted(list(product_mapping.keys())[:10]):
        info = product_mapping[product_id]
        title = info['title'][:37]
        category = info['category'][:17]
        brand = info['brand'][:12]
        price = info['price']
        rating = info['rating']
        
        print(f"{product_id:<6} {title:<40} {category:<20} {brand:<15} ${price:<9.2f} {rating:<10.1f}")


def lookup_product(product_mapping, product_id):
    """
    Looks up a single product by ID
    """
    if product_id in product_mapping:
        return product_mapping[product_id]
    else:
        return None


def filter_mapping_by_category(product_mapping, category):
    """
    Filters products in mapping by category
    """
    filtered = {}
    
    for product_id, product_info in product_mapping.items():
        if product_info['category'].lower() == category.lower():
            filtered[product_id] = product_info
    
    return filtered


def filter_mapping_by_price_range(product_mapping, min_price, max_price):
    """
    Filters products in mapping by price range
    """
    filtered = {}
    
    for product_id, product_info in product_mapping.items():
        price = product_info['price']
        if min_price <= price <= max_price:
            filtered[product_id] = product_info
    
    return filtered


def filter_mapping_by_rating(product_mapping, min_rating):
    """
    Filters products in mapping by minimum rating
    """
    filtered = {}
    
    for product_id, product_info in product_mapping.items():
        rating = product_info['rating']
        if rating >= min_rating:
            filtered[product_id] = product_info
    
    return filtered


def get_mapping_statistics(product_mapping):
    """
    Calculates statistics for the product mapping
    """
    if not product_mapping:
        return {}
    
    prices = [info['price'] for info in product_mapping.values()]
    ratings = [info['rating'] for info in product_mapping.values()]
    stocks = [info['stock'] for info in product_mapping.values()]
    
    stats = {
        'total_products': len(product_mapping),
        'price_min': min(prices),
        'price_max': max(prices),
        'price_avg': sum(prices) / len(prices),
        'price_median': sorted(prices)[len(prices) // 2],
        'rating_min': min(ratings),
        'rating_max': max(ratings),
        'rating_avg': sum(ratings) / len(ratings),
        'stock_min': min(stocks),
        'stock_max': max(stocks),
        'stock_avg': sum(stocks) / len(stocks),
        'stock_total': sum(stocks)
    }
    
    return stats


def export_mapping_to_json(product_mapping, filename):
    """
    Exports product mapping to JSON file
    """
    try:
        with open(filename, 'w') as f:
            json.dump(product_mapping, f, indent=2)
        
        print(f"✓ Product mapping exported to: {filename}")
        print(f"  File size: {len(json.dumps(product_mapping))} bytes")
    
    except Exception as e:
        print(f"✗ Error exporting mapping: {e}")


def display_mapping_statistics(stats):
    """
    Displays mapping statistics in formatted view
    """
    print(f"\n{'='*100}")
    print("PRODUCT MAPPING STATISTICS")
    print(f"{'='*100}\n")
    
    print(f"Total Products: {stats['total_products']}\n")
    
    print("PRICING STATISTICS:")
    print(f"  Minimum: ${stats['price_min']:,.2f}")
    print(f"  Maximum: ${stats['price_max']:,.2f}")
    print(f"  Average: ${stats['price_avg']:,.2f}")
    print(f"  Median: ${stats['price_median']:,.2f}\n")
    
    print("RATING STATISTICS:")
    print(f"  Minimum: {stats['rating_min']:.1f}/5.0")
    print(f"  Maximum: {stats['rating_max']:.1f}/5.0")
    print(f"  Average: {stats['rating_avg']:.2f}/5.0\n")
    
    print("INVENTORY STATISTICS:")
    print(f"  Minimum: {stats['stock_min']} units")
    print(f"  Maximum: {stats['stock_max']} units")
    print(f"  Average per Product: {stats['stock_avg']:.1f} units")
    print(f"  Total Inventory: {stats['stock_total']:,} units")


# Main execution
if __name__ == "__main__":
    try:
        print(f"\n{'='*100}")
        print("CREATE PRODUCT MAPPING FROM API PRODUCTS")
        print(f"{'='*100}\n")
        
        # Fetch all products
        print("Step 1: Fetching all products from API...")
        api_products = fetch_all_products()
        
        if not api_products:
            print("✗ Failed to fetch products")
            exit(1)
        
        # Create mapping
        print("\nStep 2: Creating product mapping...")
        product_mapping = create_product_mapping(api_products)
        
        if not product_mapping:
            print("✗ Failed to create product mapping")
            exit(1)
        
        print(f"✓ Successfully created mapping for {len(product_mapping)} products\n")
        
        # Display summary
        display_mapping_summary(product_mapping)
        
        # Get statistics
        print(f"\n{'='*100}")
        print("Step 3: Calculating statistics...")
        print(f"{'='*100}")
        
        stats = get_mapping_statistics(product_mapping)
        display_mapping_statistics(stats)
        
        # Example filters
        print(f"\n{'='*100}")
        print("EXAMPLE: FILTER BY CATEGORY")
        print(f"{'='*100}")
        
        beauty_products = filter_mapping_by_category(product_mapping, 'beauty')
        print(f"\nBeauty Products: {len(beauty_products)}")
        
        if beauty_products:
            print(f"{'ID':<6} {'Title':<40} {'Price':<12} {'Rating':<10}")
            print(f"{'-'*100}")
            for product_id in sorted(list(beauty_products.keys())[:5]):
                info = beauty_products[product_id]
                title = info['title'][:37]
                price = info['price']
                rating = info['rating']
                print(f"{product_id:<6} {title:<40} ${price:<11.2f} {rating:<10.1f}")
        
        # Example price range filter
        print(f"\n{'='*100}")
        print("EXAMPLE: FILTER BY PRICE RANGE ($100-$500)")
        print(f"{'='*100}\n")
        
        mid_range = filter_mapping_by_price_range(product_mapping, 100, 500)
        print(f"Mid-Range Products: {len(mid_range)}")
        
        if mid_range:
            print(f"{'ID':<6} {'Title':<40} {'Price':<12} {'Rating':<10}")
            print(f"{'-'*100}")
            for product_id in sorted(list(mid_range.keys())[:5]):
                info = mid_range[product_id]
                title = info['title'][:37]
                price = info['price']
                rating = info['rating']
                print(f"{product_id:<6} {title:<40} ${price:<11.2f} {rating:<10.1f}")
        
        # Example rating filter
        print(f"\n{'='*100}")
        print("EXAMPLE: FILTER BY HIGH RATING (4.5+ stars)")
        print(f"{'='*100}\n")
        
        high_rated = filter_mapping_by_rating(product_mapping, 4.5)
        print(f"High-Rated Products (4.5+): {len(high_rated)}")
        
        if high_rated:
            print(f"{'ID':<6} {'Title':<40} {'Price':<12} {'Rating':<10}")
            print(f"{'-'*100}")
            for product_id in sorted(list(high_rated.keys())[:5]):
                info = high_rated[product_id]
                title = info['title'][:37]
                price = info['price']
                rating = info['rating']
                print(f"{product_id:<6} {title:<40} ${price:<11.2f} {rating:<10.1f}")
        
        # Example product lookup
        print(f"\n{'='*100}")
        print("EXAMPLE: PRODUCT LOOKUP BY ID")
        print(f"{'='*100}\n")
        
        sample_id = list(product_mapping.keys())[0]
        product_info = lookup_product(product_mapping, sample_id)
        
        if product_info:
            print(f"Product ID {sample_id}:")
            for key, value in product_info.items():
                print(f"  {key}: {value}")
        
        # Export mapping
        print(f"\n{'='*100}")
        print("Step 4: Exporting product mapping...")
        print(f"{'='*100}\n")
        
        export_file = r'c:\Users\ADMIN\Downloads\product_mapping.json'
        export_mapping_to_json(product_mapping, export_file)
        
        # Final summary
        print(f"\n{'='*100}")
        print("PRODUCT MAPPING COMPLETE")
        print(f"{'='*100}")
        print(f"\n✓ Created mapping with {len(product_mapping)} products")
        print(f"✓ Available for lookups and filtering")
        print(f"✓ Statistics calculated and exported")
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
