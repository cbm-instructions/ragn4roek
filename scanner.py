import requests
import time
import os
import pyautogui

pyautogui.hotkey('alt', 'F11')

timeout = 1
calories = 0

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
                r = requests.get(f"{api}{id}.json?fields=ecoscore_grade,product_name_de,nutriments,countries")


                product = r.json()
                if product.get("status") != 0:
                    product = product.get('product')
                    if product.get('product_name_de'):
                        name = product.get('product_name_de')
                        print(f"Produktname: {name}")
                    elif product.get('product_name'):
                        name = product.get('product_name')
                        print(f"Produktname: {name}")
                    if product.get('nutriments') and product.get('nutriments').get('energy-kcal_100g'):
                        kcal100 = product.get('nutriments').get('energy-kcal')
                        print(f"Kalorien/100g/ml: {kcal100}")
                        kcal = product.get('nutriments').get('energy-kcal_serving')
                        calories += kcal
                        print(f"Insgesamt hast du {calories} kcal gescannt.") #<--- hier war davor energy :)-hinrik
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
                    if product.get("countries"):
                        country = product.get("countries")
                        print(f"Ursprungsland: {country}")
                else:
                    print('Product not available!')

                print("#########################")
    except requests.ConnectionError:
        print("The internet connection is down! Please connect to the internet first!")
        time.sleep(10)
        os.system('cls' if os.name == 'nt' else 'clear')