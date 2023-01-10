import requests
import time
import os
import pyautogui

pyautogui.hotkey('alt', 'F11')

timeout = 1

while True:
    try:
        requests.head("http://www.google.com/", timeout=timeout)
        # Do something
        print("The internet connection is active! Let's go!")
        print("""  ..---..
 /       \\
|         |
:         ;
 \  \~/  /
  `, Y ,'
   |_|_|
   |===|
   |===|
    \_/""")


        while True:
            id = input("Product Id:")
            if id:
                api = "https://world.openfoodfacts.org/api/2/product/"

                #print(id)
                r = requests.get(f"{api}{id}.json?fields=ecoscore_grade,product_name_de,nutriments")


                product = r.json()
                if product.get("status") != 0:
                    product = product.get('product')
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
                        if ecoscore_grade == "unknown":
                            print("Ecoscore: not available")
                        else:
                            print(f"Ecoscore: {ecoscore_grade}")
                else:
                    print('Product not available!')

                print("#########################")
    except requests.ConnectionError:
        # Do something
        print("The internet connection is down! Please connect to the internet first!")
        time.sleep(10)
        os.system('cls' if os.name == 'nt' else 'clear')