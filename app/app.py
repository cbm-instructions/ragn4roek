
from flask import Flask, render_template, request, url_for, flash, redirect
import requests


app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def index():
    result = []
    err = None
    if request.method == 'POST':
        barcode = request.form['id']
        better_product_name = ""
        better_eco_score = 0
        better_product_picture = ""
        is_best_product = True
        better_product = ""
        stores = ""
        res = requests.get(f'https://de.openfoodfacts.org/api/v0/produkt/{barcode}?fields=ecoscore_score,product_name,image_front_small_url,stores,categories_hierarchy,image_front_small_url,brands')
        product = res.json()
        if product and product.get("product"):
            product = product.get("product")
            product_name = product.get("product_name")
            brand = product.get('brands')
            if brand:
                brand = brand.split(",")[0]
                product_name = f"{product_name} ({brand})"
            picture = product.get("image_front_small_url")
            eco_score = product.get('ecoscore_score')
            category = product.get('categories_hierarchy')
            if category and len(category) > 0:
                category = category[-1]
                similar_products = get_similar_products(category)
                print(similar_products)
                if len(similar_products) > 0:
                    products_with_better_ecoscore = []
                    products_with_better_ecoscore_and_stores = []
                    for similar_product in similar_products:
                        if similar_product.get('product_name') and similar_product.get('ecoscore_score') : 
                            compare_score = eco_score if eco_score else 0
                            if similar_product.get('ecoscore_score') >= compare_score:
                                products_with_better_ecoscore.append(similar_product) if not similar_product.get('stores') \
                                    else products_with_better_ecoscore_and_stores.append(similar_product)
                    if len(products_with_better_ecoscore_and_stores) != 0 and len(products_with_better_ecoscore) != 0:
                        better_product = max(products_with_better_ecoscore_and_stores
                                            if len(products_with_better_ecoscore_and_stores) > 0
                                            else products_with_better_ecoscore, key=lambda x: x.get('ecoscore_score', 0))
                        better_product_name = better_product.get('product_name')
                        brand = better_product.get('brands')
                        if brand:
                            brand = brand.split(",")[0]
                            better_product_name = f"{better_product_name} ({brand})"
                        better_eco_score = better_product.get('ecoscore_score')
                        better_product_picture = better_product.get('image_front_small_url')
                        stores = better_product.get('stores')
                    else: 
                        is_best_product = True
                        better_product_picture = product.get('image_front_small_url')
                else: 
                    err = "Es gibt keine ähnlichen Produkte."

                if eco_score and not err:
                    if not better_product:
                        is_best_product = True
                    else:
                        is_best_product = better_product.get('ecoscore_score') == eco_score
                    if eco_score < 0: 
                            color_score = 0
                    elif eco_score > 100: 
                            color_score = 100
                    else:
                        color_score = eco_score
                    pct_diff = 1.0 - color_score/100
                    red_color = min(255, pct_diff*2 * 255)
                    green_color = min(255, color_score/100*2 * 255)
                    col = (int(red_color), int(green_color), 0)
                    col = '#%02x%02x%02x' % col
                else:
                    col = 'lightgray'
                    is_best_product = False
                return render_template('index.html', product_name=product_name, picture_src=picture, eco_score=eco_score,
                                        better_eco_score=better_eco_score, better_product_name=better_product_name,
                                        better_product_picture=better_product_picture, stores=stores,
                                        is_best_product=is_best_product, id='', col=col, err = err)
            else:
                err = "Kein besseres Produkt verfügbar. Das Produkt hat keine Kategorie."
        else:
            err = "Produkt nicht verfügbar."
    return render_template('index.html', err=err)



def get_similar_products(category):
    res = requests.get(f'https://de.openfoodfacts.org/category/{category}.json?fields=ecoscore_score,product_name,image_front_small_url,stores')
    products = res.json().get("products")
    return products


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)