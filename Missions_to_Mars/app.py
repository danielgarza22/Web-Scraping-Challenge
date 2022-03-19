from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape


# Create an instance of Flask
app = Flask(__name__)

# Conection to Mongo with PyMongo
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Main route
@app.route("/")
def home():
    mars_data = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars_data)

# Scrape route
@app.route("/scrape")
def scrape2():
    data = scrape()    
    mongo.db.mars.update_one({}, {"$set": data}, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)