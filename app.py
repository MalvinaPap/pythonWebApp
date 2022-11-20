import mysql.connector
from flask import Flask
import json

app = Flask(__name__)

#homepage
@app.route('/')
def hello_world():
    return 'Hello Book Lover'


#initialize database
@app.route('/initdb')
def initdb():
    database = mysql.connector.connect(
        host="mysql-container",
        user="root",
        password="Abc@123456789"        
    )
    cursor = database.cursor()
    cursor.execute("DROP DATABASE IF EXISTS Library")
    cursor.execute("CREATE DATABASE Library")
   
    cursor.close()    
    
    database = mysql.connector.connect(
        host="mysql-container",
        user="root",
        password="Abc@123456789",
        database="Library"
    )
    
    cursor = database.cursor()
    cursor.execute("DROP TABLE IF EXISTS Books")
    cursor.execute("CREATE TABLE Books (id INT PRIMARY KEY AUTO_INCREMENT, title VARCHAR(255), author VARCHAR(255))")
    cursor.close()  
    
    return 'Database & Tables Created' 

    
#populate database
@app.route('/populatedb')
def populatedb():
    database = mysql.connector.connect(
        host="mysql-container",
        user="root",
        password="Abc@123456789",
        database="Library"
    )
    cursor = database.cursor()
    
    cursor.execute("INSERT INTO Books(title, author) VALUES ('Les Miserables', 'Victor Hugo')")
    cursor.execute("INSERT INTO Books(title, author) VALUES ('War and Peace', 'Leo Tolstoy')")
    cursor.execute("INSERT INTO Books(title, author) VALUES ('1984', 'George Orwell')")
    cursor.execute("INSERT INTO Books(title, author) VALUES ('Pride and Prejudice', 'Jane Austen')")
    cursor.execute("INSERT INTO Books(title, author) VALUES ('Jane Eyre', 'Charlotte Bronte')")
  
    database.commit()
    
    cursor.close()    
    return "Database Populated"
    
    
#get list of books
@app.route('/books')
def get_books():
    database = mysql.connector.connect(
        host="mysql-container",
        user="root",
        password="Abc@123456789",
        database="Library"
    )
    cursor = database.cursor()
    cursor.execute("SELECT * FROM Books")
    row_headers=[x[0] for x in cursor.description]
    books = cursor.fetchall()
    json_data=[]
    for book in books:
        json_data.append(dict(zip(row_headers,book)))
    cursor.close()
    return json.dumps(json_data) #convert to JSON

  
