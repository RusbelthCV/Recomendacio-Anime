from flask import Flask, jsonify, request as req
import pandas as pd
from flask_mysqldb import MySQL
import re

app = Flask(__name__)


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'anime'

mysql = MySQL(app)



@app.route('/database/', methods = ['GET'])
def create_table():
    
    # Acomodando datos
    ratings = pd.read_csv('/home/bryan/Escritorio/anime/datos/rating.csv', encoding="ISO-8859-1")
    ratings = ratings[['user_id','anime_id','rating']]
    animes = pd.read_csv('/home/bryan/Escritorio/anime/datos/anime.csv', encoding="ISO-8859-1")
    animes = animes[['anime_id','name']]


    ratings = ratings.head(10000)
    data = pd.merge(animes,ratings)

    userRatings = data.pivot_table(index = ['user_id'], columns = ['name'], values = 'rating')
    corrMatrix = userRatings.corr()
    #to_string = str(corrMatrix.columns)
    names = ""
    for x in corrMatrix.columns:
        x = x[:60]
        names += "`"+x.rstrip()+"`"+" double"+","
    

    
    #Quitar la última coma que daría syntax error de sql
    names = names[:-1]
    #Query
    cur = mysql.connection.cursor()
    query = f"CREATE TABLE correlation({names})"
    #cur.execute(query, args)
    mysql.connection.commit()
    cur.close()
    #return jsonify({"query": query})
    return names