
from flask import Flask, render_template, request, url_for, flash, redirect
import requests


app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def index():
	result = []
	if request.method == 'POST':
		id = request.form['id']
		if id:
			api = "https://world.openfoodfacts.org/api/2/product/"

			#print(id)
			r = requests.get(f"{api}{id}.json?fields=ecoscore_grade,product_name_de,nutriments,countries")


			product = r.json()
			if product.get("status") != 0:
				product = product.get('product')
				if product.get('product_name_de'):
					name = product.get('product_name_de')
					result.append(f"Produktname: {name}")
				elif product.get('product_name'):
					name = product.get('product_name')
					result.append(f"Produktname: {name}")
				if product.get('nutriments') and product.get('nutriments').get('energy-kcal_100g'):
					kcal100 = product.get('nutriments').get('energy-kcal')
					result.append(f"Kalorien/100g/ml: {kcal100}")
					kcal = product.get('nutriments').get('energy-kcal_serving')
					#calories += kcal
					#result.append(f"Insgesamt hast du {calories} kcal gescannt.") #<--- hier war davor energy :)-hinrik
				# if product['carbon-footprint_100g']:
				#	name = product['carbon-footprint_100g']
				#	print(f"C02: {name}")
				### Eco score
				if product.get("ecoscore_grade"):
					ecoscore_grade = product.get("ecoscore_grade")
					if ecoscore_grade == "unknown":
						result.append("Ecoscore: not available")
					else:
						result.append(f"Ecoscore: {ecoscore_grade}")
			else:
				result.append('Product not available!')

	return render_template('index.html', product=result)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)