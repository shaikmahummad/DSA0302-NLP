import re

# List of products
products = [
    "Apple iPhone 15",
    "Apple MacBook Air",
    "Samsung Galaxy S24",
    "Samsung Galaxy Tab",
    "OnePlus 12",
    "OnePlus Nord",
    "Dell Laptop",
    "HP Pavilion Laptop",
    "Sony Headphones",
    "Apple AirPods"
]


# Function to search products
def search_products(keyword, search_type):

    results = []

    # Create pattern based on search type
    if search_type == "exact":
        pattern = r"\b" + re.escape(keyword) + r"\b"

    elif search_type == "prefix":
        pattern = r"\b" + re.escape(keyword) + r"\w*"

    elif search_type == "suffix":
        pattern = r"\w*" + re.escape(keyword) + r"\b"

    elif search_type == "partial":
        pattern = re.escape(keyword)

    else:
        return results

    # Search every product
    for product in products:

        # IGNORECASE makes the search case-insensitive
        if re.search(pattern, product, re.IGNORECASE):
            results.append(product)

    return results


print("========== PRODUCT SEARCH SYSTEM ==========")

# Get keyword
keyword = input("Enter search keyword: ")

print("\n1. Exact Search")
print("2. Prefix Search")
print("3. Suffix Search")
print("4. Partial Search")

choice = input("Enter your choice: ")

# Select search type
if choice == "1":
    search_type = "exact"

elif choice == "2":
    search_type = "prefix"

elif choice == "3":
    search_type = "suffix"

elif choice == "4":
    search_type = "partial"

else:
    search_type = ""


# Perform search
results = search_products(keyword, search_type)


# Display results
print("\n========== SEARCH RESULTS ==========")

if len(results) > 0:

    for product in results:
        print(product)

else:
    print("No matching products found.")


# Display total count
print("\nTotal Matching Products:", len(results))