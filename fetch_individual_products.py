"""
Fetch individual product details from DummyJSON API
and perform detailed product analysis
"""

import requests
import json
from datetime import datetime


def fetch_single_product(product_id):
    """
    Fetches a single product from DummyJSON API
    
    Args:
        product_id (int): Product ID to fetch
    
    Returns: dictionary with product details or None if error
    """
    try:
        response = requests.get(f'https://dummyjson.com/products/{product_id}')
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"✗ Error: Status code {response.status_code}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching product {product_id}: {e}")
        return None


def fetch_product_range(start_id=1, end_id=10):
    """
    Fetches multiple products from DummyJSON API
    
    Args:
        start_id (int): Starting product ID
        end_id (int): Ending product ID
    
    Returns: list of product dictionaries
    """
    products = []
    
    print(f"Fetching products {start_id} to {end_id}...")
    
    for product_id in range(start_id, end_id + 1):
        product = fetch_single_product(product_id)
        if product:
            products.append(product)
            print(f"  ✓ Product {product_id}: {product.get('title', 'Unknown')}")
    
    print(f"Successfully fetched {len(products)} products\n")
    return products


def analyze_product_details(product):
    """
    Analyzes detailed information about a single product
    """
    print("="*90)
    print("PRODUCT DETAILS ANALYSIS")
    print("="*90)
    
    print(f"""
ID:                    {product.get('id', 'N/A')}
Title:                 {product.get('title', 'N/A')}
Description:           {product.get('description', 'N/A')}
Category:              {product.get('category', 'N/A')}
Brand:                 {product.get('brand', 'N/A')}
SKU:                   {product.get('sku', 'N/A')}

PRICING & INVENTORY:
  Price:               ${product.get('price', 0):,.2f}
  Discount:            {product.get('discountPercentage', 0):.1f}%
  Stock:               {product.get('stock', 0)} units
  
RATINGS & REVIEWS:
  Rating:              {product.get('rating', 0):.1f}/5.0
  Review Count:        {product.get('reviews', []) and len(product.get('reviews', [])) or 'N/A'} reviews
  Return Rate:         {product.get('returnPolicy', 'Not specified')}
  Warranty:            {product.get('warrantyInformation', 'Not specified')}
  
PRODUCT DETAILS:
  Weight:              {product.get('weight', 'N/A')} lbs
  Dimensions:          {product.get('dimensions', {}).get('width', 'N/A')} x {product.get('dimensions', {}).get('height', 'N/A')} x {product.get('dimensions', {}).get('depth', 'N/A')} inches
  Colors:              {', '.join(product.get('availabilityStatus', ['N/A']))}
  Availability:        {product.get('availabilityStatus', 'N/A')}
    """)
    
    # Images
    images = product.get('images', [])
    if images:
        print(f"Images:                {len(images)} available")
    
    # Thumbnail
    thumbnail = product.get('thumbnail', '')
    if thumbnail:
        print(f"Thumbnail:             Available")
    
    # Meta information
    print("\nMETADATA:")
    meta = product.get('meta', {})
    if meta:
        print(f"  Created: {meta.get('createdAt', 'N/A')}")
        print(f"  Updated: {meta.get('updatedAt', 'N/A')}")
        print(f"  QR Code: {meta.get('qrCode', 'N/A')}")
    
    # Tags
    tags = product.get('tags', [])
    if tags:
        print(f"\nTags: {', '.join(tags)}")
    
    # Reviews
    reviews = product.get('reviews', [])
    if reviews:
        print(f"\nCUSTOMER REVIEWS ({len(reviews)}):")
        print("-" * 90)
        for i, review in enumerate(reviews[:3], 1):  # Show first 3 reviews
            print(f"\nReview {i}:")
            print(f"  Rating: {review.get('rating', 0)}/5")
            print(f"  Comment: {review.get('comment', 'No comment')}")
            print(f"  Reviewer: {review.get('reviewerName', 'Anonymous')} ({review.get('reviewerEmail', 'N/A')})")
            print(f"  Date: {review.get('date', 'N/A')}")


def compare_product_with_sales(product, sales_products):
    """
    Compares API product with internal sales products
    """
    print("\n" + "="*90)
    print("COMPETITIVE ANALYSIS")
    print("="*90)
    
    api_price = product.get('price', 0)
    api_rating = product.get('rating', 0)
    
    # Find similar products in sales data
    similar_category = None
    for sales_product in sales_products:
        if 'similar' in product.get('title', '').lower():
            similar_category = sales_product[0]
            break
    
    print(f"""
API Product Price:     ${api_price:,.2f}
API Product Rating:    {api_rating:.1f}/5.0

Market Position:
  - Price tier: {"Budget" if api_price < 50 else "Mid-range" if api_price < 500 else "Premium"}
  - Customer satisfaction: {"High" if api_rating >= 4.5 else "Good" if api_rating >= 4 else "Average" if api_rating >= 3 else "Below Average"}
  - Stock availability: {"High stock" if product.get('stock', 0) > 50 else "Medium stock" if product.get('stock', 0) > 20 else "Low stock"}

Pricing Recommendation:
  - If launching similar product, consider pricing: ${api_price * 1.1:,.2f} (10% premium for quality)
  - Competitor price: ${api_price:,.2f}
  - Discount potential: Can offer up to {product.get('discountPercentage', 0):.1f}% discount
    """)


def export_product_data(products, filename):
    """
    Exports product data to JSON file
    """
    try:
        with open(filename, 'w') as f:
            json.dump(products, f, indent=2)
        print(f"✓ Product data exported to: {filename}")
    except Exception as e:
        print(f"✗ Error exporting data: {e}")


# Main execution
if __name__ == "__main__":
    from read_sales_data import read_sales_data
    from parse_transactions import parse_transactions
    from top_selling_products import top_selling_products
    
    try:
        print("="*90)
        print("INDIVIDUAL PRODUCT FETCH & ANALYSIS")
        print("="*90 + "\n")
        
        # Fetch a single product
        print("FETCHING SINGLE PRODUCT (ID: 1)\n")
        single_product = fetch_single_product(1)
        
        if single_product:
            analyze_product_details(single_product)
            
            # Load sales data for comparison
            filename = r'c:\Users\ADMIN\Downloads\sales_data_cleaned_final.txt'
            raw_lines = read_sales_data(filename)
            transactions = parse_transactions(raw_lines)
            sales_products = top_selling_products(transactions, n=1000)
            
            compare_product_with_sales(single_product, sales_products)
        
        # Fetch multiple products for analysis
        print("\n\n" + "="*90)
        print("FETCHING PRODUCT RANGE (IDs 1-5)")
        print("="*90 + "\n")
        
        products_range = fetch_product_range(1, 5)
        
        if products_range:
            print("="*90)
            print("PRODUCT RANGE ANALYSIS")
            print("="*90)
            
            print(f"\n{'ID':<5} {'Title':<35} {'Price':<12} {'Rating':<10} {'Stock':<10}")
            print("-"*90)
            
            total_price = 0
            avg_rating = 0
            
            for product in products_range:
                product_id = product.get('id', 'N/A')
                title = product.get('title', 'Unknown')[:32]
                price = product.get('price', 0)
                rating = product.get('rating', 0)
                stock = product.get('stock', 0)
                
                print(f"{product_id:<5} {title:<35} ${price:<11,.2f} {rating:<10.1f} {stock:<10}")
                
                total_price += price
                avg_rating += rating
            
            avg_price = total_price / len(products_range)
            avg_rating = avg_rating / len(products_range)
            
            print("\n" + "-"*90)
            print(f"{'AVERAGE':<5} {'':<35} ${avg_price:<11,.2f} {avg_rating:<10.1f}")
            
            # Export to file
            print("\n" + "="*90)
            output_file = r'c:\Users\ADMIN\Downloads\fetched_products_detail.json'
            export_product_data(products_range, output_file)
            
            # Market insights
            print("\n" + "="*90)
            print("MARKET INSIGHTS FROM FETCHED PRODUCTS")
            print("="*90)
            
            print(f"""
Average Product Price:       ${avg_price:,.2f}
Average Product Rating:      {avg_rating:.1f}/5.0

Price Distribution:
  - Lowest: ${min(p.get('price', 0) for p in products_range):,.2f}
  - Highest: ${max(p.get('price', 0) for p in products_range):,.2f}
  - Range: ${max(p.get('price', 0) for p in products_range) - min(p.get('price', 0) for p in products_range):,.2f}

Quality Metrics:
  - Highest Rated: {max(products_range, key=lambda x: x.get('rating', 0)).get('title', 'N/A')} ({max(p.get('rating', 0) for p in products_range):.1f}★)
  - Lowest Rated: {min(products_range, key=lambda x: x.get('rating', 0)).get('title', 'N/A')} ({min(p.get('rating', 0) for p in products_range):.1f}★)

Inventory Status:
  - Total Stock: {sum(p.get('stock', 0) for p in products_range)} units
  - Average Stock Per Product: {sum(p.get('stock', 0) for p in products_range) / len(products_range):.0f} units
            """)
        
        print("\n✓ Analysis complete!")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
