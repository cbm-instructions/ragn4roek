import requests

while True:
    id = input("Product Id:")
    api = "https://world.openfoodfacts.org/api/2/product/"

    #print(id)
    r = requests.get(f"{api}{id}.json?fields=ecoscore_grade,product_name_de,nutriments")

    product = r.json()['product']
    if product.get('product_name_de'):
        name = product.get('product_name_de')
        print(f"Produktname: {name}")
    if product.get('nutriments') and product.get('nutriments').get('energy-kcal_100g'):
        kcal = product.get('nutriments').get('energy-kcal_100g')
        print(f"Kalorien/100g: {kcal}")
    # if product['carbon-footprint_100g']:
    #     name = product['carbon-footprint_100g']
    #     print(f"C02: {name}")
    ### Eco score
    if product.get("ecoscore_grade"):
        ecoscore_grade = product.get("ecoscore_grade")
        print(f"Ecoscore: {ecoscore_grade}")

    print("#########################")
#4000194240776