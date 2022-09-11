import os
from flask import Flask, render_template, request
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
mysql.init_app(app)

# Configurações para o MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mudar123'
app.config['MYSQL_DATABASE_DB'] = 'crudTest'
# caso usando o docker, o ip precisar ser o da imagem do MySQL
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/insertProduct', methods=['POST','GET'])
def insertProduct():
  prod_Name = request.form['Product Name']
  prod_Desc = request.form['Product Description']
  prod_Quantity = request.form['Product Quantity']
  prod_PriceUnity = request.form['Product Price per Unity']

  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('INSERT INTO products (prod_Name, prod_Desc, prod_Quantity, prod_PriceUnity) VALUES (%s, %s, %s, %s)', (prod_Name, prod_Desc, prod_Quantity, prod_PriceUnity))
  conn.commit()
  return render_template('index.html')

@app.route('/searchProduct', methods=['GET'])
def searchProduct():
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('SELECT prod_ID FROM products')
  data = cursor.fetchall()
  conn.commit()
  return render_template('lista.html', datas=data)

@app.route('/updateProduct', methods=['POST','GET'])
def updateProduct():
  prod_Name = request.form['Product Name']
  prod_Desc = request.form['Product Description']
  prod_Quantity = request.form['Product Quantity']
  prod_PriceUnity = request.form['Product Price per Unity']
  prod_ID = request.form['Product ID']

  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('UPDATE products SET prod_Name=%s, prod_Desc=%s, prod_Quantity=%s, prod_PriceUnity=%s WHERE prod_ID=%s', (prod_Name, prod_Desc, prod_Quantity, prod_PriceUnity, prod_ID))
  conn.commit()

  return render_template('index.html')

@app.route('/deleteProduct', methods=['POST','GET'])
def deleteProduct():
  prod_ID = request.form['Product ID']

  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('DELETE FROM products WHERE prod_ID=%s', (prod_ID))
  conn.commit()
  return render_template('index.html')


@app.route('/listar', methods=['POST','GET'])
def listar():
  conn = mysql.connect()
  cursor = conn.cursor()
  cursor.execute('SELECT prod_ID, prod_Name, prod_Desc, prod_Quantity, prod_PriceUnity FROM products')
  data = cursor.fetchall()
  conn.commit()
  return render_template('lista.html', datas=data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5008))
    app.run(host='0.0.0.0', port=port)