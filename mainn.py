import pymysql
from db_config import mysql 
from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt
engine = create_engine("mysql+pymysql://root:mishra12@localhost/register")

db=scoped_session(sessionmaker(bind=engine))
app= Flask(__name__)


		
@app.route('/add', methods=['POST'])
def add_user():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()		
		_name = request.form['Name']
		_price = request.form['Price']
		_desc = request.form['Description']
		_avail = request.form['Available']
		_cat = request.form['Category']
		_pic = request.form['Picture']
		# validate the received values
		if _name and _price and _desc and _avail and _cat and _pic and request.method == 'POST':
			# save edits
			sql = "INSERT INTO products(Name, Price,Description, Available,Category,Picture) VALUES(%s, %s, %s,%s,%s,%s)"
			data = (_name,_price, _desc, _avail,_cat,_pic)
			cursor.execute(sql, data)
			conn.commit()
		
			return redirect('/admin')
		else:
			return 'Error while adding user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/admin')
def admin():
	try:

		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products")
		row = cursor.fetchall()
		
		return render_template('product.html', row=row )
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/update', methods=['POST'])
def update_user():
	try:
		
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		_name = request.form['Name']
		_price = request.form['Price']
		_desc = request.form['Description']
		_avail = request.form['Available']
		
		_cat = request.form['Category']
		
		_pic = request.form['Picture']
		_id = request.form['id']

		# validate the received values
		if _name and _price and _desc and _avail and _cat and _pic and _id and request.method == 'POST':
			# save edits
			sql = "UPDATE products SET Name=%s,Price=%s, Description=%s, Available=%s, Category=%s, Picture=%s WHERE user_id=%s"
			data = (_name,_price, _desc, _avail,_cat,_pic,_id)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			flash("User updated successfully!","success")
			return redirect('/admin')

		else:
			return 'Error while updating user'
	except Exception as e:
		print(e)
	finally:
		cursor.close() 






		conn.close()
		
@app.route('/delete/<int:id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM products WHERE user_id=%s", (id,))
		conn.commit()
		return redirect('/admin')
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/')
def index():
	return render_template("homepage.html")

@app.route("/register",methods=["GET","POST"])
def register():
	if request.method=="POST":
		name=request.form.get("name")
		username=request.form.get("username")
		password=request.form.get("password")
		confirm=request.form.get("confirm")
		secure_password=sha256_crypt.encrypt(str(password))
		

		if password == confirm:
			db.execute("INSERT INTO users(name,username,password) VALUES(:name,:username,:password) ", {"name":name,"username":username,"password":secure_password})
			db.commit()
			return render_template('login.html')
		else:
			flash("Password does not match","danger")
			return render_template('homepage.html')
	return render_template('homepage.html')

@app.route("/signup",methods=["GET","POST"])
def signup():
	return render_template('register.html')

@app.route("/aabout/<int:id>")
def aabout(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE user_id=%s", (id,))
		row=cursor.fetchall()

		return render_template("aabout.html",row=row )
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
@app.route("/labout/<int:id>/<int:id2>")
def labout(id,id2):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE user_id=%s", (id,))
		user=db.execute("SELECT * FROM users WHERE id=:id2",{"id2":id2}).fetchall()
		row=cursor.fetchall()

		return render_template("labout.html",row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route("/habout/<int:id>")
def habout(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE user_id=%s", (id,))
		row=cursor.fetchall()

		return render_template("habout.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route("/login/<int:id>",methods=["GET","POST"])
def login(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM users WHERE id=%s", (id,))
		user=cursor.fetchall()
		return render_template("loggedin.html",user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
	

@app.route("/login_post",methods=["GET","POST"])
def login_post():
	#import pdb;pdb.set_trace()
	if request.method == "POST":
		username=request.form.get("name")
		password=request.form.get("password")
		user=db.execute("SELECT * FROM users WHERE username=:username",{"username":username}).fetchall()
		usernamedata = db.execute("SELECT username FROM users WHERE username=:username",{"username":username}).fetchone()
		passwordata = db.execute("SELECT password FROM users WHERE username=:username",{"username":username}).fetchone()
		
		if usernamedata is None:
			flash("No username","danger")
			return render_template("login.html")
		elif usernamedata==("admin@gmail.com",):
			for passwor_data in passwordata:
				if sha256_crypt.verify(password,passwor_data):
					session["log"]=True
					flash("You are now logged in","success")
					return render_template("admin.html")
				else:
					flash("Try again")
		else:
			for passwor_data in passwordata:
				if sha256_crypt.verify(password,passwor_data):
					session["log"]=True
					flash("You are now logged in","success")
					return render_template("loggedin.html",user=user)
				else:
					flash("Try again")
	return render_template('login.html')
@app.route("/back",methods=["GET","POST"])
def back():
	return render_template("admin.html")

@app.route("/hproducts",methods=["GET","POST"])
def hproducts():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='shirts'")
		row = cursor.fetchall()
		return render_template("hproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	    
@app.route("/lproducts/<int:id>")
def lproducts(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='shirts'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		return render_template("lproducts.html",row=row,user=user)

	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/aproducts",methods=["GET","POST"])
def aproducts():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='shirts'")
		row = cursor.fetchall()
		return render_template("aproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/hTshirt",methods=["GET","POST"])
def hTshirts():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='Tshirts'")
		row = cursor.fetchall()
		return render_template("hproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	    
@app.route("/lTshirt/<int:id>",methods=["GET","POST"])
def lTshirts(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='Tshirts'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		return render_template("lproducts.html",row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/aTshirt",methods=["GET","POST"])
def aTshirts():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='Tshirts'")
		row = cursor.fetchall()
		return render_template("aproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/hTrousers",methods=["GET","POST"])
def hTrousers():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='Trousers'")
		row = cursor.fetchall()
		return render_template("hproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	    
@app.route("/lTrousers/<int:id>",methods=["GET","POST"])
def lTrousers(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='Trousers'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		return render_template("lproducts.html",row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/aTrousers",methods=["GET","POST"])
def aTrousers():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='Trousers'")
		row = cursor.fetchall()
		return render_template("aproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/hhijabs",methods=["GET","POST"])
def hhijabs():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='hijabs'")
		row = cursor.fetchall()
		return render_template("hproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	    
@app.route("/lhijabs/<int:id>",methods=["GET","POST"])
def lhijabs(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='hijabs'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		return render_template("lproducts.html",row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/ahijabs",methods=["GET","POST"])
def ahijabs():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='hijabs'")
		row = cursor.fetchall()
		return render_template("aproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/hsarees",methods=["GET","POST"])
def hsarees():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='sarees'")
		row = cursor.fetchall()
		return render_template("hproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	    
@app.route("/lsarees/<int:id>",methods=["GET","POST"])
def lsarees(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='sarees'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		return render_template("lproducts.html",row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/asarees",methods=["GET","POST"])
def asarees():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='sarees'")
		row = cursor.fetchall()
		return render_template("aproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/hbelts",methods=["GET","POST"])
def hbelts():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='belts'")
		row = cursor.fetchall()
		return render_template("hproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	    
@app.route("/lbelts/<int:id>",methods=["GET","POST"])
def lbelts(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='belts'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		return render_template("lproducts.html",row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/abelts",methods=["GET","POST"])
def abelts():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='belts'")
		row = cursor.fetchall()
		return render_template("aproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/hPurse",methods=["GET","POST"])
def hPurse():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='Purse'")
		row = cursor.fetchall()
		return render_template("hproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
	    
@app.route("/lPurse/<int:id>",methods=["GET","POST"])
def lPurse(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='Purse'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		return render_template("lproducts.html",row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/aPurse",methods=["GET","POST"])
def aPurse():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='Purse'")
		row = cursor.fetchall()
		return render_template("aproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/hwatches",methods=["GET","POST"])
def hwatches():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("INSERT INTO cart(id,product_id) VALUES(%s,%s)")
		data=(user_id,product_id)
		row = cursor.fetchall()
		return render_template("hproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()

@app.route("/cart/<int:product>")
def cart(product_id,user_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE user_id=%s", (id,))
		user=db.execute("SELECT * FROM users WHERE id=:user_id",{"user_id":user_id}).fetchall()
		row=cursor.fetchall()

		return render_template("labout.html",row=row,cart=cart)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


	    
@app.route("/lwatches/<int:id>",methods=["GET","POST"])
def lwatches(id):
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='watches'")
		row = cursor.fetchall()
		user=db.execute("SELECT * FROM users WHERE id=:id",{"id":id}).fetchall()
		return render_template("lproducts.html",row=row,user=user)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
@app.route("/awatches",methods=["GET","POST"])
def awatches():
	try:
		conn=mysql.connect()
		cursor=conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM products WHERE Category='watches'")
		row = cursor.fetchall()
		return render_template("aproducts.html",row=row)
	except Exception as e:
		print(e)
	finally:
		cursor.close()
		conn.close()
															
@app.route("/logout",methods=["GET","POST"])
def logout():
	session.clear()
	flash("You are now logged out","success")
	return render_template("homepage.html")


if __name__ == '__main__':
	app.secret_key="secret_key"
	app.run(debug=True)
