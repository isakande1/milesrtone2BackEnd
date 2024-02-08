from flask import Flask, jsonify, request
# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from flask_mysqldb import MySQL
# from flask_cors import CORS

app = Flask(__name__)
# api = Api(app)


app.config.update(MYSQL_HOST = 'localhost', MYSQL_PORT = 3306, MYSQL_USER = 'root', MYSQL_PASSWORD = '122800', MYSQL_DB = 'sakila')
mysql = MySQL(app)

@app.route('/dat', methods = ['GET'])
def getdata():
    cursor = mysql.connection.cursor()
    cursor.execute("""select  film.film_id,film_category.category_id, count(film.title) as numberofrented, film.title from film join inventory 
on inventory.film_id = film.film_id join rental on 
rental.inventory_id = inventory.inventory_id join film_category on film_category.film_id = film.film_id join film_actor on film_actor.film_id = film.film_id
where film_actor.actor_id = 42
 group by film.title ,film.film_id,film_category.category_id order by numberofrented desc limit 5
""")
    data  = cursor.fetchall()
    cursor.close()
    return jsonify(data)

@app.route('/requestDetails', methods = ['POST'])
def getDetailsRequest():
    # try:
        filmTitle = request.json
        cursor = mysql.connection.cursor()
        query = """select film.film_id, film.title, category.name from film join film_category
 on film.film_id = film_category.film_id join category on category.category_id = film_category.category_id
where film.title = %s"""
        cursor.execute(query,(filmTitle,))
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
@app.route('/searchFilmQuery', methods = ['GET'])
def searchFilmQuery():
    # try:
        cursor = mysql.connection.cursor()
        query = """select film_text.title , max(actor.first_name) as first_name, max(actor.last_name) as last_name, max(category.name) as genre from film_text join film_actor on 
film_text.film_id = film_actor.film_id join actor on actor.actor_id = film_actor.actor_id 
join film_category on film_category.film_id = film_text.film_id
join category on category.category_id = film_category.category_id
group by film_text.title"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)

@app.route('/topFiveActor', methods = ['GET'])
def topFiveActor():
    # try:
        cursor = mysql.connection.cursor()
        query = """select actor_id, first_name, last_name from actor limit 5;"""
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)

@app.route('/actorFilm', methods = ['POST'])
def actorFilm():
    # try:
        actorId = int(request.json)
        cursor = mysql.connection.cursor()
        query = """select  film.title,film_category.category_id, count(film.title) as rented from film join inventory 
on inventory.film_id = film.film_id join rental on 
rental.inventory_id = inventory.inventory_id join film_category on film_category.film_id = film.film_id join film_actor on 
film_actor.film_id = film.film_id join actor on actor.actor_id = film_actor.actor_id where actor.actor_id = %s
group by film.title ,film.film_id,film_category.category_id order by rented desc limit 5

"""
        cursor.execute(query,(actorId,))
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data) 

@app.route('/chCustomer', methods = ['GET'])
def searchCustomer():
    # try:
        cursor = mysql.connection.cursor()
        query = """
select customer_id, first_name, last_name from customer limit 1000;
       """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data) 

@app.route('/erase', methods = ['POST'])
def deleteUser():
    # try:
        Id = int(request.json)
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM payment WHERE customer_id = %s", (Id,))
        cursor.execute("DELETE FROM rental WHERE customer_id = %s", (Id,))
        cursor.execute("DELETE FROM customer WHERE customer_id = %s", (Id,))
        mysql.connection.commit()
        
        cursor.close()
        return jsonify("response") 

if __name__ == "__main__":
    app.run(debug =True)
