"""
Product search API integration with market analysis and recommendations
Demonstrates: requests.get('https://dummyjson.com/products/search?q=phone')
"""

import requests
import json
from datetime import datetime


def search_api_demo(search_query='phone'):
    """
    Demonstrates the exact API call: requests.get('https://dummyjson.com/products/search?q=phone')
    
    Args:
        search_query (str): Search term
    
    Returns: raw API response
    """
    print("="*100)
    print("API REQUEST DEMONSTRATION")
    print("="*100)
    
    url = f'https://dummyjson.com/products/search?q={search_query}'
    
    print(f"\nAPI Endpoint: {url}\n")
    print("Request Details:")
    print(f"  Method: GET")
    print(f"  URL: {url}")
    print(f"  Query Parameter: q={search_query}\n")
    
    try:
        # THE EXACT API CALL
        response = requests.get(f'https://dummyjson.com/products/search?q={search_query}')
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers:")
        print(f"  Content-Type: {response.headers.get('content-type', 'N/A')}")
        print(f"  Content-Length: {len(response.text)} bytes\n")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Successfully fetched API response")
            print(f"  Response contains {len(data.get('products', []))} products\n")
            return data
        else:
            print(f"✗ Error: Status code {response.status_code}")
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error: {e}")
        return None


def extract_product_details(api_response):
    """
    Extracts and structures product details from API response
    """
    if not api_response or 'products' not in api_response:
        return None
    
    products = api_response['products']
    
    print("\n" + "="*100)
    print("RAW API RESPONSE STRUCTURE")
    print("="*100)
    
    print(f"\nResponse JSON Keys: {list(api_response.keys())}")
    print(f"Total Products in Response: {api_response.get('total', 0)}")
    print(f"Products Array Length: {len(products)}")
    
    if products:
        sample_product = products[0]
        
        print(f"\nSample Product Structure (Product ID: {sample_product.get('id')}):")
        print(f"  Keys: {list(sample_product.keys())}\n")
        
        print("Sample Product Data:")
        for key, value in list(sample_product.items())[:10]:
            if isinstance(value, list):
                print(f"  {key}: [array with {len(value)} items]")
            elif isinstance(value, dict):
                print(f"  {key}: {list(value.keys())}")
            else:
                print(f"  {key}: {value}")
    
    return products


def market_analysis_report(api_response, sales_data=None):
    """
    Creates comprehensive market analysis report
    """
    if not api_response or 'products' not in api_response:
        return
    
    products = api_response['products']
    
    print("\n" + "="*100)
    print("MARKET ANALYSIS REPORT")
    print("="*100)
    
    # Extract metrics
    prices = [p.get('price', 0) for p in products]
    ratings = [p.get('rating', 0) for p in products]
    discounts = [p.get('discountPercentage', 0) for p in products]
    stocks = [p.get('stock', 0) for p in products]
    
    print(f"""
MARKET OVERVIEW:
  Total Products: {len(products)}
  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PRICING METRICS:
  Min Price: ${min(prices):.2f}
  Max Price: ${max(prices):.2f}
  Avg Price: ${sum(prices)/len(prices):.2f}
  Total Market Value: ${sum(prices):,.2f}

CUSTOMER SATISFACTION:
  Highest Rating: {max(ratings):.1f}/5.0
  Lowest Rating: {min(ratings):.1f}/5.0
  Avg Rating: {sum(ratings)/len(ratings):.2f}/5.0

PROMOTIONAL ACTIVITY:
  Max Discount: {max(discounts):.1f}%
  Avg Discount: {sum(discounts)/len(discounts):.2f}%

INVENTORY STATUS:
  Total Units: {sum(stocks):,}
  Avg Stock/Product: {sum(stocks)/len(stocks):.1f}
  Out of Stock: {sum(1 for s in stocks if s == 0)}
    """)
    
    # Product quality tiers
    print("\nPRODUCT QUALITY TIERS:")
    print("-"*100)
    
    premium = [p for p in products if p.get('rating', 0) >= 4.5]
    good = [p for p in products if 4.0 <= p.get('rating', 0) < 4.5]
    average = [p for p in products if 3.0 <= p.get('rating', 0) < 4.0]
    poor = [p for p in products if p.get('rating', 0) < 3.0]
    
    tiers = [
        ('Premium (4.5+ ⭐)', premium),
        ('Good (4.0-4.5 ⭐)', good),
        ('Average (3.0-4.0 ⭐)', average),
        ('Poor (< 3.0 ⭐)', poor)
    ]
    
    for tier_name, tier_products in tiers:
        percentage = (len(tier_products) / len(products)) * 100
        avg_price = sum(p.get('price', 0) for p in tier_products) / len(tier_products) if tier_products else 0
        print(f"{tier_name:<25} Count: {len(tier_products):<10} ({percentage:>5.1f}%) | Avg Price: ${avg_price:,.2f}")


def detailed_product_breakdown(api_response):
    """
    Shows detailed breakdown of each product from API
    """
    if not api_response or 'products' not in api_response:
        return
    
    products = api_response['products']
    
    print("\n" + "="*100)
    print("DETAILED PRODUCT BREAKDOWN (ALL PRODUCTS FROM API)")
    print("="*100)
    
    print(f"\n{'ID':<5} {'Title':<40} {'Price':<12} {'Rating':<10} {'Stock':<8} {'Discount':<10}")
    print("-"*100)
    
    for product in products:
        product_id = product.get('id', 'N/A')
        title = product.get('title', 'Unknown')[:37]
        price = product.get('price', 0)
        rating = product.get('rating', 0)
        stock = product.get('stock', 0)
        discount = product.get('discountPercentage', 0)
        
        print(f"{product_id:<5} {title:<40} ${price:<11,.2f} {rating:<10.1f} {stock:<8} {discount:<9.1f}%")


def api_response_summary(api_response):
    """
    Displays complete API response summary
    """
    if not api_response:
        return
    
    print("\n" + "="*100)
    print("COMPLETE API RESPONSE SUMMARY")
    print("="*100)
    
    print(f"\nResponse Metadata:")
    print(f"  Total: {api_response.get('total', 'N/A')}")
    print(f"  Skip: {api_response.get('skip', 'N/A')}")
    print(f"  Limit: {api_response.get('limit', 'N/A')}")
    
    if 'products' in api_response:
        print(f"\nProducts Array: {len(api_response['products'])} items")
        
        # Show all product titles
        print("\nProduct List:")
        for i, product in enumerate(api_response['products'], 1):
            title = product.get('title', 'Unknown')
            price = product.get('price', 0)
            rating = product.get('rating', 0)
            print(f"  {i}. {title}")
            print(f"     Price: ${price:.2f} | Rating: {rating:.1f}⭐")


def export_api_response(api_response, filename):
    """
    Exports raw API response to file
    """
    try:
        with open(filename, 'w') as f:
            json.dump(api_response, f, indent=2)
        print(f"\n✓ API response exported to: {filename}")
    except Exception as e:
        print(f"✗ Error exporting: {e}")


# Main execution
if __name__ == "__main__":
    try:
        print("\n")
        print("█" * 100)
        print("DUMMYJSON PRODUCT SEARCH API INTEGRATION")
        print("Demonstrates: requests.get('https://dummyjson.com/products/search?q=phone')")
        print("█" * 100)
        
        # Execute the API call
        api_response = search_api_demo('phone')
        
        if api_response:
            # Extract and display details
            products = extract_product_details(api_response)
            
            # Market analysis
            market_analysis_report(api_response)
            
            # Detailed breakdown
            detailed_product_breakdown(api_response)
            
            # Complete summary
            api_response_summary(api_response)
            
            # Export
            print("\n" + "="*100)
            print("EXPORTING RAW API RESPONSE")
            print("="*100)
            
            output_file = r'c:\Users\ADMIN\Downloads\api_response_raw.json'
            export_api_response(api_response, output_file)
            
            # Export formatted report
            report_file = r'c:\Users\ADMIN\Downloads\search_api_report.json'
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'search_query': 'phone',
                'api_endpoint': 'https://dummyjson.com/products/search',
                'total_products_found': len(products) if products else 0,
                'response_metadata': {
                    'total': api_response.get('total'),
                    'skip': api_response.get('skip'),
                    'limit': api_response.get('limit')
                },
                'products': products[:10] if products else []  # First 10 products
            }
            
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"✓ Formatted report exported to: {report_file}")
            
            print("\n" + "="*100)
            print("✓ API INTEGRATION COMPLETE")
            print("="*100)
        else:
            print("\n✗ Failed to fetch API response")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
